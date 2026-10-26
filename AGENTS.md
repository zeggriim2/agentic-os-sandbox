# Consignes pour les agents

- Python 3.11+ et bibliothèque standard uniquement : n'ajoute aucune dépendance.
- Montants toujours en centimes (`int`), jamais en `float`.
- Chaque comportement nouveau a un test dans `tests/` (unittest).
- Commande de test : `python3 -m unittest discover -s tests -v` (doit passer avant de terminer).
- Ne supprime ni n'affaiblis aucun test existant.
