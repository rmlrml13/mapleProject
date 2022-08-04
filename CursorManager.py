from tkinter import *
import ImageLoader
from Effect import *

class CursorManager:

    # 커서의 상태 (Finite State Machine 생각)
    CURSOR_NORMAL = 0
    CURSOR_SELECTABLE_ALLY = 1
    CURSOR_SELECTABLE_NEUTRAL = 2
    CURSOR_SELECTABLE_ENEMY = 3
    CURSOR_DRAG = 4
    
    def __init__(self, game):
        
        self.canvas = game.canvas
        self.game = game

        # 애니메이션 스프라이트를 담을 2차원 배열
        self.animation_sprites = []
        self.animation_sprites.append(ImageLoader.sprite_dictionary["cursor_normal"])
        self.animation_sprites.append(ImageLoader.sprite_dictionary["cursor_ally_selectable"])
        self.animation_sprites.append(ImageLoader.sprite_dictionary["cursor_neutral_selectable"])
        self.animation_sprites.append(ImageLoader.sprite_dictionary["cursor_enemy_selectable"])
                
        # 애니메이션 프레임 갯수 및 속도
        normal_frame_number = len(self.animation_sprites[0])
        selectable_frame_number = len(self.animation_sprites[1])
        normal_frame_speed = 10
        selectable_frame_speed = 10

        # 스프라이트 업데이트 편의를 위해 중복된 정보를 리스트로 저장함
        self.animation_frame_number = [normal_frame_number, selectable_frame_number, selectable_frame_number, selectable_frame_number]
        self.animation_speed = [normal_frame_speed, selectable_frame_speed, selectable_frame_speed, selectable_frame_speed]

        # 커서 위치
        self.cursor_x = 0
        self.cursor_y = 0

        # 실제 커서 스프라이트
        self.cursor_sprite = self.canvas.create_image(self.cursor_x, self.cursor_y, image = '')

        # 애니메이션 카운터
        self.animation_counter = 0

        # 커서의 상태
        self.state = CursorManager.CURSOR_NORMAL
        self.next_state = CursorManager.CURSOR_NORMAL

        #
        # 마우스 드래그를 위한 부분
        #

        # 드래스 스프라이트 이미지
        self.cursor_sprite_drag = ImageLoader.sprite_dictionary["cursor_drag"]

        # 좌클릭시 커서 위치 기억 (드래그 박스의 시작점)
        self.cursor_old_x = 0
        self.cursor_old_y = 0

        # 녹색 드래그 박스
        self.drag_box = None

        # 마우스 모션 바인딩해주기
        self.canvas.bind_all('<Motion>', self.mouse_move)
        self.canvas.bind_all('<Button-1>', self.mouse_left_press)
        self.canvas.bind_all('<ButtonRelease-1>', self.mouse_left_release)
        self.canvas.bind_all('<Button-3>', self.mouse_right_press)
        self.canvas.bind_all('<ButtonRelease-3>', self.mouse_right_release)
        self.canvas.bind_all('<B1-Motion>', self.mouse_left_pressed_drag)

        # 우클릭시 동그란원이 나타났다 작아지는 애니메이션
        self.command_circle_effect_blueprint = EffectBluePrint(
                animation_sprites = ImageLoader.sprite_dictionary["cursor_command_animation"],
                animation_speed = 3,
                sprite_offset = (0,0),
                last_frame_remain_time = 0,
                is_effect_lower = False
            )
    #
    # 바인딩 함수들
    #
    
    # 1. 마우스 이동
    def mouse_move(self, event :Event):
        self.canvas.move(self.cursor_sprite, event.x - self.cursor_x, event.y - self.cursor_y)
        self.cursor_x = event.x
        self.cursor_y = event.y
        
        self.update_cursor_state()
        
    # 2. 마우스 왼쪽 누를 때
    def mouse_left_press(self, event: Event):
        
        # 드래그 박스 만들기 위해 기억
        self.cursor_old_x = event.x
        self.cursor_old_y = event.y


    # 3. 마우스 왼쪽 땔 때
    def mouse_left_release(self, event: Event):
        if self.drag_box is not None:
            self.canvas.delete(self.drag_box)

        # 유닛 선택 여부 확인
        self.game.unit_manager.game_object_select(event)
        self.update_cursor_state()

    # 4. 마우스 오른쪽 누를 때
    def mouse_right_press(self, event:Event):
        self.game.unit_manager.command(event)
        
    # 5. 마우스 오른쪽 땔 때
    def mouse_right_release(self, event: Event):
        None
                     
    # 6. 마우스 왼쪽 누른 채 드래그
    def mouse_left_pressed_drag(self, event: Event):
        self.canvas.move(self.cursor_sprite, event.x - self.cursor_x, event.y - self.cursor_y)
        self.cursor_x = event.x
        self.cursor_y = event.y
        self.next_state = CursorManager.CURSOR_DRAG

        if self.drag_box is not None:
            self.canvas.delete(self.drag_box)
        self.drag_box = self.canvas.create_rectangle(self.cursor_old_x, self.cursor_old_y, \
                                    self.cursor_x, self.cursor_y, outline = 'green')                                        

    # unit manager에 커서 상태 물어보기 (유닛이 위에 있는지)
    def update_cursor_state(self):
        self.next_state = self.game.unit_manager.update_cursor_state(self.cursor_x, self.cursor_y)

    # 스프라이트 업데이트
    def update_cursor_sprite(self):
        if self.next_state is CursorManager.CURSOR_DRAG:
            self.canvas.itemconfig(self.cursor_sprite, image = self.cursor_sprite_drag)
            
        if self.state is not CursorManager.CURSOR_DRAG:
            self.canvas.itemconfig(self.cursor_sprite, image = self.animation_sprites[self.state][(self.animation_counter\
                        //self.animation_speed[self.state])%self.animation_frame_number[self.state]])

    # 업데이트 함수    
    def update(self):
        self.update_cursor_sprite()
        self.state = self.next_state
        self.animation_counter += 1
