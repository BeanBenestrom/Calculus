import pygame, threading, time, sys, json
from math import *

pygame.init()


colors = {
    0 : (255, 200, 0),
    1 : (50, 50, 255),
    2 : (255, 50, 50),
    3 : (50, 255, 50),
    5 : (50, 255, 255),
    4 : (0, 0, 0)
}


# Classes ---------------------------------------------------------------------------------------------------------------------------------- #

class Camera:
    def __init__(self):
        self.pos = [cx, cy]
        self.hold = None
        self.open = False

        # Test Rotation
        self.Tmagnitude = 15
        self.Tx = None
        self.Ty = None
        self.Tradial = -45
        self.Tpos = [0, 0]


    def triangle(self, key):
        if key == pygame.K_1:
            self.Tmagnitude -= 1.1
        elif key == pygame.K_2:
            self.Tmagnitude += 1.1

        elif key == pygame.K_3:
            self.Tradial -= 0.1
        elif key == pygame.K_4:
            self.Tradial -= 0.1


        if key == pygame.K_5:
            self.Tpos[0] -= 1
        elif key == pygame.K_6:
            self.Tpos[0] += 1

        if key == pygame.K_7:
            self.Tpos[1] -= 1
        elif key == pygame.K_8:
            self.Tpos[1] += 1



    def move(self, key):
        global distance

        if key[pygame.K_w]:
            self.pos[1] += 8

        if key[pygame.K_s]:
            self.pos[1] -= 8

        if key[pygame.K_a]:
            self.pos[0] += 8

        if key[pygame.K_d]:
            self.pos[0] -= 8  # /distance*100

        # if key[pygame.K_e]:
        #     distance = distance * 1.05
        #     self.pos[0] = self.pos[0] + (self.pos[0] - cx) * 1.05
        #     self.pos[1] = self.pos[1] + (self.pos[1] - cy) * 1.05

        # if key[pygame.K_q]:
        #     distance = distance * 0.95
        #     self.pos[0] = self.pos[0] + (self.pos[0] - cx) * 0.95
        #     self.pos[1] = self.pos[1] + (self.pos[0] - cx) * 0.95

        if key[pygame.K_e]:
            distance += distance*0.1
            self.pos = [self.pos[0] + (self.pos[0]-cx)*0.1, self.pos[1] + (self.pos[1]-cy)*0.1]
            #f.parameters

        if key[pygame.K_q]:
            distance -= distance*0.1
            self.pos = [self.pos[0] - (self.pos[0]-cx)*0.1, self.pos[1] - (self.pos[1]-cy)*0.1]


