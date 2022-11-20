#пока что игровое поле ограничено соотношением своего размера (2632/1800) и я ещё не знаю как центровать изображение в полноэкранном режиме
#какую-то часть случаев для горизонтальных экранов я уже решил(у примеру, на моём маке начиная с разрешения экрана(2880/1800) и меньше высотой)
#мой экран 8 на 5
#было бы хорошо придумать зум
import pygame
#Command + Q – закрыть текущее приложение (аналог Alt + F4 в Windows)

temp = 2 #то на сколько поделить 2880 и 1800 для высоты и ширины окна соответсвенно
SCREEN_WIDTH, SCREEN_HEIGHT= 2880//temp, 1800//temp#2560//1.75, 1600//1.75 #1280, 720
FPS = 60

players_height = SCREEN_HEIGHT//15;
cursor_height = SCREEN_HEIGHT//30;
roomsXY = [(259, 883), (730, 367), (660, 882), (733, 1395), (1199, 196), (1255, 556), (993, 885), (1255, 1206), (1203, 1584), (1616, 276), (1531, 882), (1617, 1486), (2070, 335), (1876, 663), (1876, 1100), (2068, 1426), (2244, 645), (2242, 1120), (2507, 355), (2525, 882), (2523, 1398)]
#примерные координаты для разрешения 2880 на 1800 пикселей(при поле 2632 на 1800 по центру)
#комнаты под индексами 0, 10 и 18-20 не имеют гексов исследования и отсеков сверху
#нумерация комнат начинается с 1
roomsXY = [((i[0] - 124) / 2632, i[1] / 1800) for i in roomsXY]
#получил список координат на основной карте размером 1 на 1

class Moving_rectangles(object):#класс двигающихся прямоугольников(картинок)
    dragging = False #по дефолту не взято
    """docstring for ClassName"""
    def __init__(self, file, h = players_height, x = SCREEN_WIDTH//2, y = SCREEN_HEIGHT//2):
        self.name = file.split('.')[0]
        img = pygame.image.load(file).convert()
        temp = img.get_rect().size
        temp = (h/temp[1]*temp[0], h)
        self.img = pygame.transform.scale(img, temp)
        self.center = (temp[0]//2, temp[1]//2)
        self.r = pygame.rect.Rect(x-self.center[0], y-self.center[1], temp[0], temp[1])#x,y,w,h
        

pygame.init()

# screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))#окнный режим
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT), pygame.FULLSCREEN)#((0, 0), pygame.FULLSCREEN)#во весь экран, но надо угадать размер экрана заранее, зато, например, на маке cmd+tab и жесты пальцами работают
#можно использовать ((SCREEN_WIDTH, SCREEN_HEIGHT), pygame.FULLSCREEN) чтоб на маке игра растянулась на весь экран, но от туда можно выбраться разве что через Command + Q – закрыть текущее приложение (аналог Alt + F4 в Windows) или [fn]+кнопка выкл.
pygame. mouse. set_visible(False)

pygame.display.set_caption("Nemesis by Egor Zyuzin")#от Зюзина Егора Алексеевича!


background_image = pygame.image.load("Основное поле.jpg").convert()
temp = background_image.get_rect().size
w_back = SCREEN_HEIGHT/temp[1]*temp[0]#получаем итоговую ширину для фона
background_image = pygame.transform.scale(background_image, (w_back, SCREEN_HEIGHT))
b_i_x = (SCREEN_WIDTH-w_back)//2 #для положения поля по центру

roomsXY = [(i[0] * w_back + b_i_x, i[1]*SCREEN_HEIGHT) for i in roomsXY]#привожу

l = [Moving_rectangles("пилотесса.jpg"), Moving_rectangles("разведчица.jpg"), Moving_rectangles("солдат.jpg"), Moving_rectangles("механик.jpg"), Moving_rectangles("капитан.jpg"), Moving_rectangles("учёный.jpg")]

# мне придётся закоментить следующий кусок кода до тех пор пока я не организую из него автоматически расскладыющееся гексы исследований и отсеков(причём мне не придётся создавать рубашки для отсеков! отсеки только показывают лицо или прячутся - больше ничего делать они не должны, а кол-во контейнеров в отсеке можно помечать кубиками, например)
# for n in range(len(roomsXY)):
#     if n not in [0, 10, 18, 19, 20]:
#         i = roomsXY[n]
#         l.append(Moving_rectangles("разведчица.jpg", players_height, i[0], i[1]))

nemesis_mouse = Moving_rectangles("курсор.png", cursor_height)

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

            for n in range(len(l)): #бегаю по всем объектам, которые могут двигаться
                i = l[n]
                r = i.r
                if event.type == pygame.MOUSEBUTTONDOWN:
                    if event.button == 1:
                            if r.collidepoint(event.pos):
                                i.dragging = True
                                mouse_x, mouse_y = event.pos
                                offset_x = r.x - mouse_x
                                offset_y = r.y - mouse_y
                                l.insert(0,l.pop(n))
                                break

                elif i.dragging:
                    if event.type == pygame.MOUSEBUTTONUP:
                        if event.button == 1:            
                            i.dragging = False
                            break

                    elif event.type == pygame.MOUSEMOTION:
                            mouse_x, mouse_y = event.pos
                            r.x = mouse_x + offset_x
                            r.y = mouse_y + offset_y
                            break

    screen.fill((0, 0, 0,))#заполнить фон
    screen.blit(background_image, [b_i_x,0])
    for i in l[::-1]:
        screen.blit(i.img, [i.r.x, i.r.y])

    screen.blit(nemesis_mouse.img, [nemesis_mouse.r.x, nemesis_mouse.r.y])


    pygame.display.flip()


    clock.tick(FPS)


pygame.quit()