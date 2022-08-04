bar_width = 5
bar_height = 5
bar_y_offset = 3

class HealthBar:

    global bar_width, bar_height, bar_y_offset
    
    def __init__(self, unit):
        self.unit = unit
        
        # 최대 체력
        self.max_health = unit.unit_blueprint.max_health
        
        # 체력 바 갯수
        self.health_bar_number = unit.unit_blueprint.health_bar_number
        
        # 체력바를 저장할 배열
        # 작은 직사각형 여러개를 이어서 그리는 형태로 그릴것.
        self.health_bars = []

    # 선택시 체력바 생성
    def selected(self):
        x_offset = self.unit.x - self.health_bar_number * bar_width / 2
        dy = self.unit.unit_blueprint.radius
        is_shield = self.unit.unit_blueprint.has_shield
        
        # 실드가 있는 경우 한칸 밑에 그려야함
        y_offset = self.unit.y + dy + bar_y_offset + (bar_width if is_shield else 0)
        
        for i in range(self.health_bar_number):
            bar = None
            # 실드를 가진 경우 왼쪽 2칸은 다르게 그려야함
            if i is 0 and is_shield:
                bar = self.unit.canvas.create_polygon(x_offset, y_offset-bar_height, x_offset + bar_width, y_offset - bar_height/2,x_offset + bar_width,\
                            y_offset+bar_height, x_offset,y_offset+bar_height, outline = 'black')
            elif i is 1 and is_shield:
                bar = self.unit.canvas.create_polygon(x_offset, y_offset-bar_height/2, x_offset + bar_width, y_offset,x_offset + bar_width,\
                            y_offset+bar_height, x_offset,y_offset+bar_height, outline = 'black')
            else:
                bar = self.unit.canvas.create_rectangle(x_offset, y_offset, x_offset + bar_width, y_offset + bar_height, fill='gray')
                
            self.health_bars.append(bar)
            self.unit.canvas.tag_raise(bar,self.unit.sprite)
            x_offset += bar_width

    # disselect시 체력바 삭제
    def disselected(self):
        for bar in self.health_bars:
            self.unit.canvas.delete(bar)
        self.health_bars[:] = []

    def update(self):
        percent = self.unit.health / self.max_health

        # 체력 퍼센트 따라 색이 달라짐
        if percent < 0.25:
            color = 'red'
        elif percent < 0.5:
            color = 'yellow'
        else:
            color = '#22A315'
        
        limit = percent * self.health_bar_number
        for i in range(len(self.health_bars)):
            bar = self.health_bars[i]
            if i < limit:
                self.unit.canvas.itemconfig(bar, fill=color)
            else:
                self.unit.canvas.itemconfig(bar, fill='gray')

    # 유닛 이동 시에 체력바도 이동해야함
    def move(self, sx, sy):
        for bar in self.health_bars:
            self.unit.canvas.move(bar, sx, sy)
            
class ShieldBar:
    
    global bar_width, bar_height, bar_y_offset
    
    def __init__(self, unit):
        self.unit = unit
        self.max_shield = self.unit.unit_blueprint.max_shield
        self.shield_bar_number = self.unit.unit_blueprint.shield_bar_number
        self.shield_bars = []
        
    def selected(self):
        x_offset = self.unit.x - self.shield_bar_number * bar_width / 2
        dy = self.unit.unit_blueprint.radius
        y_offset = self.unit.y + dy + bar_y_offset
        for i in range(self.shield_bar_number):
            bar = self.unit.canvas.create_rectangle(x_offset, y_offset, x_offset+bar_width, y_offset + bar_height, fill='gray')
            self.shield_bars.append(bar)
            self.unit.canvas.tag_raise(bar,self.unit.sprite)
            x_offset += bar_width
            
    def disselected(self):
        for bar in self.shield_bars:
            self.unit.canvas.delete(bar)
        self.shield_bars[:] = []

    def update(self):
        percent = self.unit.shield / self.max_shield
        limit = percent * self.shield_bar_number
        for i in range(len(self.shield_bars)):
            bar = self.shield_bars[i]
            if i < limit:
                self.unit.canvas.itemconfig(bar, fill='#084CCB')
            else:
                self.unit.canvas.itemconfig(bar, fill='gray')
                
    def move(self, sx, sy):
        for bar in self.shield_bars:
            self.unit.canvas.move(bar, sx, sy)
