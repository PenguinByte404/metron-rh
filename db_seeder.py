import json
import os

def build_sonntag_1990():
    """Compiles the Sonntag 1990 Vapor Pressure Formulations into a JSON file."""
    sonntag_data = {
        "reference": "Sonntag, D. (1990). Important new values of the physical constants of 1986, vapor pressure formulations...",
        "formula": "ln(e) = a1/T + a2 + a3*T + a4*T^2 + a5*ln(T)",
        "units": {"T": "Kelvin", "e": "hPa"},
        "Water": {
            "min_k": 173.15,
            "max_k": 373.15,
            "coefficients": {
                "a1": -6096.9385,
                "a2": 21.2409642,
                "a3": -2.711193e-2,
                "a4": 1.673952e-5,
                "a5": 2.433502
            }
        },
        "Ice": {
            "min_k": 173.15,
            "max_k": 273.16,
            "coefficients": {
                "a1": -6024.5282,
                "a2": 29.32707,
                "a3": 1.0613868e-2,
                "a4": -1.3198825e-5,
                "a5": -0.49382577
            }
        }
    }

    with open('vapor_pressure_coeff.json', 'w') as f:
        json.dump(sonntag_data, f, indent=4)
    print("[+] Successfully compiled vapor_pressure_coeff.json (Sonntag 1990)")

def build_greenspan_1981():
    """Compiles Greenspan 1981 Enhancement Factor Constants."""
    greenspan_data = {
        "reference": "Greenspan, L. (1981). Functional equations for the enhancement factors for CO2-free moist air.",
        "Water": {
            "A_coeffs": [3.53624e-4, 2.932836e-5, 2.61474e-7, 8.57538e-6],
            "B_coeffs": [-1.07588e1, 6.32529e-2, -2.535920e-4, 6.33784e-7]
        },
        "Ice": {
            "A_coeffs": [3.64449e-4, 2.93631e-5, 4.88635e-7, 4.36543e-5],
            "B_coeffs": [-1.07271e1, 7.61989e-2, -1.74771e-4, 2.46721e-6]
        }
    }
    with open('enhance_factors_coeff.json', 'w') as f:
        json.dump(greenspan_data, f, indent=4)
    print("[+] Successfully compiled enhance_factors_coeff.json (Greenspan 1981)")

if __name__ == "__main__":
    print("=== METRON RH : DATABASE SEEDER ===")
    
    if os.path.exists('vapor_pressure_coeff.json'):
        if input("[!] vapor_pressure_coeff.json exists. Overwrite? (y/n): ").lower() == 'y':
            build_sonntag_1990()
    else:
        build_sonntag_1990()

    if os.path.exists('enhance_factors_coeff.json'):
        if input("[!] enhance_factors_coeff.json exists. Overwrite? (y/n): ").lower() == 'y':
            build_greenspan_1981()
    else:
        build_greenspan_1981()
        
    print("\n[i] Database seeding complete. Metron RH is ready to run.")