import math
import os
from datetime import datetime

class MetronMath:
    """Centralized thermodynamic math and utility engine for Metron RH."""

    @staticmethod
    def calc_vapor_pressure(t_kelvin, coeffs):
        """
        Evaluates the Sonntag (1990) vapor pressure equation.
        Formula: ln(e) = a1/T + a2 + a3*T + a4*T^2 + a5*ln(T)
        Returns pressure in hPa.
        """
        ln_e = (coeffs["a1"] / t_kelvin) + \
               coeffs["a2"] + \
               (coeffs["a3"] * t_kelvin) + \
               (coeffs["a4"] * (t_kelvin ** 2)) + \
               (coeffs["a5"] * math.log(t_kelvin))        
        # Sonntag natively outputs Pascals (Pa). Divide by 100 to yield hPa.
        return math.exp(ln_e) / 100.0

    @staticmethod
    def solve_dewpoint(target_e, coeffs, initial_guess_k=293.15, tolerance=1e-6, max_iter=50):
        """
        Calculates Dew/Frost point from vapor pressure using the Newton-Raphson method.
        Since we cannot isolate T algebraically in the Sonntag equation, we iterate.
        """
        t_k = initial_guess_k
        for _ in range(max_iter):
            # 1. Calculate current error: f(T) = current_e - target_e
            current_e = MetronMath.calc_vapor_pressure(t_k, coeffs)
            f_t = current_e - target_e
            
            if abs(f_t) < tolerance:
                return t_k # Target achieved
                
            # 2. Numerical Derivative: f'(T) = (f(T + h) - f(T - h)) / 2h
            h = 1e-5
            e_plus = MetronMath.calc_vapor_pressure(t_k + h, coeffs)
            e_minus = MetronMath.calc_vapor_pressure(t_k - h, coeffs)
            f_prime_t = (e_plus - e_minus) / (2 * h)
            
            # 3. Newton Step: T_new = T - f(T)/f'(T)
            t_k = t_k - (f_t / f_prime_t)
            
        raise ValueError("Newton-Raphson failed to converge on Dew Point.")

    @staticmethod
    def generate_sonntag_proof(var_name, t_kelvin, coeffs):
        """Generates the string representation of the thermodynamic equation."""
        proof = f"ln({var_name}) = ({coeffs['a1']:.4f} / {t_kelvin:.4f}) + {coeffs['a2']:.4f} "
        proof += f"+ ({coeffs['a3']:e} * {t_kelvin:.4f}) "
        proof += f"+ ({coeffs['a4']:e} * {t_kelvin:.4f}^2) "
        proof += f"+ ({coeffs['a5']:.4f} * ln({t_kelvin:.4f}))"
        return proof

    @staticmethod
    def export_proof(proof_text, exe_dir, test_name, dut_id):
        """Exports the math proof to an auditable .txt file."""
        proof_dir = os.path.join(exe_dir, "Metron_Proofs")
        if not os.path.exists(proof_dir):
            os.makedirs(proof_dir)

        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        filename = f"{timestamp}_RH_{test_name}_{dut_id}.txt"
        filepath = os.path.join(proof_dir, filename)

        with open(filepath, 'w', encoding='utf-8') as f:
            f.write(proof_text)

        return filepath
