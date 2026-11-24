# Compte rendu · TP6 : conteneuriser MaintAI (Docker, Docker Compose)

**Groupe :projet_sign_nagiage**   ·  **Membre :RAJI Moaad**  ·  **Date :24/11/2026 17:30** 
---

## 1. Mise en place (dans `TP/TP6`)

Sortie de `docker run hello-world` (première ligne) et de `docker version` (lignes Client et Server) :

```
latest: Pulling from library/hello-world
4f55086f7dd0: Pull complete 
d5e71e642bf5: Download complete 
Digest: sha256:1e4c05b897a751332ce85c7e9449da2d93514ea2dea6dbb0e2753c9e949b2bfa
Status: Downloaded newer image for hello-world:latest

Hello from Docker!

---------------------------------
Client:
 Version:           29.6.1
 API version:       1.55
 Go version:        go1.26.4
 Git commit:        8900f1d
 Built:             Fri Jun 26 11:43:32 2026
 OS/Arch:           windows/amd64
 Context:           desktop-linux

Server: Docker Desktop 4.82.0 (233772)
 Engine:
  Version:          29.6.1
  API version:      1.55 (minimum version 1.40)
  Go version:       go1.26.4
  Git commit:       8ec5ab3
  Built:            Fri Jun 26 11:41:04 2026
  OS/Arch:          linux/amd64
  Experimental:     false
 containerd:
  Version:          v2.2.5
  GitCommit:        e53c7c1516c3b2bff98eb76f1f4117477e6f4e66
 runc:
  Version:          1.3.6
  GitCommit:        v1.3.6-0-g491b69ba
 docker-init:
  Version:          0.19.0
  GitCommit:        de40ad0

```


Dernière ligne de `python -m pytest` après la mise en place :

```text
========= 5 failed, 32 passed, 4 warnings in 41.98s ===========
```

## 2. Image et conteneur (pendant le premier build)

1. Quelle différence entre une image et un conteneur ?
   Une image est un artefact immuable contenant le système et les dépendances. Un conteneur est une instance exécutée de cette image.
2. Pourquoi `COPY requirements-docker.txt` est-il placé avant `COPY maintai` ?
   Pour conserver en cache l’installation des dépendances lorsque seul le code est modifié.
3. Pourquoi `requirements-docker.txt` contient-il `scikit-learn==1.8.0` et pas `scikit-learn>=1.5` ?
   Pour garantir la compatibilité exacte avec le modèle entraîné et la reproductibilité.
4. Pourquoi ni `mlflow`, ni `dvc`, ni `pytest` dans l'image ?
   Ils servent au suivi, au versionnement et aux tests pendant le développement. L’image de production ne les utilise pas.

## 3. Sprint 1 : le Dockerfile

Votre `Dockerfile` :

```dockerfile
FROM python:3.11-slim
WORKDIR /app
COPY requirements-docker.txt .
RUN pip install --no-cache-dir -r requirements-docker.txt
COPY maintai ./maintai
COPY ui ./ui
ENV MAINTAI_MODELS_DIR=/app/models \
    MAINTAI_DATA_PATH=/app/data/sensors.csv
EXPOSE 8000
CMD ["uvicorn", "maintai.api.main:app", "--host", "0.0.0.0", "--port", "8000"]
```


| Build | Durée | Taille de l'image (`docker images`) |
|---|---|---|
| premier build |  28.5s | 259MB  |
| après une modification de `maintai/predict.py` |   0.1s | 259MB  |

Que signifie `CACHED` dans le journal du second build ?

`CACHED` signifie que Docker réutilise une couche déjà construite ; l’installation des dépendances reste donc en cache.

## 4. Sprint 1 : lancer un conteneur


Votre commande `docker run` :

```powershell
docker run -d --name test -p 8002:8000 --env-file .env -v "${PWD}\models:/app/models:ro" maintai:0.4.0
40176f2a2ecfa5f65a32a218db96aae798f58b8693fb8ec24763d41de10e4b94
```

