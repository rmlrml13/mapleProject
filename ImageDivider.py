from tkinter import *

# offset과 마진, size를 입력받아 하나의 스프라이트를 name으로 저장시키는 함수.
# 이때 배경의 경우 제거해준다.
def get_single_sprite(spritesheet, name, width, height, x_offset, y_offset, margin):

    # 가장 왼쪽 위의 픽셀 값을 읽어옴.
    temp = spritesheet.get(0,0)
    
    # 각각 background의 r, g, b 값
    br = temp[0]
    bg = temp[1]
    bb = temp[2]
    
    dst = PhotoImage()
    for x in range(width - margin[2] - margin[0]):
            i = x + x_offset + margin[0]
            for y in range(height - margin[3] - margin[1]):
                j = y + y_offset + margin[1]

                # 픽셀 추출 및 r,g,b값
                te = spritesheet.get(i,j)
                r = (te[0])
                g = (te[1])
                b = (te[2])

                # background가 아닐 경우 한 픽셀씩 dst로 옮기기
                if r!=br and g!=bg and b!=bb:
                    dst.put("#%02x%02x%02x" % ((int)(te[0]),(int)(te[1]),(int)(te[2])),(x, y))

    # 파일 쓰기
    dst.write(name,format='gif')
    return dst

# 이미지를 대칭 시킨 뒤 name으로 저장하는  함수
def inverse_x_axis(image, name):
    dst = PhotoImage()
    w = image.width()
    h = image.height()

    # 한 픽셀씩, 유효한 값을 가질 경우 옮김
    for x in range(w):
        
        # x를 대칭시킴
        ix = w-1-x
        
        for y in range(h):
            
            # 픽셀 추출 및 r,g,b값
            te = image.get(ix,y)
            r = (te[0])
            g = (te[1])
            b = (te[2])
            if r!=0 or g!=0 or b!=0:
                dst.put("#%02x%02x%02x" % ((int)(te[0]),(int)(te[1]),(int)(te[2])),(x, y))
    dst.write(name,format='gif')  
    return dst

def get_scv_sprite():
    spritesheet = PhotoImage(file = "SCV.gif")

    # 1줄 오프셋
    offsets = [2, 38, 77, 118, 158, 192, 230, 269, 306, 342]

    # 2,3줄 오프셋
    offsets2 = [2, 43, 88, 133, 177, 218, 253, 289, 327, 367]

    # y 오프셋 및 각 줄의 높이
    y_offset = 8
    height = 49-8+1
    y_offset2 = 59
    height2 = 99-59+1
    y_offset3 = 109
    height3 = 149 - 109 +1

    for i in range(9):
        x_offset = offsets[i]
        x_offset2 = offsets2[i]
        width = offsets[i+1] - offsets[i] -1
        width2 = offsets2[i+1] - offsets2[i] -1
        t = get_single_sprite(spritesheet, "res/SCV/SCV_0_"+str(i)+".gif", width, height, x_offset, y_offset, [0,0,0,0])
        t2 = get_single_sprite(spritesheet, "res/SCV/SCV_1_"+str(i)+".gif", width2, height2, x_offset2, y_offset2, [0,0,0,0])
        t3 = get_single_sprite(spritesheet, "res/SCV/SCV_2_"+str(i)+".gif", width2, height3, x_offset2, y_offset3, [0,0,0,0])
        
        # 0,8이 아닐 경우 대칭 이미지 생성
        if(i is not 0 and i is not 8):
            inverse_x_axis(t,"res/SCV/SCV_0_"+str(16-i)+".gif")
            inverse_x_axis(t2,"res/SCV/SCV_1_"+str(16-i)+".gif")
            inverse_x_axis(t3,"res/SCV/SCV_2_"+str(16-i)+".gif")
tk = Tk()
get_scv_sprite()
