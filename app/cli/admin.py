"""CLI administrativa local del Portal Developer."""

from __future__ import annotations

import argparse
from getpass import getpass
from pathlib import Path
import sys

from app.core.developer_identity import (
    REQUISITOS_PASSWORD,
    validar_password,
)
from app.core.developer_provisioning import (
    autenticar_usuario_developer,
    bootstrap_propietario,
    recuperar_propietario,
    restablecer_password_developer,
)


def _mostrar_politica_password() -> None:
    """Explica la política sin revelar información sensible."""

    print()
    print("La contraseña debe cumplir:")
    for requisito in REQUISITOS_PASSWORD:
        print(f"  - {requisito}.")
    print()


def _password_confirmada(
    etiqueta: str,
) -> str:
    """Solicita hasta obtener una contraseña válida y confirmada."""

    while True:
        primera = getpass(etiqueta)

        try:
            validar_password(primera)
        except (TypeError, ValueError):
            print()
            print(
                "La contraseña no cumple la política."
            )
            _mostrar_politica_password()
            print("Inténtelo nuevamente.")
            print()
            continue

        segunda = getpass(
            "Confirmar contraseña: "
        )

        if primera != segunda:
            print()
            print(
                "Las contraseñas no coinciden."
            )
            print(
                "Inténtelo nuevamente."
            )
            print()
            continue

        return primera


def _crear_parser() -> argparse.ArgumentParser:
    """Construye el parser de comandos administrativos Developer."""

    parser = argparse.ArgumentParser(
        prog="python -m app.cli.admin",
        description=(
            "Administración local segura del Portal Developer."
        ),
    )

    parser.add_argument(
        "--store",
        type=Path,
        default=None,
        help=argparse.SUPPRESS,
    )

    sub = parser.add_subparsers(
        dest="comando",
        required=True,
    )

    sub.add_parser(
        "bootstrap-owner",
        help="Crear la cuenta Propietario inicial.",
    )

    sub.add_parser(
        "recover-owner",
        help="Recuperar la cuenta Propietario.",
    )

    reset = sub.add_parser(
        "reset-password",
        help="Restablecer la contraseña de una cuenta ordinaria.",
    )
    reset.add_argument(
        "usuario",
        help="Usuario cuya contraseña será restablecida.",
    )

    return parser


def _bootstrap(
    ruta: Path | None,
) -> None:
    """Ejecuta la creación interactiva de la cuenta Propietario inicial."""

    print("=== Bootstrap del Propietario ===")
    usuario = input("Usuario: ").strip()
    nombre = input("Nombre visible: ").strip()
    password = _password_confirmada(
        "Contraseña: "
    )

    propietario, codigo = bootstrap_propietario(
        usuario=usuario,
        nombre_visible=nombre,
        password=password,
        ruta=ruta,
    )

    print()
    print(
        f"Propietario creado: {propietario.usuario}"
    )
    print()
    print(
        "CÓDIGO DE RECUPERACIÓN — SE MUESTRA UNA SOLA VEZ"
    )
    print(codigo)
    print()
    print(
        "Guárdelo fuera del repositorio, fuera del código "
        "y fuera de los archivos .env."
    )


def _recover(
    ruta: Path | None,
) -> None:
    """Ejecuta la recuperación protegida de la cuenta Propietario."""

    print("=== Recuperación del Propietario ===")

    codigo = getpass(
        "Código de recuperación: "
    )
    password = _password_confirmada(
        "Nueva contraseña: "
    )

    propietario, nuevo_codigo = (
        recuperar_propietario(
            codigo_recuperacion=codigo,
            nueva_password=password,
            ruta=ruta,
        )
    )

    print()
    print(
        f"Contraseña recuperada para: {propietario.usuario}"
    )
    print(
        "El código anterior quedó invalidado."
    )
    print()
    print(
        "NUEVO CÓDIGO DE RECUPERACIÓN — "
        "SE MUESTRA UNA SOLA VEZ"
    )
    print(nuevo_codigo)


def _reset(
    usuario_objetivo: str,
    ruta: Path | None,
) -> None:
    """Restablece interactivamente la contraseña de una cuenta ordinaria."""

    print("=== Restablecimiento administrativo ===")

    actor_usuario = input(
        "Usuario que autoriza la operación: "
    ).strip()
    actor_password = getpass(
        "Contraseña del usuario autorizador: "
    )

    actor = autenticar_usuario_developer(
        actor_usuario,
        actor_password,
        ruta,
    )

    if actor is None:
        raise PermissionError(
            "Credenciales de autorización incorrectas."
        )

    nueva_password = _password_confirmada(
        "Nueva contraseña de la cuenta objetivo: "
    )

    actualizado = restablecer_password_developer(
        actor=actor,
        usuario_objetivo=usuario_objetivo,
        nueva_password=nueva_password,
        ruta=ruta,
    )

    print()
    print(
        f"Contraseña restablecida: {actualizado.usuario}"
    )
    print(
        "La cuenta deberá cambiarla en su próximo acceso."
    )


def main(
    argv: list[str] | None = None,
) -> int:
    """Ejecuta el punto de entrada de la CLI administrativa Developer."""

    parser = _crear_parser()
    args = parser.parse_args(argv)

    try:
        if args.comando == "bootstrap-owner":
            _bootstrap(args.store)
        elif args.comando == "recover-owner":
            _recover(args.store)
        elif args.comando == "reset-password":
            _reset(
                args.usuario,
                args.store,
            )
        else:
            parser.error(
                "Comando no reconocido."
            )

        return 0

    except (
        ValueError,
        LookupError,
        PermissionError,
    ) as error:
        print(
            f"ERROR: {error}",
            file=sys.stderr,
        )
        return 1


if __name__ == "__main__":
    raise SystemExit(main())
