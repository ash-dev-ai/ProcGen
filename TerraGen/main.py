from config import Config
from terrain import Terrain
from weather import WeatherSystem, SeasonManager
from interactions import InteractionsManager
from events import EventManager
from visualization import Visualization
from simulation import Simulation


def main():
    # Step 1: Initialize the simulation
    simulation = Simulation(config_preset="default")

    # Step 2: Initialize all components
    print("Initializing simulation...")
    simulation.initialize_simulation()

    # Step 3: Run the simulation
    print("Starting simulation...")
    simulation.run_simulation(days=30, visualize=True)

    # Step 4: Export simulation history
    print("Exporting simulation history...")
    simulation.export_simulation_history()

    print("Simulation completed successfully!")


if __name__ == "__main__":
    main()
