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

l_adjacency_rooms = [#матрица смежности с указанием какой номер для шума имеет коридор между комнатами под индексами строк и столбцов
[0, 3, 12, 4, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
[3, 0, 0, 0, 0, 4, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
[12, 0, 0, 0, 0, 0, 34, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
[4, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
[0, 0, 0, 0, 0, 3, 0, 0, 0, 12, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
[0, 4, 0, 0, 3, 0, 1, 0, 0, 0, 2, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
[0, 0, 34, 0, 0, 1, 0, 2, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
[0, 0, 0, 1, 0, 0, 2, 0, 4, 0, 3, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
[0, 0, 0, 0, 0, 0, 0, 4, 0, 0, 0, 12, 0, 0, 0, 0, 0, 0, 0, 0, 0],
[0, 0, 0, 0, 12, 0, 0, 0, 0, 0, 0, 0, 34, 0, 0, 0, 0, 0, 0, 0, 0],
[0, 0, 0, 0, 0, 2, 0, 3, 0, 0, 0, 0, 0, 4, 1, 0, 0, 0, 0, 0, 0],
[0, 0, 0, 0, 0, 0, 0, 0, 12, 0, 0, 0, 0, 0, 0, 34, 0, 0, 0, 0, 0],
[0, 0, 0, 0, 0, 0, 0, 0, 0, 34, 0, 0, 0, 1, 0, 0, 0, 0, 2, 0, 0],
[0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 4, 0, 1, 0, 0, 0, 2, 0, 0, 0, 0],
[0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 2, 0, 3, 0, 0, 0],
[0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 34, 0, 0, 2, 0, 0, 0, 0, 0, 1],
[0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 2, 0, 0, 0, 0, 1, 34, 0],
[0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 3, 0, 0, 0, 0, 21, 4],
[0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 2, 0, 0, 0, 1, 0, 0, 0, 0],
[0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 34, 21, 0, 0, 0],
[0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 4, 0, 0, 0]]

d_connectedness_room = {
1:[2, 3, 4],
2:[1, 6],
3:[1, 7],
4:[1, 8],
5:[6, 10],
6:[2, 5, 7, 11],
7:[3, 6, 8],
8:[4, 7, 9, 11],
9:[8, 12],
10:[5, 13],
11:[6, 8, 14, 15],
12:[9, 16],
13:[10, 14, 19],
14:[11, 13, 17],
15:[11, 16, 18],
16:[12, 15, 21],
17:[14, 19, 20],
18:[15, 20, 21],
19:[13, 17],
20:[17, 18],
21:[16, 18]}

radius_small_rooms = SCREEN_HEIGHT/15*1.2
radius_big_rooms = SCREEN_HEIGHT/15*1.5
cursor_height = SCREEN_HEIGHT/30
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
    def __init__(self, file, h = SCREEN_HEIGHT/15, x = SCREEN_WIDTH/2, y = SCREEN_HEIGHT/2 - SCREEN_HEIGHT/15/4, stationary = False):
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
        self.stable_position = (self.r.x, self.r.y)
        for n in range(len(roomsXY)):
            rx, ry = roomsXY[n]
            if n not in [0, 10]:
                temp = radius_small_rooms
            else:
                temp = radius_big_rooms
            if ((self.r.x - rx)**2+(self.r.y - ry)**2)**0.5 < temp:
                self.arrival_room = n+1
        
class ClassName(object):
    """docstring for ClassName"""
    def __init__(self, arg):
        super(Interaction_obj, self).__init__()
        self.arg = arg
        

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

interactionObjArr = [Interaction_obj(file_persons + personsNames.pop(0) + ".jpg", SCREEN_HEIGHT/15, SCREEN_WIDTH / 2 + SCREEN_HEIGHT/15 * i / 3) for i in range(len(personsNames))]

roomsArr = []
num_rooms_1 = [i+1 for i in range(11)]
num_rooms_2 = [i+1 for i in range(9)]
random.shuffle(num_rooms_1)
random.shuffle(num_rooms_2)

for n in range(len(roomsXY)):#расставляю вопросы жетонов исследования и комнаты
    if n not in [0, 10, 18, 19, 20]:
        i = roomsXY[n]
        interactionObjArr.append(Interaction_obj("вопрос исследования.png", SCREEN_HEIGHT/15/1.2, i[0], i[1]+SCREEN_HEIGHT/15/1.5))
        if n+1 not in [6, 7, 8, 14, 15]:
            temp1 = "1"
            temp = num_rooms_1.pop(0)
        else:
            temp1 = "2"
            temp = num_rooms_2.pop(0)
        roomsArr.append(Interaction_obj(temp1+"/"+str(temp)+".png", SCREEN_HEIGHT/15*2.55, i[0], i[1], True))#гексы локации немного больше чем прорези под них, ибо имеет место неточность

nemesis_mouse = Interaction_obj("курсор.png", cursor_height)

offset_xy = [0, 0]#начальная позиция курсора относительно левого верхнего края взятого объекта

def game_event_loop(event, l, offset_xy = offset_xy):
    for n in range(len(l)): #бегаю по всем объектам, которые могут двигаться
        i = l[n]
        if(not i.stationary):
            if event.type == pygame.MOUSEBUTTONDOWN:#если произошел клик
                if event.button == 1:#если это была первая кнопка
                        if i.r.collidepoint(event.pos):#если клик был над рассматриваемым объектом
                            i.dragging = True#объект считается взятым
                            mouse_x, mouse_y = event.pos#координаты мыши в момент нажатия
                            i.stable_position = (i.r.x, i.r.y)
                            offset_xy[0], offset_xy[1] = i.r.x - mouse_x, i.r.y - mouse_y
                            l.insert(0,l.pop(n))
                            break

            elif i.dragging:#если считается поднятым
                if event.type == pygame.MOUSEBUTTONUP:#при отпускании кнопки мыши
                    if event.button == 1:#если отпустили первую кнопки мыши
                        i.dragging = False #больше не считается поднятым
                        is_the_final_location_acceptable = False
                        for n in d_connectedness_room[i.arrival_room] + [i.arrival_room]:
                            rx, ry = roomsXY[n-1]#ссылаюсь на x и y
                            if n-1 not in [0, 10]:#если индекс места не нулевой или десятый(1 и 11)
                                temp = radius_small_rooms#коэффициент радиуса предполагаемой локации
                            else:
                                temp = radius_big_rooms#другой коэффициент под 1 и 11 гексы на карте
                            if ((event.pos[0] - rx)**2+(event.pos[1] - ry)**2)**0.5 < (temp):#если расстояние от примерного центра искомого места меньше чем рандиус искомого места
                                i.arrival_room = n#записываю новое место прибывания
                                is_the_final_location_acceptable = True
                                break#дальнейшие проверки излишни
                        
                        if not is_the_final_location_acceptable: #если объект пытался попасть в недопуступное место
                            r = radius_small_rooms if n-1 not in [0, 10] else radius_big_rooms
                            rx, ry = roomsXY[i.arrival_room-1]
                            epx, epy = event.pos
                            x, y = epx - rx, epy - ry
                            temp = r/(x**2 + y**2)**0.5
                            i.r.x = rx-i.center[0] + x * temp#в комнату где был взят
                            i.r.y = ry-i.center[1] + y * temp

                elif event.type == pygame.MOUSEMOTION:#при движении мышкой
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

    for i in roomsArr:#пробежка по массиву с комнатами
        # if 0:#i.scouted:
            screen.blit(i.img, [i.r.x, i.r.y])
    
    screen.blit(background_image_UP, [b_i_x,0])#фон с прорезями под локации

    for n in range(len(roomsXY)):#временные круги чтоб я мог подумать
        i = roomsXY[n]
        temp = radius_small_rooms if n not in [0, 10] else radius_big_rooms#есть два места где круги побольше
        pygame.draw.circle(screen, (255,0,0), i, temp, 1)

    for i in interactionObjArr[::-1]:
        screen.blit(i.img, [i.r.x, i.r.y])#отрисовка всего c чем предполагается взаимодействие

    screen.blit(nemesis_mouse.img, [nemesis_mouse.r.x, nemesis_mouse.r.y])#мышку рисую


    pygame.display.flip()


    clock.tick(FPS)


pygame.quit()