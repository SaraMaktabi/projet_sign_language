# Canvas — Sign Letter
## Reconnaissance de lettres en langue des signes et assistant d’apprentissage

**Groupe :projet_sign_language** …  ·  **Membres :maktabi sara / IKSI Badreddine / ZAHID Malak / ** …  ·  **Date :10/11/2026** …

## 1. Contexte et utilisateurs

- **Organisation ou situation :** Contexte éducatif et apprentissage de la langue des signes. Le projet vise à faciliter l’apprentissage de l’alphabet manuel de l’American Sign Language (ASL) grâce à la reconnaissance automatique des gestes réalisés devant une caméra.
- **Utilisateur principal :** Apprenant débutant en langue des signes souhaitant s’entraîner à reconnaître et à reproduire les lettres de l’alphabet ASL.
- **Utilisateurs secondaires :** Enseignants et formateurs en langue des signes.

## 2. Problème et décision

- **Décision que l’utilisateur prend avec le système :** Déterminer si le geste réalisé correspond à la lettre souhaitée, identifier la lettre reconnue et décider s’il doit corriger son geste ou passer à l’exercice suivant.
- **Fréquence :** À chaque exercice ou tentative d’apprentissage, potentiellement plusieurs fois par session.
- **Conséquence d’une erreur, et pour qui :**
  - Une mauvaise reconnaissance peut induire l’apprenant en erreur et lui faire mémoriser une mauvaise correspondance entre un geste et une lettre.
  - Une lettre non reconnue peut décourager l’apprenant et perturber son apprentissage.
  - Les enseignants peuvent perdre confiance dans l’outil si les prédictions sont peu fiables.

## 3. Approche par sous-problème

| Sous-problème | Approche (règles / ML / DL / LLM / RAG) | Pourquoi pas une approche plus simple ? |
|---|---|---|
| Préparation et exploration des images | Data Mining, Pandas et NumPy | Une inspection manuelle ne permet pas d’analyser efficacement les distributions, les déséquilibres et les variations des images. |
| Reconnaissance des 24 lettres statiques | Deep Learning (CNN) | Les règles fixes et les méthodes classiques sont peu adaptées à la diversité des formes, positions et orientations des mains. |
| Évaluation de la généralisation | Évaluation ML : séparation des données, validation et tests par groupes de personnes si les identifiants sont disponibles | Une simple accuracy sur une séparation aléatoire peut surestimer les performances sur de nouvelles personnes. |
| Assistant d’apprentissage | LLM + RAG | Des réponses prédéfinies sont moins flexibles. Le RAG permet de rechercher des informations dans un corpus pédagogique avant de formuler une réponse contextualisée. |
| Communication entre l’interface et les modèles | API | Une API sépare les modèles de l’interface et facilite l’intégration des fonctionnalités. |

## 4. Données

| Jeu de données | Source et licence | Volume | Données personnelles ? |
|---|---|---|---|
| Sign Language MNIST | Kaggle — licence CC0 (Public Domain), selon la fiche du dataset | 27 455 images d’entraînement et 7 172 images de test ; 24 classes | Pas de données directement identifiantes dans le jeu fourni ; images de mains |
| Corpus pédagogique complémentaire | Ressources pédagogiques documentées sur l’alphabet ASL | À constituer selon les besoins du RAG | Non, si les ressources publiques retenues ne contiennent pas de données personnelles |
| Images complémentaires collectées (optionnel) | Captures volontaires auprès de participants | À définir | Potentiellement oui ; consentement et protection nécessaires |

**Caractéristiques de Sign Language MNIST :**
- Images en niveaux de gris de 28 × 28 pixels.
- 24 classes correspondant aux lettres statiques de A à Y, sauf J et Z.
- J et Z sont absentes car elles nécessitent un mouvement.

**Limite importante :** le dataset ne fournit pas de séparation fiable par identité des signataires. Il ne suffit donc pas, à lui seul, pour affirmer que le modèle généralise à de nouvelles personnes. Une évaluation complémentaire sur des volontaires non présents dans l’entraînement serait nécessaire pour mesurer cet aspect.

