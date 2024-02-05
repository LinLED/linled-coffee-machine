from enum import Enum

class CoffeeType(Enum):
    NONE = (0, "None", False, "")
    ESPRESSO = (1, "Espresso", True, "assets/coffee2.jpg")
    LONGO = (2, "Longo", True, "assets/coffee3.jpg")
    AMERICANO = (3, "Americano", True, "assets/coffee4.jpg")
    MACCHIATO = (4, "Macchiato", True, "assets/coffee3.jpg")
    LATTE = (5, "Latte", True, "assets/coffee9.jpg")
    HAZELNUT = (6, "Hazelnut coffee", True, "assets/coffee1.jpg")
    CHOCOLATE = (7, "Chocolate", True, "assets/coffee10.jpg")
    WATER = (8, "Water", False, "assets/coffee7.jpg")
    TEA = (9, "Tea", True, "assets/the.jpg")

    def __init__(self, id, label, sweet, image_path):
        self.id = id
        self.label = label
        self.sweet = sweet
        self.image_path = image_path


class Selection:
    def __init__(self, coffee_type: CoffeeType, sugar: int):
        self.coffee_type = coffee_type
        self.sugar = sugar
