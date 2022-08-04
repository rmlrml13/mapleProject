from tkinter import *
import math
from Effect import *
from HealthBar import *
from GameObject import *

class Unit(GameObject):

    # 유닛의 상태 (Finite State Machine)
    STATE_IDLE = 0
    STATE_ATTK = 1
    STATE_MOVE = 2
    STATE_DEAD = 3
    
    
    def __init__(self, x, y, unit_blueprint, game):
        GameObject.__init__(self, x, y, unit_blueprint.radius, None, game)
        self.sprite_height = unit_blueprint.sprite_height
        self.sprite_width = unit_blueprint.sprite_width
        self.unit_blueprint = unit_blueprint

        # 현재 위치
        self.x = x
        self.y = y

        # 현재 속도
        self.sx = 0
        self.sy = 0

        # 목표지점
        self.des_x = self.x
        self.des_y = self.y

        # 유닛 상태
        self.state = None
        self.mission = None
        self.next_state = Unit.STATE_IDLE
        self.remove_flag = False
        
        # 애니메이션을 위한 인덱스
        self.rot_index = 0
        self.last_rot_index = self.rot_index
        
        # 실제 화면상에 나타날 이미지 (오프셋 적용)
        self.sprite = self.canvas.create_image(self.x+ self.unit_blueprint.position_offset[0]\
                    ,self.y+ self.unit_blueprint.position_offset[1],image='')
        
        # 선택시 나타날 동그란 초록 원
        self.selection_circle = None

        # 선택 여부
        self.is_selected = False

        # animation
        self.idle_animation = self.unit_blueprint.idle_animation
        self.attack_animation = self.unit_blueprint.attack_animation
        self.move_animation = self.unit_blueprint.move_animation
        
        #
        # 애니메이션 관련 값들
        #
        
        self.animation_counter = 0
        self.current_frame_number = 0
        self.rotation_count = 0

        # 현재 재생중인 single motion의 종료 여부
        self.is_single_motion_finished = False

        # 현재 재생중인 애니메이션(single motion의 리스트)의 종료 여부
        self.is_animation_finished = False

        # 현재 재생중인 애니메이션
        self.current_animation = self.idle_animation.animation_with_probability_list[0][0]

        # 현재 재생중인 single motion
        self.current_single_motion = self.current_animation.single_motion_list[0]

        # 현재 재생중인 single motion의 리스트 인덱스
        self.current_single_motion_index = 0


        #
        # Attack 관련
        #

        # 공격 대상이 범위를 벗어났을 때 대기 시간
        self.attack_cool_time = 0

        # 데미지 딜링이 가능한지 여부
        self.can_attack = False

        # 공격대상 
        self.attack_target = None


        #
        # 체력 바
        #
        self.health = self.unit_blueprint.max_health        
        self.last_health = self.health
        self.health_bars = HealthBar(self)

        #
        # 실드
        #
        
        self.shield = self.unit_blueprint.max_shield
        self.last_shield = self.shield
        self.shield_bars = ShieldBar(self) if self.unit_blueprint.has_shield else None
        
        
    def set_keypress(self, event:Event):
        # 체력 -1
        if event.keysym == 'Left':
            self.health -=1

    def set_select(self):
        GameObject.set_select(self)
        self.health_bars.selected()
        self.health_bars.update()
        if self.shield_bars is not None:
            self.shield_bars.selected()
            self.shield_bars.update()

    def set_disselect(self):
        GameObject.set_disselect(self)
        self.health_bars.disselected()
        if self.shield_bars is not None:
            self.shield_bars.disselected()

    def move_command(self, target):
        self.next_state = Unit.STATE_MOVE
        self.mission = Unit.STATE_MOVE
        
        self.des_x = target.x
        self.des_y = target.y
        self.attack_target = None
        self.update_rot()
        
    def attack_command(self, target):
        self.mission = Unit.STATE_ATTK
        self.attack_target = target

    def right_click_command(self, target):
        if isinstance(target, Unit):
            self.attack_command(target)
        else:
            self.move_command(target)
        
    def update_sprite(self):
        # 죽었을 경우 삭제시킴
        if self.next_state == Unit.STATE_DEAD:
            self.canvas.delete(self.sprite)
            return
        
        # idle일 경우 idle_animation에 update sprite를 위임
        elif self.next_state == Unit.STATE_IDLE:
            if self.state is not Unit.STATE_IDLE:
                self.idle_animation.newly_selected(self)
            self.idle_animation.update(self)
            return
        
        # attk일 경우 attk_animation에 update sprite를 위임
        elif self.next_state == Unit.STATE_ATTK:
            if self.state is not Unit.STATE_ATTK:
                self.attack_animation.newly_selected(self)
            self.attack_animation.update(self)
            return

        # move일 경우 move_animation에 update sprite를 위임
        elif self.next_state == Unit.STATE_MOVE:
            if self.state is not Unit.STATE_MOVE:
                self.move_animation.newly_selected(self)
            self.move_animation.update(self)
            return

    def update_rot(self):
        # 목표 지점까지 남은 거리 및 각도
        dx = self.des_x - self.x
        dy = self.des_y - self.y
        self.theta = math.atan2(dy, dx)
        
        # 유닛이 돌아간 정도
        self.rot_index = (int)((self.theta + math.pi/10 + math.pi/self.unit_blueprint.sprite_row_number)/(math.pi/(self.unit_blueprint.sprite_row_number//2))\
                               + self.unit_blueprint.sprite_row_number)
        self.rot_index %= self.unit_blueprint.sprite_row_number
        
        
    def move(self):
        dx = self.des_x - self.x
        dy = self.des_y - self.y
        
        # 단위시간당 이동할 수 있는 거리만큼 이동 or
        # 단위시간당 이동할 수 있는 거리보다 적게 남았으면 그만큼만 이동
        # 정지 시 애니메이션 X.
        move_length = self.unit_blueprint.speed
        left_length = math.sqrt(dx*dx + dy*dy)
        if left_length < move_length:
            move_length = left_length
            self.next_state = Unit.STATE_IDLE
            if self.mission is not Unit.STATE_ATTK:
                self.mission = None

        # 이동 거리
        sx = move_length * math.cos(self.theta)
        sy = move_length * math.sin(self.theta)
        
        # 유닛 이동
        self.canvas.move(self.sprite, sx, sy)

        # 선택되었을 경우 selection_circle및 bar도 이동
        if self.is_selected:
            self.canvas.move(self.selection_circle, sx, sy)
            self.health_bars.move(sx, sy)
            if self.shield_bars is not None:
                self.shield_bars.move(sx, sy)
        
        # x, y 상태 변화
        self.x += sx
        self.y += sy

        self.sx = sx
        self.sy = sy

    def attack(self):
        self.des_x = self.attack_target.x
        self.des_y = self.attack_target.y

        dx = self.attack_target.x - self.x
        dy = self.attack_target.y - self.y
        dist = math.sqrt(dx*dx+dy*dy)

        # 1. in range
        if dist < (self.attack_target.unit_blueprint.radius + self.unit_blueprint.radius)\
           + self.unit_blueprint.attack_range * 20:
            
            self.next_state = Unit.STATE_ATTK
            self.attack_cool_time = 30
            self.update_rot()

            # 데미지 딜링이 가능할 때 공격 대상의 체력을 깎음
            # 애니메이션 상으로 결정함
            if self.can_attack:
                self.can_attack = False
                self.attack_target.get_damage(self.unit_blueprint.attack_power)

                # 바로 IDLE로 들어가지 않음
                # 일단 재생중인 공격 모션을 끝내야 하기 때문.
                if self.attack_target.health <= 0:
                    self.mission = None
                    self.attack_target = None
                    self.attack_cool_time = 0
                  
        # 2. out of range
        elif self.attack_cool_time is 0:
            self.next_state = Unit.STATE_MOVE
            self.update_rot()
            self.move()
            
        else:
            self.next_state = Unit.STATE_IDLE
            self.attack_cool_time -= 1

    def get_damage(self, damage):
        if self.shield >= damage:
            self.shield -= damage
        else:
            self.health -= (damage - self.shield)
            self.shield = 0

    def check_dead(self):
        if self.health <=0:
            self.next_state = Unit.STATE_DEAD
            self.mission = None

            if self.is_selected:
                self.set_disselect()

            # unit manager의 list에서 제거될 것이므로 remove_flag는 True
            self.remove_flag = True

            # unit_blueprint에 적혀있는 death_effect를 파라미터로 넘겨줘서 effect 객체를 만들고
            # 이를 game의 effect_manager에 추가함.
            self.game.effect_manager.add_effect(Effect(self.game, self.x,self.y, self.unit_blueprint.death_effect))
            
    def update_rot_index(self):
        
        # Unit_R 은 + 오프셋, Unit_L은 - 오프셋
        # 둘 사이에서 바뀔때 그거의 +에서 -를 뺀 값 즉, 오프셋의 2배만큼 움직여줘야함
        half = self.unit_blueprint.sprite_row_number // 2
        if (self.last_rot_index < half and self.rot_index >=half):
            self.canvas.move(self.sprite, -2 * self.unit_blueprint.position_offset[0] , -2 * self.unit_blueprint.position_offset[1])
        elif (self.last_rot_index >= half and self.rot_index <half):
            self.canvas.move(self.sprite, 2 * self.unit_blueprint.position_offset[0] , 2 * self.unit_blueprint.position_offset[1])
        self.last_rot_index = self.rot_index
            
    def update(self):
        self.check_dead()

        # state가 아닌 mission에 따라서 함수 수행
        if self.mission is Unit.STATE_ATTK:
            self.attack()
        elif self.mission is Unit.STATE_MOVE:
            self.move()
        
        self.update_sprite()
        self.update_rot_index()

        # 체력 및 실드 값이 다를때만 업데이트
        if self.is_selected:
            if self.last_health is not self.health:
                self.health_bars.update()
            if self.shield_bars is not None and self.last_shield is not self.shield:
                self.shield_bars.update()
            
            
        self.state = self.next_state
        self.last_health = self.health
        self.last_shield = self.shield
