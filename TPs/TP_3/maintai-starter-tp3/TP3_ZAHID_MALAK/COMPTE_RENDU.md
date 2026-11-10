# Compte rendu · TP3 : une interface Streamlit pour MaintAI

**Groupe :** …  ·  **Membres :** …  ·  **Date :** …

> Remplissez chaque partie dans ce fichier, puis rendez-le avec la pull request du TP3.
> Collez les sorties du terminal entre les lignes ``` (trois accents graves).

---

## 1. Mise en place (dans `TP/TP3`)

Dernière ligne de `python -m pytest` juste après la mise en place :

Quels fichiers de tests échouent, et quelle erreur donnent-ils ?

FAILED tests/test_client.py::test_client_returns_prediction - NotImplementedError: TP3 sprint 2 : MaintaiClient.predict
FAILED tests/test_client.py::test_client_wrong_key_raises_401 - NotImplementedError: TP3 sprint 2 : MaintaiClient.predict
FAILED tests/test_client.py::test_client_bad_reading_raises_422 - NotImplementedError: TP3 sprint 2 : MaintaiClient.predict
FAILED tests/test_ui.py::test_ui_shows_the_data - IndexError: list index out of range
FAILED tests/test_ui.py::test_ui_shows_the_prediction - IndexError: list index out of range

## 2. Lancer Streamlit

Lancez d'abord `streamlit run ui/app.py`. Que s'affiche-t-il dans le navigateur ?
ModuleNotFoundError: No module named 'maintai'
Traceback:
File "C:\Users\Malak\OneDrive\Documents\S2_EMSI\DM\projet_sign_language\TPs\TP3\maintai-starter-tp3\ui\app.py", line 9, in <module>
    from maintai.client import APIError, MaintaiClient


Lancez ensuite `python -m streamlit run ui/app.py`. Pourquoi cette commande fonctionne-t-elle et pas la première ?

fonctionne car elle lance Streamlit avec le même interpréteur Python que celui de l’environnement virtuel actif (.venv).

FileNotFoundError: [Errno 2] No such file or directory: 'C:\\Users\\Malak\\OneDrive\\Documents\\S2_EMSI\\DM\\projet_sign_language\\TPs\\TP3\\maintai-starter-tp3\\data\\sensors.csv'
Traceback:
File "C:\Users\Malak\OneDrive\Documents\S2_EMSI\DM\projet_sign_language\TPs\TP3\maintai-starter-tp3\ui\app.py", line 30, in <module>
    df = charger(get_settings().data_path)
File "C:\Users\Malak\OneDrive\Documents\S2_EMSI\DM\projet_sign_language\TPs\TP3\maintai-starter-tp3\ui\app.py", line 19, in charger
    return pd.read_csv(path)
           ~~~~~~~~~~~^^^^^^
File "C:\Users\Malak\OneDrive\Documents\S2_EMSI\DM\projet_sign_language\TPs\TP3\maintai-starter-tp3\.venv\Lib\site-packages\pandas\io\parsers\readers.py", line 873, in read_csv
    return _read(filepath_or_buffer, kwds)
File "C:\Users\Malak\OneDrive\Documents\S2_EMSI\DM\projet_sign_language\TPs\TP3\maintai-starter-tp3\.venv\Lib\site-packages\pandas\io\parsers\readers.py", line 300, in _read
    parser = TextFileReader(filepath_or_buffer, **kwds)
File "C:\Users\Malak\OneDrive\Documents\S2_EMSI\DM\projet_sign_language\TPs\TP3\maintai-starter-tp3\.venv\Lib\site-packages\pandas\io\parsers\readers.py", line 1645, in __init__
    self._engine = self._make_engine(f, self.engine)
                   ~~~~~~~~~~~~~~~~~^^^^^^^^^^^^^^^^
File "C:\Users\Malak\OneDrive\Documents\S2_EMSI\DM\projet_sign_language\TPs\TP3\maintai-starter-tp3\.venv\Lib\site-packages\pandas\io\parsers\readers.py", line 1904, in _make_engine
    self.handles = get_handle(
                   ~~~~~~~~~~^
        f,
        ^^
    ...<6 lines>...
        storage_options=self.options.get("storage_options", None),
        ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
    )
    ^
File "C:\Users\Malak\OneDrive\Documents\S2_EMSI\DM\projet_sign_language\TPs\TP3\maintai-starter-tp3\.venv\Lib\site-packages\pandas\io\common.py", line 926, in get_handle
    handle = open(
        handle,
    ...<3 lines>...
        newline="",
    )

## 3. Sprint 1 : l'onglet « Données »

Votre code de l'onglet « Données » (de `c1, c2, c3 = ...` jusqu'au nuage de points) :

<!-- with onglet_donnees:
    df = charger(get_settings().data_path)

    # 1. Trois indicateurs
    col1, col2, col3 = st.columns(3)

    col1.metric("Nombre de relevés", len(df))
    col2.metric("Taux de panne", f"{df.failure.mean():.1%}")
    col3.metric("Température moyenne", f"{df.temperature_c.mean():.1f} °C")

    # 2. Choisir une variable
    variable = st.selectbox("Choisir une variable", FEATURES)

    # 3. Taux de panne par tranche
    tranches = pd.cut(df[variable], bins=10)
    taux = df.groupby(tranches, observed=True).failure.mean()

    graphique = pd.DataFrame({
        "Milieu de tranche": [round(i.mid, 2) for i in taux.index],
        "Taux de panne": taux.values
    })

    st.subheader(f"Taux de panne selon {variable}")
    st.bar_chart(graphique.set_index("Milieu de tranche"))

    # 4. Nuage de points température / vibration
    df_nuage = df.copy()
    df_nuage["Panne"] = df_nuage["failure"].map({
        0: "Non",
        1: "Oui"
    })

    st.subheader("Température et vibration selon la panne")
    st.scatter_chart(
        df_nuage,
        x="temperature_c",
        y="vibration_mm_s",
        color="Panne"
    ) -->
| Indicateur | Valeur affichée |
|---|---|
| Relevés | 5000 |
| Taux de panne | 13.6 % |
| Température moyenne | 59.8 °C |

Choisissez `vibration_mm_s` dans la liste. Comment évolue le taux de panne quand la vibration augmente ?

Lorsque la vibration augmente, le taux de panne augmente également. Les vibrations élevées indiquent un risque plus important de panne.

Ajoutez un `print("relance")` en haut de `ui/app.py`, puis déplacez un curseur. Que voyez-vous dans le terminal, et qu'est-ce que cela montre sur le fonctionnement de Streamlit ?

À chaque déplacement du curseur, le message relance apparaît à nouveau dans le terminal. Cela montre que Streamlit réexécute tout le script Python depuis le début à chaque interaction avec l’interface. Le décorateur @st.cache_data évite cependant de recalculer inutilement les données déjà chargées.

À quoi sert `@st.cache_data` sur la fonction `charger` ?


## 4. Sprint 2 : l'onglet « Prédiction »

Votre méthode `predict` (`maintai/client.py`) :

@st.cache_data permet de mémoriser le résultat de la fonction charger. 

Dernière ligne de `python -m pytest` à la fin du sprint 2 :

==================== 4 failed, 19 passed, 1 warning in 7.82s ====================

Avec l'API lancée (`uvicorn maintai.api.main:app --reload --env-file .env`) :

| Essai | Ce qu'affiche Streamlit |
|---|---|
| valeurs par défaut, bonne clé | Probabilité de panne : 95 % et message d'alerte |
| valeurs par défaut, fausse clé | Erreur API 401 : Clé API absente ou invalide |
| API arrêtée (Ctrl+C dans le terminal d'uvicorn) | API injoignable |

Le port 8501 n'est pas dans `MAINTAI_CORS_ORIGINS`, et pourtant la prédiction fonctionne

car Streamlit envoie la requête depuis le code Python avec `MaintaiClient`. La requête ne vient pas directement du navigateur : elle ne subit donc pas la restriction CORS.



1. Dans la page web du TP2, qui envoie la requête à l'API ? Et dans Streamlit ?

Dans le TP2, le navigateur exécute le code JavaScript et envoie la requête avec `fetch()`.

Dans Streamlit, c'est le code Python qui envoie la requête à l'API grâce à `MaintaiClient`.

2. Pourquoi les tests de `test_client.py` n'ont-ils pas besoin d'uvicorn ?

Les tests utilisent `TestClient` de FastAPI. Les requêtes sont envoyées directement à l'application en mémoire, sans démarrer un serveur uvicorn.

3. Page HTML + JavaScript ou Streamlit ?

Pour une démonstration à un client, je choisirais Streamlit, car l'interface permet de présenter rapidement les graphiques et les prédictions.

Pour l'application d'un technicien de maintenance, je choisirais une page HTML + JavaScript améliorée, car elle permet davantage de personnaliser l'ergonomie, le design et les fonctionnalités professionnelles.

## 6. Le rendu Git

- Lien de la pull request : …
- Le tag `tp3` existe sur GitHub : oui / non
- `git status` avant le commit : `.env`, `data/` ou `models/` apparaissaient-ils ? oui / non

## 7. Ce qui reste flou

…
