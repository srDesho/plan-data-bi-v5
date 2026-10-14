# 16.1 Git desde cero: guardar versiones de tu trabajo

> Tiempo estimado: 50 min (lectura 20 + práctica 30). Prerrequisitos: [7.1 Qué es un programa](../07_Python_basico/01_que_es_un_programa.md) (terminal).

## Para qué sirve

Cuando trabajas durante semanas en un proyecto, necesitas poder volver a una versión que funcionaba, saber qué cambió y cuándo, y mostrar tu trabajo a otra persona. Git guarda el historial de tu carpeta de trabajo. Para este curso no necesitas dominarlo: necesitas cinco comandos y una disciplina (guardar algo verificable y describir el cambio).

## Términos nuevos

- **Git**: el programa que registra versiones de los archivos de una carpeta.
- **Repositorio** (*repo*): una carpeta con su historial de versiones (tiene una carpeta oculta `.git`).
- **Commit**: una versión guardada del proyecto, con un mensaje que describe el cambio.
- **Área de preparación** (*staging*): la zona donde eliges **qué archivos** entrarán en el próximo commit (`git add`).
- **`git status`**: muestra qué archivos cambiaron, cuáles están preparados y cuáles no se siguen.
- **`git diff`**: muestra línea por línea qué cambió.
- **`git log`**: lista los commits hechos.
- **`.gitignore`**: un archivo que lista lo que Git **no** debe seguir (entorno virtual, cachés, datos privados, claves).
- **Rama** (*branch*): una línea de trabajo separada. En este curso se trabaja en una sola rama (`main`).
- **Remoto / push**: un repositorio en otro lugar (GitHub); `git push` envía tus commits allí. **Publicar es una acción irreversible en la práctica**: una vez en un sitio público, puede copiarse.

## Ejemplo paso a paso

Todo se prueba en una carpeta temporal para no tocar tu repositorio real. (Los comandos de Git se ejecutan desde Python con `subprocess` solo para mostrar su salida; en tu terminal los escribes directamente.)

**1. Crear un repositorio y ver el estado.**

```python
import subprocess
from pathlib import Path


RAIZ = Path("proyecto")
RAIZ.mkdir(exist_ok=True)


def git(*args):
    r = subprocess.run(["git", "-c", "user.name=Alumno", "-c", "user.email=alumno@ejemplo.org", *args],
                       capture_output=True, text=True, encoding="utf-8", cwd=RAIZ)
    return (r.stdout + r.stderr).strip()


git("init", "-b", "main")
(RAIZ / "consulta.sql").write_text("SELECT 1;\n", encoding="utf-8")
(RAIZ / "notas.md").write_text("# Notas\n", encoding="utf-8")
print(git("status", "--short"))
```

```salida
?? consulta.sql
?? notas.md
```

`git init` crea el repositorio. `git status --short` muestra `??` junto a cada archivo: **no seguido** (Git los ve pero no los guarda aún).

**2. Preparar y guardar: `add` y `commit`.**

```python
import subprocess
from pathlib import Path


RAIZ = Path("proyecto")
RAIZ.mkdir(exist_ok=True)


def git(*args):
    r = subprocess.run(["git", "-c", "user.name=Alumno", "-c", "user.email=alumno@ejemplo.org", *args],
                       capture_output=True, text=True, encoding="utf-8", cwd=RAIZ)
    return (r.stdout + r.stderr).strip()


git("init", "-b", "main")
(RAIZ / "consulta.sql").write_text("SELECT 1;\n", encoding="utf-8")
(RAIZ / "notas.md").write_text("# Notas\n", encoding="utf-8")

git("add", "consulta.sql")
print(git("status", "--short"))
git("commit", "-m", "Primera consulta SQL")
print(git("status", "--short"))
print(git("log", "--format=%s"))
```

```salida
A  consulta.sql
?? notas.md
?? notas.md
Primera consulta SQL
```

