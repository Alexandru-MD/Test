import numpy as np
import matplotlib.pyplot as plt


class CityGrid:
    def __init__(self, rows, cols, obstructed_prob=0.3):
        self.rows = rows
        self.cols = cols
        self.grid = np.random.choice([0, 1], size=(rows, cols), p=[obstructed_prob, 1 - obstructed_prob])

    def display(self):
        plt.imshow(self.grid, cmap='gray', interpolation='none')
        plt.title('City Grid')
        plt.show()

    def place_tower(self, row, col, tower_range):
        for i in range(max(0, row - tower_range), min(self.rows, row + tower_range + 1)):
            for j in range(max(0, col - tower_range), min(self.cols, col + tower_range + 1)):
                self.grid[i, j] = 2  # Use 2 to represent tower coverage

    def display_with_tower(self):
        plt.imshow(self.grid, cmap='viridis', interpolation='none', vmin=0, vmax=2)
        plt.title('City Grid with Tower Coverage')
        plt.show()

    def place_towers_optimized(self, tower_range):
        towers = set()

        for i in range(self.rows):
            for j in range(self.cols):
                if self.grid[i, j] == 1:  # Non-obstructed block
                    # Check if the block is already covered by existing towers
                    covered = any(
                        abs(i - ti) <= tower_range and abs(j - tj) <= tower_range
                        for ti, tj in towers
                    )

                    if not covered:
                        self.place_tower(i, j, tower_range)
                        towers.add((i, j))

        return towers

    def display_with_paths(self, paths=None):
        cmap = plt.cm.viridis
        cmap.set_under(color='white')

        plt.imshow(self.grid, cmap='gray', interpolation='none', vmin=0, vmax=2)
        if paths:
            for path in paths:
                path_array = np.zeros_like(self.grid)
                for i, j in path:
                    path_array[i, j] = 1
                plt.imshow(path_array, cmap=cmap, interpolation='none', vmin=0.1, vmax=1)

        plt.title('City Grid with Tower Coverage and Paths')
        plt.show()


class TowerNetwork:
    def __init__(self, city_grid, tower_range):
        self.city_grid = city_grid
        self.tower_range = tower_range

    def find_reliable_path(self, start, end):
        visited = set()

        def dfs(current, path):
            if current == end:
                return path

            visited.add(current)

            neighbors = self.get_valid_neighbors(current)
            neighbors = [neighbor for neighbor in neighbors if neighbor not in visited]

            if not neighbors:
                return None  # No valid neighbors

            # Sort neighbors by reliability (fewer hops -> more reliable)
            neighbors.sort(key=lambda neighbor: len(path + [current]))

            for neighbor in neighbors:
                new_path = dfs(neighbor, path + [current])
                if new_path:
                    return new_path

            return None

        return dfs(start, [])

    def get_valid_neighbors(self, tower):
        row, col = tower
        neighbors = []

        for i in range(max(0, row - self.tower_range), min(self.city_grid.rows, row + self.tower_range + 1)):
            for j in range(max(0, col - self.tower_range), min(self.city_grid.cols, col + self.tower_range + 1)):
                if self.city_grid.grid[i, j] == 2:  # Tower coverage
                    neighbors.append((i, j))

        return neighbors


# Example usage
city = CityGrid(10, 10)
city.display()

# Example usage 2
city.place_tower(5, 5, 3)
city.display_with_tower()

# Example usage 3
towers = city.place_towers_optimized(2)
city.display_with_tower()
print("Towers placed at:", towers)

towers = city.place_towers_optimized(2)

tower_network = TowerNetwork(city, 2)
reliable_path = tower_network.find_reliable_path((0, 0), (9, 9))

city.display_with_paths([reliable_path])

print("Most reliable path:", reliable_path)
