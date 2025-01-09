# visualization.py
import matplotlib.pyplot as plt
import numpy as np

class Visualization:
    def __init__(self, terrain):
        self.terrain = terrain

    def plot_grayscale(self):
        """
        Plot the heightmap in grayscale.
        """
        if self.terrain.heightmap is not None:
            plt.imshow(self.terrain.heightmap, cmap='gray')
            plt.colorbar()
            plt.title("Grayscale Heightmap")
            plt.show()

    def plot_colored(self):
        """
        Plot the heightmap with colors for water and terrain.
        """
        if self.terrain.heightmap is not None:
            water_level = self.terrain.config.water_level
            heightmap = self.terrain.heightmap
            color_map = np.zeros((*heightmap.shape, 3))  # RGB map

            for i in range(heightmap.shape[0]):
                for j in range(heightmap.shape[1]):
                    height = heightmap[i, j]
                    if height <= water_level:  # Water
                        color_map[i, j] = [0.0, 0.0, 1.0]  # Blue for water
                    elif height <= 0.6:  # Low terrain
                        color_map[i, j] = [0.6, 0.4, 0.2]  # Brown for land
                    else:  # High terrain
                        color_map[i, j] = [0.5, 1.0, 0.5]  # Green for high terrain

            plt.imshow(color_map)
            plt.title("Colored Terrain")
            plt.show()
