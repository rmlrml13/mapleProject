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

        self.canvas = Canvas(self.tk, width=1000, height=500)
        self.canvas.pack()

        # 기준 이미지
        # 얘보다 밑으로 보낼껀지 위로 보낼껀지 결정

        self.zero_image = self.canvas.create_image(0, 0, image='')
        self.command_center = None

        ImageLoader.initialize()

        self.unit_blueprint_manager = UnitBluePrintManager(self)
        self.unit_manager = UnitManager(self)
        self.cursor_manager = CursorManager(self)
        self.effect_manager = EffectManager(self)

        snail_blueprint = self.unit_blueprint_manager.get_unit_blueprint('Snail')
        character_blueprint = self.unit_blueprint_manager.get_unit_blueprint('Character')

        for i in range(2):
            snail = Unit(120, 40 + 40 * i, snail_blueprint, self)
            character = Unit(250, 40 + 40 * i, character_blueprint, self)
            self.unit_manager.add_game_object(snail)
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
                print("FPS: ", frame_count)
                frame_count = 0
            # time.sleep(0.01)


g = Game()
g.mainLoop()
