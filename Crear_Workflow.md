# HU 3.8.1 - Crear fitxer de workflow per GitHub Actions

## Objectiu

Crear un fitxer de workflow que automatitzi la construcció i (opcionalment) el desplegament d'una imatge Docker mitjançant GitHub Actions. Aquest fitxer permet que, quan es detectin esdeveniments de codi (com ara un `push`), es pugui executar una sèrie d'accions automatitzades sense intervenció manual.

## Passos realitzats

1. **Crear les carpetes necessàries:**
   Es crea la jerarquia de carpetes dins del projecte:

   ```bash
   mkdir -p .github/workflows
   ```

2. **Crear el fitxer de workflow:**
   Dins de la carpeta `.github/workflows/` es crea el fitxer `docker_build_push.yml` amb el contingut inicial:

   ```yaml
   name: Build and Push Docker Image

   on:
     push:
       branches:
         - main

   jobs:
     build-and-push:
       runs-on: ubuntu-latest

       steps:
         - name: Checkout source code
           uses: actions/checkout@v4

         - name: Login to DockerHub
           uses: docker/login-action@v3
           with:
             username: ${{ secrets.DOCKERHUB_USERNAME }}
             password: ${{ secrets.DOCKERHUB_TOKEN }}

         - name: Build Docker image
           run: |
             docker build -t ${{ secrets.DOCKERHUB_USERNAME }}/via-project-a:latest -t ${{ secrets.DOCKERHUB_USERNAME }}/via-project-a:${{ github.sha }} .

         - name: Push Docker image with 'latest' tag
           run: docker push ${{ secrets.DOCKERHUB_USERNAME }}/via-project-a:latest

         - name: Push Docker image with 'commit hash' tag
           run: docker push ${{ secrets.DOCKERHUB_USERNAME }}/via-project-a:${{ github.sha }}
   ```

3. **Guardar i afegir el fitxer al repositori:**

   ```bash
   git add .github/workflows/docker_build_push.yml
   git commit -m "Create GitHub Actions workflow to build and push Docker image"
   git push
   ```

## Resultat esperat

- El fitxer de workflow `docker_build_push.yml` es troba dins del repositori.
- El seu contingut està preparat per a ser activat amb un `push` a la branca `main`.
- El workflow està llest per ser validat amb esdeveniments futurs.

## Observacions

- Encara que el `push` de la imatge falli si no existeix el repositori o no hi ha permisos, la creació del fitxer és completament funcional.
- Els secrets `DOCKERHUB_USERNAME` i `DOCKERHUB_TOKEN` han d'estar definits en el repositori de GitHub per tal que el login funcioni correctament.