Se preparó **solo** `consulta.sql` (`A` = añadido; `notas.md` sigue `??`). Después del commit, `consulta.sql` ya no aparece como pendiente y el log muestra el mensaje. **Añade archivos concretos**, no `git add .` a ciegas: evita guardar archivos que no querías (datos privados, salidas grandes).

**3. Ver qué cambió: `diff`.**

```python
import subprocess
from pathlib import Path


RAIZ = Path("proyecto")
RAIZ.mkdir(exist_ok=True)


def git(*args):
    r = subprocess.run(["git", "-c", "user.name=Alumno", "-c", "user.email=alumno@ejemplo.org", *args],
                       capture_output=True, text=True, encoding="utf-8", cwd=RAIZ)
    return (r.stdout + r.stderr).strip()


git("init", "-b", "main")
(RAIZ / "consulta.sql").write_text("SELECT 1;\n", encoding="utf-8")
git("add", "consulta.sql")
git("commit", "-m", "Primera consulta SQL")

(RAIZ / "consulta.sql").write_text("SELECT 1;\nSELECT 2;\n", encoding="utf-8")
print(git("status", "--short"))
salida = git("diff", "--unified=0", "consulta.sql").splitlines()
print([l for l in salida if l.startswith(("+", "-")) and not l.startswith(("+++", "---"))])
```

```salida
M consulta.sql
['+SELECT 2;']
```

` M` significa **modificado**. El `diff` muestra solo las líneas agregadas (`+`) o quitadas (`-`): aquí se agregó `SELECT 2;`. Revisar el `diff` antes de cada commit es la costumbre que evita guardar cosas por accidente.

**4. Ignorar lo que no debe versionarse.**

```python
import subprocess
from pathlib import Path


RAIZ = Path("proyecto")
RAIZ.mkdir(exist_ok=True)


def git(*args):
    r = subprocess.run(["git", "-c", "user.name=Alumno", "-c", "user.email=alumno@ejemplo.org", *args],
                       capture_output=True, text=True, encoding="utf-8", cwd=RAIZ)
    return (r.stdout + r.stderr).strip()


git("init", "-b", "main")
(RAIZ / ".gitignore").write_text(".venv/\n__pycache__/\n*.db\nsecretos.txt\n", encoding="utf-8")
(RAIZ / "secretos.txt").write_text("clave-falsa\n", encoding="utf-8")
(RAIZ / "reporte.db").write_bytes(b"binario")
(RAIZ / "etl.py").write_text("print('hola')\n", encoding="utf-8")
print(git("status", "--short"))
```

```salida
?? .gitignore
?? etl.py
```

`secretos.txt` y `reporte.db` **no aparecen**: `.gitignore` los oculta. Debe ignorar el entorno virtual (`.venv/`), cachés (`__pycache__/`), bases de datos y salidas grandes, y **cualquier credencial o dato privado**. Si algo ya se versionó antes de ignorarlo, ignorarlo después no lo borra del historial: por eso el `.gitignore` se escribe **al comienzo**.

**5. La rutina mínima.**

1. Termina una actividad que puedas **verificar** (la consulta da el resultado esperado, el corrector pasa).
2. `git status` para ver qué cambió.
3. `git diff` para revisar las líneas.
4. `git add archivo1 archivo2` (archivos concretos).
5. `git commit -m "mensaje claro"`.
6. Solo si decides publicarlo: revisa qué se va a subir y recién entonces `git push`.

**6. Mensajes de commit útiles.**

| Mal | Bien |
|---|---|
| `cambios` | `Agrega consulta de ventas entregadas por ruta` |
| `fix` | `Corrige el filtro de estado: excluye anuladas` |
| `final final 2` | `Añade validación de cuadre de filas al ETL` |

Un buen mensaje dice **qué** cambió y, si no es obvio, **por qué**.

