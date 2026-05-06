import unittest
import sys
import os
import json

# Adjust path to allow importing modules
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from modules.math_engine import MetronMath

class TestTwoPressureThermodynamics(unittest.TestCase):
    
    def setUp(self):
        # Load Databases
        sonntag_path = os.path.join(os.path.dirname(__file__), '..', 'vapor_pressure_coeff.json')
        greenspan_path = os.path.join(os.path.dirname(__file__), '..', 'enhance_factors_coeff.json')
        
        with open(sonntag_path, 'r') as f:
            self.sonntag = json.load(f)
            
        with open(greenspan_path, 'r') as f:
            self.greenspan = json.load(f)

    def test_greenspan_enhancement_factor(self):
        """
        Test the Greenspan 1981 Enhancement Factor logic.
        At standard atmospheric pressure (1013.25 hPa) and 20°C, 
        the enhancement factor over water is strictly greater than 1 (approx 1.004).
        """
        t_celsius = 20.0
        p_hpa = 1013.25
        
        # First get pure vapor pressure
        es_hpa = MetronMath.calc_vapor_pressure(t_celsius + 273.15, self.sonntag["Water"]["coefficients"])
        
        # Calculate enhancement
        f = MetronMath.calc_enhancement_factor(t_celsius, p_hpa, es_hpa, self.greenspan["Water"])
        
        # Enhancement factor at ambient is typically ~ 1.004
        self.assertGreater(f, 1.0, msg="Enhancement factor should be > 1 at standard pressure.")
        self.assertAlmostEqual(f, 1.004, places=3, msg="Enhancement factor deviated from expected standard.")

    def test_two_pressure_rh_calculation(self):
        """
        Test a theoretical Thunder 2500 output state.
        If Saturator and Chamber are at the same Temp (20°C), but Saturator is 
        at 4x the pressure (approx 4053 hPa vs 1013.25 hPa), the RH should be roughly 25%,
        shifted slightly by the enhancement factors.
        """
        t_c = 20.0
        p_t = 1013.25
        p_s = p_t * 4  # 4053.0 hPa
        
        # Common vapor pressure
        es = MetronMath.calc_vapor_pressure(t_c + 273.15, self.sonntag["Water"]["coefficients"])
        
        # Enhancement Factors
        f_s = MetronMath.calc_enhancement_factor(t_c, p_s, es, self.greenspan["Water"])
        f_t = MetronMath.calc_enhancement_factor(t_c, p_t, es, self.greenspan["Water"])
        
        # Ideal gas RH would be exactly 25.0%. 
        # Real gas RH applies the ratio of the enhancement factors.
        ideal_rh = (p_t / p_s) * 100.0
        real_rh = (f_s / f_t) * ideal_rh
        
        # Because f_s (at high pressure) is larger than f_t (at ambient pressure),
        # the real RH will be slightly higher than the ideal 25.0%.
        self.assertGreater(real_rh, ideal_rh, msg="Real RH must exceed Ideal RH due to pressure enhancement.")
        
        # Output should be roughly 25.1 - 25.3%
        self.assertAlmostEqual(real_rh, 25.2, delta=0.2, msg="Two-Pressure RH calculation out of bounds.")

if __name__ == '__main__':
    unittest.main()
