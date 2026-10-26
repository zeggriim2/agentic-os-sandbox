import csv
import io
import unittest

from frais import exporter_csv


class ExporterCsvTest(unittest.TestCase):
    def test_exporte_les_frais_dans_l_ordre_attendu(self):
        frais = [
            {"libelle": "Train", "categorie": "transport", "montant_centimes": 4550},
            {"libelle": "Déjeuner", "categorie": "repas", "montant_centimes": 1820},
        ]

        self.assertEqual(
            exporter_csv(frais),
            "libelle;categorie;montant_euros\n"
            "Train;transport;45,50\n"
            "Déjeuner;repas;18,20",
        )

    def test_exporte_les_textes_avec_caracteres_csv_speciaux(self):
        libelle = 'Déjeuner; équipe "A"\nà emporter'

        result = exporter_csv(
            [{"libelle": libelle, "categorie": "repas", "montant_centimes": 1250}]
        )
        rows = list(csv.reader(io.StringIO(result), delimiter=";"))

        self.assertEqual(rows[1], [libelle, "repas", "12,50"])

    def test_collection_doit_etre_une_liste(self):
        with self.assertRaises(TypeError):
            exporter_csv(({"libelle": "Train", "categorie": "transport", "montant_centimes": 100},))

    def test_element_doit_etre_un_mapping(self):
        with self.assertRaises(TypeError):
            exporter_csv([("Train", "transport", 100)])

    def test_frais_incomplet_est_refuse_par_value_error(self):
        with self.assertRaises(ValueError):
            exporter_csv([{"libelle": "Train", "categorie": "transport"}])

    def test_types_des_champs_texte_sont_valides(self):
        with self.assertRaises(TypeError):
            exporter_csv([{"libelle": 123, "categorie": "transport", "montant_centimes": 100}])
        with self.assertRaises(TypeError):
            exporter_csv([{"libelle": "Train", "categorie": None, "montant_centimes": 100}])

    def test_valeurs_des_champs_texte_sont_valides(self):
        with self.assertRaises(ValueError):
            exporter_csv([{"libelle": "  ", "categorie": "transport", "montant_centimes": 100}])
        with self.assertRaises(ValueError):
            exporter_csv([{"libelle": "Train", "categorie": "loisirs", "montant_centimes": 100}])

    def test_montant_doit_etre_un_entier_non_booleen(self):
        for montant in (12.5, True):
            with self.subTest(montant=montant), self.assertRaises(TypeError):
                exporter_csv(
                    [{"libelle": "Train", "categorie": "transport", "montant_centimes": montant}]
                )

    def test_montant_negatif_est_refuse_par_value_error(self):
        with self.assertRaises(ValueError):
            exporter_csv([{"libelle": "Train", "categorie": "transport", "montant_centimes": -1}])


if __name__ == "__main__":
    unittest.main()
