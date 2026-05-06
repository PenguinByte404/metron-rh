# Metron RH - Test-Driven Metrology (TDM) Criteria
**By Metzilla LLC / PenguinByte Open Source Initiative**

## Engine Validation (`test_math_engine.py`)

### Forward Calculation Accuracy
* **Objective:** Ensure the core polynomial evaluator correctly processes the Sonntag (1990) equation and handles internal conversion from Pascals (Pa) to Hectopascals (hPa).
* **Test Condition:** Engine evaluates $20.00^\circ\text{C}$ ($293.15\text{ K}$) over liquid water.
* **Pass Criteria:** Result must exactly match the Sonntag curve output of `23.392 hPa` (evaluated to 3 decimal places).

### Reverse Calculation (Newton-Raphson Convergence)
* **Objective:** Prove the iterative root-finding algorithm can work backward from a known vapor pressure to find the exact initial temperature without floating-point degradation.
* **Test Condition:** Engine is fed $23.392491...\text{ hPa}$ and asked to find the Frost/Dew point with an initial blind guess of $290.0\text{ K}$.
* **Pass Criteria:** The solver must successfully step via numerical derivatives to `293.15 K` (accurate to 4 decimal places) within 50 iterations, without diverging.

## Thermodynamic Validation (`test_thermodynamics.py`)

### The Triple Point of Water (TPW)
* **Objective:** The defining fixed point of the Kelvin scale. At $0.01^\circ\text{C}$ ($273.16\text{ K}$), water exists simultaneously as ice, liquid, and gas. The vapor pressure equations for Ice and Water MUST intersect here.
* **Test Condition:** Evaluate Sonntag Water and Sonntag Ice identically at `273.16 K`.
* **Pass Criteria:** Both outputs must equate to `6.1165 hPa` and match each other to at least 4 decimal places of precision.

### The Standard Boiling Point
* **Objective:** At $100^\circ\text{C}$ ($373.15\text{ K}$), the saturation vapor pressure of water approaches exactly one standard atmosphere.
* **Test Condition:** Evaluate Sonntag Water at `373.15 K`.
* **Pass Criteria:** The result must approach `1013.25 hPa`. *(Note: Due to the mathematical curve-fitting nature of the 1990 formulation, the test allows a 1.0 hPa delta to accommodate the polynomial's empirical reality of ~1014.19 hPa at this extreme boundary).*

## Enhancement Factor Validation (`test_two_pressure.py`)

### Greenspan 1981 Constants
* **Objective:** Prove the $\alpha$ and $\beta$ polynomials correctly compensate for non-ideal gas behavior when water vapor interacts with carrier gases.
* **Test Condition:** Evaluate enhancement factor over water at 20°C and 1 standard atmosphere (1013.25 hPa).
* **Pass Criteria:** The factor must evaluate to approximately `1.004` (strictly greater than an ideal gas state of 1.0).

### High-Pressure Ratio Reality Check
* **Objective:** Ensure the combined two-pressure generator equation functions correctly across pressure domains.
* **Test Condition:** Saturator operates at 4x atmospheric pressure (approx 4053 hPa) while Chamber operates at 1x atmospheric pressure. Both are maintained at 20°C.
* **Pass Criteria:** The ideal-gas ratio yields 25.0%. Due to the exponential shift of the Greenspan factors under high pressure, the "real" RH output must be slightly greater than the ideal ratio (evaluating to ~25.280%).

---
