# Compte rendu · TP5 : suivre les entraînements (MLflow) et versionner les données (DVC)

**Groupe :projet_sign language** …  ·  **Membres :Malak Zahid** …  ·  **Date :17/11/2026** … 18:00

> Remplissez chaque partie dans ce fichier, puis rendez-le avec la pull request du TP5.
> Collez les sorties du terminal entre les lignes ``` (trois accents graves).

---

## 1. Mise en place (dans `TP/TP5`)

Dernière ligne de `python -m pytest` après `pip install -r requirements.txt` et `pip install -e .` :

```
=========== 5 failed, 27 passed, 2 warnings in 9.22s ==========
```

Quels tests échouent, et pourquoi ?

FAILED tests/test_tracking.py::test_training_creates_a_run - AssertionError: aucun run MLflow : log_run n'a rien enregistré
FAILED tests/test_tracking.py::test_run_records_metrics - AssertionError: aucun run MLflow : log_run n'a rien enregistré
FAILED tests/test_tracking.py::test_run_records_data_version - AssertionError: aucun run MLflow : log_run n'a rien enregistré
FAILED tests/test_tracking.py::test_run_stores_the_model - AssertionError: aucun run MLflow : log_run n'a rien enregistré
FAILED tests/test_tracking.py::test_options_change_the_run - AssertionError: aucun run MLflow : log_run n'a rien enregistré
…

Avant `pip install -e .`, où pointait le package `maintai` installé dans l'environnement ? Et après ?

…

## 2. Sprint 1 : MLflow

Votre fonction `log_run` (`maintai/tracking.py`) :

```python
def log_run(params: dict, metrics: dict, model, X_example, data_path: Path) -> str:
    """Enregistre un entraînement et renvoie l'identifiant du run."""

    mlflow.set_experiment(EXPERIMENT)

    with mlflow.start_run() as run:

        mlflow.log_params(params)

        mlflow.log_param("data_md5", file_md5(data_path))

        mlflow.log_metrics(metrics)

        mlflow.sklearn.log_model(
            model,
            name="model",
            input_example=X_example,
            skops_trusted_types=TRUSTED_TYPES
        )

        return run.info.run_id
```

Dernière ligne de `python -m pytest` à la fin du sprint 1 :

```
=================== 32 passed, 4 warnings in 23.04s ============
```

Vos runs (au moins quatre), relevés dans `mlflow ui` (mode « Model training ») :

| Commande | recall | precision | accuracy |
|---|---|---|---|
| Par défaut | 0.750 | 0.622 | 0.904 |
| --C 0.01 | 0.691 | 0.653 | 0.908 |
| --threshold 0.2 | 0.838 | 0.543 | 0.882 |
| --model forest | 0.728 | 0.562 | 0.886 |

Quel run choisiriez-vous pour MaintAI, et pourquoi ? (Rappel : une panne manquée coûte plus cher qu'une fausse alerte.)
Nous retenons la régression logistique avec un seuil de 0.2,
car elle maximise le recall (83.8 %). Une panne manquée
coûtant plus cher qu'une fausse alerte, nous acceptons
une précision plus faible (54.3 %).

La forêt aléatoire n'est pas meilleure dans cette comparaison,
car son recall est inférieur (72.8 %).
…

Dans `mlflow ui`, ouvrez le modèle d'un run. Quelle version de scikit-learn est indiquée dans son `requirements.txt` ? Quel problème du TP4 cela règle-t-il ?

scikit-learn==1.8.0
…

Où MLflow enregistre-t-il les runs sur votre disque ? Ces fichiers vont-ils dans Git ? Pourquoi ?

MLflow enregistre les paramètres, les métriques et les
informations des runs dans la base SQLite `mlflow.db`.
Les modèles et les artefacts sont stockés dans `mlruns/`.

Ces fichiers ne doivent pas être versionnés dans Git,
car ce sont des fichiers générés automatiquement qui
peuvent devenir volumineux.
…

## 3. Sprint 2 : DVC

Contenu de `data/sensors.csv.dvc` après `dvc add data/sensors.csv` :

```
outs:
- md5: 73e0b7cb3c6f795c70c3ddf970b99c15
  size: 126815
  hash: md5
  path: sensors.csv

```

Comparez la valeur `md5` de ce fichier au paramètre `data_md5` de votre dernier run MLflow. Que constatez-vous ?
73e0b7cb3c6f795c70c3ddf970b99c15 
same 
…

Pourquoi `data/sensors.csv` ne va pas dans Git, alors que `data/sensors.csv.dvc` y va ?
Le fichier `sensors.csv` est géré par DVC afin d'éviter
d'alourdir le dépôt Git avec des fichiers de données.

Le fichier `sensors.csv.dvc` contient uniquement les
métadonnées du dataset, notamment son empreinte MD5,
sa taille et son chemin. Git conserve ainsi l'historique
des versions des données sans stocker leur contenu.
…

Après `python -m maintai.dataset --n 8000 --seed 7`, que dit `dvc status` ?

```
data\sensors.csv.dvc:                                                                                                                                                             
        changed outs:
                modified:           data\sensors.csv
```

| Version | Commit Git | md5 (8 premiers caractères) | Nombre de lignes |
|---|---|---|---|
| v1 | 9edf02b | 73e0b7cb | 5000 |
| v2 | bfcca7b | 93fdeef2 | 8000 |

Revenez à la v1 (`git checkout <commit> -- data/sensors.csv.dvc`, puis `dvc checkout`). Combien de lignes contient `data/sensors.csv` ? Puis revenez à la v2.

Après restauration de la v1, le fichier contient 5000 lignes.
Après retour à la v2, il contient 8000 lignes.
DVC permet donc de restaurer les différentes versions des données.
…

Supprimez `data/sensors.csv` et le dossier `.dvc/cache`, puis lancez `dvc pull`. Que se passe-t-il ?

La commande `dvc pull` récupère les données depuis le stockage
DVC, reconstitue le cache local et restaure le fichier
`sensors.csv` contenant les 8000 lignes de la v2.
…

## 4. Relier modèle et données

Entraînez un modèle sur la v2. Dans `mlflow ui`, comparez ce run à celui de la v1 avec les mêmes réglages :

| Run | data_md5 (8 caractères) | n_train | recall | precision |
|---|---|---|---|---|
| v1 | 73e0b7cb | 4000 | 0.750 | 0.622 |
| v2 | 93fdeef2 | 6400 | 0.741 | 0.650 |

Peut-on dire que le modèle v2 est « meilleur » ? Pourquoi faut-il être prudent en comparant deux runs entraînés sur des données différentes ?

Le modèle v2 présente une meilleure accuracy et une meilleure
precision, mais un recall légèrement inférieur.

On ne peut pas affirmer qu'il est meilleur, car les modèles
ont été entraînés et évalués sur des données différentes.
Une comparaison fiable nécessite un même jeu de test indépendant.
…

## 5. Décision : l'ADR 004

Dans `docs/adr/004-choix-du-modele.md` : le modèle et le seuil retenus, à partir de votre tableau MLflow. Indiquez l'identifiant du run et le `data_md5` de la version des données utilisée.

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
   …

## 7. Le rendu Git

- Lien de la pull request : …
- Le tag `tp5` existe sur GitHub : oui / non
- `git status` avant le commit : `mlflow.db`, `mlruns/`, `data/sensors.csv` ou `.dvc/cache` apparaissaient-ils ? oui / non

## 8. Ce qui reste flou

…
