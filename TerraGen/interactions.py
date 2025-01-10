from terrain import Cell

class InteractionsManager:
    def __init__(self, config):
        """
        Initialize the InteractionsManager.
        :param config: A dictionary containing interaction parameters.
        """
        self.config = config

    def simulate_erosion(self, grid):
        """
        Simulate erosion by reducing height in cells near water and transferring material downhill.
        :param grid: The hexagonal grid (dictionary of Cell objects).
        """
        erosion_rate = self.config["interaction_factors"]["erosion_rate"]
        for cell in grid.values():
            if isinstance(cell, Cell) and cell.water_level > 0 and cell.terrain_type != "ocean":  # Ocean doesn't erode
                cell.height -= erosion_rate
                cell.water_level = max(cell.water_level - erosion_rate, 0.0)
                cell.height = max(0.0, cell.height)

    def spread_vegetation(self, grid):
        """
        Spread vegetation to neighboring cells with sufficient water and suitable terrain.
        :param grid: The hexagonal grid (dictionary of Cell objects).
        """
        growth_rate = self.config["interaction_factors"]["vegetation_growth"]
        for cell_coords, cell in grid.items():
            if isinstance(cell, Cell) and cell.water_level > 0.3 and cell.terrain_type != "desert":
                # Spread vegetation to neighbors
                neighbors = self.get_neighbors(grid, *cell_coords)
                for neighbor in neighbors:
                    if neighbor.vegetation < 1.0 and neighbor.terrain_type != "desert":
                        neighbor.vegetation += growth_rate
                        neighbor.vegetation = min(1.0, neighbor.vegetation)  # Cap at 1.0

    def simulate_desertification(self, grid):
        """
        Simulate desertification by converting cells to desert if water levels are too low.
        :param grid: The hexagonal grid (dictionary of Cell objects).
        """
        desertification_rate = self.config["interaction_factors"]["desertification_rate"]
        for cell in grid.values():
            if isinstance(cell, Cell) and cell.water_level < 0.1 and cell.terrain_type != "ocean":
                # Decrease vegetation and convert to desert over time
                cell.vegetation -= desertification_rate
                cell.vegetation = max(0.0, cell.vegetation)  # Ensure vegetation is non-negative
                if cell.vegetation == 0.0:
                    cell.terrain_type = "desert"

    def apply_interactions(self, grid):
        """
        Apply all interactions to the grid.
        :param grid: The hexagonal grid (dictionary of Cell objects).
        """
        self.simulate_erosion(grid)
        self.spread_vegetation(grid)
        self.simulate_desertification(grid)

    def get_neighbors(self, grid, q, r):
        """
        Get neighboring cells for a given hexagonal cell.
        :param grid: The hexagonal grid (dictionary of Cell objects).
        :param q: Axial coordinate q of the current cell.
        :param r: Axial coordinate r of the current cell.
        :return: List of neighboring Cell objects.
        """
        directions = [
            (+1, 0), (-1, 0), (0, +1), (0, -1), (+1, -1), (-1, +1)
        ]
        neighbors = []
        for dq, dr in directions:
            neighbor_coords = (q + dq, r + dr)
            if neighbor_coords in grid:
                neighbors.append(grid[neighbor_coords])
        return neighbors
