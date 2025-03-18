import unittest
from maksukortti import Maksukortti

class TestMaksukortti(unittest.TestCase):
    def setUp(self):
        self.maksukortti = Maksukortti(1000)

    #Kortti alussa
    def test_luotu_kortti_on_olemassa(self):
        self.assertNotEqual(self.maksukortti, None)

    def test_saldo_alussa_oikein(self):
        self.assertEqual(str(self.maksukortti), "Kortilla on rahaa 10.00 euroa")

    #Kortin lataaminen
    def test_lataaminen_kasvattaa_saldoa_oikein(self):
        self.maksukortti.lataa_rahaa(700)

        self.assertEqual(self.maksukortti.saldo_euroina(), 17.0)

    #Saldon vähennys
    def test_saldo_vahenee_jos_rahaa_tarpeeksi(self):
        self.maksukortti.ota_rahaa(600)

        self.assertEqual(self.maksukortti.saldo_euroina(), 4.0)

    def test_saldo_ei_muutu_jos_rahaa_ei_tarpeeksi(self):
        self.maksukortti.ota_rahaa(1200)

        self.assertEqual(self.maksukortti.saldo_euroina(), 10.0)

    #Bool tarkastus
    def test_rahat_riittivat_palauttaa_true(self):
        self.assertEqual(self.maksukortti.ota_rahaa(900), True)

    def test_rahat_ei_riita_palauttaa_false(self):

        self.assertEqual(self.maksukortti.ota_rahaa(1200), False)