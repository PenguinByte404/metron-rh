# 💧 Metron RH
**By Metzilla LLC / PenguinByte Open Source Initiative**

> 💡 **TL;DR:** Metron RH is a zero-dependency, mathematically rigorous relative humidity metrology suite designed for ISO/IEC 17025 accredited laboratories. Built entirely on the Python standard library, it eliminates external dependency risks and provides an immutable, highly auditable framework for chilled mirror calibrations, psychrometry, and trace moisture root-finding.

---

## 🏗️ 1. System Architecture (Developer Perspective)
The application utilizes a decoupled, modular architecture to ensure calculation consistency across all testing paradigms.

| Component | Role | Description |
| :--- | :--- | :--- |
| 💻 **`metron_rh.py`** | **Master Controller** | The CLI entry point. Loads static JSON databases into memory on startup and routes user inputs to specific metrology workflows. |
| 🧠 **`math_engine.py`** | **The Core Engine** | Centralized thermodynamic processor. Handles Sonntag exponential formulations and a pure-Python Newton-Raphson root-finding algorithm for reverse dewpoint/frostpoint solving. Guarantees UTF-8 encoding for math proofs. |
| 📚 **Data Layer** | **Standard Refs** | `vapor_pressure_coeff.json` & `enhance_factors_coeff.json`. Immutable dictionaries of standard reference coefficients strictly split by thermodynamic phase (Ice vs. Water). |

---

## 📜 2. Metrological Standards & Compliance
Metron RH is strictly bound to the following international metrology standards:

| Standard | Application in Metron RH |
| :--- | :--- |
| **Sonntag (1990)** | The globally recognized standard for vapor pressure over liquid water and ice. Computes purely in hPa/mbar. |
| **Greenspan (1981)** | Dictates the enhancement factors ($\alpha$ and $\beta$) required to correct for non-ideal gas interactions between water vapor and carrier gases at varying pressures. |
| **WMO / NIST Guidelines** | Enforces the strict demarcation of the supercooled water ambiguity (ensuring sub-zero readings explicitly define their phase state). |
| **ISO/IEC 17025** | Supported via automatic generation of timestamped, immutable `.txt` math proofs for unbroken data traceability. |

---

## ⚙️ 3. Module Operations (Technician & Developer Perspectives)

| 🔢 Mode | 🎯 Metrological Objective | 🔬 Physical Lab Setup | 🖥️ App Function |
| :--- | :--- | :--- | :--- |
| **1. Chilled Mirror** | Map highly accurate Dew/Frost points to an SPRT to find actual RH. | Decoupled Chilled Mirror Hygrometer and SPRT inside an environmental chamber. | Calculates partial pressure ($e$) from the mirror, saturation pressure ($e_s$) from the SPRT, and derives exact RH. |
| **2. Psychrometer** | Calculate RH via latent heat of evaporation. | Assmann/Aspirated Wet Bulb & Dry Bulb thermometers in an air stream. | Applies the psychrometric constant against ambient pressure to calculate vapor depression and derive pure RH. |
| **3. Trace Moisture** | Convert volume fraction to physical Frost Point. | Moisture analyzer outputting PPMv in a pressurized gas line. | Translates PPMv to partial pressure, then uses a Newton-Raphson iterative solver to reverse-calculate the exact Frost Point. |

---

## 🛠️ 4. Quick Setup & Deployment

### 🏗️ Step 1: Run the DB Seeder
Generates your fresh, immutable standard JSON databases based on metrological literature.
```bash
python db_seeder.py
```

### 🚀 Step 2: Run Metrology Suite
Boot up the master controller for terminal use.
```bash
python metron_rh.py
```

### 🧪 Step 3: Validate the App Functionality
Execute the native Test-Driven Metrology (TDM) suite to mathematically prove the engine.
```bash
python -m unittest discover tests/
```

### 📦 Step 4: Compile the Application
Bundle the suite into a single, portable Windows executable (Zero Python installation required on lab workstations!).
```bash
pyinstaller --onefile --add-data "vapor_pressure_coeff.json;." --add-data "enhance_factors_coeff.json;." metron_rh.py
```

### ✅ Finished!
Distribute `dist/metron_rh.exe` to the lab floor.

---

## ⚖️ License & Copyright

**Copyright © 2026 Metzilla LLC. > This repository is licensed under the MIT License.**

* **Permission:** You are free to use, copy, modify, merge, and distribute this software for any purpose.
* **Condition:** The above copyright notice and this permission notice must be included in all copies or substantial portions of the software.

### ⚠️ Disclaimer

**THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND. > In no event shall the authors or copyright holders be liable for any claim, damages, or other liability, whether in an action of contract, tort, or otherwise, arising from, out of, or in connection with the software or the use of the scripts provided herein. Always test in a sandbox environment before production use.**

---
