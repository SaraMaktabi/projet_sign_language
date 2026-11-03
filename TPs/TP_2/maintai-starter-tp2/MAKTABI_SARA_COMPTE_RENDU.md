# Compte rendu · TP2 : tester, sécuriser et appeler l'API MaintAI

**Groupe : projet_sign_language** …  ·  **Membres :** …  ·  **Date :** …

> Remplissez chaque partie dans ce fichier, puis rendez-le avec la pull request du TP2.
> Collez les sorties du terminal entre les lignes ``` (trois accents graves).

---

## 1. Activité 1 : casser son API (dans `TP/TP1`)

Vos cinq requêtes, le code que vous aviez **prévu**, puis le code **obtenu** dans `/docs` :

| Requête | Ce qui ne va pas | Code prévu | Code obtenu |
|---|---|---:|---:|
| 1 | Champ manquant (`load_pct`) | 422 | 422 |
| 2 | Valeur absurde (`load_pct = 250`) | 422 | 422 |
| 3 | Texte au lieu d'un nombre (`temperature_c = "chaud"`) | 422 | 422 |
| 4 | Champ en trop (`pressure`) | 422 | 422 |
| 5 | Mauvaise route (`/v1/predicte`) | 404 | 404 |

Une de vos prévisions était-elle fausse ? Laquelle, et pourquoi ?

Aucune de nos prévisions n'était fausse. Les quatre premières requêtes sont refusées par la validation de Pydantic avec le code 422. La dernière retourne 404 car la route demandée n'existe pas.
…

Dernière ligne de `python -m pytest` avec `tests/test_casser.py` (dans `TP/TP1`) :

```
==================================================================== 19 passed, 1 warning in 1.96s =======================================
```

À quoi sert `@pytest.mark.parametrize` ? Combien de tests pytest compte-t-il pour votre fonction, et pourquoi ?

@pytest.mark.parametrize permet d'exécuter la même fonction de test plusieurs fois avec des paramètres différents. Dans notre cas, pytest exécute cinq tests, un pour chaque ligne de CAS_REFUSES. Cela évite de répéter cinq fois le même code et permet d'identifier chaque cas dans le rapport.
…

## 2. ruff

Sortie de `ruff check .` dans `TP/TP1` :


``Found 5 errors.
[*] 5 fixable with `--fix`.

Après correction avec ruff check . --fix

Found 7 errors (7 fixed, 0 remaining).`

```

Quelle différence entre `ruff check .` et `python -m pytest` ? Que vérifie chacun ?

ruff check . analyse le code source pour détecter les problèmes de qualité, les erreurs de style et les imports mal organisés. Il permet de garder un code propre et cohérent.

python -m pytest exécute les tests automatisés pour vérifier que les fonctionnalités de l'application fonctionnent correctement et produisent les résultats attendus.
…

## 3. Mise en place du TP2 (dans `TP/TP2`)

Dernière ligne de `python -m pytest` juste après la mise en place :

```
============== 2 failed, 16 passed, 1 warning in 2.73s ====================
```

Quels sont les deux tests qui échouent, et que reçoivent-ils au lieu de 401 ?

FAILED tests/test_security.py::test_missing_key_is_rejected - AssertionError: assert 200 == 401
FAILED tests/test_security.py::test_wrong_key_is_rejected - assert 200 == 401
…

## 4. La clé API (sprint 1)

Votre fonction `require_api_key()` (`maintai/api/security.py`) :

```
def require_api_key(x_api_key: str | None = Header(default=None)) -> None:
    """Refuse la requête si la clé est absente ou fausse."""

    expected_key = get_settings().api_key

    if not expected_key:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Clé API non configurée sur le serveur"
        )

    if not x_api_key or not secrets.compare_digest(x_api_key, expected_key):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Clé API manquante ou invalide"
        )
