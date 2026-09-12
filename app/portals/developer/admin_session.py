"""Sesiones web del Portal Developer con identidad y revisión de seguridad."""

from __future__ import annotations

from dataclasses import dataclass
from datetime import datetime, timedelta, timezone
import secrets

from app.core.config import (
    ADMIN_MAX_SESSIONS,
    ADMIN_SESSION_MAX_HOURS,
    ADMIN_SESSION_MINUTES,
)
from app.portals.developer.developer_identity import RolDeveloper


@dataclass
class SesionAdministrativa:
    """Representa una sesión temporal del Portal Developer."""

    identificador: str
    creada: datetime
    ultima_actividad: datetime
    usuario_id: str | None = None
    usuario: str | None = None
    rol: RolDeveloper | None = None
    revision_seguridad: int | None = None
    sesiones_cerradas_por_limite: int = 0

    @property
    def tiene_identidad(self) -> bool:
        """Indica si la sesión posee una identidad Developer completa."""

        return bool(
            self.usuario_id
            and self.usuario
            and self.rol is not None
            and isinstance(
                self.revision_seguridad,
                int,
            )
            and self.revision_seguridad >= 1
        )


_sesiones: dict[str, SesionAdministrativa] = {}


def _ahora_utc() -> datetime:
    """Devuelve la hora UTC utilizada por el almacén de sesiones."""

    return datetime.now(timezone.utc)


def crear_sesion_admin(
    *,
    usuario_id: str | None = None,
    usuario: str | None = None,
    rol: RolDeveloper | str | None = None,
    revision_seguridad: int | None = None,
) -> str:
    """Crea una sesión administrativa legacy o una sesión R6 identificada."""

    limpiar_sesiones_expiradas()

    valores_identidad = (
        usuario_id,
        usuario,
        rol,
        revision_seguridad,
    )
    cantidad_presentes = sum(
        valor is not None
        for valor in valores_identidad
    )

    if cantidad_presentes not in {0, 4}:
        raise ValueError(
            "La identidad de sesión debe proporcionarse completa."
        )

    rol_normalizado: RolDeveloper | None = None

    if cantidad_presentes == 4:
        usuario_id = str(usuario_id).strip()
        usuario = str(usuario).strip()

        if not usuario_id or not usuario:
            raise ValueError(
                "La identidad de sesión no puede contener valores vacíos."
            )

        rol_normalizado = RolDeveloper(rol)

        if (
            not isinstance(revision_seguridad, int)
            or isinstance(revision_seguridad, bool)
            or revision_seguridad < 1
        ):
            raise ValueError(
                "La revisión de seguridad de sesión es inválida."
            )

    identificador = secrets.token_urlsafe(32)
    ahora = _ahora_utc()

    _sesiones[identificador] = SesionAdministrativa(
        identificador=identificador,
        creada=ahora,
        ultima_actividad=ahora,
        usuario_id=usuario_id,
        usuario=usuario,
        rol=rol_normalizado,
        revision_seguridad=revision_seguridad,
    )

    cerradas_por_limite = limitar_sesiones_activas(
        usuario_id=usuario_id,
    )

    sesion_creada = _sesiones.get(
        identificador
    )

    if sesion_creada is not None:
        sesion_creada.sesiones_cerradas_por_limite = (
            cerradas_por_limite
        )

    return identificador


def obtener_sesion_admin(
    identificador: str,
    *,
    actualizar_actividad: bool = True,
) -> SesionAdministrativa | None:
    """Obtiene una sesión vigente y opcionalmente renueva su actividad."""

    limpiar_sesiones_expiradas()

    sesion = _sesiones.get(identificador)

    if sesion is None:
        return None

    ahora = _ahora_utc()

    if ahora - sesion.ultima_actividad > timedelta(
        minutes=ADMIN_SESSION_MINUTES,
    ):
        eliminar_sesion_admin(identificador)
        return None

    if ahora - sesion.creada > timedelta(
        hours=ADMIN_SESSION_MAX_HOURS,
    ):
        eliminar_sesion_admin(identificador)
        return None

    if actualizar_actividad:
        sesion.ultima_actividad = ahora

    return sesion


