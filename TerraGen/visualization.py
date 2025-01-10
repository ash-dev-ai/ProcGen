import matplotlib.pyplot as plt
import numpy as np
from mpl_toolkits.mplot3d import Axes3D
from matplotlib.colors import LightSource


class Visualization:
    def __init__(self, terrain):
        self.terrain = terrain

    def plot_grayscale(self):
        """
        Plot the heightmap in grayscale with enhanced resolution.
        """
        if self.terrain.heightmap is not None:
            plt.figure(figsize=(12, 10), dpi=150)
            plt.imshow(self.terrain.heightmap, cmap='gray', interpolation='bilinear')
            plt.colorbar(label="Height")
            plt.title("Grayscale Heightmap", fontsize=16)
            plt.xlabel("X-axis")
            plt.ylabel("Y-axis")
            plt.grid(False)
            plt.show()

    def plot_colored(self):
        """
        Create a complex 2D colored visualization with smooth gradients.
        """
        if self.terrain.heightmap is not None:
            heightmap = self.terrain.heightmap
            water_level = self.terrain.config.water_level

            # Custom gradient map with smooth transitions
            gradient_map = np.zeros((*heightmap.shape, 3))
            for i in range(heightmap.shape[0]):
                for j in range(heightmap.shape[1]):
                    height = heightmap[i, j]
                    if height <= water_level:  # Water (blue shades)
                        gradient_map[i, j] = [0.2, 0.4, 0.8 + 0.2 * (height / water_level)]
                    elif height <= 0.6:  # Sand (yellow to brown)
                        gradient_map[i, j] = [0.9, 0.8 - 0.2 * (height / 0.6), 0.4]
                    else:  # Forested or high terrain (green to dark green)
                        gradient_map[i, j] = [0.1 + 0.2 * height, 0.8 - 0.3 * height, 0.2]

            # Render the gradient map
            plt.figure(figsize=(12, 10), dpi=150)
            plt.imshow(gradient_map, interpolation='bilinear')
            plt.title("Enhanced Colored Terrain", fontsize=16)
            plt.xlabel("X-axis")
            plt.ylabel("Y-axis")
            plt.axis('off')  # No gridlines or ticks for a cleaner look
            plt.show()

    def plot_3d_surface(self):
        """
        Render a complex 3D surface with lighting and shadows.
        """
        if self.terrain.heightmap is not None:
            heightmap = self.terrain.heightmap
            x = np.linspace(0, heightmap.shape[1], heightmap.shape[1])
            y = np.linspace(0, heightmap.shape[0], heightmap.shape[0])
            x, y = np.meshgrid(x, y)
    
            fig = plt.figure(figsize=(14, 10), dpi=150)
            ax = fig.add_subplot(111, projection='3d')
    
            # Fix: Use a colormap object
            from matplotlib import cm
            cmap = cm.get_cmap('terrain')  # Retrieve the colormap object
            ls = LightSource(azdeg=315, altdeg=45)
            rgb = ls.shade(heightmap, cmap=cmap, vert_exag=1.5, blend_mode='soft')
    
            ax.plot_surface(x, y, heightmap, rstride=1, cstride=1, facecolors=rgb, antialiased=True, shade=False)
            ax.set_title("3D Terrain Surface with Shadows", fontsize=16)
            ax.set_xlabel("X-axis")
            ax.set_ylabel("Y-axis")
            ax.set_zlabel("Height")
            plt.show()

    def plot_elevation_with_contours(self):
        """
        Create a complex 2D visualization with elevation shading and contour lines.
        """
        if self.terrain.heightmap is not None:
            heightmap = self.terrain.heightmap

            fig, ax = plt.subplots(figsize=(12, 10), dpi=150)
            ax.imshow(heightmap, cmap='terrain', interpolation='bilinear')
            ax.contour(heightmap, levels=10, colors='black', linewidths=0.5)
            ax.set_title("Elevation Map with Contour Lines", fontsize=16)
            ax.set_xlabel("X-axis")
            ax.set_ylabel("Y-axis")
            plt.colorbar(plt.cm.ScalarMappable(cmap='terrain'), ax=ax, label="Height")
            plt.show()
