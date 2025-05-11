class Location:
    x: float = 0.0
    y: float = 0.0

    @classmethod
    def set(cls, x_modified, y_modified):
        cls.x = x_modified
        cls.y = y_modified

    @classmethod
    def get(cls):
        return cls.x, cls.y


class PhysicalLocation(Location):
    pass


class VirtualLocation(Location):
    pass
