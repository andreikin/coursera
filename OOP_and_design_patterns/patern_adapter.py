
class Light:
    def __init__(self, dim):  # подаются размеры поля
        self.dim = dim
        self.grid = [[0 for i in range(dim[0])] for _ in range(dim[1])]
        self.lights = []
        self.obstacles = []

    def set_dim(self, dim):
        self.dim = dim
        self.grid = [[0 for i in range(dim[0])] for _ in range(dim[1])]

    def set_lights(self, lights): # рассчитывает освещенность по массиву источников света
        self.lights = lights
        self.generate_lights()

    def set_obstacles(self, obstacles): # рассчитывает освещенность по массиву препятствий
        self.obstacles = obstacles
        self.generate_lights()

    def generate_lights(self):
        return self.grid.copy()


class System:
    def __init__(self):
        self.map = self.grid = [[0 for i in range(30)] for _ in range(20)]
        self.map[5][7] = 1  # Источники света
        self.map[5][2] = -1  # Стены

    def get_lightening(self, light_mapper):  # запуск метода lighten обьекта light_mapper
        self.lightmap = light_mapper.lighten(self.map)


class MappingAdapter:
    def __init__(self, adaptee):
        self.adaptee = adaptee
        self.lights = list()
        self.obstacles = list()
        self.dim = [0, 0]

    def lighten(self, grid):
        self.dim = [len(grid[0]), len(grid)]

        for i in range(self.dim[0]):
            for j in range(self.dim[1]):
                if grid[j][i] > 0:
                    self.lights.append((i, j))
                elif grid[j][i] < 0:
                    self.obstacles.append((i, j))
        self.adaptee.set_dim(self.dim)
        self.adaptee.set_lights(self.lights)
        self.adaptee.set_obstacles(self.obstacles)
        return self.adaptee.generate_lights()
