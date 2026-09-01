"""Servicios seguros del Centro de desarrollo.

El Centro de desarrollo expone metadata técnica, un visor acotado de eventos
JSONL, una exportación controlada y un autodiagnóstico local de Developer
Diagnostics. No lee documentos personales, no inspecciona cuerpos HTTP y no
devuelve rutas absolutas locales.
"""

from __future__ import annotations

from dataclasses import dataclass
from datetime import datetime, timezone
import json
import platform
from pathlib import Path
from typing import Any, Mapping

from app.core.observability import (
    ENV_DEV_MODE,
    ENV_DIAGNOSTIC_DIR,
    SCHEMA_VERSION,
    directorio_diagnostico,
    exportar_diagnostico,
    modo_desarrollo_activo,
    ruta_log_actual,
)
from app.core.version import APP_VERSION


_MAX_BACKUPS_VISIBLES = 3
_MAX_EVENTOS_VISIBLES = 200
_MAX_TEXTO_EVENTO = 120
_ARCHIVO_PRUEBA_AUTODIAGNOSTICO = ".mrp-dev-autodiagnostico.tmp"
_METADATA_VISIBLE = {
    "exception_type",
    "method",
    "operation",
    "status_code",
}
_ESTADOS_AUTODIAGNOSTICO = ("OK", "ADVERTENCIA", "BLOQUEADO", "NO_EVALUADO")


@dataclass(frozen=True)
class ArchivoDiagnostico:
    """Resumen no sensible de un archivo diagnóstico conocido."""

    nombre: str
    existe: bool
    tamano_bytes: int
    actualizado_utc: str | None
    tamano_legible: str = "0 B"


@dataclass(frozen=True)
class EventoDiagnostico:
    """Evento JSONL resumido para revisión local sin datos de simulación."""

    archivo: str
    timestamp: str
    level: str
    event: str
    component: str
    outcome: str
    correlation_id: str | None
    duration_ms: float | None
    metadata: dict[str, Any]


@dataclass(frozen=True)
class ResultadoAutodiagnostico:
    """Resultado resumido de una comprobación técnica local."""

    codigo: str
    componente: str
    estado: str
    detalle: str
    accion: str


def _timestamp_utc(ruta: Path) -> str | None:
    """Devuelve una fecha UTC legible sin exponer la ruta local."""

    if not ruta.is_file():
        return None
    return datetime.fromtimestamp(
        ruta.stat().st_mtime,
        tz=timezone.utc,
    ).isoformat(timespec="seconds")


def _formatear_bytes(cantidad: int) -> str:
    """Convierte bytes a una representación compacta y segura."""

    valor = max(0, int(cantidad))
    unidades = ("B", "KB", "MB", "GB")

    indice = 0
    cantidad_visible = float(valor)

    while cantidad_visible >= 1024 and indice < len(unidades) - 1:
        cantidad_visible /= 1024
        indice += 1

    if indice == 0:
        return f"{valor} B"

    return f"{cantidad_visible:.1f} {unidades[indice]}"


def _resumir_archivo(ruta: Path) -> ArchivoDiagnostico:
    """Resume un archivo permitido sin abrir ni leer su contenido completo."""

    existe = ruta.is_file()
    tamano = ruta.stat().st_size if existe else 0

    return ArchivoDiagnostico(
        nombre=ruta.name,
        existe=existe,
        tamano_bytes=tamano,
        actualizado_utc=_timestamp_utc(ruta) if existe else None,
        tamano_legible=_formatear_bytes(tamano),
    )


def _rutas_diagnostico_conocidas() -> list[Path]:
    """Devuelve el JSONL vigente y sus rotaciones esperadas."""

    actual = ruta_log_actual()
    candidatos = [actual]
    candidatos.extend(
        actual.with_suffix(actual.suffix + f".{numero}")
        for numero in range(1, _MAX_BACKUPS_VISIBLES + 1)
    )
    return candidatos


def archivos_diagnostico_conocidos() -> list[ArchivoDiagnostico]:
    """Lista únicamente el JSONL vigente y sus rotaciones esperadas."""

    return [_resumir_archivo(ruta) for ruta in _rutas_diagnostico_conocidas()]


def _etiqueta_directorio() -> str:
    """Describe el directorio sin revelar rutas absolutas del equipo."""

    directorio = directorio_diagnostico()
    if directorio == Path.cwd() / "logs" / "diagnostico":
        return "logs/diagnostico"
    return "directorio personalizado definido por MRP_DIAGNOSTIC_DIR"


