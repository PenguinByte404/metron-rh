# Metron RH - System Architecture & Metrological Operations
**By Metzilla LLC / PenguinByte Open Source Initiative**

## Executive Summary
Metron RH is a zero-dependency, mathematically rigorous relative humidity metrology suite designed for metrology laboratories. Built entirely on the Python standard library, it eliminates the risk of external dependency deprecation and provides an immutable, highly auditable framework for high-precision humidity calculations, trace moisture root-finding, and environmental chamber characterizations.

## 1. System Architecture (Developer Perspective)
The application utilizes a decoupled, modular architecture to ensure calculation consistency across all thermodynamic pathways.

### Core Components
* **`metron_rh.py` (Master Controller):** The CLI entry point. It loads static JSON databases into memory on startup to minimize disk I/O and routes user inputs to specific instrument sub-modules.
* **`modules/math_engine.py` (The Core Engine):** The centralized mathematical processor. Unlike standard linear evaluations, humidity requires exponential evaluations and complex natural logarithms. This engine also houses a **Newton-Raphson iterative solver** and numerical derivative generator for reverse calculations (Vapor Pressure $\rightarrow$ Temperature).
* **The Data Layer (`vapor_pressure_coeff.json`, `enhance_factors_coeff.json`):** Immutable dictionaries of standard reference coefficients. Because water behaves fundamentally differently as a solid versus a liquid, the engine strictly delineates calculations through explicit `Ice` and `Water` coefficient blocks.

## 2. Metrological Standards & Compliance
Metron RH is strictly bound to the following international metrology standards:
* **Sonntag (1990):** An internationally recognized update to the Wexler formulas. Evaluates exact partial and saturation vapor pressures over liquid water and ice.
* **Greenspan (1981):** Provides the mathematical constants necessary to calculate Enhancement Factors ($f$), correcting for non-ideal gas behavior when water vapor interacts with Nitrogen and Oxygen under pressure.
* **ISO/IEC 17025:** Supported via the automatic generation of timestamped, immutable `.txt` math proofs for every calculation, ensuring unbroken data traceability.

---

## 3. Module Operations (Technician & Developer Perspectives)

### Mode 1: Chilled Mirror Metrology
* **Metrological Objective:** Map the high-accuracy Dew/Frost point of a chilled mirror to the ambient dry-bulb temperature of a metrology-grade SPRT to calculate pure actual Relative Humidity.
* **Physical Lab Setup:** A chilled mirror hygrometer and a PRT/SPRT are placed in an environmental chamber. The mirror provides the condensation equilibrium point, while the SPRT provides the highly stable ambient reference.
* **App Function:** Resolves the supercooled water ambiguity by querying the technician for phase state if $T < 0^\circ\text{C}$. Evaluates the Sonntag polynomial for partial vapor pressure ($e$) and saturation vapor pressure ($e_s$), then natively calculates $\% RH$.

### Mode 2: Psychrometer (Wet Bulb / Dry Bulb)
* **Metrological Objective:** Calculate actual vapor pressure via the latent heat of evaporation.
* **Physical Lab Setup:** An aspirated psychrometer (Assmann type) measures the ambient air temperature and the suppressed temperature of a water-wicked thermometer.
* **App Function:** Calculates saturation vapor pressure at the wet-bulb temperature. Applies the psychrometric constant (accounting for atmospheric pressure and phase) to calculate actual vapor pressure, then compares it to dry-bulb saturation to find RH.

### Mode 3: Trace Moisture (PPMv)
* **Metrological Objective:** Translate volume fraction readings from industrial/trace moisture sensors into physical Frost Point temperatures.
* **Physical Lab Setup:** A trace moisture analyzer outputs a Parts-Per-Million by Volume (PPMv) reading from a pressurized gas line.
* **App Function:** Mathematically translates the molar volume fraction and line pressure into a direct partial vapor pressure. Since temperature cannot be isolated algebraically from the Sonntag formula, the application executes a pure-Python Newton-Raphson root-finding algorithm to converge on the exact Frost Point.

---