import numpy as np
from noise import pnoise2


class Cell:
    def __init__(self, q, r, height=0.0, terrain_type="default", water_level=0.0, vegetation=0.0, temperature=25.0):
        """
        Initialize a single hexagonal grid cell.
        :param q: Axial coordinate q.
        :param r: Axial coordinate r.
        :param height: Elevation of the cell.
        :param terrain_type: Type of terrain (e.g., desert, forest).
        :param water_level: Current water level in the cell.
        :param vegetation: Vegetation level of the cell (0.0 - 1.0).
        :param temperature: Temperature in Celsius for the cell.
        """
        self.q = q
        self.r = r
        self.height = height
        self.terrain_type = terrain_type
        self.water_level = water_level
        self.vegetation = vegetation
        self.temperature = temperature


class Terrain:
    def __init__(self, config):
        self.config = config
        self.grid = {}  # Hexagonal grid stored as a dictionary

    def initialize_hex_grid(self, presets):
        """
        Initialize a hexagonal grid with default cells and assign regions based on presets.
        :param presets: A list of Config objects for different terrain types.
        """
        grid_radius = self.config.grid_width // 2
        self.grid = {}

        for q in range(-grid_radius, grid_radius + 1):
            for r in range(-grid_radius, grid_radius + 1):
                if abs(q + r) <= grid_radius:
                    preset = presets[np.random.randint(0, len(presets))]
                    self.grid[(q, r)] = Cell(q, r, terrain_type=preset.terrain_type)

    def generate(self, presets, seed=None):
        """
        Generate a mixed heightmap using Perlin noise and refine terrain types based on rules.
        :param presets: A list of Config objects for different terrain types.
        :param seed: Random seed for noise generation (default: None for random).
        """
        if seed is None:
            seed = np.random.randint(0, 10000)

        np.random.seed(seed)  # Set seed for reproducibility

        for (q, r), cell in self.grid.items():
            # Generate height using Perlin noise
            cell.height = pnoise2(
                (q + seed) / self.config.scale,
                (r + seed) / self.config.scale,
                octaves=self.config.octaves,
                persistence=self.config.persistence,
                lacunarity=self.config.lacunarity,
            )

            # Apply terrain rules based on height
            if cell.height < self.config.water_level:
                cell.terrain_type = "ocean"
            elif cell.height > 0.6:
                cell.terrain_type = "mountains"
            elif 0.3 < cell.height <= 0.6:
                cell.terrain_type = np.random.choice(["plains", "forest"], p=[0.5, 0.5])
            else:
                cell.terrain_type = np.random.choice(["desert", "plains"], p=[0.3, 0.7])

    def normalize(self):
        """
        Normalize the grid's height values to the range [0, 1].
        """
        if self.grid:
            heights = [cell.height for cell in self.grid.values()]
            min_val = min(heights)
            max_val = max(heights)

            for cell in self.grid.values():
                if max_val > min_val:  # Avoid division by zero
                    cell.height = (cell.height - min_val) / (max_val - min_val)

    def apply_water(self):
        """
        Set water levels in the grid based on height and the configured water level.
        Adjust water levels dynamically to prevent terrain flooding.
        """
        if self.grid:
            for cell in self.grid.values():
                if isinstance(cell, Cell):
                    if cell.height < self.config.water_level:
                        cell.water_level = max(cell.water_level, self.config.water_level)
                    else:
                        cell.water_level = max(cell.water_level - 0.01, 0.0)

                    cell.water_level = min(cell.water_level, 0.2)  # Cap water level

    def apply_vegetation_growth(self):
        """
        Simulate vegetation growth based on water levels and terrain type.
        """
        if self.grid:
            for cell in self.grid.values():
                if cell.water_level > 0.3:  # Example threshold for vegetation growth
                    growth_rate = self.config.interaction_factors["vegetation_growth"]
                    cell.vegetation = min(1.0, cell.vegetation + growth_rate)

    def mix_terrains(self, configs, weights=None):
        """
        Generate a mixed terrain using multiple configurations.
        :param configs: List of Config objects for different terrains.
        :param weights: List of weights for blending terrains.
        """
        if weights is None:
            weights = [1 / len(configs)] * len(configs)

        for coord, cell in self.grid.items():
            selected_config = np.random.choice(configs, p=weights)
            cell.terrain_type = selected_config.terrain_type