def _texto_seguro(valor: Any, *, maximo: int = _MAX_TEXTO_EVENTO) -> str:
    """Convierte valores técnicos a texto corto sin expandir estructuras."""

    if valor is None:
        return ""
    if isinstance(valor, (bool, int, float)):
        return str(valor)
    texto = str(valor).replace("\r", " ").replace("\n", " ").strip()
    return texto[:maximo]


def _metadata_visible(metadata: Mapping[str, Any] | None) -> dict[str, Any]:
    """Expone solo metadata operacional permitida para el visor Developer."""

    if not metadata:
        return {}

    visible: dict[str, Any] = {}
    for clave in sorted(_METADATA_VISIBLE):
        if clave not in metadata:
            continue
        valor = metadata[clave]
        if clave == "status_code" and isinstance(valor, int):
            visible[clave] = valor
        else:
            visible[clave] = _texto_seguro(valor)
    return visible


def _evento_desde_json(archivo: str, datos: Mapping[str, Any]) -> EventoDiagnostico:
    """Normaliza un evento JSONL a campos seguros para la plantilla."""

    correlation_id = datos.get("correlation_id")
    if isinstance(correlation_id, str):
        correlation_id_visible = correlation_id[:32]
    else:
        correlation_id_visible = None

    duration = datos.get("duration_ms")
    duration_ms = round(float(duration), 3) if isinstance(duration, (int, float)) else None

    metadata = datos.get("metadata")
    return EventoDiagnostico(
        archivo=archivo,
        timestamp=_texto_seguro(datos.get("timestamp")),
        level=_texto_seguro(datos.get("level") or "INFO", maximo=24).upper(),
        event=_texto_seguro(datos.get("event")),
        component=_texto_seguro(datos.get("component")),
        outcome=_texto_seguro(datos.get("outcome")),
        correlation_id=correlation_id_visible,
        duration_ms=duration_ms,
        metadata=_metadata_visible(metadata if isinstance(metadata, Mapping) else None),
    )


def leer_eventos_diagnostico(
    limite: int = _MAX_EVENTOS_VISIBLES,
) -> tuple[list[EventoDiagnostico], int]:
    """Lee eventos recientes de JSONL sin exponer valores arbitrarios."""

    eventos: list[EventoDiagnostico] = []
    invalidos = 0

    for ruta in _rutas_diagnostico_conocidas():
        if not ruta.is_file():
            continue
        for linea in ruta.read_text(encoding="utf-8").splitlines():
            if not linea.strip():
                continue
            try:
                datos = json.loads(linea)
            except json.JSONDecodeError:
                invalidos += 1
                continue
            if not isinstance(datos, Mapping):
                invalidos += 1
                continue
            eventos.append(_evento_desde_json(ruta.name, datos))

    eventos_ordenados = sorted(
        eventos,
        key=lambda evento: evento.timestamp,
        reverse=True,
    )
    return eventos_ordenados[: max(0, limite)], invalidos


def _resumen_por_nivel(eventos: list[EventoDiagnostico]) -> dict[str, int]:
    """Cuenta eventos visibles por nivel operacional."""

    resumen = {"INFO": 0, "WARNING": 0, "ERROR": 0, "OTRO": 0}
    for evento in eventos:
        if evento.level in resumen:
            resumen[evento.level] += 1
        else:
            resumen["OTRO"] += 1
    return resumen


def exportar_zip_diagnostico_sanitizado() -> Path:
    """Genera el ZIP diagnóstico permitido si hay logs locales disponibles."""

    if not modo_desarrollo_activo():
        raise PermissionError(
            "Developer Diagnostics está desactivado; active MRP_DEV_MODE=1."
        )

    if not any(ruta.is_file() for ruta in _rutas_diagnostico_conocidas()):
        raise FileNotFoundError(
            "No existen archivos diagnósticos para exportar."
        )

    return exportar_diagnostico()


def _resultado_autodiagnostico(
    *,
    codigo: str,
    componente: str,
    estado: str,
    detalle: str,
    accion: str,
) -> ResultadoAutodiagnostico:
    """Construye un resultado técnico con estado normalizado."""

    estado_normalizado = estado if estado in _ESTADOS_AUTODIAGNOSTICO else "NO_EVALUADO"
    return ResultadoAutodiagnostico(
        codigo=codigo,
        componente=componente,
        estado=estado_normalizado,
        detalle=detalle,
        accion=accion,
    )


