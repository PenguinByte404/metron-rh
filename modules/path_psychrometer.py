import math
from modules.math_engine import MetronMath

def execute(db, exe_dir):
    """Execution logic for Psychrometer (Wet/Dry Bulb) Metrology."""
    print("\n" + "="*50)
    print("  MODULE: PSYCHROMETER (WET/DRY BULB) METROLOGY  ")
    print("="*50)

    dut_id = input("Enter DUT Asset ID / Serial Number: ").strip()
    sonntag = db['sonntag']

    master_audit_log =  "==================================================\n"
    master_audit_log += "          METRON RH : CALIBRATION AUDIT           \n"
    master_audit_log += "==================================================\n"
    master_audit_log += f"DUT Asset ID    : {dut_id}\n"
    master_audit_log += f"Vapor Equation  : {sonntag['reference']}\n"
    master_audit_log += "Method          : Assmann Aspirated Psychrometer\n"
    master_audit_log += "==================================================\n\n"

    test_point_count = 1

    while True:
        print(f"\n--- NEW TEST POINT : {dut_id} (Point {test_point_count}) ---")
        try:
            dry_bulb = float(input("Enter Dry Bulb Temp (°C): "))
            wet_bulb = float(input("Enter Wet Bulb Temp (°C): "))
            pressure_hpa = float(input("Enter Atmospheric Pressure (hPa/mbar): "))
        except ValueError:
            print("[!] Input error. Please enter valid numeric values.")
            continue

        if wet_bulb > dry_bulb:
            print("[!] Metrology Error: Wet bulb cannot be warmer than dry bulb. Re-enter data.")
            continue

        db_k = dry_bulb + 273.15
        wb_k = wet_bulb + 273.15

        point_log = f"--- TEST POINT {test_point_count} ---\n"
        
        # STEP 1: Saturation Vapor Pressure at Wet Bulb
        point_log += f"STEP 1: Calculate Saturation Vapor Pressure at Wet Bulb (e_sw)\n"
        phase = "Ice" if wet_bulb < 0.0 else "Water"
        wb_coeffs = sonntag[phase]["coefficients"]
        e_sw = MetronMath.calc_vapor_pressure(wb_k, wb_coeffs)
        
        point_log += MetronMath.generate_sonntag_proof("e_sw", wb_k, wb_coeffs) + "\n"
        point_log += f">> Result (e_sw): {e_sw:.5f} hPa\n\n"

        # STEP 2: Actual Vapor Pressure via Psychrometric Equation
        point_log += f"STEP 2: Calculate Actual Vapor Pressure (e)\n"
        # Standard Assmann psychrometric coefficient (A) for water above freezing is ~ 6.62e-4
        A = 6.62e-4 if wet_bulb >= 0 else 5.83e-4 
        
        e_actual = e_sw - (A * pressure_hpa * (dry_bulb - wet_bulb))
        point_log += f"Formula: e = e_sw - (A * P * (T_dry - T_wet))\n"
        point_log += f"Constants: A = {A} K^-1, P = {pressure_hpa} hPa\n"
        point_log += f">> Result (e): {e_actual:.5f} hPa\n\n"

        # STEP 3: Saturation Vapor Pressure at Dry Bulb
        point_log += f"STEP 3: Calculate Saturation Vapor Pressure at Dry Bulb (e_s)\n"
        db_phase = "Ice" if dry_bulb < 0.0 else "Water"
        db_coeffs = sonntag[db_phase]["coefficients"]
        e_s = MetronMath.calc_vapor_pressure(db_k, db_coeffs)
        
        point_log += MetronMath.generate_sonntag_proof("e_s", db_k, db_coeffs) + "\n"
        point_log += f">> Result (e_s): {e_s:.5f} hPa\n\n"

        # STEP 4: Relative Humidity
        point_log += f"STEP 4: Calculate Relative Humidity (RH)\n"
        rh = (e_actual / e_s) * 100.0
        
        # Check for super-saturation or negative humidity (impossible states)
        if rh > 100.0: rh = 100.0
        if rh < 0.0: rh = 0.0
            
        point_log += f"Formula: RH = (e / e_s) * 100\n"
        point_log += f">> Final RH: {rh:.3f} %\n"
        point_log += "--------------------------------------------------\n\n"

        print("\n" + point_log.strip())
        master_audit_log += point_log

        test_point_count += 1
        if input("\nRun another test point for this DUT? (y/n): ").strip().lower() != 'y':
            break

    if input("\nSave this composite math proof to a .txt file? (y/n): ").strip().lower() == 'y':
        saved_path = MetronMath.export_proof(
            proof_text=master_audit_log.strip(), exe_dir=exe_dir,
            test_name="Psychrometer", dut_id=dut_id
        )
        print(f"[i] Composite proof successfully saved to: {saved_path}")