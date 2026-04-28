from modules.math_engine import MetronMath

def execute(db, exe_dir):
    """Execution logic for Trace Moisture (PPMv) Metrology."""
    print("\n" + "="*50)
    print("  MODULE: TRACE MOISTURE (PPMv) METROLOGY  ")
    print("="*50)

    dut_id = input("Enter DUT Asset ID / Serial Number: ").strip()
    sonntag = db['sonntag']

    master_audit_log =  "==================================================\n"
    master_audit_log += "          METRON RH : CALIBRATION AUDIT           \n"
    master_audit_log += "==================================================\n"
    master_audit_log += f"DUT Asset ID    : {dut_id}\n"
    master_audit_log += f"Vapor Equation  : {sonntag['reference']}\n"
    master_audit_log += "Method          : Volume Fraction to Frost Point\n"
    master_audit_log += "==================================================\n\n"

    test_point_count = 1

    while True:
        print(f"\n--- NEW TEST POINT : {dut_id} (Point {test_point_count}) ---")
        try:
            ppmv = float(input("Enter Moisture Content (PPMv): "))
            pressure_hpa = float(input("Enter Line Pressure (hPa/mbar absolute): "))
        except ValueError:
            print("[!] Input error. Please enter valid numeric values.")
            continue

        point_log = f"--- TEST POINT {test_point_count} ---\n"
        
        # STEP 1: Calculate Partial Vapor Pressure
        point_log += f"STEP 1: Convert Volume Fraction to Partial Pressure (e)\n"
        # Formula: e = (PPMv * P) / (1,000,000 + PPMv)
        e_actual = (ppmv * pressure_hpa) / (1e6 + ppmv)
        
        point_log += f"Formula: e = (PPMv * P_total) / (1,000,000 + PPMv)\n"
        point_log += f">> Result (e): {e_actual:.6f} hPa\n\n"

        # STEP 2: Newton-Raphson Reverse Solve for Frost Point
        point_log += f"STEP 2: Iterative Root-Finding for Frost Point (T_f)\n"
        point_log += f"Algorithm: Pure-Python Newton-Raphson Method\n"
        
        # Trace moisture is almost exclusively frost point (Ice)
        ice_coeffs = sonntag["Ice"]["coefficients"]
        
        try:
            # We start the guess very cold (e.g., -40 C / 233.15 K) for trace moisture
            tf_k = MetronMath.solve_dewpoint(e_actual, ice_coeffs, initial_guess_k=233.15)
            tf_c = tf_k - 273.15
            
            point_log += f"Target e: {e_actual:.6f} hPa\n"
            point_log += f">> Result Frost Point (T_f): {tf_c:.3f} °C\n"
            point_log += "--------------------------------------------------\n\n"

        except ValueError as e:
            point_log += f"[!] Engine Error: {e}\n"
            print(f"[!] Root-finding failed. {e}")

        print("\n" + point_log.strip())
        master_audit_log += point_log

        test_point_count += 1
        if input("\nRun another test point for this DUT? (y/n): ").strip().lower() != 'y':
            break

    if input("\nSave this composite math proof to a .txt file? (y/n): ").strip().lower() == 'y':
        saved_path = MetronMath.export_proof(
            proof_text=master_audit_log.strip(), exe_dir=exe_dir,
            test_name="TraceMoisture", dut_id=dut_id
        )
        print(f"[i] Composite proof successfully saved to: {saved_path}")