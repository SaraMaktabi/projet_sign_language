# ADR 004 — Choix du modèle

## Statut

Accepté.

## Contexte

MaintAI doit prédire les pannes industrielles.
Une panne non détectée est plus coûteuse qu'une fausse alerte.
Le recall est donc la métrique prioritaire.

## Décision

Nous retenons la régression logistique avec un seuil de 0.2,
entraînée sur la version v1 des données.

## Justification

Ce modèle présente le meilleur recall parmi les runs MLflow :

- Accuracy : 88.2 %
- Recall : 83.8 %
- Precision : 54.3 %
- Seuil : 0.2

## Traçabilité

- Run ID : 3314f3695ce845c398559b333339917f
- Version des données : v1
- Commit Git : 9edf02b
- data_md5 : 73e0b7cb3c6f795c70c3ddf970b99c15

## Conséquences

La diminution du seuil permet de détecter davantage de pannes,
mais augmente le nombre de fausses alertes.

MLflow et DVC permettent de retrouver le modèle et la version
exacte des données utilisées lors de son entraînement.

## 6. Questions de compréhension

1. **Quelle différence entre Git, DVC et MLflow ? Que versionne chacun ?**

   - Git : versionne le code source et les fichiers de configuration.
   - DVC : versionne les jeux de données.
   - MLflow : assure le suivi des expériences, des hyperparamètres,
     des métriques et des modèles entraînés.

2. **Pourquoi le stockage DVC est-il ajouté avec `--local` dans ce TP ?
   Que faudrait-il pour que tout le groupe partage les mêmes données ?**

   L'option `--local` permet de conserver une configuration propre
   à chaque machine, sans la versionner dans Git.
   Pour partager les données, il faudrait configurer un stockage
   distant commun, accessible à tous les membres du groupe.

3. **Livrer un modèle, c'est trois choses (TP4).
   Lesquelles, et où sont-elles maintenant ?**

   - Le modèle entraîné : sauvegardé dans les artefacts MLflow.
   - Le code de prédiction : versionné dans Git.
   - Les dépendances : déclarées dans le `pyproject.toml` et
     enregistrées avec leurs versions dans le `requirements.txt`
     généré par MLflow.