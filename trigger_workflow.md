# HU 3.8.2 - Configurar el trigger del workflow amb esdeveniments de push

## Objectiu
Configurar el trigger del workflow de GitHub Actions per tal que s'executi automàticament quan es faci un `push` a la branca principal (`main`). Això permet automatitzar el procés de construcció i desplegament de la imatge Docker quan es detecten nous canvis al repositori.

## Passos realitzats

1. **Obrir el fitxer del workflow:**
   Es localitza el fitxer `.github/workflows/docker_build_push.yml` dins del projecte.

2. **Afegir la configuració del trigger:**
   Es configura l'activador per detectar esdeveniments de `push` a la branca `main`:

   ```yaml
   on:
     push:
       branches:
         - main
   ```

3. **Guardar i commitejar el canvi:**
   Un cop afegida la configuració, es desa el fitxer i s'executen les ordres:

   ```bash
   git add .github/workflows/docker_build_push.yml
   git commit -m "Configurar trigger del workflow per esdeveniments de push"
   git push
   ```

4. **Verificar l'execució del workflow:**
   Es comprova que el workflow s'ha executat automàticament des de la pestanya `Actions` de GitHub un cop fet el `push`.

## Resultat esperat

- El workflow s'activa automàticament quan es fa un `push` a la branca `main`.
- L'activador està ben configurat mitjançant `on: push -> branches: main`.
- El workflow apareix a GitHub Actions i comença l'execució automàtica sense intervenció manual.

## Observacions
- Aquest pas és essencial per garantir l'automatització del desplegament.
- Si més endavant es vol que s'activi també en altres branques, simplement s'afegeixen a la llista de `branches`.