class TextBox():
    def __init__(self, active, limit=10, textMiddle=False, text="", color=(0, 0, 0), textColor=(255, 255, 255), borderColor=(0, 150, 255)):
        self.pos = [0, 0]
        self.size = [0, 0]
        self.text = text
        self.limit = limit
        self.color = color
        self.textMiddle = textMiddle
        self.textColor = textColor
        self.borderColor = borderColor
        self.active = active
        self.textSize = 0
        self.borderSize = 5


    def draw(self, screen):
        if user.selectedBox == self:
            bS = self.borderSize
            pygame.draw.rect(screen, self.borderColor,(self.pos[0]-bS//2, self.pos[1]-bS//2, self.size[0]+bS, self.size[1]+bS))
        pygame.draw.rect(screen, self.color,(self.pos[0], self.pos[1], self.size[0], self.size[1]))
        base_font = pygame.font.SysFont("consolas", self.textSize, 1, 0)
        text = base_font.render(self.text, 1, self.textColor)
        if self.textMiddle:
            screen.blit(text, (self.pos[0]+self.size[0]//2-text.get_rect().width//2, self.pos[1]+self.size[1]//2-text.get_rect().height//2))
        else:
            tX, tY = text.get_rect().width, text.get_rect().height
            # print((self.size[0]-tX)/2/self.size[0])
            screen.blit(text, (self.size[0]*0.04+self.pos[0], self.pos[1]+self.size[1]//2-tY//2))


class Button():
    def __init__(self, active, text="", color=(255, 50, 50), textColor=(200, 0, 0), borderColor=(200, 0, 0)):
        self.pos = [0, 0]
        self.size = [0, 0]
        self.text = text
        self.color = color
        self.textColor = textColor
        self.borderColor = borderColor
        self.hoverOver = False
        self.active = active
        self.textSize = 0
        self.borderSize = 20


    def draw(self, screen):
        bS = self.borderSize
        borderColor = (max(0, self.borderColor[0]), max(0, self.borderColor[1]), max(0, self.borderColor[2]))
        textColor = (max(0, self.textColor[0]), max(0, self.textColor[1]), max(0, self.textColor[2]))
        pygame.draw.rect(screen, borderColor,(self.pos[0]-bS//2, self.pos[1]-bS//2, self.size[0]+bS, self.size[1]+bS))
        pygame.draw.rect(screen, self.color,(self.pos[0], self.pos[1], self.size[0], self.size[1]))
        base_font = pygame.font.SysFont("consolas", self.textSize, 1, 0)
        text = base_font.render(self.text, 1, textColor)
        # print(text.get_rect())
        screen.blit(text, (self.pos[0]+self.size[0]//2-text.get_rect().width//2, self.pos[1]+self.size[1]//2-text.get_rect().height//2))


class Text():
    def __init__(self, x, y , _w, _h, active, text="TEXT", textSize=30, textColor=(255, 255, 255)):
        self.pos = [x, y]
        self.size = [_w, _h]
        self.text = text
        self.textColor = textColor
        self.textSize = textSize
        self.base_font = pygame.font.SysFont("consolas", self.textSize, 1, 0)


    def draw(self, screen):
        text = self.base_font.render(self.text, 1, self.textColor)
        screen.blit(text, (self.pos[0]+self.size[0]//2-text.get_rect().width//2, self.pos[1]+self.size[1]//2-text.get_rect().height//2))


class Function:
    def __init__(self, color):
        self.vectors = []
        self.line = True
        self.color = color
        self.use = True
        self.math = ""

        # Dots
        self.drawDots = True
        self.dotThickness = 6

        # Lines
        self.drawLines = True
        self.lineThickness = 3

        # Other variables
        self.Usefunction = True
        self.speed = -1
        self.sizeLimit = inf
        self.centerMagnitudeLimit = inf

        # Gui variables
        self.name = "f(x)"
        self.bS = 6 # border size
        self.size = [70, 70]
        self.pos = [self.size[0]*len(Grid.functions), h-self.size[1]]
        self.objects = [] # The buttons, textboxes and sliders that can be interacted by the user


    def create_dots(self):
        global times
        self.vectors = []
        index = 0
        size = 0.5

        # print(f"{-(w/distance//2+1)} : {(w/distance/2+2)}")

        # j = 100
        # n = 2 * pi / j

        # for i in range(0, j):
        #     i = n * i
        #     x = cos(pi) * Cam.Tmagnitude + Cam.Tpos[0]
        #     y = sin(pi) * Cam.Tmagnitude + Cam.Tpos[1]

        # return None

        # x = cos(0.5 * pi) * Cam.Tmagnitude + Cam.Tpos[0]
        # y = sin(0.5 * pi) * Cam.Tmagnitude + Cam.Tpos[1]

        # self.vectors = [[0, 0], [x, y]]

        # return None

        # int add = 0.1;
        # for (int i=0; i<2*PI; i+=add*2*PI) {
        #     int value = sin(i)+2;
        #     analogWrite(slot1, value/4*255);
        # }
        

        j = 0.05
        n = 10
        self.drawDots = False

        for i in range(int(-n/j), int(n/j) + 1):
            i *= j
            try:
                # if times == 0: self.vectors.append([i, -sin(pi*pow(2*i*4, 2))*pi*2*i*4*1/5])
                if times == 1: self.vectors.append([i, cos(pi*pow(i, 2))])
                elif times == 2: self.vectors.append([i, -sin(pi*pow(i, 2))*pi*2*i])
                elif times == 3: self.vectors.append([i, cos(i)+sin(i)])
                elif times == 4: self.vectors.append([i, cos(pi*pow(i, 2))+cos(i)+sin(i)])
                
                else:
                    self.vectors.append([cos(i), sin(i)])
            except: pass
        times += 1

        return None

        line = [1.5, 0]
        if times == 0:
            self.line = True
            self.vectors.append([0, line[1]])
            self.vectors.append([10, line[0]*10+line[1]])
        else:
            self.line = False
            with open("graph5 copy 3.json") as f:
                f = json.load(f)
                for i in f:
                    if times == 1:
                        self.vectors.append([i[0], i[1]])
                    elif times == 2:
                        # print((line[0]*i[0]+line[1])-i[1])
                        self.vectors.append([i[0], pow((line[0]*i[0]+line[1])-i[1], 2)*(1/(len(f)*2))])
                if times > 2:
                    self.line = True; tries = 0; dot = 0; j = 0
                    for i in range(0, 5*10):
                        i = i/10
                        for n in f:
                            dot += (i*n[0]+j)-n[1]
                        self.vectors.append([i, dot*(1/100)])
                        # tries += 0.1
                        # for j in range(-3*10, 3*10):
                        #     j = j / 10
                        #     for n in f:
                        #         dot += (i*n[0]+j)-n[1]
                        #     self.vectors.append([tries, dot*(1/1000)])
                        #     tries += 0.01
        times += 1

        return None

        j = 0.1
        n = 1

        for i in range(-50, 50 + 1):
            try: self.vectors.append([i*j, asin(i*j)])
            except: pass
        print("------------")
        return None

        j = 100
        smoothness = 0.1

        for i in range(-j, j + 1):
            i *= smoothness
            self.vectors.append([i, pow(i, 2) + 2*i - 7])

        return None

        add = 0.01

        i = 0
        j = 0
        while i<2*pi:
            value = sin(i)
            self.vectors.append([j*0.1/2, (2*value+2)/4]) # j = i
            i += add*2*pi; j += 1

        return None

        j = 100
        n = 2 * pi / j

        for i in range(0, j + 1):
            i = n*i
            self.vectors.append([i, 2*sin(i)])

        return None

        n = 0.1

        for i in range(int(10/n + 1)):
            i = i*n
            self.vectors.append([i, pow(i, 2)])
        print()

        return None

        n = 0.1

        for i in range(int(1/n + 1)):
            i = i*n
            print(f"{int(i/n)}: {round(i * 12.6, 1)}cm - {round(pow(i, 2) * 11.2, 1)}cm || x{round(i, 3)} - y{round(pow(i, 2), 3)}")
            self.vectors.append([i, pow(i, 2)])
        print()

        return None

        j = 10
        n = 2 * pi / j

        for i in range(0, j + 1):
            i = n*i
            x = cos(i) * Cam.Tmagnitude + Cam.Tpos[0]
            y = sin(i) * Cam.Tmagnitude + Cam.Tpos[1]

            self.vectors.append([x, y])

        return None

        x = cos(Cam.Tradial) * Cam.Tmagnitude + Cam.Tpos[0]
        y = sin(Cam.Tradial) * Cam.Tmagnitude + Cam.Tpos[1]

        self.vectors = [[Cam.Tpos[0], Cam.Tpos[1]], [x, Cam.Tpos[1]], [x, y], [Cam.Tpos[0], Cam.Tpos[1]]]

        return None

        print(f"{int(-(w/distance/2+1)/size-Cam.pos[0]/distance/size)} : {int((w/distance/2+1)/size-Cam.pos[0]/distance/size)}")
        for x in range(int(-(w/distance/2+1)/size), int((w/distance/2+1)/size)):
            x *= size
            print(x)
            index += 1
            if self.sizeLimit < index > 30//size: break
            self.vectors.append([x, sin(x)*2])
        print(" - ")

        # while self.sizeLimit > index < 30//x:
        #     y =
        #     self.vectors.append()


    def f_check_click_position(self, mX, mY):
        if self.pos[0] < mX < self.pos[0] + self.size[0] and self.pos[1] < mY < self.pos[1] + self.size[1]:
            return self
        for obj in self.objects:
            if obj.pos[0] < mX < obj.pos[0] + obj.size[0] and obj.pos[1] < mY < obj.pos[1] + obj.size[1]:
                return obj
        return None


    def drawButton(self):
        pygame.draw.rect(screen, (0, 0, 0), (self.pos[0], self.pos[1], self.size[0], self.size[1]))
        pygame.draw.rect(screen, self.color, (self.pos[0]-self.bS/2, self.pos[1]-self.bS/2, self.size[0]-self.bS, self.size[1]-self.bS))
        # [Insert drawing the function sign/picture]


    def drawSettings(self):
        pygame.draw.rect(screen, (50, 50, 50), (0, 0, w//5, h))


    def drawFunc(self):
        # if True: retur
        pref = None
        for i in self.vectors:
            if self.drawDots: 
                pygame.draw.circle(screen, self.color, (int(i[0]*distance+Cam.pos[0]), int(-i[1]*distance+Cam.pos[1])), 6)
            if pref and self.line:
                try:
                    pygame.draw.line(
                        screen,
                        self.color,
                        (pref[0]*distance+Cam.pos[0], -pref[1]*distance+Cam.pos[1]),
                        (i[0]*distance+Cam.pos[0], -i[1]*distance+Cam.pos[1]),
                        3
                    )
                except: pass
            pref = i


class Grid():
    def __init__(self):
        self.functions = []


    def draw(self):
        dotX = cx//distance*2+1; dotY = cy//distance*2+1
        offset = [Cam.pos[0] % distance, Cam.pos[1] % distance]

        # Draws the X axis
        for i in range(0, int(dotY+1)):
            pygame.draw.line(screen, (100, 100, 100), (0, i*distance+offset[1]), (w, i*distance+offset[1]), 1)

        # Draws the Y axis
        for i in range(0, int(dotX+1)):
            pygame.draw.line(screen, (100, 100, 100), (i*distance+offset[0], 0), (i*distance+offset[0], h), 1)

        # print(Cam.pos)
        # print(distance)
        pygame.draw.line(screen, (255, 0, 0), (0, Cam.pos[1]), (w, Cam.pos[1]), 3)
        pygame.draw.line(screen, (0, 255, 0), (Cam.pos[0], 0), (Cam.pos[0], h), 3)
        # pygame.draw.circle(screen, (255, 255, 255), (cx, cy), 8)


# Functions -------------------------------------------------------------------------------------------------------------------------------- #
#math[-1]
def create_funtion(color):
    f = Function(color)
    f.create_dots()
    Grid.functions.append(f)


def render():
    global cx, cy
    screen.fill((255, 255, 255))

    Grid.draw()
    for i in Grid.functions:
        i.drawFunc()
    for i in Grid.functions:
        if Cam.open == i: i.drawSettings()
    for i in Grid.functions:
        i.drawButton()
    pygame.draw.line(screen, (128, 0, 128), (cx-10, cy), (cx+10, cy), 1)
    pygame.draw.line(screen, (128, 0, 128), (cx, cy-10), (cx, cy+10), 1)
    # size = (70, 70)
    # pygame.draw.rect(screen, (255, 0, 0), (-size[0]+size[0]*1, h-size[1], size[0], size[1]))
    # pygame.draw.rect(screen, (0, 255, 0), (-size[0]+size[0]*2, h-size[1], size[0], size[1]))
    pygame.display.update()


# Variables -------------------------------------------------------------------------------------------------------------------------------- #

w, h = 1200, 800; cx, cy = w//2, h//2; distance = 50; delfDistance = 50; times = 0
Grid, Cam = Grid(), Camera()
screen = pygame.display.set_mode((w, h))
clock = pygame.time.Clock()


# Run -------------------------------------------------------------------------------------------------------------------------------------- #

while True:
    clock.tick(100)
    key = pygame.key.get_pressed()
    mX, mY = pygame.mouse.get_pos()

    for event in pygame.event.get():
        if event == pygame.QUIT:
            pygame.quit()
            sys.exit()

        if event.type == pygame.MOUSEBUTTONDOWN:
            obj = None
            for i in Grid.functions:
                obj = i.f_check_click_position(mX, mY)
                if obj != None:
                    break

            if obj:
                if str(Grid.functions).find(str(obj)) != -1:
                    if Cam.open != obj: Cam.open = obj
                    else: Cam.open = None
                # Does stuff

        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_f:
                color = colors.get(times)
                create_funtion(color)

            Cam.triangle(event.key)

    if key[pygame.K_ESCAPE]:
        pygame.quit()
        sys.exit()



    Cam.move(key)
    render()