| Essai | Réponse |
|---|---|
| `GET /health` | `200`, avec `model_loaded: true` |
| `POST /v1/predict` sans clé | `401 Unauthorized` |
| `POST /v1/predict` avec la clé | `200`, prédiction retournée |

**Piège 1.** Sans l'option `-v ...models...`, `/health` répond avec `model_loaded: false` et `/v1/predict` répond `503`, car le modèle n’entre pas dans l’image.

**Piège 2.** Avec `--host 127.0.0.1`, le serveur écoute seulement dans le conteneur. `localhost:8002` n’est alors pas joignable depuis le PC ; il faut `0.0.0.0`.



## 5. Sprint 2 : Docker Compose

Votre `compose.yaml` :

```yaml
services:
  api:
    build: .
    image: maintai:0.4.0
    env_file: .env
    ports:
      - "8000:8000"
    volumes:
      - ./models:/app/models:ro
  ui:
    image: maintai:0.4.0
    command: ["python", "-m", "streamlit", "run", "ui/app.py", "--server.address=0.0.0.0", "--server.port=8501", "--server.headless=true"]
    environment:
      MAINTAI_API_URL: http://api:8000
    ports:
      - "8501:8501"
    volumes:
      - ./data:/app/data:ro
    depends_on:
      - api
```


Sortie de `docker compose ps` :

```text
(projet_sign_language) PS C:\Users\hp\Documents\GitHub\projet_sign_language\TPs\TP_6> docker compose up -d --build
#1 [internal] load local bake definitions
#1 reading from stdin 608B 0.0s done
#1 DONE 0.0s

#2 [internal] load build definition from Dockerfile
#2 transferring dockerfile: 504B done
#2 DONE 0.0s

#3 [internal] load metadata for docker.io/library/python:3.11-slim
#3 DONE 1.4s

#4 [internal] load .dockerignore
#4 transferring context: 245B done
#4 DONE 0.0s

#5 [internal] load build context
#5 transferring context: 1.56kB 0.0s done
#5 DONE 0.0s

#6 [1/6] FROM docker.io/library/python:3.11-slim@sha256:61e01f72680f86a5279ad510818ab7b2ee9f049822589d4e34e33e044360356c
#6 resolve docker.io/library/python:3.11-slim@sha256:61e01f72680f86a5279ad510818ab7b2ee9f049822589d4e34e33e044360356c 0.0s done
#6 DONE 0.0s

#7 [2/6] WORKDIR /app
#7 CACHED

#8 [3/6] COPY requirements-docker.txt .
#8 CACHED

#9 [4/6] RUN pip install --no-cache-dir -r requirements-docker.txt
#9 CACHED

#10 [5/6] COPY maintai ./maintai
#10 CACHED

#11 [6/6] COPY ui ./ui
#11 CACHED

#12 exporting to image
#12 exporting layers done
#12 exporting manifest sha256:9d432026e5d4e196e6e44768779bb29899836b660d1b09908fa6a477747aacb0 0.0s done
#12 exporting config sha256:672faab3a4ca1133bf469a7d39d844e2f4fe1d964d9e0efa38169744085437f2 0.0s done
#12 exporting attestation manifest sha256:e69f6db0115153c9b000380863aaca084bb07e86ec636cd59d4ab3ec323bead8
#12 exporting attestation manifest sha256:e69f6db0115153c9b000380863aaca084bb07e86ec636cd59d4ab3ec323bead8 0.0s done
#12 exporting manifest list sha256:e80ff7deacf324916b67a255b266ccf092e6fd9c1ac326420327802df46ee0c5 0.0s done
#12 naming to docker.io/library/maintai:0.4.0 done
#12 unpacking to docker.io/library/maintai:0.4.0 0.0s done
#12 DONE 0.1s

#13 resolving provenance for metadata file
#13 DONE 0.0s
[+] up 4/4
 ✔ Image maintai:0.4.0  Built                                                                                                         2.3s
 ✔ Network tp_6_default Created                                                                                                       0.1s
 ✔ Container tp_6-api-1 Started                                                                                                       0.5s
 ✔ Container tp_6-ui-1  Started                                                                                                       0.7s
```