def _diagnosticar_modo_desarrollo(activo: bool) -> ResultadoAutodiagnostico:
    """Valida la activación explícita del modo de desarrollo."""

    if activo:
        return _resultado_autodiagnostico(
            codigo="dev_mode",
            componente="Modo desarrollador",
            estado="OK",
            detalle=f"{ENV_DEV_MODE}=1 está activo para pruebas locales.",
            accion="Mantenerlo activo solo durante desarrollo y validación.",
        )

    return _resultado_autodiagnostico(
        codigo="dev_mode",
        componente="Modo desarrollador",
        estado="ADVERTENCIA",
        detalle=f"{ENV_DEV_MODE} no está activo; el diagnóstico solo muestra estado pasivo.",
        accion=(
            "Activar MRP_DEV_MODE=1 únicamente cuando se necesite observar "
            "Developer Diagnostics."
        ),
    )


def _diagnosticar_directorio() -> ResultadoAutodiagnostico:
    """Evalúa el directorio diagnóstico sin mostrar su ruta absoluta."""

    directorio = directorio_diagnostico()
    if directorio.exists() and directorio.is_dir():
        return _resultado_autodiagnostico(
            codigo="directorio_diagnostico",
            componente="Directorio diagnóstico",
            estado="OK",
            detalle=f"{_etiqueta_directorio()} existe como directorio local.",
            accion="Mantener el directorio fuera de Git y usarlo solo para desarrollo.",
        )

    if directorio.exists() and not directorio.is_dir():
        return _resultado_autodiagnostico(
            codigo="directorio_diagnostico",
            componente="Directorio diagnóstico",
            estado="BLOQUEADO",
            detalle="La ubicación diagnóstica existe, pero no es un directorio.",
            accion="Corregir la ubicación configurada antes de exportar diagnóstico.",
        )

    return _resultado_autodiagnostico(
        codigo="directorio_diagnostico",
        componente="Directorio diagnóstico",
        estado="ADVERTENCIA",
        detalle=f"{_etiqueta_directorio()} todavía no existe.",
        accion="El directorio se creará automáticamente al registrar eventos en modo DEV.",
    )


def _diagnosticar_permisos(activo: bool) -> ResultadoAutodiagnostico:
    """Comprueba escritura y lectura con un archivo temporal no sensible."""

    if not activo:
        return _resultado_autodiagnostico(
            codigo="permisos_diagnostico",
            componente="Permisos locales",
            estado="NO_EVALUADO",
            detalle="La prueba de lectura/escritura se omite con Developer Diagnostics desactivado.",
            accion="Activar MRP_DEV_MODE=1 para evaluar permisos locales de diagnóstico.",
        )

    directorio = directorio_diagnostico()
    prueba = directorio / _ARCHIVO_PRUEBA_AUTODIAGNOSTICO
    try:
        directorio.mkdir(parents=True, exist_ok=True)
        prueba.write_text("ok", encoding="utf-8")
        contenido = prueba.read_text(encoding="utf-8")
        if contenido != "ok":
            raise OSError("lectura de comprobación no coincide")
    except OSError:
        return _resultado_autodiagnostico(
            codigo="permisos_diagnostico",
            componente="Permisos locales",
            estado="BLOQUEADO",
            detalle="No se pudo completar una prueba controlada de lectura/escritura.",
            accion="Revisar permisos del directorio diagnóstico local.",
        )
    finally:
        try:
            if prueba.exists():
                prueba.unlink()
        except OSError:
            pass

    return _resultado_autodiagnostico(
        codigo="permisos_diagnostico",
        componente="Permisos locales",
        estado="OK",
        detalle="La lectura y escritura controladas funcionan en el directorio diagnóstico.",
        accion="No se requiere acción mientras el entorno siga siendo local.",
    )


def _diagnosticar_log_vigente(archivos: list[ArchivoDiagnostico]) -> ResultadoAutodiagnostico:
    """Evalúa si el archivo JSONL vigente existe."""

    actual = archivos[0] if archivos else None
    if actual and actual.existe:
        return _resultado_autodiagnostico(
            codigo="log_vigente",
            componente="Log vigente",
            estado="OK",
            detalle=f"{actual.nombre} existe con {actual.tamano_bytes} byte(s).",
            accion="Revisar el visor si se necesita confirmar eventos recientes.",
        )

    return _resultado_autodiagnostico(
        codigo="log_vigente",
        componente="Log vigente",
        estado="ADVERTENCIA",
        detalle="No existe todavía un archivo JSONL vigente.",
        accion="Generar tráfico local con MRP_DEV_MODE=1 para crear eventos diagnósticos.",
    )


