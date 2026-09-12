"""Contrato estructural NOR.3 R3+R4 para ownership HTTP."""

from pathlib import Path
import ast
import unittest

from app.main import app
from app.portals.asegurado.router import router as asegurado_router
from app.portals.developer.router import router as developer_router


ROOT = Path(__file__).resolve().parents[1]

ROUTE_METHODS = {
    "get",
    "post",
    "put",
    "patch",
    "delete",
    "options",
    "head",
}


def _decorated_paths(
    path: Path,
    owner: str,
) -> list[str]:
    tree = ast.parse(
        path.read_text(
            encoding="utf-8"
        )
    )

    result = []

    for node in tree.body:
        if not isinstance(
            node,
            (
                ast.FunctionDef,
                ast.AsyncFunctionDef,
            ),
        ):
            continue

        for decorator in node.decorator_list:
            if not isinstance(
                decorator,
                ast.Call,
            ):
                continue

            func = decorator.func

            if not (
                isinstance(func, ast.Attribute)
                and isinstance(func.value, ast.Name)
                and func.value.id == owner
                and func.attr in ROUTE_METHODS
            ):
                continue

            if (
                decorator.args
                and isinstance(
                    decorator.args[0],
                    ast.Constant,
                )
                and isinstance(
                    decorator.args[0].value,
                    str,
                )
            ):
                result.append(
                    decorator.args[0].value
                )

    return result


def _effective_routes():
    direct = [
        route
        for route in app.routes
        if getattr(
            route,
            "path",
            None,
        )
        is not None
    ]

    return [
        *direct,
        *list(asegurado_router.routes),
        *list(developer_router.routes),
    ]


class TestNOR3R3R4PortalRouters(
    unittest.TestCase
):
    def test_main_es_composition_root_acotado(self):
        main = ROOT / "app" / "main.py"

        self.assertLess(
            len(
                main.read_text(
                    encoding="utf-8"
                ).splitlines()
            ),
            700,
        )

        self.assertEqual(
            {
                "/favicon.ico",
                "/salud",
            },
            set(
                _decorated_paths(
                    main,
                    "app",
                )
            ),
        )

    def test_middleware_no_se_interpreta_como_ruta(self):
        main = ROOT / "app" / "main.py"

        self.assertNotIn(
            "http",
            _decorated_paths(
                main,
                "app",
            ),
        )

    def test_router_developer_posee_29_rutas(self):
        path = (
            ROOT
            / "app"
            / "portals"
            / "developer"
            / "router.py"
        )

        routes = _decorated_paths(
            path,
            "router",
        )

        self.assertEqual(
            29,
            len(routes),
        )

        self.assertTrue(
            all(
                route.startswith("/dev")
                for route in routes
            )
        )

    def test_router_asegurado_posee_24_rutas(self):
        path = (
            ROOT
            / "app"
            / "portals"
            / "asegurado"
            / "router.py"
        )

        routes = _decorated_paths(
            path,
            "router",
        )

        self.assertEqual(
            24,
            len(routes),
        )

        self.assertFalse(
            any(
                route.startswith("/dev")
                for route in routes
            )
        )

    def test_runtime_conserva_60_rutas(self):
        direct = [
            route
            for route in app.routes
            if getattr(
                route,
                "path",
                None,
            )
            is not None
        ]

        self.assertEqual(
            9,
            len(app.routes),
        )

        self.assertEqual(
            7,
            len(direct),
        )

        self.assertEqual(
            60,
            len(
                _effective_routes()
            ),
        )

    def test_ownership_backend_materializado(self):
        self.assertTrue(
            (
                ROOT
                / "app"
                / "portals"
                / "developer"
                / "development_center.py"
            ).is_file()
        )

        self.assertTrue(
            (
                ROOT
                / "app"
                / "portals"
                / "asegurado"
                / "pdf_files.py"
            ).is_file()
        )

        self.assertFalse(
            (
                ROOT
                / "app"
                / "services"
                / "development_center.py"
            ).exists()
        )

        self.assertFalse(
            (
                ROOT
                / "app"
                / "core"
                / "constants.py"
            ).exists()
        )


if __name__ == "__main__":
    unittest.main()
