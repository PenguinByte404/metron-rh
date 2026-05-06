from modules.math_engine import MetronMath

def execute(db, exe_dir):
    """Execution logic for Two-Pressure (Thunder Scientific) Metrology."""
    print("\n" + "="*50)
    print("  MODULE: TWO-PRESSURE (THUNDER SCIENTIFIC)  ")
    print("="*50)

    dut_id = input("Enter DUT Asset ID / Serial Number: ").strip()
    
    sonntag = db['sonntag']
    greenspan = db['greenspan']

    # --- INITIALIZE MASTER AUDIT LOG ---
    master_audit_log =  "==================================================\n"
    master_audit_log += "          METRON RH : CALIBRATION AUDIT           \n"
    master_audit_log += "==================================================\n"
    master_audit_log += f"DUT Asset ID    : {dut_id}\n"
    master_audit_log += f"Vapor Equation  : {sonntag['reference']}\n"
    master_audit_log += f"Enhancement Eq  : {greenspan['reference']}\n"
    master_audit_log += "Method          : Two-Pressure Generator\n"
    master_audit_log += "==================================================\n\n"

    test_point_count = 1

    while True:
        print(f"\n--- NEW TEST POINT : {dut_id} (Point {test_point_count}) ---")
        try:
            # Saturator Conditions
            t_s = float(input("Enter Saturator Temp (T_s) [°C]: "))
            p_s = float(input("Enter Saturator Pressure (P_s) [hPa/mbar absolute]: "))
            
            # Chamber Conditions
            t_t = float(input("Enter Chamber Temp (T_t) [°C]: "))
            p_t = float(input("Enter Chamber Pressure (P_t) [hPa/mbar absolute]: "))
        except ValueError:
            print("[!] Input error. Please enter valid numeric values.")
            continue

        point_log = f"--- TEST POINT {test_point_count} ---\n"
        
        # Determine Phases (Ice vs Water)
        phase_s = "Ice" if t_s < 0.0 else "Water"
        phase_t = "Ice" if t_t < 0.0 else "Water"

        # STEP 1: Saturator Thermodynamics
        point_log += f"STEP 1: Saturator Thermodynamics (T_s = {t_s}°C, P_s = {p_s} hPa)\n"
        es_ts = MetronMath.calc_vapor_pressure(t_s + 273.15, sonntag[phase_s]["coefficients"])
        f_s = MetronMath.calc_enhancement_factor(t_s, p_s, es_ts, greenspan[phase_s])
        
        point_log += f">> Saturation Vapor Pressure e_s(T_s) : {es_ts:.5f} hPa\n"
        point_log += f">> Enhancement Factor f(P_s, T_s)     : {f_s:.6f}\n\n"

        # STEP 2: Chamber Thermodynamics
        point_log += f"STEP 2: Chamber Thermodynamics (T_t = {t_t}°C, P_t = {p_t} hPa)\n"
        es_tt = MetronMath.calc_vapor_pressure(t_t + 273.15, sonntag[phase_t]["coefficients"])
        f_t = MetronMath.calc_enhancement_factor(t_t, p_t, es_tt, greenspan[phase_t])
        
        point_log += f">> Saturation Vapor Pressure e_s(T_t) : {es_tt:.5f} hPa\n"
        point_log += f">> Enhancement Factor f(P_t, T_t)     : {f_t:.6f}\n\n"

        # STEP 3: Relative Humidity Calculation
        point_log += f"STEP 3: Two-Pressure RH Calculation\n"
        rh = ((f_s * es_ts) / (f_t * es_tt)) * (p_t / p_s) * 100.0
        
        point_log += MetronMath.generate_two_pressure_proof(t_s, p_s, t_t, p_t, es_ts, es_tt, f_s, f_t)
        point_log += f">> Final Generated RH: {rh:.3f} %\n"
        point_log += "--------------------------------------------------\n\n"

        print("\n" + point_log.strip())
        master_audit_log += point_log

        test_point_count += 1
        if input("\nRun another test point for this DUT? (y/n): ").strip().lower() != 'y':
            break

    if input("\nSave this composite math proof to a .txt file? (y/n): ").strip().lower() == 'y':
        saved_path = MetronMath.export_proof(
            proof_text=master_audit_log.strip(), exe_dir=exe_dir,
            test_name="TwoPressure_Thunder", dut_id=dut_id
        )
        print(f"[i] Composite proof successfully saved to: {saved_path}")