def _diagnosticar_rotaciones(archivos: list[ArchivoDiagnostico]) -> ResultadoAutodiagnostico:
    """Resume las rotaciones conocidas sin abrirlas."""

    rotaciones = [archivo for archivo in archivos[1:] if archivo.existe]
    if rotaciones:
        nombres = ", ".join(archivo.nombre for archivo in rotaciones)
        return _resultado_autodiagnostico(
            codigo="rotaciones",
            componente="Rotaciones JSONL",
            estado="OK",
            detalle=f"Se detectaron {len(rotaciones)} rotación(es): {nombres}.",
            accion="Confirmar que solo sean archivos JSONL conocidos antes de exportar.",
        )

    return _resultado_autodiagnostico(
        codigo="rotaciones",
        componente="Rotaciones JSONL",
        estado="OK",
        detalle="No hay rotaciones diagnósticas conocidas.",
        accion="No se requiere acción; la ausencia de rotaciones es normal.",
    )


def _diagnosticar_exportacion(
    *,
    activo: bool,
    hay_archivos: bool,
) -> ResultadoAutodiagnostico:
    """Evalúa disponibilidad lógica de exportación ZIP."""

    if activo and hay_archivos:
        return _resultado_autodiagnostico(
            codigo="exportacion_zip",
            componente="Exportación ZIP",
            estado="OK",
            detalle="La exportación ZIP sanitizada está disponible.",
            accion="Exportar solo cuando se necesite compartir diagnóstico técnico.",
        )

    if not activo:
        return _resultado_autodiagnostico(
            codigo="exportacion_zip",
            componente="Exportación ZIP",
            estado="BLOQUEADO",
            detalle="La exportación está bloqueada porque Developer Diagnostics está desactivado.",
            accion="Activar MRP_DEV_MODE=1 solo durante desarrollo si se necesita exportar.",
        )

    return _resultado_autodiagnostico(
        codigo="exportacion_zip",
        componente="Exportación ZIP",
        estado="ADVERTENCIA",
        detalle="La exportación no tiene archivos JSONL disponibles.",
        accion="Generar eventos locales antes de intentar exportar.",
    )


def _diagnosticar_visor(
    *,
    eventos: list[EventoDiagnostico],
    invalidos: int,
) -> ResultadoAutodiagnostico:
    """Evalúa el estado del visor diagnóstico seguro."""

    if invalidos:
        return _resultado_autodiagnostico(
            codigo="visor_eventos",
            componente="Visor diagnóstico",
            estado="ADVERTENCIA",
            detalle=f"El visor cargó {len(eventos)} evento(s) y omitió {invalidos} línea(s) inválida(s).",
            accion="Revisar si el JSONL fue editado manualmente o quedó truncado.",
        )

    if eventos:
        return _resultado_autodiagnostico(
            codigo="visor_eventos",
            componente="Visor diagnóstico",
            estado="OK",
            detalle=f"El visor tiene {len(eventos)} evento(s) normalizado(s).",
            accion="Usar el visor para revisar metadata operacional permitida.",
        )

    return _resultado_autodiagnostico(
        codigo="visor_eventos",
        componente="Visor diagnóstico",
        estado="ADVERTENCIA",
        detalle="El visor no tiene eventos recientes para mostrar.",
        accion="Generar actividad local con Developer Diagnostics activo.",
    )


def _diagnosticar_privacidad() -> ResultadoAutodiagnostico:
    """Declara las barreras de privacidad aplicadas al diagnóstico Developer."""

    return _resultado_autodiagnostico(
        codigo="privacidad",
        componente="Privacidad del diagnóstico",
        estado="OK",
        detalle="El visor y el ZIP se limitan a metadata operacional y archivos JSONL conocidos.",
        accion="Mantener fuera del diagnóstico cuerpos HTTP, PDFs, secretos y valores financieros.",
    )


def ejecutar_autodiagnostico(
    *,
    activo: bool | None = None,
    archivos: list[ArchivoDiagnostico] | None = None,
    eventos: list[EventoDiagnostico] | None = None,
    invalidos: int = 0,
) -> list[ResultadoAutodiagnostico]:
    """Ejecuta comprobaciones técnicas locales sin exponer rutas absolutas."""

    activo_resuelto = modo_desarrollo_activo() if activo is None else activo
    archivos_resueltos = archivos if archivos is not None else archivos_diagnostico_conocidos()
    eventos_resueltos = eventos if eventos is not None else leer_eventos_diagnostico()[0]
    hay_archivos = any(archivo.existe for archivo in archivos_resueltos)

    return [
        _diagnosticar_modo_desarrollo(activo_resuelto),
        _diagnosticar_directorio(),
        _diagnosticar_permisos(activo_resuelto),
        _diagnosticar_log_vigente(archivos_resueltos),
        _diagnosticar_rotaciones(archivos_resueltos),
        _diagnosticar_exportacion(
            activo=activo_resuelto,
            hay_archivos=hay_archivos,
        ),
        _diagnosticar_visor(
            eventos=eventos_resueltos,
            invalidos=invalidos,
        ),
        _diagnosticar_privacidad(),
    ]


