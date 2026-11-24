# ADR 005 : image Docker sans données ni secrets


## Décision

Nous construisons une image reproductible contenant le code MaintAI et ses dépendances figées, mais pas les données, le modèle entraîné, les artefacts MLflow ni la clé API. Ces éléments sont fournis au lancement par volumes Docker et variables d’environnement afin de pouvoir les remplacer sans reconstruire l’image et de ne pas exposer de secret.

## Conséquences

Le modèle doit être entraîné avant le démarrage et le dossier `models/` doit être monté ; en échange, la même image sert à l’API et à l’interface, avec un cache de build efficace.
