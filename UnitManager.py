from tkinter import *
import CursorManager
from Effect import *
from Unit import *
import math


class UnitManager:
    def __init__(self, game):
        self.canvas = game.canvas
        self.game = game

        self.game_object_list = []
        self.selected_game_object_list = []

        self.cursor_x = 100
        self.cursor_y = 100

        # 좌표
        self.monster_x = 0
        self.monster_y = 0
        self.character_x = 0
        self.character_y = 0

        # 키보드 입력 연결
        self.canvas.bind_all('<KeyPress>', self.set_keypress)

    def add_game_object(self, game_object):
        self.game_object_list.append(game_object)

    def update(self):
        next_game_object_list = []
        next_selected_game_object_list = []

        for game_object in self.game_object_list:
            game_object.update()

            # 이터레이션 도중 리스트 변경 불가하기 때문에
            # 새로운 리스트를 만들어서 옮겨담음.
            if not game_object.remove_flag:
                next_game_object_list.append(game_object)

        for game_object in self.selected_game_object_list:
            if not game_object.remove_flag:
                next_selected_game_object_list.append(game_object)

        self.game_object_list = next_game_object_list
        self.selected_game_object_list = next_selected_game_object_list

    # 우클릭시 명령
    def command(self, event: Event):
        target = None
        for game_object in self.game_object_list:
            if game_object.is_cursor_on_sprite(event.x, event.y):
                target = game_object
                break

        # 대상이 있으면 공격 명령
        # 이미 선택된 대상이면 무시
        if target is not None:

            if not target.is_selected:

                # selected effect 발생
                selected_effect = SelectedCircleEffect(target)
                self.game.effect_manager.add_effect(selected_effect)

                for selected_game_object in self.selected_game_object_list:
                    selected_game_object.right_click_command(target)
            # tag_raise해줘야 커서가 제대로 보임
            self.game.canvas.tag_raise(self.game.cursor_manager.cursor_sprite, target.sprite)


        # 대상이 없으면 땅바닥을 우클릭한것
        # 이동 명령
        else:
            # 커서 애니메이션 추가
            self.game.effect_manager.add_effect(
                Effect(self.game, event.x, event.y, self.game.cursor_manager.command_circle_effect_blueprint))

            # 이동 명령
            for selected_game_object in self.selected_game_object_list:
                selected_game_object.move_command(event)

    def auto_attack(self):
        closet_emeny_unit = None
        closet_dist = 100000
        for unit in self.game_object_list:
            if unit.monster:
                self.monster_x = unit.x
                self.monster_y = unit.y
                closet_emeny_unit = unit
            else:
                self.character_x = unit.x
                self.character_y = unit.y
            dx = self.monster_x - self.character_x
            dy = self.monster_y - self.character_y
            dist = math.sqrt(dx * dx + dy * dy)


    def set_keypress(self, event: Event):
        None

    def auto_game_object_select1(self):

        # 선택되는 유닛을 저장할 임시 배열
        # 선택이 유효할 경우 (0이 아닐 경우에만) 바꿔줄거임
        next_selected_game_object_list = []

        # 드래그 박스
        x = 20
        y = 25
        old_x = 40
        old_y = 35

        # 1. 유닛들에게 그 중심이 드래그 박스 안에 들어가 있는지 물어보기
        # 최대 12기 까지 선택 가능
        for unit in self.game_object_list:
            if isinstance(unit, Unit) and unit.is_on_drag_box(x, y, old_x, old_y):
                next_selected_game_object_list.append(unit)

        if len(next_selected_game_object_list) != 0:

            # 기존 선택 유닛 disselect
            for game_object in self.selected_game_object_list:
                game_object.set_disselect()

            # 새로운 유닛들 select
            for game_object in next_selected_game_object_list:
                game_object.set_select()

                # tag_raise해줘야 커서가 제대로 보임
                self.game.canvas.tag_raise(self.game.cursor_manager.cursor_sprite, game_object.sprite)

            for selected_game_object in next_selected_game_object_list:
                selected_game_object.automove1()

    def auto_game_object_select2(self):

        # 선택되는 유닛을 저장할 임시 배열
        # 선택이 유효할 경우 (0이 아닐 경우에만) 바꿔줄거임
        next_selected_game_object_list = []

        # 드래그 박스
        x = 960
        y = 25
        old_x = 980
        old_y = 35

        # 1. 유닛들에게 그 중심이 드래그 박스 안에 들어가 있는지 물어보기
        # 최대 12기 까지 선택 가능
        for unit in self.game_object_list:
            if isinstance(unit, Unit) and unit.is_on_drag_box(x, y, old_x, old_y):
                next_selected_game_object_list.append(unit)

        if len(next_selected_game_object_list) != 0:

            # 기존 선택 유닛 disselect
            for game_object in self.selected_game_object_list:
                game_object.set_disselect()

            # 새로운 유닛들 select
            for game_object in next_selected_game_object_list:
                game_object.set_select()

                # tag_raise해줘야 커서가 제대로 보임
                self.game.canvas.tag_raise(self.game.cursor_manager.cursor_sprite, game_object.sprite)

            for selected_game_object in next_selected_game_object_list:
                selected_game_object.automove2()

    def auto_game_object_select3(self):

        # 선택되는 유닛을 저장할 임시 배열
        # 선택이 유효할 경우 (0이 아닐 경우에만) 바꿔줄거임
        next_selected_game_object_list = []

        # 드래그 박스
        x = 960
        y = 765
        old_x = 980
        old_y = 775

        # 1. 유닛들에게 그 중심이 드래그 박스 안에 들어가 있는지 물어보기
        # 최대 12기 까지 선택 가능
        for unit in self.game_object_list:
            if isinstance(unit, Unit) and unit.is_on_drag_box(x, y, old_x, old_y):
                next_selected_game_object_list.append(unit)

        if len(next_selected_game_object_list) != 0:

            # 기존 선택 유닛 disselect
            for game_object in self.selected_game_object_list:
                game_object.set_disselect()

            # 새로운 유닛들 select
            for game_object in next_selected_game_object_list:
                game_object.set_select()

                # tag_raise해줘야 커서가 제대로 보임
                self.game.canvas.tag_raise(self.game.cursor_manager.cursor_sprite, game_object.sprite)

            for selected_game_object in next_selected_game_object_list:
                selected_game_object.automove3()

    def auto_game_object_select4(self):

        # 선택되는 유닛을 저장할 임시 배열
        # 선택이 유효할 경우 (0이 아닐 경우에만) 바꿔줄거임
        next_selected_game_object_list = []

        # 드래그 박스
        x = 20
        y = 765
        old_x = 40
        old_y = 775

        # 1. 유닛들에게 그 중심이 드래그 박스 안에 들어가 있는지 물어보기
        # 최대 12기 까지 선택 가능
        for unit in self.game_object_list:
            if isinstance(unit, Unit) and unit.is_on_drag_box(x, y, old_x, old_y):
                next_selected_game_object_list.append(unit)

        if len(next_selected_game_object_list) != 0:

            # 기존 선택 유닛 disselect
            for game_object in self.selected_game_object_list:
                game_object.set_disselect()

            # 새로운 유닛들 select
            for game_object in next_selected_game_object_list:
                game_object.set_select()

                # tag_raise해줘야 커서가 제대로 보임
                self.game.canvas.tag_raise(self.game.cursor_manager.cursor_sprite, game_object.sprite)

            for selected_game_object in next_selected_game_object_list:
                selected_game_object.automove4()

    def game_object_select(self, event: Event):

        # 선택되는 유닛을 저장할 임시 배열
        # 선택이 유효할 경우 (0이 아닐 경우에만) 바꿔줄거임
        next_selected_game_object_list = []

        #
        # 선택의 유효성 검사
        #

        # 드래그 상태일 때
        if self.game.cursor_manager.state is CursorManager.CursorManager.CURSOR_DRAG:

            # 드래그 박스
            x = self.game.cursor_manager.cursor_x
            y = self.game.cursor_manager.cursor_y
            old_x = self.game.cursor_manager.cursor_old_x
            old_y = self.game.cursor_manager.cursor_old_y

            # 1. 유닛들에게 그 중심이 드래그 박스 안에 들어가 있는지 물어보기
            # 최대 12기 까지 선택 가능
            for unit in self.game_object_list:
                if isinstance(unit, Unit) and unit.is_on_drag_box(x, y, old_x, old_y):
                    next_selected_game_object_list.append(unit)
                if len(next_selected_game_object_list) >= 12:
                    break

            # 2. 범위 안에 유닛이 하나도 없는 경우
            # -> 건물 혹은 미네랄 하나 선택

            if len(next_selected_game_object_list) == 0:
                for game_object in self.game_object_list:
                    if game_object.is_on_drag_box(x, y, old_x, old_y):
                        next_selected_game_object_list.append(game_object)
                        break

        # 단순 single 선택의 경우
        else:
            for game_object in self.game_object_list:
                if game_object.is_cursor_on_sprite(event.x, event.y):
                    next_selected_game_object_list.append(game_object)
                    print("single game_object selected")

                    # 하나만 선택하고 종료
                    break

        # 하나라도 선택 된게 있으면 바꿈
        # 그렇지 않으면 아무것도 하지 않음
        if len(next_selected_game_object_list) != 0:

            # 기존 선택 유닛 disselect
            for game_object in self.selected_game_object_list:
                game_object.set_disselect()

            # 새로운 유닛들 select
            for game_object in next_selected_game_object_list:
                game_object.set_select()

                # tag_raise해줘야 커서가 제대로 보임
                self.game.canvas.tag_raise(self.game.cursor_manager.cursor_sprite, game_object.sprite)

            # 리스트 바꿔주기
            self.selected_game_object_list = next_selected_game_object_list

    # 커서의 상태를 알려주기
    def update_cursor_state(self, cursor_x, cursor_y):
        for game_object in self.game_object_list:
            if game_object.is_cursor_on_sprite(cursor_x, cursor_y):
                return CursorManager.CursorManager.CURSOR_SELECTABLE_ALLY
        return CursorManager.CursorManager.CURSOR_NORMAL
