from __future__ import annotations

import csv
import io
from collections.abc import Mapping
from dataclasses import dataclass

CATEGORIES = frozenset({"transport", "repas", "hebergement", "autre"})


@dataclass(frozen=True)
class Frais:
    """Une dépense : libellé, montant en centimes (> 0) et catégorie connue."""

    libelle: str
    montant_centimes: int
    categorie: str = "autre"

    def __post_init__(self) -> None:
        if not self.libelle.strip():
            raise ValueError("libellé vide")
        if not isinstance(self.montant_centimes, int) or isinstance(self.montant_centimes, bool):
            raise TypeError("le montant doit être un entier en centimes")
        if self.montant_centimes <= 0:
            raise ValueError("le montant doit être strictement positif")
        if self.categorie not in CATEGORIES:
            raise ValueError(f"catégorie inconnue : {self.categorie}")


def total(frais: list[Frais]) -> int:
    """Somme des montants, en centimes."""
    return sum(f.montant_centimes for f in frais)


def total_par_categorie(frais: list[Frais]) -> dict[str, int]:
    """Total par catégorie (seules les catégories présentes apparaissent)."""
    out: dict[str, int] = {}
    for f in frais:
        out[f.categorie] = out.get(f.categorie, 0) + f.montant_centimes
    return out


def exporter_csv(frais: list[Mapping[str, object]]) -> str:
    """Exporte une liste de frais en CSV séparé par des points-virgules.

    Le contrat d'entrée est strict : ``frais`` doit être une ``list`` et
    chaque élément doit être un mapping contenant ``libelle``, ``categorie``
    et ``montant_centimes``. Les deux premiers champs sont des chaînes non
    vides ; la catégorie doit être l'une des catégories connues. Le montant
    est un entier de centimes non négatif (les booléens sont refusés).

    Une collection ou un élément d'un type incompatible provoque ``TypeError``.
    Une valeur invalide ou un frais incomplet provoque ``ValueError``. Le
    résultat conserve l'ordre d'entrée et ne comporte pas de saut de ligne
    final.
    """
    if not isinstance(frais, list):
        raise TypeError("frais doit être une liste")

    output = io.StringIO(newline="")
    writer = csv.writer(output, delimiter=";", lineterminator="\n")
    writer.writerow(("libelle", "categorie", "montant_euros"))

    for item in frais:
        if not isinstance(item, Mapping):
            raise TypeError("chaque frais doit être un mapping")
        try:
            libelle = item["libelle"]
            categorie = item["categorie"]
            montant_centimes = item["montant_centimes"]
        except KeyError:
            raise ValueError("un frais doit fournir libelle, categorie et montant_centimes") from None

        if not isinstance(libelle, str) or not isinstance(categorie, str):
            raise TypeError("libelle et categorie doivent être des chaînes")
        if not libelle.strip():
            raise ValueError("libelle vide")
        if categorie not in CATEGORIES:
            raise ValueError(f"catégorie inconnue : {categorie}")
        if not isinstance(montant_centimes, int) or isinstance(montant_centimes, bool):
            raise TypeError("le montant doit être un entier en centimes")
        if montant_centimes < 0:
            raise ValueError("le montant doit être non négatif")

        euros, centimes = divmod(montant_centimes, 100)
        writer.writerow((libelle, categorie, f"{euros},{centimes:02d}"))

    return output.getvalue().removesuffix("\n")


# Nom historique conservé pour les consommateurs de la première version.
export_csv = exporter_csv
