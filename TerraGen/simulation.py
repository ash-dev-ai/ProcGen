from config import Config
from terrain import Terrain
from weather import WeatherSystem, SeasonManager
from interactions import InteractionsManager
from events import EventManager
from visualization import Visualization
import numpy as np
import json
import os
from datetime import datetime


class CustomEncoder(json.JSONEncoder):
    def default(self, obj):
        if isinstance(obj, (np.floating, np.integer)):
            return float(obj)
        elif isinstance(obj, bool):
            return bool(obj)  # Explicitly handle bool
        elif isinstance(obj, np.ndarray):
            return obj.tolist()
        elif hasattr(obj, "__dict__"):
            return obj.__dict__  # Handle custom objects with a `__dict__` attribute
        return str(obj)  # Fallback for unsupported types


class Simulation:
    def __init__(self, config_preset="default"):
        """
        Initialize the simulation.
        :param config_preset: The name of the preset to use for the configuration.
        """
        self.config = Config(preset=config_preset)
        self.terrain = None
        self.weather_system = None
        self.season_manager = None
        self.interactions_manager = None
        self.event_manager = None
        self.visualization = None
        self.current_day = 0
        self.simulation_history = []

    def initialize_simulation(self):
        """
        Initialize all components of the simulation.
        """
        # Initialize terrain with multiple presets
        presets = [
            Config(preset="desert"),
            Config(preset="forest"),
            Config(preset="mountains"),
            Config(preset="plains"),
            Config(preset="arctic"),
        ]
        self.terrain = Terrain(self.config)
        self.terrain.initialize_hex_grid(presets)  # Initialize the hexagonal grid
        self.terrain.generate(presets)            # Generate terrain for all regions
        self.terrain.normalize()                  # Normalize height values
        self.terrain.apply_water()                # Apply water levels

        # Initialize other systems
        self.weather_system = WeatherSystem(self.config.__dict__)
        self.season_manager = SeasonManager()
        self.interactions_manager = InteractionsManager(self.config.__dict__)
        self.event_manager = EventManager(self.config.__dict__)
        self.visualization = Visualization(self.terrain)

    def run_simulation(self, days=100, visualize=True):
        """
        Run the simulation for a specified number of days.
        :param days: Number of days to simulate.
        :param visualize: Whether to visualize daily updates.
        """
        print(f"Starting simulation for {days} days.")
        for _ in range(days):
            self.update_day(visualize)

    def update_day(self, visualize=True):
        """
        Perform the daily update cycle.
        :param visualize: Whether to visualize the changes after each day.
        """
        print(f"Day {self.current_day + 1}: Starting updates.")

        # Generate weather and apply effects
        weather = self.weather_system.generate_weather()
        self.weather_system.apply_weather_effects(self.terrain.grid)

        # Apply seasonal effects
        self.season_manager.apply_seasonal_effects(self.terrain.grid, self.config.__dict__)

        # Apply terrain interactions
        self.interactions_manager.apply_interactions(self.terrain.grid)

        # Trigger and apply events
        event_type = self.event_manager.trigger_event()
        if event_type:
            print(f"Event triggered: {event_type}")
            self.event_manager.apply_event(event_type, self.terrain.grid)

        # Save the current state
        self.save_simulation_state(weather, event_type)

        # Visualize the updates
        if visualize:
            self.visualize_day(weather, event_type)

        # Advance the day
        self.season_manager.advance_day()
        self.current_day += 1

    def save_simulation_state(self, weather, event_type):
        """
        Save the current state of the simulation for later analysis.
        :param weather: Current weather conditions.
        :param event_type: The event type triggered on this day (if any).
        """
        state = {
            "day": self.current_day,
            "weather": {
                key: float(value) if isinstance(value, (np.floating, np.integer)) else value
                for key, value in weather.items()
            },
            "event": event_type,
            "terrain": {
                f"({q},{r})": {
                    "height": float(cell.height),
                    "water_level": float(cell.water_level),
                    "terrain_type": cell.terrain_type,
                    "vegetation": float(cell.vegetation),
                    "temperature": float(cell.temperature),
                }
                for (q, r), cell in self.terrain.grid.items()
            },
        }
        self.simulation_history.append(state)

    def visualize_day(self, weather, event_type):
        """
        Visualize the terrain, weather, and events for the current day.
        :param weather: Current weather conditions.
        :param event_type: The event type triggered on this day (if any).
        """
        print("Visualizing updates...")
        self.visualization.plot_grayscale()
        self.visualization.plot_colored()
        self.visualization.plot_3d_surface()
        self.visualization.plot_weather_overlay(weather)
        if event_type:
            self.visualization.plot_event_effects(event_type)

    def export_simulation_history(self, filename=None):
        """
        Export the simulation history to a JSON file for analysis.
        :param filename: Optional name of the file to save the history. If None, it generates a name with date and time.
        """
        os.makedirs("output", exist_ok=True)  # Ensure the output directory exists
    
        if filename is None:
            # Create a timestamped filename
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            filename = f"simulation_history_{timestamp}.json"
    
        filepath = os.path.join("output", filename)
    
        with open(filepath, "w") as f:
            json.dump(self.simulation_history, f, indent=4, cls=CustomEncoder)
    
        print(f"Simulation history saved to {filepath}.")