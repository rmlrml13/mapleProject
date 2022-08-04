import random


# 애니메이션 클래스
class Animation:
    def __init__(self, single_motion_list):

        # single motion_list 를 파라미터로 받음.
        # 이것을 순차적으로 재생하여 애니메이션 생성
        self.single_motion_list = single_motion_list
        self.notice_index = -1

    def set_notice_index(self, n):
        self.notice_index = n

    # unit을 파라미터로 받음.     
    def update(self, unit):
        unit.current_single_motion.update(unit)
        if unit.is_single_motion_finished:
            # 인덱스가 마지막이면 종료된것 이므로 종료 flag를 True로
            if unit.current_single_motion_index is len(self.single_motion_list) - 1:
                unit.is_animation_finished = True
                return

            # 아닐 경우 다음 single motion 재생
            else:
                unit.current_single_motion_index += 1

                # notice_index일 경우 애니메이션 상
                # 데미지 딜링일 들어갈 타이밍이라는 뜻
                if self.notice_index is unit.current_single_motion_index:
                    unit.can_attack = True
                unit.current_single_motion = self.single_motion_list[unit.current_single_motion_index]
                unit.current_single_motion.newly_selected(unit)

    # 초기화 함수            
    def newly_selected(self, unit):
        unit.is_animation_finished = False
        unit.current_single_motion = self.single_motion_list[0]
        unit.current_single_motion_index = 0
        unit.current_single_motion.newly_selected(unit)
        unit.can_attack = False


# 단일모션 클래스
class SingleMotion():
    def __init__(self, animation_speed):
        self.animation_speed = animation_speed

    def animate(self, unit):
        None

    def update(self, unit):
        if unit.animation_counter is self.animation_speed:
            unit.animation_counter = 0
            self.animate(unit)
        unit.animation_counter += 1

    def newly_selected(self, unit):
        unit.is_single_motion_finished = False
        unit.animation_counter = 0


# 단순 대기. 스프라이트 업데이트 없이 오직 대기 시간만 체크함        
class Wait(SingleMotion):
    def __init__(self, wait_time):
        self.wait_time = wait_time
        self.is_finished = False

    def update(self, unit):
        if unit.animation_counter is self.wait_time:
            unit.is_single_motion_finished = True
        unit.animation_counter += 1

    def newly_selected(self, unit):
        unit.is_single_motion_finished = False
        unit.animation_counter = 0


# 정상재생
class ForwardMotion(SingleMotion):
    def __init__(self, animation_sprites, animation_speed):
        SingleMotion.__init__(self, animation_speed)
        self.animation_sprites = animation_sprites

    def animate(self, unit):
        unit.current_frame_number += 1
        if unit.current_frame_number <= len(self.animation_sprites) - 1:
            unit.canvas.itemconfig(unit.sprite, image=self.animation_sprites[unit.current_frame_number][unit.rot_index])

        else:
            unit.is_single_motion_finished = True

    def newly_selected(self, unit):
        unit.current_frame_number = 0
        unit.animation_counter = 0
        unit.canvas.itemconfig(unit.sprite, image=self.animation_sprites[unit.current_frame_number][unit.rot_index])
        unit.is_single_motion_finished = False


# 거꾸로 재생
class BackwardMotion(SingleMotion):
    def __init__(self, animation_sprites, animation_speed):
        SingleMotion.__init__(self, animation_speed)
        self.animation_sprites = animation_sprites

    def animate(self, unit):
        unit.current_frame_number -= 1
        if unit.current_frame_number >= 0:
            unit.canvas.itemconfig(unit.sprite, image=self.animation_sprites[unit.current_frame_number][unit.rot_index])

        else:
            unit.is_single_motion_finished = True

    def newly_selected(self, unit):
        unit.current_frame_number = len(self.animation_sprites) - 1
        unit.animation_counter = 0
        unit.canvas.itemconfig(unit.sprite, image=self.animation_sprites[unit.current_frame_number][unit.rot_index])
        unit.is_single_motion_finished = False


# 돌기
class Rotate(SingleMotion):
    def __init__(self, rotation_animation, animation_speed, maximum_rotation, is_clockwise):
        SingleMotion.__init__(self, animation_speed)
        self.rotation_animation = rotation_animation
        self.maximum_rotation = maximum_rotation
        self.is_clockwise = is_clockwise

    def rotate(self, unit):
        unit.rotation_count += 1
        unit.rot_index += (1 if self.is_clockwise else -1)
        unit.rot_index += unit.unit_blueprint.sprite_row_number
        unit.rot_index %= unit.unit_blueprint.sprite_row_number

    def animate(self, unit):
        self.rotate(unit)
        unit.canvas.itemconfig(unit.sprite, image=self.rotation_animation[unit.rot_index])
        # 최대 회전 횟수만큼만 돌기
        if unit.rotation_count is self.maximum_rotation:
            unit.is_single_motion_finished = True
            return

    def newly_selected(self, unit):
        unit.is_single_motion_finished = False
        unit.canvas.itemconfig(unit.sprite, image=self.rotation_animation[unit.rot_index])
        unit.animation_counter = 0
        unit.rotation_count = 0


# 진짜 Idle상태
class TruelyIdle(SingleMotion):
    def __init__(self, idle_animation, animation_speed):
        SingleMotion.__init__(self, animation_speed)
        self.idle_animation = idle_animation
        self.is_finished = False

    def animate(self, unit):
        unit.is_single_motion_finished = True

    def newly_selected(self, unit):
        unit.is_single_motion_finished = False
        unit.animation_counter = 0
        unit.canvas.itemconfig(unit.sprite, image=self.idle_animation[unit.rot_index])