def validar_sesion_admin(
    identificador: str,
) -> bool:
    """Valida una sesión administrativa existente."""

    return obtener_sesion_admin(
        identificador,
    ) is not None


def validar_sesion_admin_con_identidad(
    identificador: str,
) -> bool:
    """Valida una sesión vigente vinculada a una identidad Developer."""

    sesion = obtener_sesion_admin(
        identificador,
    )

    return bool(
        sesion is not None
        and sesion.tiene_identidad
    )


def validar_sesion_admin_para_usuario(
    identificador: str,
    *,
    usuario_id: str,
    revision_seguridad: int,
) -> bool:
    """Valida que una sesión pertenezca al usuario y revisión actuales."""

    sesion = obtener_sesion_admin(
        identificador,
    )

    if (
        sesion is None
        or not sesion.tiene_identidad
        or sesion.usuario_id != usuario_id
        or sesion.revision_seguridad
        != revision_seguridad
    ):
        if sesion is not None:
            eliminar_sesion_admin(
                identificador
            )
        return False

    return True


def eliminar_sesion_admin(
    identificador: str,
) -> None:
    """Elimina una sesión administrativa."""

    _sesiones.pop(
        identificador,
        None,
    )


def obtener_sesiones_activas() -> list[str]:
    """Devuelve los identificadores de sesiones vigentes."""

    limpiar_sesiones_expiradas()
    return list(_sesiones.keys())


def obtener_sesiones_activas_usuario(
    usuario_id: str,
) -> list[str]:
    """Devuelve sesiones vigentes asociadas a una identidad Developer."""

    limpiar_sesiones_expiradas()

    objetivo = str(
        usuario_id
    ).strip()

    if not objetivo:
        return []

    return [
        identificador
        for identificador, sesion
        in _sesiones.items()
        if sesion.usuario_id == objetivo
    ]


def revocar_sesiones_usuario(
    usuario_id: str,
) -> int:
    """Revoca las sesiones en memoria asociadas a una identidad."""

    objetivo = str(usuario_id).strip()

    if not objetivo:
        return 0

    revocadas = 0

    for identificador, sesion in list(
        _sesiones.items()
    ):
        if sesion.usuario_id == objetivo:
            eliminar_sesion_admin(
                identificador
            )
            revocadas += 1

    return revocadas


def revocar_todas_las_sesiones_admin() -> None:
    """Revoca todas las sesiones administrativas en memoria."""

    _sesiones.clear()


def limpiar_sesiones_expiradas() -> None:
    """Elimina sesiones que superaron inactividad o duración máxima."""

    ahora = _ahora_utc()

    for identificador, sesion in list(
        _sesiones.items()
    ):
        if (
            ahora - sesion.ultima_actividad
            > timedelta(
                minutes=ADMIN_SESSION_MINUTES
            )
            or ahora - sesion.creada
            > timedelta(
                hours=ADMIN_SESSION_MAX_HOURS
            )
        ):
            eliminar_sesion_admin(
                identificador
            )


def limitar_sesiones_activas(
    *,
    usuario_id: str | None = None,
) -> int:
    """Aplica el límite configurado únicamente al grupo de sesión indicado."""

    limite = max(
        1,
        int(ADMIN_MAX_SESSIONS),
    )

    candidatas = [
        sesion
        for sesion in _sesiones.values()
        if sesion.usuario_id == usuario_id
    ]

    candidatas.sort(
        key=lambda sesion: (
            sesion.creada,
            sesion.identificador,
        )
    )

    cerradas = 0

    while len(candidatas) > limite:
        mas_antigua = candidatas.pop(0)
        eliminar_sesion_admin(
            mas_antigua.identificador
        )
        cerradas += 1

    return cerradas
