import json
import sys
import os

# Import the core Metrology Suite modules
import modules.path_chilled_mirror as path_chilled_mirror
import modules.path_psychrometer as path_psychrometer
import modules.path_ppmv as path_ppmv

class MetronRH:
    """
    Metron RH: Master Controller
    Routes technicians to specific humidity metrology test modules and manages database state.
    """
    def __init__(self):
        # Handle PyInstaller pathing for bundled JSONs
        if getattr(sys, 'frozen', False):
            base_dir = sys._MEIPASS 
            self.exe_dir = os.path.dirname(sys.executable) 
        else:
            base_dir = os.path.dirname(os.path.abspath(__file__))
            self.exe_dir = base_dir

        sonntag_path = os.path.join(base_dir, "vapor_pressure_coeff.json")
        greenspan_path = os.path.join(base_dir, "enhance_factors_coeff.json")

        self.db = {}

        try:
            with open(sonntag_path, 'r') as f:
                self.db['sonntag'] = json.load(f)
            
            with open(greenspan_path, 'r') as f:
                self.db['greenspan'] = json.load(f)
                
        except FileNotFoundError as e:
            print(f"\n[!] Critical Error: Missing database file. {e}")
            print("[i] Ensure you have run 'python db_seeder.py' to generate the standard databases.")
            sys.exit(1)

    def display_header(self):
        print("\n" + r"  __  __      _                     ____  _   _ ")
        print(r" |  \/  | ___| |_ _ __ ___  _ __   |  _ \| | | |")
        print(r" | |\/| |/ _ \ __| '__/ _ \| '_ \  | |_) | |_| |")
        print(r" | |  | |  __/ |_| | | (_) | | | | |  _ <|  _  |")
        print(r" |_|  |_|\___|\__|_|  \___/|_| |_| |_| \_\_| |_|")
        print(" Relative Humidity Metrology Suite v1.1.0")
        print("------------------------------------------------")

    def run(self):
        self.display_header()
        
        while True:
            print("\n=== METRON RH : MAIN MENU ===")
            print("1. Chilled Mirror Reference (Td/Tf & Ta -> RH)")
            print("2. Psychrometer Reference (Tw & Ta -> RH) [WIP]")
            print("3. Trace Moisture (PPMv -> RH) [WIP]")
            print("0. Exit Metron RH")
            
            selection = input("\nSelect Metrology Module: ").strip()
            
            if selection == '0':
                print("Shutting down Metron RH. Goodbye.")
                sys.exit(0)

            # Route to appropriate module
            if selection == '1':
                print("\n[i] Routing to Chilled Mirror Module...")
                path_chilled_mirror.execute(self.db, self.exe_dir)
            elif selection == '2':
                print("\n[i] Routing to Psychrometer Module...")
                path_psychrometer.execute(self.db, self.exe_dir)
            elif selection == '3':
                print("\n[i] Routing to Trace Moisture Module...")
                path_ppmv.execute(self.db, self.exe_dir)
            else:
                print("[!] Invalid selection. Please choose a valid module.\n")

if __name__ == "__main__":
    app = MetronRH()
    app.run()