Quelle URL affiche la barre latérale de l'interface ? D'où vient-elle ?

`http://api:8000`, fournie par la variable `MAINTAI_API_URL`. Depuis le PC, l’interface est accessible sur `http://localhost:8501`.

Résultat des deux commandes `docker compose exec ui ...` (avec `api` puis avec `localhost`). Pourquoi la seconde échoue-t-elle ?

```powershell
(projet_sign_language) PS C:\Users\hp\Documents\GitHub\projet_sign_language\TPs\TP_6> docker compose exec ui python -c "import httpx; print(httpx.get('http://api:8000/health').text)"
{"status":"ok","model_loaded":true}

(projet_sign_language) PS C:\Users\hp\Documents\GitHub\projet_sign_language\TPs\TP_6> docker compose exec ui python -c "import httpx; print(httpx.get('http://localhost:8000/health').text)"
Traceback (most recent call last):
  File "/usr/local/lib/python3.11/site-packages/httpx/_transports/default.py", line 101, in map_httpcore_exceptions
    yield
  File "/usr/local/lib/python3.11/site-packages/httpx/_transports/default.py", line 250, in handle_request
    resp = self._pool.handle_request(req)
           ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
  File "/usr/local/lib/python3.11/site-packages/httpcore/_sync/connection_pool.py", line 256, in handle_request
    raise exc from None
  File "/usr/local/lib/python3.11/site-packages/httpcore/_sync/connection_pool.py", line 236, in handle_request
    response = connection.handle_request(
               ^^^^^^^^^^^^^^^^^^^^^^^^^^
  File "/usr/local/lib/python3.11/site-packages/httpcore/_sync/connection.py", line 101, in handle_request
    raise exc
  File "/usr/local/lib/python3.11/site-packages/httpcore/_sync/connection.py", line 78, in handle_request
    stream = self._connect(request)
             ^^^^^^^^^^^^^^^^^^^^^^
```

La première fonctionne car `api` est le nom DNS du service Compose. La seconde échoue car `localhost` désigne le conteneur `ui`, pas le conteneur `api`.



Dernière ligne de `python -m pytest` à la fin du sprint 2 :

```text
============ 38 passed, 4 warnings in 23.08s ========
```

## 6. Décision : l'ADR 005

Dans `docs/adr/005-image-docker.md`. Résumez ici votre décision en deux phrases :

L’image contient le code et les dépendances figées, mais pas les données, le modèle, les artefacts MLflow ni la clé API. Ces éléments arrivent au lancement par volumes et variables d’environnement afin d’être remplaçables sans reconstruire l’image et sans exposer le secret.

## 7. Questions de compréhension

1. Qu'est-ce qui entre dans l'image, et qu'est-ce qui arrive au lancement ? Donnez le moyen pour chaque élément.
   Le code entre par `COPY`, les bibliothèques par `pip install`, le modèle et les données par volumes, et la clé par `env_file` ou variable d’environnement.
2. Pourquoi la clé API n'est-elle jamais dans l'image ?
   Pour éviter qu’elle apparaisse dans les couches Docker ou soit publiée avec l’image.
3. Livrer un modèle (TP4, TP5) : qu'est-ce que Docker ajoute à la liste ?
   Docker ajoute la reproductibilité, l’isolation des dépendances, le réseau entre services et l’orchestration API/interface.

## 8. Le rendu Git

- Lien de la pull request : …
- Le tag `tp6` existe sur GitHub : oui / non
- `git status` avant le commit : `.env`, `models/` ou `data/*.csv` apparaissaient-ils ? oui / non

## 9. Ce qui reste flou

…
