import unittest

from frais import Frais, total, total_par_categorie


class FraisTest(unittest.TestCase):
    def test_total(self):
        self.assertEqual(total([Frais("Train", 4550, "transport"), Frais("Déjeuner", 1820, "repas")]), 6370)

    def test_total_vide(self):
        self.assertEqual(total([]), 0)

    def test_total_par_categorie(self):
        notes = [Frais("Train", 4550, "transport"), Frais("Taxi", 2000, "transport"), Frais("Déjeuner", 1820, "repas")]
        self.assertEqual(total_par_categorie(notes), {"transport": 6550, "repas": 1820})

    def test_montant_invalide(self):
        with self.assertRaises(ValueError):
            Frais("Gratuit", 0)
        with self.assertRaises(TypeError):
            Frais("Float", 12.5)

    def test_categorie_inconnue(self):
        with self.assertRaises(ValueError):
            Frais("Cinéma", 1000, "loisirs")

    def test_libelle_vide(self):
        with self.assertRaises(ValueError):
            Frais("  ", 1000)


if __name__ == "__main__":
    unittest.main()
