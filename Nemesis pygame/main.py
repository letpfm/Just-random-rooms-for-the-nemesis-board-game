#пока что игровое поле ограничено соотношением своего размера (2632/1800) и я ещё не знаю как центровать изображение в полноэкранном режиме
#какую-то часть случаев для горизонтальных экранов я уже решил(у примеру, на моём маке начиная с разрешения экрана(2880/1800) и меньше высотой)
#мой экран 8 на 5
#было бы хорошо придумать зум
import pygame, random
#Command + Q – закрыть текущее приложение (аналог Alt + F4 в Windows)

 #- - - - - тут можно поменять разрешение
divider_of_my_screen_resolution = 1 #то на сколько поделить 2880 и 1800 для высоты и ширины окна соответсвенно
SCREEN_WIDTH = 2880 / divider_of_my_screen_resolution #1600/1.75 #1280
SCREEN_HEIGHT = 1800 / divider_of_my_screen_resolution #2560/1.75 #720
FPS = 60
#- - - - -

fifteenthPartOfH = SCREEN_HEIGHT/15;
cursor_height = SCREEN_HEIGHT/30;
roomsXY = [(259, 883), (730, 367), (660, 882), (733, 1395), (1199, 196), (1255, 556), (993, 890), (1255, 1206), (1203, 1595), (1616, 276), (1531, 882), (1617, 1486), (2070, 335), (1876, 663), (1876, 1100), (2068, 1426), (2244, 645), (2242, 1120), (2507, 355), (2525, 882), (2523, 1398)]
#примерные координаты для разрешения 2880 на 1800 пикселей(при поле 2632 на 1800 по центру)
#комнаты под индексами 0, 10 и 18-20 не имеют гексов исследования и отсеков сверху
#нумерация комнат начинается с 1
roomsXY = [((i[0] - 124) / 2632, i[1] / 1800) for i in roomsXY]
#получил список координат на основной карте размером 1 на 1

dictionary_of_an_existing_one = {}
class Interaction_obj(object):#класс двигающихся прямоугольников(картинок)
    dragging = False #по дефолту не взято
    """docstring for ClassName"""
    def __init__(self, file, h = fifteenthPartOfH, x = SCREEN_WIDTH/2, y = SCREEN_HEIGHT/2 - fifteenthPartOfH/4, stationary = False):
        self.stationary = stationary #по дефолту все подвижные 
        
        if file not in dictionary_of_an_existing_one:
            self.name = file.split('.')[0]
            self.original_img = pygame.image.load('img/' + file)
            if file.split('.')[-1] == 'png':
                self.original_img = self.original_img.convert_alpha()
            else:
                self.original_img = self.original_img.convert()

            img = self.original_img
            self.original_size = img.get_rect().size
            self.final_width = (h/self.original_size[1]*self.original_size[0], h)
            self.img = pygame.transform.scale(img, self.final_width)
            self.center = (self.final_width[0]//2, self.final_width[1]//2)
            dictionary_of_an_existing_one[file] = self
        else:
            like_me = dictionary_of_an_existing_one[file]
            self.name = like_me.name
            self.original_img = like_me.original_img
            self.original_size = like_me.original_size
            self.final_width = like_me.final_width
            self.img = like_me.img
            self.center = like_me.center
        self.r = pygame.rect.Rect(x-self.center[0], y-self.center[1], self.final_width[0], self.final_width[1])#x,y,w,h
        for n in range(len(roomsXY)):
            rx, ry = roomsXY[n]
            if n not in [0, 10]:
                coefficient_radius_of_rooms = 1.3
            else:
                coefficient_radius_of_rooms = 1.7
            if ((self.r.x - rx)**2+(self.r.y - ry)**2)**0.5 < fifteenthPartOfH * coefficient_radius_of_rooms:
                self.arrival_room = n+1
        

pygame.init()

# screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))#окнный режим
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT), pygame.FULLSCREEN)#((0, 0), pygame.FULLSCREEN)#во весь экран, но надо угадать размер экрана заранее, зато, например, на маке cmd+tab и жесты пальцами работают
#можно использовать ((SCREEN_WIDTH, SCREEN_HEIGHT), pygame.FULLSCREEN) чтоб на маке игра растянулась на весь экран, но от туда можно выбраться разве что через Command + Q – закрыть текущее приложение (аналог Alt + F4 в Windows) или [fn]+кнопка выкл.
pygame. mouse. set_visible(False)

pygame.display.set_caption("Nemesis by Egor Zyuzin")#от Зюзина Егора Алексеевича!

