import math

class GameObject:

    def __init__(self, x, y, r, photoimage, game):

        self.x = x
        self.y = y
        self.r = r
        
        self.game = game
        self.canvas = game.canvas

        self.selection_circle = None
        self.is_selected = False
        self.remove_flag = False

        # 초기 설정 이미지가 없는 경우
        # 그냥 리턴
        if photoimage is None:
            return

        self.sprite_height = photoimage.height()
        self.sprite_width = photoimage.width()

        self.sprite = self.canvas.create_image(x,y, image = photoimage)

        # r = -1이면 알아서 설정해줌
        if r is -1:
            self.r = math.sqrt(self.sprite_height*self.sprite_height+\
                      self.sprite_width * self.sprite_width)/2
        
        
    # 단일 선택
    def is_cursor_on_sprite(self, cursor_x, cursor_y):
        return abs(self.x - cursor_x) < self.sprite_width/2 \
               and abs(self.y - cursor_y) < self.sprite_height/2

    # 드래그 박스 위에 있는지 여부
    def is_on_drag_box(self, x, y, old_x, old_y):
        return self.x > min(x,old_x) and self.x < max(x,old_x) \
               and self.y > min(y,old_y) and self.y < max(y,old_y)

    def set_select(self):
        self.is_selected = True
        self.set_selection_circle()
        
    def set_disselect(self):
        self.is_selected = False
        self.delete_selection_circle()

    def set_selection_circle(self):
        # 이미 있다면 중복 생성막기 위해 그냥 리턴
        if self.selection_circle is not None:
            return
        
        # 타원의 두 축 의 길이
        oval_rx = self.sprite_width / 2
        oval_ry = self.sprite_width / 6

        # 타원 중심
        center_x = self.x
        center_y = self.y + oval_ry

        # 타원 만들기
        self.selection_circle = self.canvas.create_oval(center_x - oval_rx, \
                center_y - oval_ry, center_x + oval_rx, center_y + oval_ry, outline = 'green')

        # 타원보다 이미지를 앞으로 가져오기
        # 안그러면 타원이 이미지를 가리게됨.
        self.canvas.tag_lower( self.selection_circle, self.sprite)    
        
    def delete_selection_circle(self):
        if self.selection_circle is None:
            return
        self.canvas.delete(self.selection_circle)
        self.selection_circle = None
        
    def right_click_command(self, target):
        None
        
    def update(self):
        None