Source : [Sign Language MNIST — Kaggle](https://www.kaggle.com/datasets/datamunge/sign-language-mnist).

## 5. Métriques, baseline et critères d’acceptation

- **Baseline et son résultat :**
  - Baseline 1 : classificateur naïf prédisant systématiquement la classe majoritaire (`DummyClassifier`). Son résultat sera calculé sur le jeu de test.
  - Baseline 2 : CNN simple servant de référence pour comparer d’éventuelles architectures améliorées.
  - Une prédiction aléatoire uniforme aurait une accuracy théorique de 4,17 % (1/24).

- **Métrique principale :** Accuracy, pour mesurer la proportion globale de lettres correctement reconnues parmi les 24 classes.
- **Métriques secondaires :**
  - Precision, Recall et F1-score macro.
  - Matrice de confusion pour repérer les lettres fréquemment confondues.
  - Temps moyen de prédiction pour évaluer la fluidité de l’application.

**Critères d’acceptation proposés :**
1. Atteindre une accuracy d’au moins 90 % sur le jeu de test officiel de Sign Language MNIST.
2. Obtenir un F1-score macro d’au moins 90 % sur ce même jeu de test.
3. Comparer le CNN à la baseline et documenter les erreurs à l’aide d’une matrice de confusion.
4. Évaluer séparément la généralisation à des personnes non présentes dans les données d’entraînement, si un jeu complémentaire avec identifiants de participants est constitué.
5. L’assistant pédagogique doit fournir des réponses pertinentes fondées sur le corpus documentaire retenu.

Ces seuils sont des objectifs à atteindre et non des performances déjà obtenues.

## 6. Architecture prévue (après la séance 5)

L’architecture comporte deux modules complémentaires : un système de reconnaissance visuelle et un assistant pédagogique. Une API permet leur intégration dans une interface utilisateur.

### A. Module de reconnaissance des lettres

1. **Entrée :** image de la main provenant d’une caméra ou importée par l’utilisateur.
2. **Prétraitement :** redimensionnement en 28 × 28 pixels et normalisation.
3. **Classification :** modèle CNN entraîné sur les 24 classes de Sign Language MNIST.
4. **Sortie :** lettre prédite et score de confiance.

### B. Module assistant d’apprentissage

1. **Entrée :** question de l’apprenant.
2. **Recherche documentaire :** récupération des passages pertinents dans le corpus pédagogique à l’aide du RAG.
3. **Génération :** LLM qui formule une réponse à partir du contexte récupéré.
4. **Sortie :** explication ou information pédagogique accompagnée, si possible, de ses sources.

### C. Intégration

- **Backend/API :** reçoit les requêtes de l’interface et appelle le module de reconnaissance ou l’assistant pédagogique.
- **Interface utilisateur :** permet de soumettre une image ou d’utiliser la caméra, de consulter la lettre prédite, de réaliser des exercices et de poser des questions à l’assistant.

## 7. Choix technologiques (après la séance 5)

| Besoin | Outil | Justification |
|---|---|---|
| Manipulation des données | Python, Pandas, NumPy | Exploration et préparation des données |
| Traitement d’images | OpenCV | Capture et prétraitement des images |
| Développement du CNN | TensorFlow / Keras | Construction, entraînement et évaluation du réseau de neurones |
| Évaluation | Scikit-learn | Baseline, métriques et matrices de confusion |
| Backend | FastAPI | Exposer les fonctionnalités via une API |
| Assistant IA | LLM | Compréhension des questions et génération de réponses |
| Recherche documentaire | ChromaDB + Sentence Transformers | Indexation vectorielle et recherche sémantique pour le RAG |
| Interface utilisateur | Streamlit | Développement rapide d’une interface interactive |
| Gestion du code | Git et GitHub | Collaboration et suivi du développement en équipe |

## 8. Risques, éthique et confidentialité

1. **Biais des données :** le dataset peut ne pas représenter suffisamment la diversité des morphologies des mains, des carnations et des conditions de prise de vue. Le modèle risque donc d’être moins performant sur certains utilisateurs.
2. **Généralisation :** les performances sur les images du dataset ne garantissent pas les mêmes résultats avec de nouvelles personnes, de nouveaux éclairages ou différents arrière-plans.
3. **Confidentialité :** les images capturées par la caméra peuvent contenir des informations permettant d’identifier les personnes. Leur collecte et leur stockage nécessitent le consentement des participants.
4. **Sécurité des données :** les images et les informations collectées doivent être protégées contre les accès non autorisés.
5. **Fiabilité des prédictions :** une mauvaise classification peut induire l’apprenant en erreur. Le système doit afficher un score de confiance et permettre de recommencer l’exercice.
6. **Limites du LLM :** l’assistant peut générer des informations incorrectes. Le RAG doit privilégier des sources pédagogiques fiables et permettre de retrouver les documents utilisés.
7. **Accessibilité et inclusion :** le système repose uniquement sur l’ASL et ne représente pas toutes les langues des signes ni leurs particularités culturelles et linguistiques.
8. **Responsabilité et usage :** le projet est un outil d’apprentissage complémentaire. Il ne doit pas être présenté comme un traducteur professionnel ni comme un substitut à un enseignant en langue des signes.

## 9. Limites et hors périmètre

- Reconnaissance limitée aux 24 lettres statiques de l’alphabet ASL.
- Les lettres J et Z sont exclues, car elles nécessitent des mouvements.
- Le système ne reconnaît pas des mots, des phrases ou des conversations complètes.
- La reconnaissance des expressions faciales, des mouvements du corps et des composantes grammaticales de la langue des signes n’est pas prise en charge.
- Le projet ne couvre pas les autres langues des signes (LSM, LSF, etc.).
- L’assistant pédagogique ne remplace pas un enseignant et ses réponses restent limitées au corpus documentaire disponible.
- La traduction en temps réel de conversations entre personnes sourdes et entendantes est hors périmètre.
- Le déploiement sur une application mobile ou une infrastructure industrielle n’est pas prévu dans cette version.

---

**Équipe :** 3 étudiants.
