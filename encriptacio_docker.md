## Encriptació de contenidors Docker i eines associades

---

### 🔒 Enfocaments d'encriptació i eines disponibles

#### 1. Docker Content Trust (DCT) i Notary

* **Funció**: Signatura digital de les imatges per garantir la seva integritat i autenticitat.
* **Comprovació**:

  ```bash
  export DOCKER_CONTENT_TRUST=1
  docker pull nom-imatge:tag
  docker trust inspect --pretty nom-imatge
  ```
* **Eina associada**: Docker + Notary.

#### 2. Encriptació de dades amb LUKS o fscrypt

* **Funció**: Encriptar els volums o sistemes de fitxers on s'emmagatzemen dades sensibles.
* **Comprovació**:

  ```bash
  lsblk -o NAME,MOUNTPOINT,TYPE,FSTYPE
  sudo cryptsetup status nom_encriptat
  ```

#### 3. Imatges distroless

* **Funció**: Imatges sense shell ni eines de debugging que redueixen la superfície d'atac.
* **Benefici**: No permeten execució remota de comandes no autoritzades.

#### 4. Runtimes aïllats: gVisor i Kata Containers

* **Funció**: Proporcionen aïllament addicional i suport per a entorns encriptats.
* **Comprovació**:

  ```bash
  docker info | grep -i runtime
  docker run --runtime=runsc ...
  ```

#### 5. Docker Secrets

* **Funció**: Injectar secrets de manera segura durant l'execució de contenidors.
* **Combinació recomanada**: Amb un entrypoint personalitzat que valida un token abans d'arrencar serveis.

#### 6. Validació prèvia d'autenticació

* **Mètode**: Entrypoint amb comprovació de token:

  ```bash
  # entrypoint.sh
  if [ "$(cat /run/secrets/token)" != "TOKEN_SEGUR" ]; then
    echo "Token invàlid"
    exit 1
  fi
  exec "$@"
  ```

  Dockerfile:

  ```Dockerfile
  FROM alpine
  COPY entrypoint.sh /entrypoint.sh
  RUN chmod +x /entrypoint.sh
  ENTRYPOINT ["/entrypoint.sh"]
  CMD ["servei"]
  ```

  docker-compose.yml:

  ```yaml
  version: '3.8'
  services:
    servei:
      build: .
      secrets:
        - token
      security_opt:
        - no-new-privileges:true
      cap_drop:
        - ALL
  secrets:
    token:
      file: ./token.txt
  ```

---

### 🎨 Gràfics explicatius

#### Diagrama: Capes de seguretat en contenidors Docker

```
+-----------------------------+
|   Docker Content Trust     |  <- Signatura d'imatge
+-----------------------------+
|   Encriptació de volums    |  <- LUKS / fscrypt
+-----------------------------+
| Runtimes aïllats (gVisor)  |
+-----------------------------+
|  Imatges distroless        |
+-----------------------------+
|  Validació prèvia (token)   |
+-----------------------------+
```

---

### ✅ Verificació de l'encriptació i seguretat

| Aspecte a verificar  | Comprovació                              |
| -------------------- | ---------------------------------------- |
| Signatura d'imatge   | `docker trust inspect`                   |
| Encriptació de dades | `cryptsetup status`, `lsblk`             |
| Usuari no root       | Dockerfile amb `USER`                    |
| Execució remota      | Prova de `docker exec`, hauria de fallar |
| Runtimes segurs      | `docker info` mostra `runsc` o `kata`    |
| Validació prèvia     | Provar arrencar contenidor sense token   |
| Escaneig seguretat   | `trivy`, `dockle`                        |

---

### 🔗 Eines recomanades

| Finalitat                   | Eina                         |
| --------------------------- | ---------------------------- |
| Signatura d'imatges         | Docker Content Trust, Notary |
| Encriptació de dades        | LUKS, fscrypt                |
| Execució sense shell        | Distroless images            |
| Aïllament fort              | gVisor, Kata Containers      |
| Gestor de secrets           | Docker Secrets               |
| Escaneig de vulnerabilitats | Trivy, Dockle                |
| Detecció anomalies          | Falco, Auditd, Prometheus    |

---

### 📊 Conclusions

Encara que Docker no té suport natiu per a contenidors completament encriptats, es pot aconseguir un alt nivell de seguretat combinant:

* Signatures digitals (DCT),
* Encriptació de dades en disc (LUKS, fscrypt),
* Execució d'imatges minimalistes (distroless),
* Secrets gestionats i validació d'autenticació,
* Runtimes aïllats com gVisor o Kata,
* Monitorització i escaneig regular de vulnerabilitats.
