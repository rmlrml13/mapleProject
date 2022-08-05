from Animation import *
import ImageLoader

class MoveAnimation:
    def __init__(self, unit_name):
        # 필요 이미지
        move_animation_sprites = ImageLoader.sprite_dictionary[unit_name+"_move_animation_sprites"]

        # 필요 single_motion
        self.move = ForwardMotion(move_animation_sprites, 20)

    def update(self,unit):
        self.move.update(unit)
        if unit.is_single_motion_finished:
            self.move.newly_selected(unit)

    def newly_selected(self, unit):
        self.move.newly_selected(unit)
