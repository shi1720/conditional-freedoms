import unittest
from itertools import product
from src.model import *

class TestScope(unittest.TestCase):
    def test_status_is_not_recruitment_exemption(self):
        for bits in product((False, True), repeat=8):
            self.assertEqual(recruitment_trigger(Recruitment(*bits, status='free')),
                             recruitment_trigger(Recruitment(*bits, status='bond')))

    def test_craft_exempts_recruitment_but_not_early_departure(self):
        p = Recruitment(True, True, False, True, False, False, False, True)
        self.assertFalse(recruitment_trigger(p))
        self.assertTrue(early_departure_trigger(True, False, False))

    def test_cause_and_licence_are_independent_routes(self):
        self.assertFalse(early_departure_trigger(True, False, True))
        self.assertFalse(early_departure_trigger(True, True, False))
        self.assertTrue(early_departure_trigger(True, False, False))
        self.assertFalse(early_departure_trigger(False, False, False))

    def test_unknown_is_not_permission(self):
        self.assertIsNone(seasonal_restriction(True, True, None))
        self.assertIsNone(early_departure_trigger(True, False, None))
        self.assertFalse(seasonal_restriction(False, True, None))

    def test_surety_preserves_service(self):
        for obligation in (False, True, None):
            s = release_on_service_surety(CustodyState(True, obligation, 'refusal'))
            self.assertFalse(s.in_custody)
            self.assertTrue(s.service_obligation)
            self.assertFalse(s.acquitted)

    def test_acquittal_does_not_invent_service(self):
        s = acquit_presented_charge(CustodyState(True, None, 'excess'))
        self.assertFalse(s.in_custody)
        self.assertTrue(s.acquitted)
        self.assertIsNone(s.service_obligation)

    def test_seasonal_exception_does_not_settle_existing_term(self):
        self.assertFalse(seasonal_restriction(True, True, True))
        self.assertTrue(combined_departure_restriction(True, False, False, True, True, True))

    def test_commission_is_conjunctive_not_blanket_release_ban(self):
        self.assertTrue(commission_concern(True, True, True))
        for bits in product((False, True), repeat=3):
            self.assertEqual(commission_concern(*bits), all(bits))
        self.assertIsNone(commission_concern(True, None, True))

    def test_three_valued_connectives(self):
        self.assertFalse(conjunction(False, None))
        self.assertTrue(disjunction(True, None))
        self.assertIsNone(conjunction(True, None))
        self.assertIsNone(disjunction(False, None))

if __name__ == '__main__':
    unittest.main()
