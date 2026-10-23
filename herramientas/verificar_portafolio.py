"""Lista de verificación del repositorio de portafolio (GIT01).

Uso:
    python herramientas/verificar_portafolio.py <carpeta de tu repositorio de portafolio>

Comprueba, sin modificar nada: que sea un repositorio Git con al menos 2 commits, un .gitignore que excluya `.venv/`, `*.db` y archivos privados,
un README con al menos 6 secciones y que no haya subido bases de datos, entornos virtuales ni credenciales evidentes.
"""
from pathlib import Path
import re
import subprocess
import sys

if hasattr(sys.stdout, "reconfigure"):  # una consola Windows cp1252 no debe romper el mensaje
    sys.stdout.reconfigure(errors="replace")

PRIVADOS = (".env", ".env*", "mi_trabajo/", "*.private", "privado/", "secretos/", "secrets/", "credenciales*")
SECRETOS = re.compile(r"(password|passwd|contrase[nñ]a|api[_-]?key|token|secret)\s*[=:]\s*\S{4,}", re.I)


def git(carpeta, *args):
    r = subprocess.run(["git", "-C", str(carpeta), *args], capture_output=True, text=True, encoding="utf-8", errors="replace")
    return r.returncode, r.stdout.strip()


def verificar(carpeta):
    carpeta = Path(carpeta).resolve()
    resultados = []

    def ok(condicion, texto):
        resultados.append((bool(condicion), texto))

    if not (carpeta / ".git").exists():
        raise SystemExit(f"REVISAR: {carpeta} no es un repositorio Git (falta la carpeta .git). Ejecuta `git init` dentro de ella.")
    codigo, n = git(carpeta, "rev-list", "--count", "HEAD")
    ok(codigo == 0 and n.isdigit() and int(n) >= 2, f"Al menos 2 commits (hay {n if codigo == 0 else 0})")

    gi = carpeta / ".gitignore"
    lineas = [l.strip() for l in gi.read_text(encoding="utf-8", errors="replace").splitlines()] if gi.exists() else []
    ok(gi.exists(), ".gitignore existe")
    ok(any(l in (".venv/", ".venv", "/.venv/", "/.venv") for l in lineas), ".gitignore excluye `.venv/`")
    ok("*.db" in lineas, ".gitignore excluye `*.db`")
    ok(any(l in PRIVADOS for l in lineas), ".gitignore excluye archivos privados (`.env`, `mi_trabajo/` o similar)")

    readme = carpeta / "README.md"
    texto = readme.read_text(encoding="utf-8", errors="replace") if readme.exists() else ""
    secciones = re.findall(r"^#{2}\s+\S", texto, re.M)
    ok(readme.exists(), "README.md existe")
    ok(len(secciones) >= 6, f"README con al menos 6 secciones `##` (hay {len(secciones)})")

    _, rastreados = git(carpeta, "ls-files")
    archivos = [a for a in rastreados.splitlines() if a]
    ok(not [a for a in archivos if a.lower().endswith((".db", ".sqlite", ".sqlite3"))], "No hay bases de datos rastreadas por Git")
    ok(not [a for a in archivos if a.startswith(".venv/") or "/.venv/" in a], "No hay entorno virtual rastreado por Git")
    ok(not [a for a in archivos if Path(a).name.startswith(".env")], "No hay archivos `.env` rastreados por Git")
    candidatos = [a for a in archivos if Path(a).suffix.lower() in (".md", ".txt", ".py", ".sql", ".json", ".yml", ".yaml", ".ini", ".cfg", ".toml", ".csv")]
    con_secretos = []
    for a in candidatos:
        p = carpeta / a
        if p.is_file() and p.stat().st_size < 2_000_000 and SECRETOS.search(p.read_text(encoding="utf-8", errors="replace")):
            con_secretos.append(a)
    ok(not con_secretos, "Sin credenciales evidentes en archivos de texto" + (f" (revisa: {', '.join(con_secretos[:3])})" if con_secretos else ""))
    return resultados


def main():
    if len(sys.argv) != 2:
        raise SystemExit(__doc__)
    resultados = verificar(sys.argv[1])
    for bien, texto in resultados:
        print(("OK       " if bien else "REVISAR  ") + texto)
    fallos = sum(1 for b, _ in resultados if not b)
    print(f"\n{len(resultados) - fallos}/{len(resultados)} comprobaciones correctas." + (" Corrige lo marcado como REVISAR y vuelve a ejecutar." if fallos else " Ahora revisa tú `git diff` y `git log --oneline` y explica qué subiste y qué no."))
    raise SystemExit(1 if fallos else 0)


if __name__ == "__main__":
    main()
