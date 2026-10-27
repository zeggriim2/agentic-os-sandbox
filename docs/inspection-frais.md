# Inspection du module `frais`

Inspection réalisée sur la branche `develop` (base du worktree).

## Chemin du module

Le module est le package Python `frais/`, avec son implémentation dans `frais/notes.py`.

Le point d'entrée public du package est `frais/__init__.py`.

## Représentation concrète d'un frais

Un frais n'est pas un mapping : il est représenté par une instance immuable (`@dataclass(frozen=True)`) de la classe `Frais` définie dans `frais/notes.py`.

Ses champs sont :

- `libelle: str` ;
- `montant_centimes: int` ; le montant est exprimé en centimes et doit être strictement positif ;
- `categorie: str`, avec la valeur par défaut `"autre"`.

Exemple présent dans `tests/test_notes.py` :

```python
Frais("Train", 4550, "transport")
```

Les catégories autorisées sont `transport`, `repas`, `hebergement` et `autre`.

Écart avec l'hypothèse du ticket : la structure concrète n'est pas une liste de mappings ayant les clés `libelle`, `categorie` et `montant`. Les fonctions attendent une liste de `Frais` ; le champ de montant s'appelle `montant_centimes` et non `montant`.

## Imports et exposition publique

Les consommateurs importent les symboles depuis le package :

```python
from frais import Frais, total, total_par_categorie
```

`frais/__init__.py` ré-exporte `Frais`, `total` et `total_par_categorie`, et les déclare dans `__all__`. L'implémentation interne se trouve dans `frais.notes`.

Les fonctions publiques observées sont :

- `total(frais: list[Frais]) -> int` ;
- `total_par_categorie(frais: list[Frais]) -> dict[str, int]` ;
- `exporter_csv(frais: list[Mapping[str, object]]) -> str` (avec l'alias historique `export_csv`).

## Contrat d'entrée de `exporter_csv`

`frais` doit être strictement une liste. Chaque élément doit être un mapping
qui fournit les clés `libelle`, `categorie` et `montant_centimes`. `libelle` et
`categorie` doivent être des chaînes ; le libellé ne peut pas être vide et la
catégorie doit appartenir aux catégories autorisées. `montant_centimes` doit
être un entier de centimes non négatif ; les booléens sont refusés.

Un type incompatible (collection qui n'est pas une liste, élément qui n'est
pas un mapping, ou champ dont le type est incorrect) provoque `TypeError`.
Un frais incomplet ou une valeur invalide (texte vide, catégorie inconnue,
montant négatif) provoque `ValueError`.

## Exceptions

La validation est effectuée dans `Frais.__post_init__` :

- `ValueError` pour un libellé vide, un montant inférieur ou égal à zéro, ou une catégorie inconnue ;
- `TypeError` si le montant n'est pas un entier (les booléens sont également refusés).

Les tests vérifiant ces conventions sont dans `tests/test_notes.py` : `test_montant_invalide`, `test_categorie_inconnue` et `test_libelle_vide`.

## Emplacement et conventions des tests

Les tests unitaires sont dans `tests/test_notes.py`, sous forme de `unittest.TestCase`. La commande documentée et utilisée par le dépôt est :

```bash
python3 -m unittest discover -s tests -v
```

Le contrat ci-dessus est également détaillé dans la docstring de
`frais.notes.exporter_csv` et couvert par `tests/test_export.py`.
