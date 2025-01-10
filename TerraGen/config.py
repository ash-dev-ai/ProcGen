import json

class Config:
    def __init__(self, preset="default", config_file="config_presets.json"):
        self.preset = preset
        self.config_file = config_file
        self.grid_width = 100
        self.grid_height = 100
        self.scale = 20.0
        self.water_level = 0.4
        self.octaves = 6
        self.persistence = 0.5
        self.lacunarity = 2.0
        self.terrain_type = "default"  # Default terrain type
        self.load_preset(preset)

    def load_preset(self, preset):
        try:
            with open(self.config_file, "r") as file:
                presets = json.load(file)
                if preset in presets:
                    for key, value in presets[preset].items():
                        setattr(self, key, value)
                else:
                    print(f"Preset '{preset}' not found. Loading default configuration.")
                    self.load_preset("default")
        except FileNotFoundError:
            print(f"Configuration file '{self.config_file}' not found. Using default values.")
