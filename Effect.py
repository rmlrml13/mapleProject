from tkinter import *


class EffectBluePrint:
    def __init__(self, **kwargs):
        self.animation_sprites = kwargs['animation_sprites']
        self.animation_frame_number = len(self.animation_sprites)
        self.animation_speed = kwargs['animation_speed']

        # 죽는 모션 오프셋
        # 질럿의 경우 이 값이 0,0 이 아님.
        self.sprite_offset = kwargs['sprite_offset']

        # 마지막 프레임 잔류 시간.
        # (여기에 animation_speed를 곱한 만큼 기다림)
        self.last_frame_remain_time = kwargs['last_frame_remain_time']

        # 이팩트가  밑으로 갈껀지
        self.is_effect_lower = kwargs['is_effect_lower']


class Effect:

    def __init__(self, game, x, y, effect_blueprint: EffectBluePrint):
        self.canvas = game.canvas
        self.effect_blueprint = effect_blueprint

        # 오프셋 적용
        self.sprite = self.canvas.create_image(x + self.effect_blueprint.sprite_offset[0],
                                               y + self.effect_blueprint.sprite_offset[1],
                                               image=self.effect_blueprint.animation_sprites[0])

        # 밑에 깔리는지 위에 뜨는지 여부
        if self.effect_blueprint.is_effect_lower:
            self.canvas.tag_lower(self.sprite, game.zero_image)

        # 애니메이션 위한 값들
        self.animation_counter = 0
        self.current_frame_number = 0

        self.remove_flag = False
        self.is_last_frame = False

    def update(self):

        # last frame인지 아닌지 여부.
        # last frame일 경우 last_frame_remain_time * animation_speed만큼 더 기다린다.

        if self.is_last_frame:
            if self.animation_counter >= self.effect_blueprint.last_frame_remain_time * self.effect_blueprint.animation_speed:
                self.remove_flag = True
                self.canvas.delete(self.sprite)

        # 그외의 경우는 animation_speed로 애니메이션 재생
        elif self.animation_counter >= self.effect_blueprint.animation_speed:
            self.current_frame_number += 1
            self.animation_counter = 0

            if self.current_frame_number == self.effect_blueprint.animation_frame_number:
                self.is_last_frame = True
                return

            self.canvas.itemconfig(self.sprite,
                                   image=self.effect_blueprint.animation_sprites[self.current_frame_number])

        self.animation_counter += 1


# 우클릭으로 선택시 깜박거리는 이팩트
class SelectedCircleEffect:
    def __init__(self, unit):
        self.count = 0
        self.animation_speed = 20
        self.animation_counter = 0
        self.unit = unit
        self.unit.set_selection_circle()
        self.remove_flag = False

    def update(self):
        # 중간에 다시 선택될 경우 애니메이션 취소 
        if self.unit.is_selected:
            self.unit.set_selection_circle()
            self.remove_flag = True
            return

        # 총 2번 깜박거림
        if self.animation_counter is self.animation_speed:
            self.unit.delete_selection_circle()
        elif self.animation_counter is self.animation_speed * 2:
            self.unit.set_selection_circle()
        elif self.animation_counter is self.animation_speed * 3:
            self.unit.delete_selection_circle()
            self.remove_flag = True
        self.animation_counter += 1
