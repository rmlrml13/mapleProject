from tkinter import *
import time
from UnitBluePrintManager import *
from UnitManager import *
from CursorManager import *
from EffectManager import *
from Unit import *
from Worker import *
import ImageLoader


class Game:
    def __init__(self):
        self.tk = Tk()
        self.tk.config(cursor="none")
        self.tk.title("Game")
        self.tk.resizable(0, 0)
        self.tk.wm_attributes("-topmost", 1)
        self.start = time.time()
        self.monster_count = 0
        self.total_monster = 0
        self.play_count = 0

        self.canvas = Canvas(self.tk, width=1000, height=800)
        self.canvas.pack()

        # 기준 이미지
        # 얘보다 밑으로 보낼껀지 위로 보낼껀지 결정

        self.background = PhotoImage(file='./map_5.png')
        self.zero_image = self.canvas.create_image(500, 400, image=self.background)
        self.command_center = None

        ImageLoader.initialize()

        self.unit_blueprint_manager = UnitBluePrintManager(self)
        self.unit_manager = UnitManager(self)
        self.cursor_manager = CursorManager(self)
        self.effect_manager = EffectManager(self)

        self.createCharacter('Character')

    def createMonster(self, name):
        monster_blueprint = self.unit_blueprint_manager.get_unit_blueprint(name)
        monster = Unit(30, 30, monster_blueprint, self)
        self.unit_manager.add_game_object(monster)

    def createCharacter(self, name):
        character_blueprint = self.unit_blueprint_manager.get_unit_blueprint(name)
        character = Unit(500, 400, character_blueprint, self)
        self.unit_manager.add_game_object(character)

    def mainLoop(self):
        frame_count = 0
        old_time = time.time()
        old_frame_time = old_time
        FPS = 60
        time_delta = 1 / FPS

        while True:

            self.unit_manager.update()
            self.cursor_manager.update()
            self.effect_manager.update()
            self.tk.update()
            current_frame_time = time.time()

            elapsed = old_time - self.start

            if 5 < elapsed:
                if self.monster_count < 5:
                    if self.play_count % 100 == 0:
                        self.createMonster('Orange_Mushroom')
                        self.monster_count += 1

            self.unit_manager.auto_game_object_select1()
            self.unit_manager.auto_game_object_select2()
            self.unit_manager.auto_game_object_select3()
            self.unit_manager.auto_game_object_select4()
            self.unit_manager.auto_attack()

            # 기대시간보다 적게 걸릴 경우
            # 기대시간만큼 걸리도록 남은 시간을 대기
            if current_frame_time - old_frame_time < time_delta:
                time.sleep(time_delta - (current_frame_time - old_frame_time))
            old_frame_time = current_frame_time
            frame_count += 1

            # 1초 지났을 경우 old_time을 바꿔주고
            # frame count즉 FPS를 출력
            if current_frame_time - old_time > 1:
                old_time = current_frame_time
                # print("FPS: ", frame_count)
                frame_count = 0
            time.sleep(0.01)
            self.play_count += 1


g = Game()
g.mainLoop()
