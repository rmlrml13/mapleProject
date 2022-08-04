import ImageLoader
from GameObject import *

class CommandCenter(GameObject):
    command_center_sprite = None
    
    # 초기화. ImageLoader 초기화 이후에 불려야함.
    def initialize():
        CommandCenter.command_center_sprite = ImageLoader.sprite_dictionary["Command_Center"]

    def __init__(self, x, y, game):
        GameObject.__init__(self, x, y, -1, CommandCenter.command_center_sprite, game)
