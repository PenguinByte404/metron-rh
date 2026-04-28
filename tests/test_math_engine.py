import unittest
import math
import sys
import os

# Adjust path to allow importing modules
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from modules.math_engine import MetronMath

class TestMetronMathEngine(unittest.TestCase):
    
    def setUp(self):
        # Sonntag 1990 Coefficients for Water
        self.water_coeffs = {
            "a1": -6096.9385,
            "a2": 21.2409642,
            "a3": -2.711193e-2,
            "a4": 1.673952e-5,
            "a5": 2.433502
        }
        
    def test_vapor_pressure_forward_calculation(self):
        """Test if the engine calculates accurate hPa from known Temperatures."""
        t_k = 293.15  # Exactly 20.00 deg C
        
        e_s = MetronMath.calc_vapor_pressure(t_k, self.water_coeffs)
        
        # Sonntag 1990 specifically evaluates to ~23.3925 hPa at 20 C.
        self.assertAlmostEqual(e_s, 23.392, places=3, 
                               msg=f"Vapor pressure forward calc failed. Got {e_s}")

    def test_newton_raphson_reverse_calculation(self):
        """Test if the Newton-Raphson solver can accurately find the Dew Point."""
        # Instead of a hardcoded approximation, we feed the exact output of 
        # 20 C back into the solver to prove the root-finding is mathematically lossless.
        exact_e_at_20c = 23.392491605340155 
        
        t_k_found = MetronMath.solve_dewpoint(exact_e_at_20c, self.water_coeffs, initial_guess_k=290.0)
        
        # Check to 4 decimal places (0.0001 K resolution)
        self.assertAlmostEqual(t_k_found, 293.15, places=4, 
                               msg=f"Newton-Raphson failed to converge. Got {t_k_found}")

if __name__ == '__main__':
    unittest.main()
