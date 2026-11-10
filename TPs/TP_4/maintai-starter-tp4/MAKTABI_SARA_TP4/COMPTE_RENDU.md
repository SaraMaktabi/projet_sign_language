# Compte rendu · TP4 : MaintAI devient un package Python

**Groupe :projet_sign_language** …  ·  **Membres :maktabi sara** …  ·  **Date :10/11/2026 18:18** …

> Remplissez chaque partie dans ce fichier, puis rendez-le avec la pull request du TP4.
> Collez les sorties du terminal entre les lignes ``` (trois accents graves).

---

## 1. Mise en place (dans TP/TP4, avec son propre .venv)

Dernière ligne de python -m pytest juste après pip install -r requirements.txt :

======================= 2 failed, 25 passed, 1 warning in 69.75s (0:01:09) =======================

Quels sont les deux tests qui échouent, et pourquoi ?

tests/test_package.py::test_installed_version_matches_the_code
tests/test_package.py::test_command_is_declared

## 2. Sprint 1 : pyproject.toml et pip install -e .

Vos sections dependencies et [project.scripts] :
<!-- 
[build-system]
requires = ["setuptools>=69"]
build-backend = "setuptools.build_meta"

[project]
name = "maintai"
dynamic = ["version"]
description = "Prédiction de panne à partir de relevés de capteurs"
readme = "README.md"
requires-python = ">=3.11"
dependencies = [
    "numpy>=2.4",
    "pandas>=3.0",
    "scikit-learn>=1.8",
    "joblib>=1.5",
]

[project.optional-dependencies]
api = ["fastapi>=0.115", "uvicorn[standard]>=0.30"]
ui = ["streamlit>=1.40"]
dev = ["pytest>=8", "ruff"]

[project.scripts]
maintai-predict = "maintai.cli:main"

[tool.setuptools.dynamic]
version = {attr = "maintai._version_"}

[tool.setuptools.packages.find]
include = ["maintai*"] -->

Pourquoi pytest et fastapi ne sont-ils pas dans dependencies ?

pytest sert uniquement à exécuter les tests : c’est une dépendance de développement (dev).
fastapi sert uniquement à lancer l’API : c’est une fonctionnalité optionnelle (api).

Sortie de pip show maintai (les quatre premières lignes) :
Name: maintai
Version: 0.2.0
Summary: Prédiction de panne à partir de relevés de capteurs
Home-page: 

Dernière ligne de python -m pytest à la fin du sprint 1 :

================================= 27 passed, 1 warning in 10.44s =================================

Placez-vous dans un autre dossier (cd %TEMP%) et lancez maintai-predict 72 6 85 15000, puis python -c "import maintai; print(maintai.__file__)". Qu'affichent ces deux commandes ? Où Python trouve-t-il le code de maintai ?

Probabilité de panne : 95 % (ALERTE)
C:\Users\Malak\OneDrive\Documents\S2_EMSI\DM\projet_sign_language\TPs\TP_4\maintai-starter-tp4\maintai\_init_.py

Python trouve le code dans le dossier source grâce à l’installation editable

Modifiez le message affiché par maintai/cli.py, puis relancez maintai-predict sans réinstaller. Le changement est-il visible ? Pourquoi ?

Le changement est visible sans réinstaller, car le mode editable pointe directement vers les fichiers sources.

## 3. Sprint 2 : construire et installer le wheel

Sortie de dir dist après python -m build :


Mode                 LastWriteTime         Length Name                                      
----                 -------------         ------ ----                                      
-a----        10/11/2026     18:02          11730 maintai-0.2.0-py3-none-any.whl            
-a----        10/11/2026     18:02          12238 maintai-0.2.0.tar.gz   

Contenu du wheel (tar -tf dist\maintai-0.2.0-py3-none-any.whl). Le modèle, les tests et ui/ y sont-ils ? Pourquoi ?

maintai/_init_.py
maintai/cli.py
maintai/client.py
maintai/config.py
maintai/data.py
maintai/dataset.py
maintai/predict.py
maintai/train.py
maintai/api/_init_.py
maintai/api/main.py
maintai/api/schemas.py
maintai/api/security.py
maintai-0.2.0.dist-info/METADATA
maintai-0.2.0.dist-info/WHEEL
maintai-0.2.0.dist-info/entry_points.txt
maintai-0.2.0.dist-info/top_level.txt
maintai-0.2.0.dist-info/RECORD

Le wheel contient uniquement les packages Python commençant par maintai.


Dans un environnement neuf (%TEMP%\essai), installez le wheel et lancez maintai-predict :

| Étape | Ce qui s’affiche |
|---|---|
| sans MAINTAI_MODELS_DIR | Modèle introuvable|
| avec MAINTAI_MODELS_DIR vers vos models | probabilité de panne = 95 % (ALERTE) |
| après pip install scikit-learn==1.8.0 | Même résultat, avec disparition de l’avertissement InconsistentVersionWarning |

D'où vient l'avertissement InconsistentVersionWarning ? Quelle ligne de models/model_info.json permet de le comprendre ?

L’avertissement InconsistentVersionWarning apparaît lorsque le modèle a été entraîné avec une version différente de celle utilisée pour le charger.

## 4. Questions de compréhension

1. Quelle différence entre requirements.txt et la liste dependencies de pyproject.toml ?
  requirements.txt contient les dépendances complètes et souvent figées pour reproduire l’environnement du projet. dependencies contient uniquement les dépendances nécessaires à l’utilisation du package installé.
2. Quelle différence entre pip install -e . et pip install dist\maintai-0.2.0-py3-none-any.whl ?
  pip install -e . installe le projet en mode éditable : les modifications du code source sont immédiatement visibles. Le wheel est une distribution construite et installée comme une copie figée du package.
3. Qu'est-ce qu'un « point d'entrée » ([project.scripts]) ? Où pip crée-t-il le fichier maintai-predict.exe ?
  [project.scripts] crée une commande terminal. ,  pip crée maintai-predict.exe

## 5. Le rendu Git

- Lien de la pull request : …
- Le tag tp4 existe sur GitHub : oui / non
- git status avant le commit : dist/, build/ ou maintai.egg-info/ apparaissaient-ils ? oui / non

## 6. Ce qui reste flou

…