**7. Lo que NO hace falta en este curso.** Ramas complejas, rebase, fusiones y resolución de conflictos quedan para un nivel posterior. Trabajas en una sola rama. Tampoco es necesario un commit todos los días: un día de descanso no se mide con commits (lección 16.3).

**8. Qué nunca va a Git.** Credenciales y claves; bases de datos reales de una empresa; datos personales de clientes; archivos con información del empleador. Los datos de este curso son sintéticos o inventados y sí pueden versionarse. Si por error guardas algo privado, no lo «borres en el siguiente commit»: el historial lo conserva; hay que reescribir el historial con cuidado o rotar la credencial, y conviene pedir ayuda.

Ejemplo comercial: después de terminar la consulta de ventas por ruta y verificarla contra Excel, haces `git add consulta_rutas.sql`, `git commit -m "Consulta de ventas entregadas por ruta, cuadrada con Excel"`. Dentro de un mes, `git log` te cuenta la historia de tu aprendizaje.

## Errores comunes

- **`git add .` sin revisar** y subir un archivo privado.
- **Mensajes vagos** (`cambios`).
- **Empezar sin `.gitignore`.**
- **Guardar la base de datos o las salidas grandes.**
- **Publicar (`push`) sin revisar** qué se envía.
- **Subir credenciales** «por un momento».
- **Medir el progreso por cantidad de commits** en lugar de por lo que puedes explicar.

## Para comprobar que entendiste

1. ¿Qué diferencia hay entre `git add` y `git commit`?
2. ¿Qué hace `git status --short` con un archivo nuevo sin seguir?
3. ¿Para qué sirve `.gitignore` y cuándo conviene escribirlo?
4. ¿Por qué no basta borrar una credencial en un commit posterior?

<details><summary>Respuestas</summary>

1. `add` prepara archivos para el próximo commit; `commit` guarda la versión con un mensaje.
2. Lo marca con `??`.
3. Para que Git no siga archivos que no deben versionarse; conviene escribirlo al principio.
4. Porque el historial conserva la versión anterior donde estaba la credencial.

</details>

## Micropráctica

1. En una carpeta de práctica fuera de tu repo del curso, crea un repositorio, un archivo `.py` y un `.gitignore` que excluya `.venv/` y `*.db`.
2. Haz dos commits con mensajes claros y comprueba el log.
3. Modifica el archivo, revisa el `diff` y escribe qué línea se agregó.
4. Escribe una lista de cinco cosas que nunca subirías.

Cómo saber que está bien: `git log --oneline` muestra tus dos commits y `git status` queda limpio.

<details><summary>Comprobación de los pasos 1 y 2</summary>

```python
import subprocess
from pathlib import Path


RAIZ = Path("proyecto")
RAIZ.mkdir(exist_ok=True)


def git(*args):
    r = subprocess.run(["git", "-c", "user.name=Alumno", "-c", "user.email=alumno@ejemplo.org", *args],
                       capture_output=True, text=True, encoding="utf-8", cwd=RAIZ)
    return (r.stdout + r.stderr).strip()


git("init", "-b", "main")
(RAIZ / ".gitignore").write_text(".venv/\n*.db\n", encoding="utf-8")
(RAIZ / "etl.py").write_text("print('v1')\n", encoding="utf-8")
git("add", ".gitignore", "etl.py")
git("commit", "-m", "Primera versión del ETL")
(RAIZ / "etl.py").write_text("print('v1')\nprint('v2')\n", encoding="utf-8")
git("add", "etl.py")
git("commit", "-m", "Agrega segunda etapa")
print(git("log", "--format=%s"))
print(repr(git("status", "--short")))
```

```salida
Agrega segunda etapa
Primera versión del ETL
''
```

</details>

## Después, en los ejercicios

Usa esta rutina en el proyecto SQL, el proyecto ETL y el portafolio. La publicación en GitHub es de ejecución manual: **nada se sube automáticamente desde este paquete**. Siguiente: [16.2 Documentar y explicar tu trabajo](02_documentar_y_explicar.md).
