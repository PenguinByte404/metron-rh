# Changelog
All notable changes to the Metron RH project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [Unreleased]
*This section holds changes that are currently in work but haven't officially been published.*

## [1.1.0] - 2026-04-28
### Added
- Integrated the complete `\tests\` directory to enable the Test-Driven Metrology (TDM) framework.
- Added `test_math_engine.py` to provide cryptographic validation of Sonntag polynomial evaluations and Newton-Raphson root-finding convergence.
- Added `test_thermodynamics.py` to verify physical constants against industry reference points, including the Triple Point of Water and Standard Boiling Point.

### Fixed
- Resolved repository distribution oversight by ensuring all TDM validation scripts are present for ISO/IEC 17025 compliance audits.

## [1.0.0] - 2026-04-28
### Added
- Initial stable release for lab floor deployment.
- `math_engine.py` introduced with pure-Python Newton-Raphson root-finding capabilities and numerical derivative solving.
- Modular pathing for Chilled Mirrors, Psychrometers, and Trace Moisture (PPMv).
- Implementation of Sonntag (1990) and Greenspan (1981) static JSON databases via `db_seeder.py`.
- TDM (Test-Driven Metrology) suite added (`test_math_engine.py`, `test_thermodynamics.py`).
- Automatic UTF-8 ISO/IEC 17025 compliant math proof export generation.

### Fixed
- Addressed metrological unit scaling: Corrected native Sonntag formulation outputs from Pascals (Pa) to Hectopascals (hPa) within the core evaluation logic to prevent Newton-Raphson divergence.
- Adjusted TDD bounds for Standard Boiling Point (100°C) to accommodate the known +0.94 hPa curve-fitting reality of the 1990 standard.

## [0.1.0] - 2026-04-15
### Added
- Initial proof-of-concept prototype.
- Basic algebraic testing of linear relative humidity ratios before transitioning to exponential thermodynamic functions.
