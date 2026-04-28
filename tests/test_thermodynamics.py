import unittest
import sys
import os
import json

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from modules.math_engine import MetronMath

class TestThermodynamicConstants(unittest.TestCase):
    
    def setUp(self):
        db_path = os.path.join(os.path.dirname(__file__), '..', 'vapor_pressure_coeff.json')
        with open(db_path, 'r') as f:
            self.db = json.load(f)

    def test_triple_point_of_water(self):
        """
        At the Triple Point of Water (0.01 °C or 273.16 K), 
        the vapor pressure over liquid water and ice MUST be identical.
        """
        tpw_k = 273.16
        
        e_water = MetronMath.calc_vapor_pressure(tpw_k, self.db["Water"]["coefficients"])
        e_ice = MetronMath.calc_vapor_pressure(tpw_k, self.db["Ice"]["coefficients"])
        
        # Now calculating in hPa, so 6.1165...
        self.assertAlmostEqual(e_water, e_ice, places=4, 
                               msg=f"Triple point mismatch! Water:{e_water}, Ice:{e_ice}")

    def test_standard_boiling_point(self):
        """At 100°C (373.15 K), vapor pressure over water approaches 1 standard atm (1013.25 hPa)."""
        bp_k = 373.15
        e_boil = MetronMath.calc_vapor_pressure(bp_k, self.db["Water"]["coefficients"])
        
        # Sonntag 1990 mathematically yields ~1014.19 hPa at 100 C. 
        # Using a delta of 1.0 to validate the polynomial bounds without failing on empirical realities.
        self.assertAlmostEqual(e_boil, 1013.25, delta=1.0, 
                               msg=f"Boiling point pressure out of bounds. Got: {e_boil}")

if __name__ == '__main__':
    unittest.main()
