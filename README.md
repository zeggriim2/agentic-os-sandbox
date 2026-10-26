# agentic-os-sandbox

Dépôt bac à sable pour la recette d'[Agentic OS](https://github.com/zeggriim2/agentic-os) :
les agents (PO, Tech Lead, Développeur, Reviewer, QA) y développent de petites features,
jusqu'à une PR draft que seul un humain merge.

Projet volontairement minimal : Python 3 **bibliothèque standard uniquement** (le bac à sable des
agents n'a pas de réseau, aucune dépendance ne peut être téléchargée).

## Tests

```bash
python3 -m unittest discover -s tests -v
```

## Module `frais`

Calculs sur des notes de frais : montants en centimes (entiers), catégories, total.
