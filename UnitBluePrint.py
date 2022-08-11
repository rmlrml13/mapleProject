from tkinter import *
import time
import Unit
import Effect
import ImageLoader


class UnitBluePrint:

    def __init__(self, unit_blueprint_manager, **kwargs):
        self.name = kwargs['name']
        self.speed = kwargs['speed']
        self.max_health = kwargs['max_health']
        self.health_bar_number = kwargs['health_bar_number']

        self.max_shield = kwargs['max_shield']
        self.shield_bar_number = self.health_bar_number
        self.has_shield = self.max_shield > 0

        self.radius = kwargs['radius']
        self.attack_range = kwargs['attack_range']
        self.attack_power = kwargs['attack_power']

        # 스프라이트와 포지션 간의 오프셋
        self.position_offset = kwargs['position_offset']

        # 적인지 여부
        self.monster = kwargs['monster']

        # animation
        self.idle_animation = kwargs['idle_animation']
        self.attack_animation = kwargs['attack_animation']
        self.move_animation = kwargs['move_animation']

        # 스프라이트 시트 행갯수
        self.sprite_row_number = len(self.idle_animation.idle_animation)

        # 실제 스프라이트 크기
        self.sprite_width = self.idle_animation.idle_animation[0].width()
        self.sprite_height = self.idle_animation.idle_animation[0].height()

        # EffectBluePrint 객체 생성
        self.death_effect = Effect.EffectBluePrint(
            animation_sprites=ImageLoader.sprite_dictionary[self.name + "_death"],
            animation_speed=10,
            sprite_offset=kwargs['death_effect_offset'],
            last_frame_remain_time=kwargs['death_effect_remain_time'],
            is_effect_lower=kwargs['is_effect_lower']
        )

        # dictionary에 저장
        unit_blueprint_manager.unit_blueprint_dictionary[self.name] = self