def resumir_autodiagnostico(
    resultados: list[ResultadoAutodiagnostico],
) -> dict[str, Any]:
    """Resume el autodiagnóstico para la interfaz."""

    conteos = {estado: 0 for estado in _ESTADOS_AUTODIAGNOSTICO}
    for resultado in resultados:
        conteos[resultado.estado] = conteos.get(resultado.estado, 0) + 1

    if conteos["BLOQUEADO"]:
        estado_global = "BLOQUEADO"
    elif conteos["ADVERTENCIA"] or conteos["NO_EVALUADO"]:
        estado_global = "ADVERTENCIA"
    else:
        estado_global = "OK"

    return {
        "estado_global": estado_global,
        "total": len(resultados),
        "OK": conteos["OK"],
        "ADVERTENCIA": conteos["ADVERTENCIA"],
        "BLOQUEADO": conteos["BLOQUEADO"],
        "NO_EVALUADO": conteos["NO_EVALUADO"],
    }


def _entorno_runtime_seguro() -> dict[str, str]:
    """Describe el runtime sin hostname, usuario ni rutas locales."""

    return {
        "python": platform.python_version(),
        "sistema": platform.system() or "No disponible",
        "release": platform.release() or "No disponible",
        "arquitectura": platform.machine() or "No disponible",
    }


def construir_estado_centro_desarrollo() -> dict[str, Any]:
    """Construye el estado seguro mostrado por la interfaz Developer."""

    activo = modo_desarrollo_activo()
    archivos = archivos_diagnostico_conocidos()
    archivos_existentes = [archivo for archivo in archivos if archivo.existe]
    eventos, invalidos = leer_eventos_diagnostico()
    autodiagnostico = ejecutar_autodiagnostico(
        activo=activo,
        archivos=archivos,
        eventos=eventos,
        invalidos=invalidos,
    )

    advertencias = [
        "No usar con datos personales reales, PDFs reales ni información financiera real.",
        "Los logs son locales y permanecen excluidos de Git.",
    ]
    if not activo:
        advertencias.insert(
            0,
            "Developer Diagnostics está desactivado; active MRP_DEV_MODE=1 solo durante desarrollo.",
        )

    total_bytes = sum(
        archivo.tamano_bytes
        for archivo in archivos_existentes
    )

    return {
        "componente": "developer_diagnostics",
        "estado_portal": "Observabilidad local segura",
        "titulo": "Centro de desarrollo",
        "descripcion": (
            "Superficie interna para revisar el estado técnico de Developer Diagnostics "
            "sin exponer datos personales, datos financieros, PDFs ni secretos."
        ),
        "app_version": APP_VERSION,
        "entorno_runtime": _entorno_runtime_seguro(),
        "dev_mode_env": ENV_DEV_MODE,
        "diagnostic_dir_env": ENV_DIAGNOSTIC_DIR,
        "dev_mode_activo": activo,
        "schema_version": SCHEMA_VERSION,
        "directorio_diagnostico": _etiqueta_directorio(),
        "archivo_log_actual": ruta_log_actual().name,
        "archivos_diagnostico": [archivo.__dict__ for archivo in archivos],
        "total_archivos_existentes": len(archivos_existentes),
        "total_bytes": total_bytes,
        "total_bytes_legible": _formatear_bytes(total_bytes),
        "exportacion_zip_disponible": activo and bool(archivos_existentes),
        "eventos_recientes": [evento.__dict__ for evento in eventos],
        "total_eventos_visibles": len(eventos),
        "limite_eventos_visibles": _MAX_EVENTOS_VISIBLES,
        "total_eventos_invalidos": invalidos,
        "resumen_eventos": _resumen_por_nivel(eventos),
        "autodiagnostico": [resultado.__dict__ for resultado in autodiagnostico],
        "resumen_autodiagnostico": resumir_autodiagnostico(autodiagnostico),
        "advertencias": advertencias,
        "controles_privacidad": [
            "No lee cuerpos HTTP ni contenido de formularios.",
            "No lee ni exporta PDFs, uploads, bases de datos ni sessionStorage.",
            "No muestra rutas absolutas locales del equipo.",
            "No incluye identidad, ingresos, aportes ni importes de beneficio.",
            "El ZIP diagnóstico permitido se limita a archivos mrp-diagnostics.jsonl conocidos.",
            "El visor muestra solo metadata operacional permitida.",
            "El autodiagnóstico no muestra rutas absolutas ni contenido de archivos.",
        ],
    }
