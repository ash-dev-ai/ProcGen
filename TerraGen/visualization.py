import matplotlib.pyplot as plt
import numpy as np
from matplotlib.patches import RegularPolygon
from mpl_toolkits.mplot3d import Axes3D
from matplotlib.colors import LightSource


class Visualization:
    def __init__(self, terrain):
        self.terrain = terrain

    def plot_hex_grid(self):
        """
        Plot the hexagonal grid with colored terrain regions.
        """
        if self.terrain.grid:
            fig, ax = plt.subplots(figsize=(12, 10))
            for (q, r), cell in self.terrain.grid.items():
                x, y = self.hex_to_cartesian(q, r)
                color = self.get_color_for_terrain(cell.terrain_type)

                # Draw hexagonal cells
                hexagon = RegularPolygon(
                    (x, y),
                    numVertices=6,
                    radius=0.5,
                    orientation=np.radians(30),
                    facecolor=color,
                    edgecolor='black',
                )
                ax.add_patch(hexagon)

            ax.set_xlim(-self.terrain.config.grid_width, self.terrain.config.grid_width)
            ax.set_ylim(-self.terrain.config.grid_width, self.terrain.config.grid_width)
            ax.set_aspect('equal')
            plt.title("Hexagonal Terrain Visualization", fontsize=16)
            plt.xlabel("X-axis")
            plt.ylabel("Y-axis")
            plt.grid(False)
            plt.show()

    def get_color_for_terrain(self, terrain_type):
        """
        Get color for the given terrain type.
        :param terrain_type: Type of terrain (e.g., desert, forest).
        :return: Color for the terrain.
        """
        color_map = {
            "desert": "#E3C16F",
            "forest": "#228B22",
            "mountains": "#8B8B83",
            "plains": "#ADDF84",
            "arctic": "#B3E5FC",
            "ocean": "#1E88E5",
        }
        return color_map.get(terrain_type, "#FFFFFF")

    def plot_grayscale(self):
        """
        Plot the heightmap in grayscale.
        """
        if self.terrain.grid:
            heightmap = self.get_heightmap()
            plt.figure(figsize=(12, 10), dpi=150)
            plt.imshow(heightmap, cmap='gray', interpolation='nearest', aspect='equal')
            plt.colorbar(label="Height")
            plt.title("Grayscale Heightmap", fontsize=16)
            plt.xlabel("X-axis")
            plt.ylabel("Y-axis")
            plt.grid(False)
            plt.show()

    def plot_colored(self):
        """
        Create a complex 2D colored visualization with regional distinctions.
        """
        if self.terrain.grid:
            heightmap = self.get_heightmap()
            gradient_map = np.zeros((*heightmap.shape, 3))
            for (q, r), cell in self.terrain.grid.items():
                x, y = self.hex_to_cartesian(q, r)
                gradient_map[int(y) % gradient_map.shape[0]][int(x) % gradient_map.shape[1]] = self.get_rgb_for_terrain(cell.terrain_type)

            plt.figure(figsize=(12, 10), dpi=150)
            plt.imshow(gradient_map, interpolation='nearest', aspect='equal')
            plt.title("Regional Colored Terrain", fontsize=16)
            plt.xlabel("X-axis")
            plt.ylabel("Y-axis")
            plt.axis('off')
            plt.show()

    def get_rgb_for_terrain(self, terrain_type):
        """
        Get RGB color for the given terrain type.
        :param terrain_type: Type of terrain (e.g., desert, forest).
        :return: RGB tuple for the terrain.
        """
        color_map = {
            "desert": [227/255, 193/255, 111/255],
            "forest": [34/255, 139/255, 34/255],
            "mountains": [139/255, 139/255, 131/255],
            "plains": [173/255, 223/255, 132/255],
            "arctic": [179/255, 229/255, 252/255],
            "ocean": [30/255, 136/255, 229/255],
        }
        return color_map.get(terrain_type, [1.0, 1.0, 1.0])

    def plot_3d_surface(self):
        """
        Render a complex 3D surface with lighting and shadows.
        """
        if self.terrain.grid:
            heightmap = self.get_heightmap()
            x = np.linspace(0, heightmap.shape[1], heightmap.shape[1])
            y = np.linspace(0, heightmap.shape[0], heightmap.shape[0])
            x, y = np.meshgrid(x, y)

            fig = plt.figure(figsize=(14, 10), dpi=150)
            ax = fig.add_subplot(111, projection='3d')

            cmap = plt.get_cmap('terrain')  # Colormap for terrain
            ls = LightSource(azdeg=315, altdeg=45)
            rgb = ls.shade(heightmap, cmap=cmap, vert_exag=2.0, blend_mode='soft')

            ax.plot_surface(x, y, heightmap, rstride=1, cstride=1, facecolors=rgb, antialiased=True, shade=False)
            ax.set_title("3D Terrain Surface with Shadows", fontsize=16)
            ax.set_xlabel("X-axis")
            ax.set_ylabel("Y-axis")
            ax.set_zlabel("Height")
            plt.show()

    def get_heightmap(self):
        """
        Extract the heightmap from the grid.
        :return: 2D numpy array of heights.
        """
        grid_width = self.terrain.config.grid_width
        heightmap = np.zeros((grid_width, grid_width))
        for (q, r), cell in self.terrain.grid.items():
            x, y = self.hex_to_cartesian(q, r)
            heightmap[int(y) % grid_width][int(x) % grid_width] = cell.height
        return heightmap

    def hex_to_cartesian(self, q, r):
        """
        Convert hexagonal coordinates to Cartesian coordinates for visualization.
        :param q: Axial q-coordinate.
        :param r: Axial r-coordinate.
        :return: Tuple of Cartesian x, y coordinates.
        """
        x = 3 / 2 * q
        y = np.sqrt(3) * (r + q / 2)
        return x, y

    def plot_weather_overlay(self, weather):
        """
        Plot the terrain with a weather overlay.
        :param weather: A dictionary containing weather information (e.g., rain, snow).
        """
        if self.terrain.grid:
            heightmap = self.get_heightmap()
            plt.figure(figsize=(12, 10), dpi=150)
            plt.imshow(heightmap, cmap='terrain', interpolation='nearest', aspect='equal')

            # Add weather overlays
            if weather.get("rain_intensity", 0) > 0.5:
                plt.imshow(np.random.random(heightmap.shape), cmap="Blues", alpha=0.3)
                plt.title("Rain Overlay", fontsize=16)

            if weather.get("snow_intensity", 0) > 0.5:
                plt.imshow(np.random.random(heightmap.shape), cmap="cool", alpha=0.3)
                plt.title("Snow Overlay", fontsize=16)

            plt.xlabel("X-axis")
            plt.ylabel("Y-axis")
            plt.colorbar(label="Height")
            plt.show()

    def plot_event_effects(self, event_type):
        """
        Plot the terrain with visual markers for an event's effects.
        :param event_type: The type of event (e.g., "earthquake", "flood").
        """
        if self.terrain.grid:
            heightmap = self.get_heightmap()
            plt.figure(figsize=(12, 10), dpi=150)
            plt.imshow(heightmap, cmap='terrain', interpolation='nearest', aspect='equal')
            plt.title(f"Event Effect: {event_type.capitalize()}", fontsize=16)

            if event_type == "earthquake":
                plt.imshow(np.random.random(heightmap.shape), cmap="Reds", alpha=0.3)
            elif event_type == "flood":
                plt.imshow(np.random.random(heightmap.shape), cmap="Blues", alpha=0.3)
            elif event_type == "wildfire":
                plt.imshow(np.random.random(heightmap.shape), cmap="Oranges", alpha=0.3)

            plt.xlabel("X-axis")
            plt.ylabel("Y-axis")
            plt.colorbar(label="Height")
            plt.show()
