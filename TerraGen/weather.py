import numpy as np
from terrain import Cell


class WeatherSystem:
    def __init__(self, config):
        """
        Initialize the WeatherSystem.
        :param config: A dictionary-like object containing weather parameters.
        """
        self.config = config
        self.current_weather = None

    def generate_weather(self):
        """
        Generate daily weather conditions based on random factors.
        :return: A dictionary representing the day's weather.
        """
        weather = {
            "rain_intensity": np.random.uniform(0, 0.5),  # Reduced max rain intensity
            "snow_intensity": np.random.uniform(0, 0.3),  # Reduced max snow intensity
            "wind_speed": np.random.uniform(0, 0.3),      # Mild wind
            "drought": np.random.choice([True, False], p=[0.1, 0.9])  # 10% chance of drought
        }
        self.current_weather = weather
        return weather

    def apply_weather_effects(self, grid):
        """
        Apply the effects of the current weather to the terrain grid.
        :param grid: The hexagonal grid (dictionary of Cell objects).
        """
        if not self.current_weather:
            raise ValueError("Weather has not been generated yet. Call generate_weather first.")

        rain_intensity = self.current_weather["rain_intensity"]
        snow_intensity = self.current_weather["snow_intensity"]
        wind_speed = self.current_weather["wind_speed"]
        drought = self.current_weather["drought"]

        max_water_level = 1.0  # Maximum water level cap

        for cell in grid.values():
            if isinstance(cell, Cell):  # Ensure the object is a Cell
                # Apply rain effects
                if not drought and rain_intensity > 0.2:  # Only significant rain affects terrain
                    cell.water_level += rain_intensity * self.config["weather_impact"]["rain_absorption"]

                # Apply snow effects (only at high altitudes or during winter)
                if cell.height > 0.6 and snow_intensity > 0.2:  # Significant snow
                    cell.water_level += snow_intensity * self.config["weather_impact"]["snow_accumulation"]

                # Reduce water level slightly due to wind
                cell.water_level -= wind_speed * 0.01
                cell.water_level = min(cell.water_level, max_water_level)  # Cap water level
                cell.water_level = max(0.0, cell.water_level)  # Ensure non-negative water level

                # Simulate drought effects
                if drought:
                    cell.water_level *= 0.9  # Reduce water by 10%


class SeasonManager:
    def __init__(self, days_per_season=90):
        """
        Initialize the SeasonManager.
        :param days_per_season: Number of days per season.
        """
        self.seasons = ["spring", "summer", "autumn", "winter"]
        self.current_season_index = 0
        self.days_per_season = days_per_season
        self.current_day = 0

    def get_current_season(self):
        """
        Get the current season based on the simulation day.
        :return: The name of the current season.
        """
        return self.seasons[self.current_season_index]

    def advance_day(self):
        """
        Advance the simulation by one day and update the season if needed.
        """
        self.current_day += 1
        if self.current_day % self.days_per_season == 0:
            self.current_season_index = (self.current_season_index + 1) % len(self.seasons)

    def apply_seasonal_effects(self, grid, config):
        """
        Apply seasonal effects to the terrain grid.
        :param grid: The terrain grid (dictionary of Cell objects).
        :param config: A dictionary-like object containing seasonal effect parameters.
        """
        current_season = self.get_current_season()
        seasonal_effects = config["seasonal_effects"].get(current_season, {})

        for cell in grid.values():
            if isinstance(cell, Cell):  # Ensure the object is a Cell
                # Adjust vegetation growth based on the season
                if "vegetation_growth_multiplier" in seasonal_effects:
                    cell.vegetation *= seasonal_effects["vegetation_growth_multiplier"]

                # Adjust desertification rates
                if "desertification_rate_multiplier" in seasonal_effects and cell.terrain_type == "desert":
                    cell.vegetation -= config["interaction_factors"]["desertification_rate"] * seasonal_effects["desertification_rate_multiplier"]
                    cell.vegetation = max(0.0, cell.vegetation)

                # Adjust snow accumulation
                if "snow_accumulation_multiplier" in seasonal_effects and cell.height > 0.6:
                    cell.water_level += config["weather_impact"]["snow_accumulation"] * seasonal_effects["snow_accumulation_multiplier"]

                # Ensure vegetation and water level remain within valid bounds
                cell.vegetation = max(0.0, min(1.0, cell.vegetation))
                cell.water_level = max(0.0, min(1.0, cell.water_level))
