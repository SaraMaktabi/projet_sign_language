# Compte rendu · TP5 : suivre les entraînements (MLflow) et versionner les données (DVC)

**Groupe :projet_sign language** …  ·  **Membres :Maktabi_sara** …  ·  **Date :17/11/2016** …

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
(collez ici)
```

| Version | Commit Git (`git log --oneline`) | md5 (8 premiers caractères) | Nombre de lignes |
|---|---|---|---|
| v1 | | | |
| v2 | | | |

Revenez à la v1 (`git checkout <commit> -- data/sensors.csv.dvc`, puis `dvc checkout`). Combien de lignes contient `data/sensors.csv` ? Puis revenez à la v2.

…

Supprimez `data/sensors.csv` et le dossier `.dvc/cache`, puis lancez `dvc pull`. Que se passe-t-il ?

…

## 4. Relier modèle et données

Entraînez un modèle sur la v2. Dans `mlflow ui`, comparez ce run à celui de la v1 avec les mêmes réglages :

| Run | data_md5 (8 caractères) | n_train | recall | precision |
|---|---|---|---|---|
| v1 | | | | |
| v2 | | | | |

Peut-on dire que le modèle v2 est « meilleur » ? Pourquoi faut-il être prudent en comparant deux runs entraînés sur des données différentes ?

…

## 5. Décision : l'ADR 004

Dans `docs/adr/004-choix-du-modele.md` : le modèle et le seuil retenus, à partir de votre tableau MLflow. Indiquez l'identifiant du run et le `data_md5` de la version des données utilisée.

## 6. Questions de compréhension

1. Quelle différence entre Git, DVC et MLflow ? Que versionne chacun ?
   …
2. Pourquoi le stockage DVC est-il ajouté avec `--local` dans ce TP ? Que faudrait-il pour que tout le groupe partage les mêmes données ?
   …
3. Livrer un modèle, c'est trois choses (TP4). Lesquelles, et où sont-elles maintenant ?
   …

## 7. Le rendu Git

- Lien de la pull request : …
- Le tag `tp5` existe sur GitHub : oui / non
- `git status` avant le commit : `mlflow.db`, `mlruns/`, `data/sensors.csv` ou `.dvc/cache` apparaissaient-ils ? oui / non

## 8. Ce qui reste flou

…
