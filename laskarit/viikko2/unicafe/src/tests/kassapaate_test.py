import unittest
from kassapaate import Kassapaate
from maksukortti import Maksukortti

class TestKassapaate(unittest.TestCase):
    def setUp(self):
        self.kassa = Kassapaate()
        self.kortti = Maksukortti(1000)

    # Constructor
    def test_constructor_sets_correct_amount_of_money(self):
        self.assertEqual(self.kassa.kassassa_rahaa, 100000)

    def test_constructor_sets_correct_amount_of_money_euros(self):
        self.assertEqual(self.kassa.kassassa_rahaa_euroina(), 1000)

    def test_set_correct_amount_of_edulliset_lunch_sold(self):
        self.assertEqual(self.kassa.edulliset, 0)

    def test_set_correct_amount_of_maukkaat_lunch_sold(self):
        self.assertEqual(self.kassa.maukkaat, 0)

    # Edulliset cash
    def test_buy_edullinen_with_cash_successful_amount_over(self):
        self.assertEqual(self.kassa.syo_edullisesti_kateisella(500), 260)

    def test_buy_edullinen_with_cash_successful_amount_exact(self):
        self.assertEqual(self.kassa.syo_edullisesti_kateisella(240), 0)

    def test_buy_edullinen_with_cash_successful_register_balance_up(self):
        self.kassa.syo_edullisesti_kateisella(300)
        self.assertEqual(self.kassa.kassassa_rahaa_euroina(), 1002.4)

    def test_buy_edullinen_with_cash_successful_sold_count_up(self):
        self.kassa.syo_edullisesti_kateisella(240)
        self.assertEqual(self.kassa.edulliset, 1)

    def test_buy_edullinen_with_cash_fail_return_cash(self):
        self.assertEqual(self.kassa.syo_edullisesti_kateisella(200), 200)

    def test_buy_edullinen_with_cash_fail_register_balance_same(self):
        self.kassa.syo_edullisesti_kateisella(200)
        self.assertEqual(self.kassa.kassassa_rahaa_euroina(), 1000)

    def test_buy_edullinen_with_cash_fail_sold_count_same(self):
        self.kassa.syo_edullisesti_kateisella(200)
        self.assertEqual(self.kassa.edulliset, 0)

    # Maukkaat cash
    def test_buy_maukas_with_cash_successful_amount_over(self):
        self.assertEqual(self.kassa.syo_maukkaasti_kateisella(500), 100)

    def test_buy_maukas_with_cash_successful_amount_exact(self):
        self.assertEqual(self.kassa.syo_maukkaasti_kateisella(400), 0)

    def test_buy_maukas_with_cash_successful_register_balance_up(self):
        self.kassa.syo_maukkaasti_kateisella(500)
        self.assertEqual(self.kassa.kassassa_rahaa_euroina(), 1004)

    def test_buy_maukas_with_cash_successful_sold_count_up(self):
        self.kassa.syo_maukkaasti_kateisella(400)
        self.assertEqual(self.kassa.maukkaat, 1)

    def test_buy_maukas_with_cash_fail_return_cash(self):
        self.assertEqual(self.kassa.syo_maukkaasti_kateisella(300), 300)

    def test_buy_maukas_with_cash_fail_register_balance_same(self):
        self.kassa.syo_maukkaasti_kateisella(300)
        self.assertEqual(self.kassa.kassassa_rahaa_euroina(), 1000)

    def test_buy_maukas_with_cash_fail_sold_count_same(self):
        self.kassa.syo_maukkaasti_kateisella(300)
        self.assertEqual(self.kassa.maukkaat, 0)

    # Edulliset card
    def test_buy_edullinen_with_card_successful_return_true(self):
        self.assertEqual(self.kassa.syo_edullisesti_kortilla(self.kortti), True)

    def test_buy_edullinen_with_card_successful_card_balance(self):
        self.kassa.syo_edullisesti_kortilla(self.kortti)
        self.assertEqual(self.kortti.saldo, 760)

    def test_buy_edullinen_with_card_successful_sold_count_up(self):
        self.kassa.syo_edullisesti_kortilla(self.kortti)
        self.assertEqual(self.kassa.edulliset, 1)
    
    def test_buy_edullinen_with_card_fail_return_false(self):
        self.kortti = Maksukortti(200)
        self.assertEqual(self.kassa.syo_edullisesti_kortilla(self.kortti), False)

    def test_buy_edullinen_with_card_fail_sold_count_same(self):
        self.kortti = Maksukortti(200)
        self.kassa.syo_edullisesti_kortilla(self.kortti)
        self.assertEqual(self.kassa.edulliset, 0)

    # Maukkaat card
    def test_buy_maukas_with_card_successful_return_true(self):
        self.assertEqual(self.kassa.syo_maukkaasti_kortilla(self.kortti), True)

    def test_buy_maukas_with_card_successful_card_balance(self):
        self.kassa.syo_maukkaasti_kortilla(self.kortti)
        self.assertEqual(self.kortti.saldo, 600)

    def test_buy_maukas_with_card_successful_sold_count_up(self):
        self.kassa.syo_maukkaasti_kortilla(self.kortti)
        self.assertEqual(self.kassa.maukkaat, 1)
    
    def test_buy_maukas_with_card_fail_return_false(self):
        self.kortti = Maksukortti(300)
        self.assertEqual(self.kassa.syo_maukkaasti_kortilla(self.kortti), False)

    def test_buy_maukas_with_card_fail_sold_count_same(self):
        self.kortti = Maksukortti(300)
        self.kassa.syo_maukkaasti_kortilla(self.kortti)
        self.assertEqual(self.kassa.maukkaat, 0)
    
    # Load card
    def test_load_money_to_card_successful_card_balance_up(self):
        self.kassa.lataa_rahaa_kortille(self.kortti, 500)
        self.assertEqual(self.kortti.saldo, 1500)

    def test_load_money_to_card_successful_register_balance_up(self):
        self.kassa.lataa_rahaa_kortille(self.kortti, 500)
        self.assertEqual(self.kassa.kassassa_rahaa_euroina(), 1005)

    def test_load_money_to_card_fail_return_None(self):
        self.assertEqual(self.kassa.lataa_rahaa_kortille(self.kortti, -500), None)

    def test_load_money_to_card_fail_register_balance_same(self):
        self.kassa.lataa_rahaa_kortille(self.kortti, -500)
        self.assertEqual(self.kassa.kassassa_rahaa_euroina(), 1000)
