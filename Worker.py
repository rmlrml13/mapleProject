import math
from tkinter import *
from Mineral import *
from CommandCenter import *
from Unit import *

class Worker(Unit):
    STATE_MINE = 4

    # Specific mine mission
    MOVE_TO_MINE = 0
    MINING = 1
    MOVE_TO_RETURN_CARGO = 2
    RETURNING_CARGO = 3

    MINE_TIME = 150
    RETURN_CARGO_TIME = 10
    MINE_PER_ONCE = 8
    
    def __init__(self, x, y, unit_blueprint, game):
        Unit.__init__(self, x, y, unit_blueprint, game)

        # 채굴 대상
        self.mine_target = None

        # 미네랄 반환 커맨드 센터
        self.return_cargo_target = game.command_center

        # 미네랄을 손에 들고 있는지
        self.has_cargo = False
        self.cargo_sprite = None

        # 구체적인 mine mission
        self.mine_mission = None
    
    def mine_command(self, mineral):
        self.mine_target = mineral
        self.mission = Worker.STATE_MINE
        self.mine_mission = Worker.MOVE_TO_MINE
        self.des_x = mineral.x
        self.des_y = mineral.y
        self.update_rot()

    def return_cargo_command(self, command_center):
        self.return_cargo_target = command_center
        self.mission = Worker.STATE_MINE
        self.mine_mission = Worker.MOVE_TO_RETURN_CARGO
        self.des_x = command_center.x
        self.des_y = command_center.y
        self.update_rot()
    

    # mine_mission # 0. 미네랄 채굴 위해 이동
    
    def move_to_mine(self):
        dx = self.mine_target.x - self.x
        dy = self.mine_target.y - self.y
        dist = math.sqrt(dx*dx+dy*dy)

        # 1. in range
        if dist < (self.mine_target.r + self.r + self.unit_blueprint.attack_range):

            if self.has_cargo:
                self.return_cargo_command(self.return_cargo_target)
            
            else:
                # 채굴 모션이 공격모션과 동일함.
                self.next_state = Unit.STATE_ATTK
                self.mining_left_time = Worker.MINE_TIME
                self.mine_mission = Worker.MINING
                self.update_rot()

        # 2. out of range
        else:
            self.next_state = Unit.STATE_MOVE
            self.move()
            
    # mine_mission # 1. 미네랄 채굴 중
    
    def mine(self):
        # 아직 채굴중
        if self.mining_left_time > 0:
            self.mining_left_time -= 1

        # 채굴 완료
        elif self.mining_left_time is 0:
            self.has_cargo = True
            self.cargo_sprite = self.canvas.create_image(self.x, self.y, image = Mineral.mineral_chunk)
            self.mine_target.amount -= Worker.MINE_PER_ONCE
            self.return_cargo_command(self.return_cargo_target)
            
    # mine_mission # 2. 미네랄 반환하기 위해 이동
            
    def move_to_return_cargo(self):
        dx = self.return_cargo_target.x - self.x
        dy = self.return_cargo_target.y - self.y
        dist = math.sqrt(dx*dx+dy*dy)

        # 1. in range
        if dist < (self.return_cargo_target.r + self.r + self.unit_blueprint.attack_range):
            self.next_state = Unit.STATE_IDLE
            self.mine_mission = Worker.RETURNING_CARGO
            self.returning_cargo_left_time = Worker.RETURN_CARGO_TIME
            self.update_rot()

        # 2. out of range
        else:
            self.next_state = Unit.STATE_MOVE
            self.move()

    
    # mine_mission # 3. 미네랄 반환
    
    def return_cargo(self):
        if self.returning_cargo_left_time > 0:
            self.returning_cargo_left_time -= 1
            return
        elif self.returning_cargo_left_time is 0:
            self.has_cargo = False
            self.canvas.delete(self.cargo_sprite)
            self.cargo_sprite = None
            self.mine_mission = Worker.MOVE_TO_MINE
            
            if self.mine_target is None:
                self.mission = None
                self.state = Unit.STATE_IDLE
            else:
                self.mine_command(self.mine_target)

    def move(self):
        Unit.move(self)
        # 이부분만 추가
        if self.has_cargo:
            self.canvas.move(self.cargo_sprite, self.sx, self.sy)

    # 우클릭시 커맨드
    def right_click_command(self, target):
        if isinstance(target, Unit):
            self.attack_command(target)
        elif isinstance(target, Mineral):
            self.mine_command(target)
        elif self.has_cargo and isinstance(target, CommandCenter):
            self.return_cargo_command(target)
        else:
            self.move_command(target)
        
    def update(self):
        Unit.update(self)
        # mine_mission에 따라 다르게 움직임
        if self.mission is Worker.STATE_MINE:
            if self.mine_mission is Worker.MOVE_TO_MINE:
                self.move_to_mine()
            elif self.mine_mission is Worker.MINING:
                self.mine()
            elif self.mine_mission is Worker.MOVE_TO_RETURN_CARGO:
                self.move_to_return_cargo()
            else:
                self.return_cargo()