```

Votre ligne `router = ...` dans `maintai/api/main.py` :

```
router = APIRouter(
    prefix="/v1",
    dependencies=[Depends(require_api_key)]
)
```

Après avoir écrit `security.py` seul (sans toucher au router), combien de tests échouent ? Pourquoi ?

…

Dernière ligne de `python -m pytest` à la fin du sprint 1 :

```
================= 18 passed, 1 warning in 2.17s =========
```

Lancez `uvicorn maintai.api.main:app --reload --env-file .env`, puis envoyez ces requêtes :

| Requête | Code obtenu | Réponse (le corps JSON) |
|---|---:|---|
| `GET /health`, sans clé | 200 | `{"status":"ok","model_loaded":true}` |
| `POST /v1/predict`, relevé normal, sans clé | 401 | `{"detail":"Clé API manquante ou invalide"}` |
| `POST /v1/predict`, relevé normal, fausse clé | 401 | `{"detail":"Clé API manquante ou invalide"}` |
| `POST /v1/predict`, relevé normal, bonne clé | 200 | `[Coller ici la réponse JSON réelle]` |
| `POST /v1/predict`, 500 °C, sans clé | 401 | `{"detail":"Clé API manquante ou invalide"}` |
| `POST /v1/predict`, 500 °C, bonne clé | 422 | Erreur de validation indiquant que la température dépasse la limite autorisée de 150 °C. |

**500 °C sans clé et 500 °C avec la clé ne donnent pas le même code. Pourquoi ?**

Lorsque la requête est envoyée sans clé API, l'authentification échoue en premier et l'API retourne une erreur 401 Unauthorized. Lorsque la clé est correcte, l'authentification passe et FastAPI vérifie ensuite les données envoyées. Comme 500 °C dépasse la limite autorisée de 150 °C, la validation échoue et retourne une erreur 422 Unprocessable Entity.

**Relancez uvicorn sans `--env-file .env` et envoyez un relevé avec votre clé. Quel code obtenez-vous, et pourquoi ce n'est pas 401 ?**

Le code obtenu est 500 Internal Server Error, avec la réponse :

`{"detail":"Clé API non configurée sur le serveur"}`

Sans l'option `--env-file .env`, le serveur ne charge pas la clé API configurée dans le fichier `.env`. La fonction `require_api_key()` constate que la clé attendue est absente et retourne une erreur 500. Ce n'est pas une erreur 401, car le problème vient de la configuration du serveur et non de la clé envoyée par le client.

## 5. La page web (sprint 2)

Votre code `fetch` (le contenu du `addEventListener` dans `web/index.html`) :

```javascript
const url = document.getElementById("url").value.trim();
const apiKey = document.getElementById("key").value;

