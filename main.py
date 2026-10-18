import pygame as pg
import random
from character import Caracter
from star import Star
from wheel import Wheel

screen = pg.display.set_mode([1920,1080])
running = True

pg.mixer.init()
pg.init()

fps = 770
clock = pg.time.Clock()


rect = pg.Rect(0,0,100,150)
#direction = "right"
screen.fill(pg.Color(231,173,199))
road = pg.image.load("background.jpg")
road = pg.transform.scale(road,(1920,1080))
cat = Caracter(y=455,x=170)
star = Star()
pg.mixer.music.load("assets/music/music.mp3")
pg.mixer.music.set_volume(0.05)
pg.mixer.music.play()

stars = pg.sprite.Group()
stars.add(Star())
stars.add(Star())
stars.add(Star())
stars.add(Star())

wheels = pg.sprite.Group()


score = 0
cnt = 0
loose = False
state = "menu"
pause = False
sound_value = 0.05
selected_index = 0
expanded = False
options = ["920,1080", "1440,1080", "1920,1080"]
TIME_EVENT = pg.USEREVENT+1
CREATE_WHEELS = pg.USEREVENT+2
pg.time.set_timer(TIME_EVENT,1000)
pg.time.set_timer(CREATE_WHEELS,3000)


header_font = pg.font.SysFont('Comic Sans MS', 64)
text_font = pg.font.SysFont('Comic Sans MS', 46)
loose_text = header_font.render('Game Over', False, (230,0,38))
name_game = header_font.render('Bear jumps', False, (0, 0, 255))
play_button = header_font.render('Play', False, (75, 0, 130))
play_rect = play_button.get_rect(center=(960,445))
music_lvl = header_font.render('Music: ', False, (75, 0, 130))
music_rect = music_lvl.get_rect(center=(360,245))
menu_button = header_font.render('Menu', False, (75, 0, 130))
menu_rect = menu_button.get_rect(center=(960,445))
settings_button = header_font.render('Settings', False, (75, 0, 130))
settings_rect = settings_button.get_rect(center=(960,545))
back_to_menu_button = header_font.render('Back to menu', False, (75, 0, 130))
back_to_menu_rect = back_to_menu_button.get_rect(center=(310,990))
play_button_color = (0, 128, 128)
settings_button_color = (0, 128, 128)
menu_button_color = (0, 128, 128)
back_to_menu_color = (0, 128, 128)
sound_click = pg.mixer.Sound("assets/music/click.mp3")
sound_click.set_volume(0.4)


def draw_slider(screen, pos, width, value, handle_radius=10, track_color=(100,100,100), handle_color=(200,200,200)):
    """
    Рисует горизонтальный слайдер и обрабатывает его перетаскивание мышкой.
    
    Параметры:
        screen       - поверхность Pygame
        pos          - кортеж (x, y) центра дорожки
        width        - ширина дорожки
        value        - текущее значение [0..1]
        handle_radius- радиус кружка-ползунка
        track_color  - цвет дорожки
        handle_color - цвет ручки
    Возвращает:
        value - новое значение [0..1] после перетаскивания
    """
    mouse_x, mouse_y = pg.mouse.get_pos()
    x, y = pos

    track_rect = pg.Rect(x, y - 2, width, 4)
    pg.draw.rect(screen, track_color, track_rect)

    handle_x = int(x + value * width)
    handle_pos = (handle_x, y)
    pg.draw.circle(screen, handle_color, handle_pos, handle_radius)

    pressed = pg.mouse.get_pressed()[0]
    if pressed and abs(mouse_y - y) <= handle_radius*1.5 and x <= mouse_x <= x + width:
        value = (mouse_x - x) / width
        value_sound = value/10
        pg.mixer.music.set_volume(value_sound)

    return max(0.0, min(value, 1.0))

def draw_dropdown(screen, pos, width, options, selected_index, expanded, font, bg_color=(50,50,50), text_color=(255,255,255), highlight_color=(70,70,70)):
    """
    Рисует выпадающий список и обрабатывает клики.
    
    Параметры:
        screen         - поверхность Pygame
        pos            - кортеж (x, y) верхнего левого угла
        width          - ширина списка
        options        - список строк
        selected_index - индекс выбранного элемента
        expanded       - bool, раскрыт ли список
        font           - Pygame шрифт
        bg_color       - цвет фона
        text_color     - цвет текста
        highlight_color- цвет выделения при наведении мыши
    Возвращает:
        selected_index - новый выбранный элемент
        expanded       - новый статус expanded
    """
    x, y = pos
    mouse_x, mouse_y = pg.mouse.get_pos()
    mouse_pressed = pg.mouse.get_pressed()[0]
    row_height = font.get_height() + 6
    rect = pg.Rect(x, y, width, row_height)
    pg.draw.rect(screen, bg_color, rect)
    text_surf = font.render(options[selected_index], True, text_color)
    screen.blit(text_surf, (x + 5, y + 3))
    clicked = rect.collidepoint((mouse_x, mouse_y)) and mouse_pressed

    if clicked:
        expanded = True
    if expanded:
        for i, option in enumerate(options):
            option_rect = pg.Rect(x, y + (i+1)*row_height, width, row_height)
            color = highlight_color if option_rect.collidepoint((mouse_x, mouse_y)) else bg_color
            pg.draw.rect(screen, color, option_rect)
            screen.blit(font.render(option, True, text_color), (x + 5, y + (i+1)*row_height + 3))
            if option_rect.collidepoint((mouse_x, mouse_y)) and mouse_pressed:
                selected_index = i
                screen.fill("gray")
                pg.draw.rect(screen,back_to_menu_color, back_to_menu_rect,border_radius=15)
                screen.blit(back_to_menu_button, back_to_menu_rect)
                screen.blit(music_lvl, music_rect)
                selected_options = options[selected_index]
                split_options = selected_options.split(",")
                split_options[0] = int(split_options[0])
                split_options[1] = int(split_options[1])
                screen = pg.display.set_mode([split_options[0],split_options[1]])
                expanded = False

    return selected_index, expanded

