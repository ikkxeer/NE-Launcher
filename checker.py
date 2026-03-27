"""
checker.py
Verifica si Node.js y npm están instalados en el sistema.
También maneja la instalación abriendo el instalador oficial.
"""

import subprocess
import webbrowser

NODE_DOWNLOAD_URL = "https://nodejs.org/en/download"


def run_command(command: str) -> tuple[bool, str]:
    """Ejecuta un comando en la terminal y devuelve (éxito, output)."""
    try:
        result = subprocess.run(
            command,
            shell=True,
            capture_output=True,
            text=True,
            timeout=10
        )
        output = result.stdout.strip() or result.stderr.strip()
        return result.returncode == 0, output
    except subprocess.TimeoutExpired:
        return False, "Timeout: el comando tardó demasiado."
    except Exception as e:
        return False, str(e)


def check_node() -> tuple[bool, str]:
    """Comprueba si Node.js está instalado. Devuelve (instalado, versión)."""
    ok, version = run_command("node --version")
    return ok, version if ok else "No encontrado"


def check_npm() -> tuple[bool, str]:
    """Comprueba si npm está instalado. Devuelve (instalado, versión)."""
    ok, version = run_command("npm --version")
    return ok, version if ok else "No encontrado"


def get_status() -> dict:
    """Devuelve el estado completo de Node y npm."""
    node_ok, node_version = check_node()
    npm_ok, npm_version = check_npm()

    return {
        "node": {"installed": node_ok, "version": node_version},
        "npm":  {"installed": npm_ok,  "version": npm_version},
        "ready": node_ok and npm_ok,
    }


def open_node_download_page():
    """Abre la página oficial de descarga de Node.js en el navegador."""
    webbrowser.open(NODE_DOWNLOAD_URL)