try {
  const response = await fetch(`${url}/v1/predict`, {
    method: "POST",
    headers: {
      "Content-Type": "application/json",
      "X-API-Key": apiKey
    },
    body: JSON.stringify(reading)
  });

  const data = await response.json();

  if (!response.ok) {
    show("err", `Erreur ${response.status} : ${JSON.stringify(data.detail)}`);
  } else {
    show("ok", JSON.stringify(data, null, 2));
  }
} catch (error) {
  show("err", `Erreur de connexion : ${error.message}`);
}
```

Ce qu'affiche la page (servie sur le port 5500) :

| Essai | Ce qu'affiche la page |
|---|---|
| relevé normal, bonne clé | Résultat de la prédiction (HTTP 200). |
| 500 °C, bonne clé | Erreur HTTP 422 : température hors limites. |
| relevé normal, fausse clé | 	Erreur HTTP 401 : clé API manquante ou invalide. |

**Expérience CORS.** Servez la page sur le port 5501. Que dit la page, et que dit la console (F12) ?

La page affiche une erreur de connexion. La console indique que la requête est bloquée par la politique CORS, car l'origine http://localhost:5501 n'est pas autorisée par l'API.

Pourquoi `curl.exe` obtient-il une réponse alors que la page du port 5501 est bloquée ?

curl.exe n'applique pas la politique CORS des navigateurs. Il peut donc envoyer la requête et recevoir la réponse de l'API. Le navigateur, en revanche, vérifie si l'origine est autorisée par le serveur avant de permettre à la page d'accéder à la réponse.
…

## 6. Les tests de l'activité 1 dans le TP2

Copiez `test_casser.py` dans `TP/TP2/tests`. Sans `headers=HEADERS`, combien de tests échouent, et avec quel code ? Lequel des cinq cas passe quand même, et pourquoi ?

FAILED tests/test_casser.py::test_requete_refusee[champ manquant-/v1/predict-corps0-422] - assert 401 == 422
FAILED tests/test_casser.py::test_requete_refusee[valeur absurde-/v1/predict-corps1-422] - assert 401 == 422
FAILED tests/test_casser.py::test_requete_refusee[texte au lieu d'un nombre-/v1/predict-corps2-422] - assert 401 == 422
FAILED tests/test_casser.py::test_requete_refusee[champ en trop-/v1/predict-corps3-422] - assert 401 == 422
=================== 4 failed, 19 passed, 1 warning in 10.26s =======
…

Dernière ligne de `python -m pytest` avec `headers=HEADERS` :

```
=========== 23 passed, 1 warning in 1.85s =============
```

## 7. Questions de compréhension

**1. Quelle différence entre 401 et 422 ? Et entre 401 et 403 ?**

- **401 Unauthorized** : la requête ne possède pas une clé API valide ou la clé est absente.
- **422 Unprocessable Entity** : la requête est correctement reçue, mais les données envoyées ne respectent pas les règles de validation (exemple : une température de 500 °C).
- **403 Forbidden** : l'utilisateur est authentifié, mais il n'a pas l'autorisation d'accéder à la ressource.

**2. Pourquoi la clé n'est-elle ni dans le code ni dans Git ? Que contiennent `.env` et `.env.example`, et lequel est commité ?**

La clé API est une information sensible. Si elle est écrite directement dans le code ou envoyée sur Git, d'autres personnes pourraient la récupérer et accéder à l'API.

- `.env` contient les vraies valeurs de configuration, notamment la clé API. Il ne doit pas être commité sur Git.
- `.env.example` contient un modèle de configuration avec des valeurs fictives ou des champs à compléter. Il peut être commité pour aider les autres développeurs à configurer le projet.

**3. Pourquoi la clé voyage-t-elle dans un en-tête et pas dans l'URL ?**

La clé API est envoyée dans l'en-tête HTTP `X-API-Key` pour éviter qu'elle apparaisse dans l'URL. Les URL peuvent être enregistrées dans l'historique du navigateur, les logs des serveurs ou les outils de suivi. L'utilisation d'un en-tête réduit donc les risques d'exposition de la clé.

**4. Que fait `secrets.compare_digest` de plus qu'un simple `==` ?**

`secrets.compare_digest` compare deux chaînes de manière sécurisée en limitant les différences de temps d'exécution selon les caractères comparés. Cela réduit le risque d'attaque par analyse temporelle (*timing attack*), contrairement à une comparaison classique avec `==`.

**5. Qu'est-ce qu'une « origine » ? `http://localhost:5500` et `http://localhost:8000` sont-elles la même origine ?**

Une origine est définie par trois éléments :
- Le protocole (HTTP ou HTTPS).
- Le nom d'hôte (localhost, par exemple).
- Le port.

`http://localhost:5500` et `http://localhost:8000` ne sont pas de la même origine, car leurs ports sont différents. Le navigateur applique donc la politique CORS pour contrôler les échanges entre ces deux origines.

## 8. Le rendu Git

- Lien de la pull request : …
- Le tag `tp2` existe sur GitHub : oui / non
- `git status` avant le commit : le fichier `.env` apparaissait-il ? oui / non
- Qui a relu la pull request, et quel commentaire a-t-il laissé ?
  …

## 9. Ce qui reste flou

…
