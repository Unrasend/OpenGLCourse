class Vector:
    """Simple vector class"""
    def __init__(self, x: float, y: float, z: float):
        self.x, self.y, self.z = x, y, z

    def get_list(self):
        return [self.x, self.y, self.z]
