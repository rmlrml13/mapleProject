from UnitBluePrint import *
import Effect
from IdleAnimation import *
from AttackAnimation import *
from MoveAnimation import *


class UnitBluePrintManager:
    def __init__(self, game):
        self.game = game

        # 모든 유닛들의 blueprint들을 dictionary 형태로 관리
        self.unit_blueprint_dictionary = {}

        # snail
        snail_blueprint = UnitBluePrint(
            self,
            name='Snail',
            speed=50,
            max_health=35,
            max_shield=0,
            health_bar_number=5,

            radius=10,
            attack_range=0,
            attack_power=10,
            position_offset=(0, 0),

            death_effect_offset=(0, 0),
            death_effect_remain_time=5,
            is_effect_lower=False,
            monster=True,

            idle_animation=StaticIdleAnimation("Snail"),
            attack_animation=ForwardOnlyAttackAnimation("Snail"),
            move_animation=MoveAnimation("Snail")
        )

        # snail
        orange_Mushroom_blueprint = UnitBluePrint(
            self,
            name='Orange_Mushroom',
            speed=1,
            max_health=50,
            max_shield=0,
            health_bar_number=5,

            radius=10,
            attack_range=0,
            attack_power=10,
            position_offset=(0, 0),

            death_effect_offset=(0, 0),
            death_effect_remain_time=5,
            is_effect_lower=False,
            monster=True,

            idle_animation=StaticIdleAnimation("Orange_Mushroom"),
            attack_animation=ForwardOnlyAttackAnimation("Orange_Mushroom"),
            move_animation=MoveAnimation("Orange_Mushroom")
        )

        # character
        character_blueprint = UnitBluePrint(
            self,
            name='Character',
            speed=1,
            max_health=50,
            max_shield=0,
            health_bar_number=5,

            radius=10,
            attack_range=10,
            attack_power=10,
            position_offset=(0, 0),

            death_effect_offset=(0, 0),
            death_effect_remain_time=5,
            is_effect_lower=True,
            monster=False,

            idle_animation=StaticIdleAnimation("Character"),
            attack_animation=ForwardOnlyAttackAnimation("Character"),
            move_animation=MoveAnimation("Character")
        )

    # 해당 이름의 unit_blueprit를 dictionary에서 불러와서 넘겨주는 함수
    def get_unit_blueprint(self, name):
        return self.unit_blueprint_dictionary[name]
