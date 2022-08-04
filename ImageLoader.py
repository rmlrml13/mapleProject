import time
from tkinter import *

sprite_dictionary = {}


def initialize():
    start_time = time.time()
    print("Loading Image Started")

    # 유닛 애니메이션 (idle, attack, move)
    sprite_dictionary["Snail_action"] = load_unit_action_sprite("Snail", 2, 5)
    sprite_dictionary["Character_action"] = load_unit_action_sprite("Character", 2, 7)

    # idle animation
    sprite_dictionary["Snail_idle_sprites"] = sprite_dictionary["Snail_action"][0]
    sprite_dictionary["Character_idle_sprites"] = sprite_dictionary["Character_action"][0]

    # 공격 animation
    sprite_dictionary["Snail_attack_animation_sprites"] = sprite_dictionary["Snail_action"][0:5]
    sprite_dictionary["Character_attack_animation_sprites"] = sprite_dictionary["Character_action"][4:7]

    # move animation
    sprite_dictionary["Snail_move_animation_sprites"] = sprite_dictionary["Snail_action"][0:5]
    sprite_dictionary["Character_move_animation_sprites"] = sprite_dictionary["Character_action"][0:4]

    # # shooting animation
    # sprite_dictionary["Marine_shooting_animation_sprites"] = sprite_dictionary["Marine_action"][2:4]

    # 유닛 death 애니메이션
    sprite_dictionary["Snail_death"] = load_sprite_in_row("Snail_death", 9)
    sprite_dictionary["Character_death"] = load_sprite_in_row("Snail_death", 9)

    # 커서 이미지
    sprite_dictionary["cursor_normal"] = load_sprite_in_row("cursor_normal", 5)
    sprite_dictionary["cursor_ally_selectable"] = load_sprite_in_row("cursor_ally_selectable", 14)
    sprite_dictionary["cursor_neutral_selectable"] = load_sprite_in_row("cursor_neutral_selectable", 14)
    sprite_dictionary["cursor_enemy_selectable"] = load_sprite_in_row("cursor_enemy_selectable", 14)

    # 커맨드 애니메이션
    temp = load_sprite_in_row("cursor_command", 6)
    temp.append(temp[4])
    temp.append(temp[3])
    temp.append(temp[2])
    temp.append(temp[1])
    temp.append(temp[0])
    sprite_dictionary["cursor_command_animation"] = temp

    # 커서 드래그 이미지
    sprite_dictionary["cursor_drag"] = PhotoImage(file="res/cursor_drag/cursor_drag.gif")

    end_time = time.time()
    print("Loading Image Finished: " + str(end_time - start_time) + "sec")


def load_unit_action_sprite(unit_name, row, column):
    animation_sprites = []

    # 스프라이트들을 읽어서 2d list로 저장
    for j in range(column):
        temp_column = []
        for i in range(row):
            temp_column.append(
                PhotoImage(file="res/" + unit_name + "/" + unit_name + "_" + str(j) + "_" + str(i) + ".png"))

        animation_sprites.append(temp_column)

    return animation_sprites


# 한 줄 로드
def load_sprite_in_row(name, n):
    sprites_in_row = []

    for i in range(n):
        temp = PhotoImage(file="res/" + name + "/" + name + "_" + str(i) + ".png")
        sprites_in_row.append(temp)

    return sprites_in_row


def save_1d_sprite_list(name):
    sprite_list = sprite_dictionary[name]
    index = 0
    for photoimage in sprite_list:
        photoimage.write("res/" + name + "/" + name + "_" + str(index) + ".png", format='png')
        index += 1
