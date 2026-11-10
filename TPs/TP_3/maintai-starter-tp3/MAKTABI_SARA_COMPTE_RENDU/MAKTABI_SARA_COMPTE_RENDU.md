# Compte rendu · TP3 : une interface Streamlit pour MaintAI

**Groupe :** …  ·  **Membres :** …  ·  **Date :** …

> Remplissez chaque partie dans ce fichier, puis rendez-le avec la pull request du TP3.
> Collez les sorties du terminal entre les lignes ``` (trois accents graves).

---

## 1. Mise en place (dans `TP/TP3`)

Dernière ligne de `python -m pytest` juste après la mise en place :

```
============================== 5 failed, 18 passed, 1 warning in 10.26s =======================
```

Quels fichiers de tests échouent, et quelle erreur donnent-ils ?

FAILED tests/test_client.py::test_client_returns_prediction - NotImplementedError: TP3 sprint 2 : MaintaiClient.predict
FAILED tests/test_client.py::test_client_wrong_key_raises_401 - NotImplementedError: TP3 sprint 2 : MaintaiClient.predict
FAILED tests/test_client.py::test_client_bad_reading_raises_422 - NotImplementedError: TP3 sprint 2 : MaintaiClient.predict
FAILED tests/test_ui.py::test_ui_shows_the_data - IndexError: list index out of range
FAILED tests/test_ui.py::test_ui_shows_the_prediction - IndexError: list index out of range
…

## 2. Lancer Streamlit

Lancez d'abord `streamlit run ui/app.py`. Que s'affiche-t-il dans le navigateur ?

```
ModuleNotFoundError: No module named 'maintai'
Traceback:
File "D:\Users\Sara\Documents\Semestre 9 IADA\app ai\projet_sign_language\TPs\TP_3\maintai-starter-tp3\ui\app.py", line 9, in <module>
    from maintai.client import APIError, MaintaiClient
```

Lancez ensuite `python -m streamlit run ui/app.py`. Pourquoi cette commande fonctionne-t-elle et pas la première ?

Lors du lancement avec `streamlit run ui/app.py`, le navigateur affiche une erreur `ModuleNotFoundError: No module named 'maintai'`. Python ne parvient pas à trouver le package `maintai`.

En revanche, la commande `python -m streamlit run ui/app.py` fonctionne, car elle lance Streamlit à travers l'interpréteur Python de l'environnement actif. Cela permet à Streamlit d'utiliser le même environnement et le même chemin de recherche des modules Python, dans lequel le package `maintai` est accessible.

La différence est donc liée à la manière dont Streamlit est lancé et à l'interpréteur Python utilisé.
…

## 3. Sprint 1 : l'onglet « Données »

Votre code de l'onglet « Données » (de `c1, c2, c3 = ...` jusqu'au nuage de points) :

# Sprint 1 : explorer les données


with onglet_donnees:
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
    )

```

| Indicateur | Valeur affichée |
|---|---|
| Relevés | 5000 |
| Taux de panne | 13.6 % |
| Température moyenne | 59.8 °C |

Choisissez vibration_mm_s dans la liste. Comment évolue le taux de panne quand la vibration augmente ?

Lorsque la vibration augmente, le taux de panne augmente également. Les vibrations élevées indiquent un risque plus important de panne.
…

**1. Ajoutez un `print("relance")` en haut de `ui/app.py`, puis déplacez un curseur. Que voyez-vous dans le terminal, et qu'est-ce que cela montre sur le fonctionnement de Streamlit ?**

À chaque déplacement du curseur, le message `relance` apparaît dans le terminal. Cela montre que Streamlit réexécute automatiquement le script de haut en bas à chaque interaction avec un élément de l'interface.

**2. À quoi sert `@st.cache_data` sur la fonction `charger` ?**

`@st.cache_data` permet de mettre en cache le résultat de la fonction `charger`. Ainsi, le fichier CSV n'est pas relu à chaque réexécution du script. Streamlit réutilise les données déjà chargées, ce qui améliore les performances et évite les lectures répétitives du fichier.


## 4. Sprint 2 : l'onglet « Prédiction »

Votre méthode `predict` (`maintai/client.py`) :

```    if envoye:
        try:
            client = MaintaiClient(url, api_key=cle)
            resultat = client.predict(releve)

        except APIError as e:
            st.warning(f"Erreur {e.code} : {e.detail}")

        except httpx.HTTPError as e:
            st.error(f"API injoignable : {e}")

        else:
            pct = round(resultat["failure_probability"] * 100)

            st.metric("Probabilité de panne", f"{pct} %")

            if resultat["alert"]:
                st.error("Alerte : risque de panne détecté !")
            else:
                st.success("Fonctionnement normal : aucun risque de panne détecté.")
```

Dernière ligne de `python -m pytest` à la fin du sprint 2 :

```
===== 23 passed, 1 warning in 3.44s =======
```

| Essai | Ce qu'affiche Streamlit |
|---|---|
| Valeurs par défaut, bonne clé | La probabilité de panne s'affiche en pourcentage, accompagnée d'un message indiquant le risque de panne ou le fonctionnement normal. |
| Valeurs par défaut, fausse clé | Un avertissement s'affiche avec l'erreur HTTP 401 : clé API manquante ou invalide. |
| API arrêtée (Ctrl+C dans le terminal d'uvicorn) | Un message d'erreur s'affiche : API injoignable, avec une erreur de connexion. |

**Le port 8501 n'est pas dans `MAINTAI_CORS_ORIGINS`, et pourtant la prédiction fonctionne. Pourquoi ?**

Streamlit communique avec l'API directement depuis le serveur Python, et non depuis le navigateur. La politique CORS est appliquée par les navigateurs web et ne bloque donc pas cette communication entre deux programmes Python.

## 5. Questions de compréhension

**1. Dans la page web du TP2, qui envoie la requête à l'API ? Et dans Streamlit ?**

Dans le TP2, c'est le navigateur qui envoie la requête à l'API grâce à JavaScript et à la fonction `fetch()`.

Dans Streamlit, c'est le serveur Python qui envoie la requête grâce à `httpx`, utilisé par la classe `MaintaiClient`.

**2. Pourquoi les tests de `test_client.py` n'ont-ils pas besoin d'uvicorn ?**

Les tests utilisent un client de test fourni directement à `MaintaiClient` grâce au paramètre `http`. Ce client simule les requêtes HTTP vers l'API sans avoir besoin de démarrer un véritable serveur avec uvicorn.

**3. Page HTML + JavaScript (TP2) ou Streamlit (TP3) : laquelle choisiriez-vous pour une démonstration à un client ? Et pour l'application d'un technicien de maintenance ? Pourquoi ?**

Pour une démonstration à un client, je choisirais Streamlit, car son interface est simple, rapide à mettre en place et permet de présenter facilement les données et les prédictions.

Pour un technicien de maintenance, je choisirais également Streamlit, car il peut explorer les données, modifier les paramètres d'un relevé et obtenir une prédiction sans avoir besoin de connaissances en programmation.

## 6. Le rendu Git

- Lien de la pull request : [À compléter]
- Le tag `tp3` existe sur GitHub : [Oui / Non]
- `git status` avant le commit : `.env`, `data/` ou `models/` apparaissaient-ils ? [Oui / Non]

## 7. Ce qui reste flou

Aucun point particulier pour le moment.