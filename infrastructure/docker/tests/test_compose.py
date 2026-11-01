import json
import subprocess
import unittest
from functools import lru_cache
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parents[3]
SERVICES = ("postgres", "rustfs")


def run_compose(*args: str) -> subprocess.CompletedProcess[str]:
    return subprocess.run(
        ["docker", "compose", *args],
        cwd=REPO_ROOT,
        text=True,
        capture_output=True,
    )


@lru_cache(maxsize=1)
def compose_config() -> dict:
    result = run_compose("config", "--format", "json")
    if result.returncode != 0:
        raise AssertionError(result.stderr)
    return json.loads(result.stdout)


class ComposeConfigTest(unittest.TestCase):
    def service(self, name: str) -> dict:
        return compose_config()["services"][name]

    def published_ports(self, name: str) -> set[str]:
        return {port["published"] for port in self.service(name).get("ports", [])}

    def mount_points(self, name: str) -> set[tuple[str, str]]:
        return {
            (volume["source"], volume["target"])
            for volume in self.service(name).get("volumes", [])
        }

    def environment(self, name: str) -> dict:
        return self.service(name).get("environment", {})

    def test_compose_es_valido(self) -> None:
        result = run_compose("config")

        self.assertEqual(result.returncode, 0, msg=result.stderr)

    def test_define_postgres_y_rustfs_con_sus_puertos(self) -> None:
        for name in SERVICES:
            self.assertIn(name, compose_config()["services"])

        self.assertIn("5432", self.published_ports("postgres"))
        self.assertIn("9000", self.published_ports("rustfs"))
        self.assertIn("9001", self.published_ports("rustfs"))

    def test_conecta_ambos_servicios_a_la_red_agro_net(self) -> None:
        self.assertIn("agro-net", compose_config().get("networks", {}))
        for name in SERVICES:
            self.assertIn("agro-net", self.service(name).get("networks", {}))

    def test_declara_y_monta_los_volumenes_pgdata_y_rustfs_data(self) -> None:
        self.assertIn("pgdata", compose_config().get("volumes", {}))
        self.assertIn("rustfs-data", compose_config().get("volumes", {}))

        self.assertIn(("pgdata", "/var/lib/postgresql/data"), self.mount_points("postgres"))
        self.assertIn(("rustfs-data", "/data"), self.mount_points("rustfs"))

    def test_aplica_restart_unless_stopped_en_ambos_servicios(self) -> None:
        for name in SERVICES:
            self.assertEqual(self.service(name).get("restart"), "unless-stopped")

    def test_resuelve_las_variables_de_postgres_y_rustfs(self) -> None:
        postgres_env = self.environment("postgres")
        rustfs_env = self.environment("rustfs")

        self.assertEqual(postgres_env.get("POSTGRES_DB"), "agro_help_db")
        for name in ("POSTGRES_USER", "POSTGRES_PASSWORD"):
            self.assertTrue(postgres_env.get(name), f"{name} sin valor")
        for name in ("RUSTFS_ACCESS_KEY", "RUSTFS_SECRET_KEY"):
            self.assertTrue(rustfs_env.get(name), f"{name} sin valor")
