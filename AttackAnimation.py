from Animation import *
import ImageLoader
from Unit import *

# 총쏘는 공격모션
class ShootingAttackAnimation:
    def __init__(self, unit_name):
        # 필요 이미지들
        attack_animation_sprites = ImageLoader.sprite_dictionary[unit_name+"_attack_animation_sprites"]
        shooting_animation_sprites = ImageLoader.sprite_dictionary[unit_name + "_shooting_animation_sprites"]

        # SingleMotion 객체
        pull_out_gun = ForwardMotion(attack_animation_sprites, 10)
        fire_once = BackwardMotion(shooting_animation_sprites, 5)
        wait = Wait(20)

        # Animation 객체
        self.pull_out_gun_once = Animation([pull_out_gun])
        self.firing = Animation([fire_once,fire_once,fire_once,wait])
        self.firing.set_notice_index(3)

    def update(self, unit):
        unit.current_animation.update(unit)
        if unit.is_animation_finished:
            # 공격 모션이 끝났고 공격 대상이 죽었으면
            # state를 Idle로 
            if unit.attack_target is None:
                unit.next_state = Unit.STATE_IDLE
                unit.idle_animation.newly_selected(unit)
                return
            unit.current_animation = self.firing
            unit.current_animation.newly_selected(unit)
        
    def newly_selected(self, unit):
        unit.current_animation = self.pull_out_gun_once
        unit.current_animation.newly_selected(unit)

# 왕복하는 모션
class FowardAndBackwardAttackAnimation:
    def __init__(self, unit_name):
        # 필요 이미지
        attack_animation_sprites = ImageLoader.sprite_dictionary[unit_name+"_attack_animation_sprites"]

        # Single Motion 객체
        attack_forward = ForwardMotion(attack_animation_sprites, 7)
        attack_backward = BackwardMotion(attack_animation_sprites[:-1], 7)
        wait = Wait(20)

        # Animation 객체
        self.attack = Animation([attack_forward, attack_backward, wait])
        self.attack.set_notice_index(1)

    def update(self, unit):
        unit.current_animation.update(unit)
        if unit.is_animation_finished:
            if unit.attack_target is None:
                unit.next_state = Unit.STATE_IDLE
                unit.idle_animation.newly_selected(unit)
                return
            unit.current_animation.newly_selected(unit)

    def newly_selected(self, unit):
        unit.current_animation = self.attack
        unit.current_animation.newly_selected(unit)

# 단순 반복 모션
class ForwardOnlyAttackAnimation:
    def __init__(self, unit_name):
        # 필요 이미지
        attack_animation_sprites = ImageLoader.sprite_dictionary[unit_name+"_attack_animation_sprites"]
        
        # SIngle Motion 객체
        attack_forward = ForwardMotion(attack_animation_sprites, 5)
        wait = Wait(15)

        # Animation 객체
        self.attack = Animation([attack_forward, wait])
        self.attack.set_notice_index(1)
        
    def update(self, unit):
        unit.current_animation.update(unit)
        if unit.is_animation_finished:
            if unit.mission is None and unit.attack_target is None:
                unit.next_state = Unit.STATE_IDLE
                unit.idle_animation.newly_selected(unit)
                return
            unit.current_animation.newly_selected(unit)

    def newly_selected(self, unit):
        unit.current_animation = self.attack
        unit.current_animation.newly_selected(unit)
