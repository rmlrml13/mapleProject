import ImageLoader
from GameObject import *

class Mineral(GameObject):
    mineral_field_width = 68
    mineral_field_height = 56
    mineral_field_radius = 20
    
    mineral_chunk_width = 20
    mineral_chunk_height = 20

    mineral_chunk = None
    mineral_field_images = None

    # 초기화. ImageLoader 초기화 이후에 불려야함.
    def initialize():
        Mineral.mineral_chunk = ImageLoader.sprite_dictionary["Mineral_Chunk"]
        Mineral.mineral_field_images = ImageLoader.sprite_dictionary["Mineral"]
    
    def __init__(self, x, y, mineral_field_type, game):
        GameObject.__init__(self, x, y, Mineral.mineral_field_radius, Mineral.mineral_field_images[mineral_field_type], game)

        self.amount = 1500
        self.mineral_field_type = mineral_field_type
