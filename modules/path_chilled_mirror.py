import math
from modules.math_engine import MetronMath

def execute(db, exe_dir):
    """Execution logic for Chilled Mirror to SPRT Humidity mapping."""
    print("\n" + "="*50)
    print("  MODULE: CHILLED MIRROR / SPRT METROLOGY  ")
    print("="*50)

    dut_id = input("Enter DUT Asset ID / Serial Number: ").strip()
    
    sonntag = db['sonntag']

    # --- INITIALIZE MASTER AUDIT LOG ---
    master_audit_log =  "==================================================\n"
    master_audit_log += "          METRON RH : CALIBRATION AUDIT           \n"
    master_audit_log += "==================================================\n"
    master_audit_log += f"DUT Asset ID    : {dut_id}\n"
    master_audit_log += f"Vapor Equation  : {sonntag['reference']}\n"
    master_audit_log += "==================================================\n\n"

    test_point_count = 1

    while True:
        print(f"\n--- NEW TEST POINT : {dut_id} (Point {test_point_count}) ---")
        try:
            mirror_temp = float(input("Enter Chilled Mirror Temp (°C): "))
            
            # State Management: Resolve Supercooled Water Ambiguity
            phase = "Water"
            if mirror_temp < 0.0:
                print("[!] Sub-zero measurement detected.")
                p_choice = input("Is the mirror phase (1) Frost/Ice or (2) Supercooled Water? [1/2]: ").strip()
                phase = "Ice" if p_choice == '1' else "Water"

            sprt_temp = float(input("Enter SPRT Air Temp (°C): "))
        except ValueError:
            print("[!] Input error. Please enter valid numeric values.")
            continue

        # Convert to Kelvin for thermodynamic equations
        mirror_k = mirror_temp + 273.15
        sprt_k = sprt_temp + 273.15

        point_log = f"--- TEST POINT {test_point_count} ---\n"
        
        # STEP 1: Partial Vapor Pressure (e) from Mirror
        point_log += f"STEP 1: Calculate Partial Vapor Pressure (e) from Mirror\n"
        point_log += f"Measured Mirror Temp (T_d/f): {mirror_temp} °C ({mirror_k} K)\n"
        point_log += f"Phase State Assumed: {phase}\n"
        
        mirror_coeffs = sonntag[phase]["coefficients"]
        e_actual = MetronMath.calc_vapor_pressure(mirror_k, mirror_coeffs)
        
        point_log += MetronMath.generate_sonntag_proof("e", mirror_k, mirror_coeffs) + "\n"
        point_log += f">> Result (e): {e_actual:.5f} hPa\n\n"

        # STEP 2: Saturation Vapor Pressure (e_s) from SPRT
        point_log += f"STEP 2: Calculate Saturation Vapor Pressure (e_s) from SPRT\n"
        point_log += f"Measured Air Temp (T_a): {sprt_temp} °C ({sprt_k} K)\n"
        
        # Air is almost always treated as water phase unless ambient is sub-zero
        ambient_phase = "Ice" if sprt_temp < 0.0 else "Water"
        sprt_coeffs = sonntag[ambient_phase]["coefficients"]
        e_sat = MetronMath.calc_vapor_pressure(sprt_k, sprt_coeffs)

        point_log += MetronMath.generate_sonntag_proof("e_s", sprt_k, sprt_coeffs) + "\n"
        point_log += f">> Result (e_s): {e_sat:.5f} hPa\n\n"

        # STEP 3: Relative Humidity Calculation
        point_log += f"STEP 3: Calculate Relative Humidity (RH)\n"
        rh = (e_actual / e_sat) * 100.0
        point_log += f"Formula: RH = (e / e_s) * 100\n"
        point_log += f">> Final RH: {rh:.3f} %\n"
        point_log += "--------------------------------------------------\n\n"

        print("\n" + point_log.strip())
        master_audit_log += point_log

        test_point_count += 1
        if input("\nRun another test point for this DUT? (y/n): ").strip().lower() != 'y':
            break

    # --- EXPORT PROMPT ---
    if input("\nSave this composite math proof to a .txt file? (y/n): ").strip().lower() == 'y':
        saved_path = MetronMath.export_proof(
            proof_text=master_audit_log.strip(),
            exe_dir=exe_dir,
            test_name="ChilledMirror",
            dut_id=dut_id
        )
        print(f"[i] Composite proof successfully saved to: {saved_path}")

    print("\n[i] Exiting Chilled Mirror Module. Returning to Main Menu...")