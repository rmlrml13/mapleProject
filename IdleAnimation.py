from Animation import *
import ImageLoader


class ActiveIdleAnimation:
    def __init__(self, unit_name):

        # 애니메이션 스프라이트 배열
        self.idle_animation = ImageLoader.sprite_dictionary[unit_name + "_idle_sprites"]
        self.attack_animation_sprites = ImageLoader.sprite_dictionary[unit_name + "_attack_animation_sprites"]

        # 단일 모션들 (SingleMotion의 자식클래스들의 인스턴스)
        truely_idle = TruelyIdle(self.idle_animation, 50)
        pull_in_gun = BackwardMotion(self.attack_animation_sprites, 10)
        pull_out_gun = ForwardMotion(self.attack_animation_sprites, 10)

        stand_and_rotate_1 = Rotate(self.idle_animation, 10, 2, True)
        stand_and_rotate_2 = Rotate(self.idle_animation, 10, 2, False)

        pull_out_gun_and_rotate_1 = Rotate(self.attack_animation_sprites[-1], 10, 4, True)
        pull_out_gun_and_rotate_2 = Rotate(self.attack_animation_sprites[-1], 10, 4, False)
        wait = Wait(30)

        # 조합된 애니메이션들
        self.idle = Animation([truely_idle, wait])
        stand_and_rotate_1 = Animation([stand_and_rotate_1, wait, stand_and_rotate_1])
        stand_and_rotate_2 = Animation([stand_and_rotate_2, wait, stand_and_rotate_2])
        pull_out_and_in_gun = Animation([pull_out_gun, wait, pull_in_gun])
        pull_out_and_rotate_1 = Animation(
            [pull_out_gun, wait, pull_out_gun_and_rotate_1, wait, pull_out_gun_and_rotate_2, wait, pull_in_gun])
        pull_out_and_rotate_2 = Animation(
            [pull_out_gun, wait, pull_out_gun_and_rotate_2, wait, pull_out_gun_and_rotate_1, wait, pull_in_gun])

        # 확률 정보
        self.animation_with_probability_list = [
            (self.idle, 0.92),
            (stand_and_rotate_1, 0.02),
            (stand_and_rotate_2, 0.02),
            (pull_out_and_in_gun, 0.02),
            (pull_out_and_rotate_1, 0.01),
            (pull_out_and_rotate_2, 0.01)
        ]

    # 확률적으로 다음 애니메이션 리턴    
    def get_animation(self):
        temp = random.random()
        accumulated_probablity = 0
        for i in range(len(self.animation_with_probability_list)):
            probablity = self.animation_with_probability_list[i][1]
            if accumulated_probablity <= temp and temp <= accumulated_probablity + probablity:
                return self.animation_with_probability_list[i][0]
            accumulated_probablity += probablity

    # 유닛을 파라미터로 받아서 업데이트  
    def update(self, unit):
        unit.current_animation.update(unit)
        # 현재 재생중인 애니메이션 종료시 다음 애니메이션을 받아옴
        if unit.is_animation_finished:
            unit.current_animation = self.get_animation()
            unit.current_animation.newly_selected(unit)

    # 초기화 함수        
    def newly_selected(self, unit):
        unit.current_animation = self.idle
        unit.current_animation.newly_selected(unit)


class StaticIdleAnimation:
    def __init__(self, unit_name):
        self.idle_animation = ImageLoader.sprite_dictionary[unit_name + "_idle_sprites"]

        # 단일 모션들 (SingleMotion의 자식클래스들의 인스턴스)
        truely_idle = TruelyIdle(self.idle_animation, 100000)

        # 조합된 애니메이션들
        self.idle = Animation([truely_idle])

        # 확률 정보
        self.animation_with_probability_list = [
            (self.idle, 1)
        ]

    def update(self, unit):
        None

    def newly_selected(self, unit):
        unit.current_animation = self.idle
        unit.current_animation.newly_selected(unit)
