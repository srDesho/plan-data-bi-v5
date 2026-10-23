# GIT01 · Tu repositorio de portafolio

Nivel 1/3 · Tiempo objetivo 30 min · Primera vez: 27–33 min.
Requisito previo: haber estudiado la lección [16.1 · Git desde cero](../../02_TEORIA/16_Git_comunicacion/01_git_desde_cero.md) y haber hecho su micropráctica en una carpeta de práctica. Aquí creas el repositorio **real** de tu portafolio.

## Situación

Quien revise tu perfil de GitHub verá primero tu README y tu historial de commits. Necesitas un repositorio ordenado, que explique qué hay en él, que nunca incluya datos privados y que tenga un historial entendible desde el principio.

## Qué debes hacer

1. Crea una carpeta **fuera de este repositorio** (por ejemplo `C:\portafolio-datos` o `~/portafolio-datos`) y ejecuta `git init` dentro de ella.
2. Escribe un `README.md` con estas **seis secciones** (`##`): Problema, Datos, Método, Resultados, Límites y Cómo reproducir. Aún puedes dejarlas breves; lo importante es la estructura y no incluir datos privados ni credenciales.
3. Crea un `.gitignore` que excluya como mínimo `.venv/`, `*.db` y una entrada para archivos privados (por ejemplo `.env` o `mi_trabajo/`).
4. Haz el **primer commit** con el README y el `.gitignore`.
5. Agrega un archivo de trabajo terminado (por ejemplo, una consulta SQL tuya ya corregida con su comentario de interpretación). Antes del segundo commit, revisa `git status` y **`git diff`** (o `git diff --staged`) y confirma qué entra.
6. Haz el **segundo commit** con un mensaje que diga qué cambió. Revisa `git log --oneline`.
7. En un archivo propio (`mi_trabajo/git/GIT01_nunca_subir.md`, no dentro del portafolio) lista **5 cosas que nunca subirás** a un repositorio público y explica en una frase por qué cada una.

## Cómo comprobarlo

`python herramientas/verificar_portafolio.py <carpeta de tu portafolio>`. Comprueba: repositorio Git con al menos 2 commits, `.gitignore` con `.venv/`, `*.db` y archivos privados, README con al menos 6 secciones, y que no haya bases de datos, entornos virtuales ni credenciales evidentes en lo rastreado. Después revisa tú mismo `git diff` y `git log --oneline`: la herramienta no sustituye tu lectura del `diff`.

Entrega: la carpeta del repositorio, la captura de `git log --oneline` y tu lista de 5 cosas que nunca subirás.

## Pistas (en este orden, solo cuando las necesites)

1. **Orientación.** Haz la secuencia completa en una carpeta vacía: `git init`, crear archivos, `git add`, `git commit`, cambiar algo, `git add`, `git commit`. Son solo seis comandos distintos.
2. **Concepto Git.** `git add` prepara cambios, `git commit` los guarda con un mensaje, `git diff` muestra lo que cambió y todavía no está preparado, y `git log --oneline` resume el historial (lección 16.1).
3. **Si no cuadra.** Si Git ya rastrea un archivo que luego pusiste en `.gitignore`, ignorarlo no lo quita del historial: pide ayuda antes de subir nada y mueve el archivo fuera de la carpeta.

Método: intenta 10 minutos antes de leer la primera pista y depura otros 10 antes de la tercera.

## Criterios de aceptación

- [ ] Tu repositorio tiene al menos 2 commits con mensajes que explican el cambio.
- [ ] `.gitignore` excluye `.venv/`, `*.db` y archivos privados.
- [ ] El README tiene las 6 secciones y no incluye credenciales ni datos privados.
- [ ] Revisaste `git diff` antes del segundo commit.
- [ ] Escribiste 5 cosas que nunca subirás, cada una con su motivo.
- [ ] `python herramientas/verificar_portafolio.py <tu carpeta>` no marca nada como REVISAR.

No subas el repositorio a GitHub todavía si no has revisado que ningún archivo de `04_DATASETS/` ni de `mi_trabajo/` esté dentro de él.
