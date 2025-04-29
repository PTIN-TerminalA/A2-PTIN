# Documentación del Workflow: Build and Push Docker Image

## Descripción general
Este workflow de GitHub Actions se activa automáticamente al hacer un `push` a la rama principal (`main`). Su función es:

- Construir una imagen Docker a partir del `Dockerfile` presente en el repositorio.
- Etiquetar la imagen con `latest` y el `commit SHA` actual.
- Subir (push) la imagen al registro de DockerHub.

Automatizar este proceso permite agilizar el flujo de trabajo de desarrollo y despliegue.

## Requisitos previos
Para que el workflow funcione correctamente, se deben cumplir los siguientes requisitos:

- Tener una cuenta en [DockerHub](https://hub.docker.com/).
- Crear y configurar los siguientes **Secrets** en el repositorio de GitHub:
  - `DOCKERHUB_USERNAME`: Nombre de usuario de DockerHub.
  - `DOCKERHUB_TOKEN`: Token de acceso generado en DockerHub (recomendado) o contraseña de usuario.

## Activador del workflow
- **Evento:** Push a la rama `main` (o rama configurada).
- **Condición:** Cada vez que se realiza un push, se dispara automáticamente el workflow.

## Flujo de ejecución
1. **Checkout del código fuente:** Se descarga el contenido del repositorio.
2. **Login en DockerHub:** Se autentica en DockerHub usando los secrets configurados.
3. **Construcción de la imagen Docker:** Utilizando el `Dockerfile` del proyecto.
4. **Etiquetado de la imagen:**
   - `latest`
   - `commit SHA` (identificador del commit que ha activado el workflow)
5. **Push de la imagen a DockerHub:** Publicación de las dos versiones de la imagen.
6. **Error handling:** Si cualquier paso falla, el workflow termina en error y no sube la imagen.

## Resultado esperado
Al finalizar correctamente el workflow:

- Se crea una imagen Docker.
- La imagen queda subida a DockerHub en el repositorio del usuario.
- Existen dos etiquetas asociadas a la imagen:
  - `latest`
  - El hash del commit (`SHA`)

## Comprobación de funcionamiento
- Verificar que el workflow se ejecuta correctamente en la pestaña `Actions` de GitHub.
- Comprobar que las imágenes aparecen en el repositorio de DockerHub con los tags correspondientes.
- En caso de error, revisar los logs proporcionados por GitHub Actions.

## Observaciones
- Se recomienda que antes de construir y subir la imagen, se integren pasos de **tests** y **linting** para asegurar la calidad del código (si el proyecto los tiene).
- Cualquier cambio en el nombre de la imagen o en el Dockerfile puede requerir ajustes en el archivo del workflow.

---

