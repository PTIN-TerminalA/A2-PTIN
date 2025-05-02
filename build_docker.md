# HU 3.8.3 - Afegir passos per fer build de la imatge Docker

## Objectiu

Afegir al fitxer de workflow de GitHub Actions els passos necessaris per construir automàticament una imatge Docker quan es faci un `push` al repositori (normalment a la branca `main`).

## Passos generals

### 1. Verificar que existeix un `Dockerfile`

Assegura't que el projecte conté un fitxer anomenat `Dockerfile` amb les instruccions per construir la imatge Docker. Exemple de contingut:

```Dockerfile
FROM python:3.10-slim
WORKDIR /app
COPY . .
RUN pip install -r requirements.txt
CMD ["python", "main.py"]
```

Aquest fitxer pot estar a l'arrel del projecte o dins una subcarpeta (per exemple: `./backend` o `./ai`).

### 2. Crear o obrir el fitxer del workflow

El fitxer de workflow s'ha de trobar a la ruta:

```
.github/workflows/docker_build_push.yml
```

### 3. Afegir el pas de construcció de la imatge al workflow

Dins del bloc `steps` del `job`, afegeix el següent pas:

```yaml
- name: Build Docker image
  run: |
    docker build -t ${{ secrets.DOCKERHUB_USERNAME }}/nom-de-la-imatge:latest \
                 -t ${{ secrets.DOCKERHUB_USERNAME }}/nom-de-la-imatge:${{ github.sha }} .
```

Nota: si el `Dockerfile` no es troba a l'arrel, substitueix el `.` pel camí correcte, per exemple `./backend` o `./ai`.

### 4. Afegir secrets al repositori de GitHub

Ves a **Settings > Secrets and variables > Actions** i crea:

* `DOCKERHUB_USERNAME`: nom d'usuari de DockerHub.
* `DOCKERHUB_TOKEN`: token d'accés personal (des de [hub.docker.com](https://hub.docker.com/settings/security)).

### 5. Fer commit i push del fitxer

```bash
git add .github/workflows/docker_build_push.yml
git commit -m "Afegit pas per fer build de la imatge Docker"
git push
```

### 6. Verificar a GitHub Actions

* A la pestanya `Actions`, comprova que el workflow s'ha executat.
* El pas `Build Docker image` hauria d'aparèixer com a completat (✔).

## Resultat esperat

* El workflow detecta un `push` i executa el `docker build` sense errors.
* La imatge es construeix amb dues etiquetes:

  * `latest`
  * hash del commit `${{ github.sha }}`

## Notes addicionals

* El pas de build s'ha de col·locar **abans** dels passos de `docker push`.
* Si el projecte té tests o linting, és recomanable fer-los abans del `docker build`.
* El `Dockerfile` hauria de contenir els camps `EXPOSE` i `CMD` adequats segons el tipus d'aplicació.
