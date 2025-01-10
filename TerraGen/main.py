from config import Config
from terrain import Terrain
from visualization import Visualization

def main():
    # Step 1: Load multiple configurations
    desert_config = Config(preset="desert")
    forest_config = Config(preset="forest")
    ocean_config = Config(preset="ocean")
    mountain_config = Config(preset="mountains")
    plains_config = Config(preset="plains")
    arctic_config = Config(preset="arctic")

    # Step 2: Generate and mix terrains
    terrain = Terrain(mountain_config)  # Use "mountains" as the base config
    terrain.mix_terrains(
        configs=[mountain_config, plains_config, arctic_config, desert_config],
        weights=[0.4, 0.3, 0.2, 0.1]  # Adjust weights to prioritize mountains
    )
    terrain.add_random_variation(intensity=0.05)  # Add slight dynamic variability

    # Step 3: Visualize the mixed terrain with enhanced visuals
    viz = Visualization(terrain)
    print("Generating Grayscale Visualization...")
    viz.plot_grayscale()                # Grayscale heightmap
    print("Generating Colored Visualization...")
    viz.plot_colored()                  # Enhanced colored terrain
    print("Generating 3D Surface Visualization...")
    viz.plot_3d_surface()               # 3D surface visualization
    print("Generating Contour Visualization...")
    viz.plot_elevation_with_contours()  # Contour visualization

if __name__ == "__main__":
    main()
