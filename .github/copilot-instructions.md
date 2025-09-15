# Copilot Instructions for acn-tp1

## Project Overview
This project simulates the arrival and management of airplanes approaching Aeroparque (AEP), focusing on their sequencing, speed control, and possible rerouting to Montevideo. The simulation is implemented in Python and includes both core logic and visualization tools.

## Key Components
- **`tp.py`**: Main simulation logic, including airplane (`Avion`) class, simulation loop, and data output. Also contains a minimal integration example for visualization.
- **`tools_visualizacion.py`**: Visualization utilities using Pygame. Defines color schemes, drawing functions, and time formatting for the simulation.
- **`calcular_proba.py`**: Probability/statistics analysis on simulation outputs, e.g., comparing empirical and theoretical results.
- **`codigoAdicional.py`**: (Commented) Alternative or experimental airplane logic and print helpers.
- **`salidas_sim/`**: Stores simulation output as JSON files, named by parameters (e.g., `run_p=..._sim=....json`).

## Developer Workflows
- **Run Simulation**: Execute `tp.py` to run the main simulation and generate output in `salidas_sim/`.
- **Visualize**: Use the Pygame-based demo in `tp.py` (see `if __name__ == "__main__": demo()`) or call visualization functions from `tools_visualizacion.py`.
- **Analyze Results**: Use `calcular_proba.py` to analyze output JSONs.
- **Modify Airplane Logic**: Update the `Avion` class in `tp.py` for main logic, or refer to `codigoAdicional.py` for alternative approaches.

## Project-Specific Patterns
- **Distance Units**: 1 nautical mile (NM) = 1.852 km. All distances and speeds are managed in km or km/h, but logic often refers to NM.
- **Franja Temporal**: Airplanes are categorized into temporal bands (franjas) based on distance, affecting speed and sequencing.
- **Reubicación**: If airplanes are too close (less than 4 minutes apart), their speed is adjusted or they may be rerouted.
- **Visualization**: Airplanes are drawn as polygons, with color indicating their franja. Retroceso (reverse) is shown in white.
- **Output Format**: Simulation results are saved as JSON with parameters and matrices for arrivals and reroutes.

## Integration Points
- **Pygame**: Required for visualization. Ensure it is installed (`pip install pygame`).
- **NumPy**: Used for matrix operations and random sampling.
- **JSON**: Used for saving and loading simulation results.

## Example: Adding a New Airplane Rule
To add a new rule for airplane sequencing, modify the `Avion` class or the main simulation loop in `tp.py`. For visualization changes, update `tools_visualizacion.py`.

## Conventions
- Use explicit units in variable names (e.g., `dist_km`, `velocidad_kmh`).
- Keep all simulation outputs in `salidas_sim/`.
- Prefer modifying `tp.py` for core logic; use `codigoAdicional.py` for experiments.

---

If any section is unclear or missing, please provide feedback for further refinement.