def draw_game():
    global score
    global loose
    global state
    global pause
    global cnt

    score_cnt = header_font.render(f'Score: {score}', False, (75, 0, 130))
    score_cnt_rect = score_cnt.get_rect(center=(960,55))

    # cnt+=1
    # if cnt % 750 == 0:
        # if loose == False:
        #     wheel = Wheel(x=2000,y=700)
        #     wheels.add(wheel)
        
    stars.update()
    if loose == False and not pause:
        wheels.update()
        cat.update()

    screen.blit(road,(0,0))
    pg.draw.line(screen,"white",(0,810),(1920,800),15)
    screen.blit(cat.image,(cat.rect))
    wheels.draw(screen)
    stars.draw(screen)
    screen.blit(score_cnt, score_cnt_rect)

    if pause:
        pg.draw.rect(screen,menu_button_color, menu_rect,border_radius=15)
        screen.blit(menu_button, menu_rect)

    collide = pg.sprite.spritecollide(cat,wheels,dokill=False)
    #print(collide)
    # print(cat.rect)
    # if len(wheels.sprites()) > 0:
    #     print(wheels.sprites()[0].rect)
    if len(collide) > 0:
        text_rect = loose_text.get_rect(center=(960,375))
        screen.blit(loose_text, text_rect)
        loose_sound = pg.mixer.Sound("assets/music/loose.mp3")
        loose_sound.set_volume(0.03)
        loose_sound.play()
        loose = True
        cat.alive = False

def draw_menu():
    screen.fill("gray")
    name_rect = name_game.get_rect(center=(960,150))
    screen.blit(name_game, name_rect)
    pg.draw.rect(screen,play_button_color, play_rect,border_radius=15)
    screen.blit(play_button, play_rect)
    pg.draw.rect(screen,settings_button_color, settings_rect,border_radius=15)
    screen.blit(settings_button, settings_rect)


def draw_settings():
    global selected_index, expanded, sound_value, options, screen
    screen.fill("gray")
    pg.draw.rect(screen,back_to_menu_color, back_to_menu_rect,border_radius=15)
    screen.blit(back_to_menu_button, back_to_menu_rect)
    screen.blit(music_lvl, music_rect)
    sound_value = draw_slider(screen, (550,245),350,sound_value,12,(255, 255, 255),(255, 160, 122))
    selected_index, expanded = draw_dropdown(screen,(550,445),450,options,selected_index,expanded,header_font)
    

while running:
    events = pg.event.get()
    for event in events:
        if event.type == pg.QUIT:
            running = False
        if event.type == TIME_EVENT and state == "game" and not pause and not loose:
            score+=1
        if event.type == CREATE_WHEELS and state == "game" and not pause and not loose:
            time = random.randint(1500,4500)
            pg.time.set_timer(CREATE_WHEELS,time)
            wheel = Wheel(x=2000,y=700)
            wheels.add(wheel)
        if event.type == pg.MOUSEBUTTONDOWN:
            if play_rect.collidepoint(event.pos) and state == "menu":
                play_button_color = (0, 255, 255)
                sound_click.play()
            elif menu_rect.collidepoint(event.pos) and state == "game" and pause:
                menu_button_color = (0, 255, 255)
                sound_click.play()
            elif settings_rect.collidepoint(event.pos) and state == "menu":
                settings_button_color = (0, 255, 255)
                sound_click.play()
            elif back_to_menu_rect.collidepoint(event.pos) and state == "settings":
                back_to_menu_color = (0, 255, 255)
                sound_click.play()
        if event.type == pg.MOUSEBUTTONUP:
            if play_rect.collidepoint(event.pos) and state == "menu":
                play_button_color = (0, 128, 128)
                state = "game"
            elif settings_rect.collidepoint(event.pos) and state == "menu":
                settings_button_color = (0, 128, 128)
                state = "settings"
            elif menu_rect.collidepoint(event.pos) and state == "game" and pause:
                menu_button_color = (0, 128, 128)
                state = "menu"
                pause = False
            elif back_to_menu_rect.collidepoint(event.pos) and state == "settings":
                back_to_menu_color = (0, 128, 128)
                state = "menu"
        if event.type == pg.KEYDOWN:
            if event.key == pg.K_RETURN:
                sound = pg.mixer.Sound("assets/music/soud.mp3")
                pause = False
                sound.play()
            if event.key == pg.K_SPACE:
                cat.jump()
            if event.key == pg.K_ESCAPE and state == "game":
                pause = True

    if state == "game":
        draw_game()
    elif state == "menu":
        draw_menu()
    elif state == "settings":
        draw_settings()


    pg.display.flip()
    clock.tick(fps)