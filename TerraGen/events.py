from terrain import Cell
import numpy as np

class EventManager:
    def __init__(self, config):
        """
        Initialize the EventManager.
        :param config: A dictionary containing event-related parameters.
        """
        self.config = config

    def trigger_event(self):
            """
            Trigger a random event based on defined probabilities.
            :return: The type of event or None if no event is triggered.
            """
            event_types = ["earthquake", "flood", "wildfire", "rapid_growth", None]  # None means no event
            probabilities = [0.1, 0.05, 0.1, 0.05, 0.7]  # Adjusted probabilities to sum to 1
    
            # Ensure probabilities sum to 1
            probabilities = np.array(probabilities) / np.sum(probabilities)
    
            return np.random.choice(event_types, p=probabilities)

    def apply_event(self, event_type, grid):
        """
        Apply the effects of an event to the terrain grid.
        :param event_type: The type of event to apply.
        :param grid: The terrain grid (dictionary of Cell objects).
        """
        if event_type == "earthquake":
            self.simulate_earthquake(grid)
        elif event_type == "flood":
            self.simulate_flood(grid)
        elif event_type == "wildfire":
            self.simulate_wildfire(grid)
        elif event_type == "rapid_growth":
            self.simulate_rapid_growth(grid)

    def simulate_earthquake(self, grid):
        """
        Simulate an earthquake by randomizing elevation changes.
        """
        for cell in grid.values():
            if isinstance(cell, Cell):
                cell.height -= np.random.uniform(0, 0.05)  # Decrease height slightly
                cell.height = max(0.0, cell.height)

    def simulate_flood(self, grid):
        """
        Simulate a flood by increasing water levels.
        """
        for cell in grid.values():
            if isinstance(cell, Cell):
                cell.water_level += np.random.uniform(0.1, 0.3)
                cell.water_level = min(1.0, cell.water_level)  # Cap at max water level

    def simulate_wildfire(self, grid):
        """
        Simulate a wildfire by reducing vegetation in affected areas.
        """
        for cell in grid.values():
            if isinstance(cell, Cell) and cell.vegetation > 0.2:
                cell.vegetation -= np.random.uniform(0.1, 0.3)
                cell.vegetation = max(0.0, cell.vegetation)

    def simulate_rapid_growth(self, grid):
        """
        Simulate rapid vegetation growth.
        """
        for cell in grid.values():
            if isinstance(cell, Cell) and cell.water_level > 0.3 and cell.terrain_type != "desert":
                cell.vegetation += np.random.uniform(0.2, 0.5)
                cell.vegetation = min(1.0, cell.vegetation)
