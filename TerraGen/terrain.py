import numpy as np
from noise import pnoise2
from scipy.ndimage import zoom


class Terrain:
    def __init__(self, config):
        """
        Initialize the Terrain object.
        :param config: A Config object containing parameters for terrain generation.
        """
        self.config = config
        self.heightmap = None

    def generate(self, seed=None):
        """
        Generate a heightmap using Perlin noise.
        :param seed: Random seed for noise generation (default: None for random).
        """
        if seed is None:
            seed = np.random.randint(0, 10000)

        np.random.seed(seed)  # Set seed for reproducibility
        width, height = self.config.grid_width, self.config.grid_height
        scale, octaves, persistence, lacunarity = (
            self.config.scale,
            self.config.octaves,
            self.config.persistence,
            self.config.lacunarity,
        )

        self.heightmap = np.zeros((width, height))
        for i in range(width):
            for j in range(height):
                self.heightmap[i][j] = pnoise2(
                    (i + seed) / scale,
                    (j + seed) / scale,
                    octaves=octaves,
                    persistence=persistence,
                    lacunarity=lacunarity,
                )

    def add_random_variation(self, intensity=0.05):
        """
        Add random noise to the heightmap to create more variability.
        :param intensity: Maximum deviation as a fraction of the range.
        """
        if self.heightmap is not None:
            noise = np.random.uniform(-intensity, intensity, self.heightmap.shape)
            self.heightmap += noise
            self.heightmap = np.clip(self.heightmap, 0, 1)  # Ensure values stay in range

    def normalize(self):
        """
        Normalize the heightmap to the range [0, 1].
        """
        if self.heightmap is not None:
            min_val = np.min(self.heightmap)
            max_val = np.max(self.heightmap)
            if max_val > min_val:  # Avoid division by zero
                self.heightmap = (self.heightmap - min_val) / (max_val - min_val)

    def apply_water(self):
        """
        Flatten areas below the water level to the water level.
        """
        if self.heightmap is not None:
            water_level = self.config.water_level
            self.heightmap[self.heightmap < water_level] = water_level

    def resize_heightmap(self, heightmap, target_shape):
        """
        Resize a heightmap to the target shape using interpolation.
        :param heightmap: The heightmap to resize.
        :param target_shape: Tuple (new_width, new_height).
        :return: Resized heightmap.
        """
        zoom_factors = (
            target_shape[0] / heightmap.shape[0],
            target_shape[1] / heightmap.shape[1],
        )
        return zoom(heightmap, zoom_factors)

    def mix_terrains(self, configs, weights=None):
        """
        Generate a mixed terrain using multiple configurations.
        :param configs: List of Config objects for different terrains.
        :param weights: List of weights for blending terrains.
        """
        if weights is None:
            weights = [1 / len(configs)] * len(configs)  # Equal weights if none provided

        if not np.isclose(sum(weights), 1.0):
            raise ValueError("Weights must sum to 1.")

        # Set a common shape (use the shape of the base terrain's config)
        target_shape = (self.config.grid_width, self.config.grid_height)

        # Generate heightmaps for each config and blend them
        combined_heightmap = np.zeros(target_shape)
        for config, weight in zip(configs, weights):
            temp_terrain = Terrain(config)
            temp_terrain.generate()
            temp_terrain.normalize()
            resized_heightmap = self.resize_heightmap(temp_terrain.heightmap, target_shape)
            combined_heightmap += resized_heightmap * weight

        # Normalize the combined heightmap after blending
        min_val = np.min(combined_heightmap)
        max_val = np.max(combined_heightmap)
        if max_val > min_val:  # Avoid division by zero
            combined_heightmap = (combined_heightmap - min_val) / (max_val - min_val)

        self.heightmap = combined_heightmap
