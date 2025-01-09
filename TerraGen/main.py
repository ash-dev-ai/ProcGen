from config import Config
from terrain import Terrain
from visualization import Visualization

def main():
    # Step 1: Load multiple configurations
    desert_config = Config(preset="desert")
    forest_config = Config(preset="forest")
    ocean_config = Config(preset="ocean")

    # Step 2: Generate and mix terrains
    terrain = Terrain(desert_config)  # Use any base config
    terrain.mix_terrains(
        configs=[desert_config, forest_config, ocean_config],
        weights=[0.4, 0.3, 0.3]  # Example weights
    )
    terrain.add_random_variation(intensity=0.1)  # Add more dynamic variability

    # Step 3: Visualize the mixed terrain
    viz = Visualization(terrain)
    viz.plot_grayscale()
    viz.plot_colored()

if __name__ == "__main__":
    main()