background_image = pygame.image.load("img/Основное поле.jpg").convert()
background_image_UP = pygame.image.load("img/Основное поле UP.png").convert_alpha()
temp = background_image.get_rect().size
w_back = SCREEN_HEIGHT/temp[1]*temp[0]#получаем итоговую ширину для фона
background_image = pygame.transform.scale(background_image, (w_back, SCREEN_HEIGHT))
background_image_UP = pygame.transform.scale(background_image_UP, (w_back, SCREEN_HEIGHT))
b_i_x = (SCREEN_WIDTH-w_back)//2 #для положения поля по центру

roomsXY = [(i[0] * w_back + b_i_x, i[1]*SCREEN_HEIGHT) for i in roomsXY]#привожу
file_persons = "персонажи/"
personsNames = ["пилотесса", "разведчица", "солдат", "механик", "капитан", "учёный"]
interactionObjArr = [Interaction_obj(file_persons + personsNames.pop(0) + ".jpg", fifteenthPartOfH, SCREEN_WIDTH / 2 + fifteenthPartOfH * i / 3) for i in range(len(personsNames))]

roomsArr = []
num_rooms_1 = [i+1 for i in range(11)]
num_rooms_2 = [i+1 for i in range(9)]
random.shuffle(num_rooms_1)
random.shuffle(num_rooms_2)
for n in range(len(roomsXY)):#расставляю вопросы жетонов исследования и комнаты
    if n not in [0, 10, 18, 19, 20]:
        i = roomsXY[n]
        interactionObjArr.append(Interaction_obj("вопрос исследования.png", fifteenthPartOfH/1.2, i[0], i[1]+fifteenthPartOfH/1.5))
        if n+1 not in [6, 7, 8, 14, 15]:
            temp = num_rooms_1.pop(0)
        else:
            temp = num_rooms_2.pop(0)
        roomsArr.append(Interaction_obj("1/"+str(temp)+".png", fifteenthPartOfH*2.55, i[0], i[1], True))#гексы локации немного больше чем прорези под них, ибо имеет место неточность

nemesis_mouse = Interaction_obj("курсор.png", cursor_height)

offset_xy = [0, 0]#начальная позиция курсора относительно левого верхнего края взятого объекта

def game_event_loop(event, l, offset_xy = offset_xy):
    for n in range(len(l)): #бегаю по всем объектам, которые могут двигаться
        i = l[n]
        if(not i.stationary):
            if event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 1:
                        if i.r.collidepoint(event.pos):
                            i.dragging = True
                            mouse_x, mouse_y = event.pos
                            offset_xy[0], offset_xy[1] = i.r.x - mouse_x, i.r.y - mouse_y
                            l.insert(0,l.pop(n))
                            break

            elif i.dragging:
                if event.type == pygame.MOUSEBUTTONUP:
                    if event.button == 1:            
                        i.dragging = False
                        for n in range(len(roomsXY)):
                            rx, ry = roomsXY[n]
                            if n not in [0, 10]:
                                coefficient_radius_of_rooms = 1.3
                            else:
                                coefficient_radius_of_rooms = 1.7
                            if (((event.pos[0] - rx)**2+(event.pos[1]- ry)**2))**0.5 < (fifteenthPartOfH * coefficient_radius_of_rooms):
                                i.arrival_room = n+1
                                break
                        i.r.x = roomsXY[i.arrival_room-1][0]-i.center[0]
                        i.r.y = roomsXY[i.arrival_room-1][1]-i.center[1]

                elif event.type == pygame.MOUSEMOTION:
                        mouse_x, mouse_y = event.pos
                        i.r.x = mouse_x + offset_xy[0]
                        i.r.y = mouse_y + offset_xy[1]
                        break


clock = pygame.time.Clock()

running = True

while running:

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        else:
            if event.type == pygame.MOUSEMOTION:#движение картинки поверх невидимой мышки
                mouse_x, mouse_y = event.pos
                nemesis_mouse.r.x = mouse_x
                nemesis_mouse.r.y = mouse_y

            game_event_loop(event, interactionObjArr)


    screen.fill((0, 0, 0,))#заполнить фон
    screen.blit(background_image, [b_i_x,0])#"нижний" фон

    for i in roomsArr:
        screen.blit(i.img, [i.r.x, i.r.y])
    
    screen.blit(background_image_UP, [b_i_x,0])#фон с прорезями под локации

    for n in range(len(roomsXY)):#временные круги чтоб я мог подумать
        i = roomsXY[n]
        temp = fifteenthPartOfH*1.3 if n not in [0, 10] else fifteenthPartOfH*1.7#есть два места где круги побольше
        pygame.draw.circle(screen, (255,0,0), i, temp, 1)

    for i in interactionObjArr[::-1]:
        screen.blit(i.img, [i.r.x, i.r.y])#отрисовка всего x чем предполагается взаимодействие

    screen.blit(nemesis_mouse.img, [nemesis_mouse.r.x, nemesis_mouse.r.y])#мышку рисую


    pygame.display.flip()


    clock.tick(FPS)


pygame.quit()