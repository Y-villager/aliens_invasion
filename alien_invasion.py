import pygame
from settings import Settings
from ship import Ship
import game_funcions as gf
from pygame.sprite import Group
from alien import Alien
from game_stats import GameStats
from button import Button
from scoreboard import Scoreboard


def run_game():
    pygame.init()
    ai_settings = Settings()
    screen = pygame.display.set_mode((ai_settings.screen_width,
                                      ai_settings.screen_height))
    pygame.display.set_caption("Alien Invasion")

    # 创建一飞船
    ship = Ship(ai_settings, screen)
    # alien = Alien(ai_settings, screen)
    # 创建一个用于存储子弹的编组
    bullets = Group()

    # 设置背景颜色
    # bg_color = (230, 230, 230)
    aliens = Group()
    #创建外星人群
    gf.create_fleet(ai_settings, screen, ship, aliens)
    #创建一个用于存储游戏统计信息的实例， 并创建记分牌
    stats = GameStats(ai_settings)

    play_button = Button(ai_settings, screen, "play")
    # 计分
    sb = Scoreboard(ai_settings, screen, stats)

    #背景音乐
    # pygame.mixer.music.load("D:/py/pygame/sounds/111.mp3")
    # pygame.mixer.music.play(loops=-1, start=0.0)
    music1 = pygame.mixer.Sound("D:/py/pygame/sounds/222.wav")
    #开始游戏的主循环
    while True:
        #监视键盘和鼠标事件
        gf.check_events(ai_settings, screen, stats, play_button, ship, aliens,
                        bullets, music1, sb)

        if stats.game_active:  #判断是否处于活动状态（是否有命）

            #根据移动标志调整飞船的位置
            ship.update()

            # 更新子弹位置并删除已消失的子弹  删除子弹击中的外星人
            gf.update_bullets(ai_settings, screen, stats, sb, ship, aliens,
                              bullets)

            #更新外星人位置
            gf.update_aliens(ai_settings, stats, screen, sb, ship, aliens,
                             bullets)

        # 更新屏幕上的图像，并切换到新屏幕
        gf.update_screen(ai_settings, screen, stats, sb, ship, aliens, bullets,
                         play_button)


run_game()
