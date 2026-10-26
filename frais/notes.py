from __future__ import annotations

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
