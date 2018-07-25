import pygame
from pygame.sprite import Sprite


class Alien(Sprite):
    def __init__(self, ai_settings, screen):
        # 初始化外星人并设置其初始位置
        super(Alien, self).__init__()
        self.screen = screen
        self.ai_settings = ai_settings
        # 加在外星人图像设置rect属性
        self.image = pygame.image.load("D:/py/pygame/image/aliens.jpg")
        self.rect = self.image.get_rect()

        # 将每艘新外星人放在左上角附近
        self.rect.x = self.rect.width
        self.rect.y = self.rect.height

        # 在外星人的属性center中存储小数值
        self.x = float(self.rect.centerx)

    def blitem(self):
        # 在指定的位置绘制外星人
        self.screen.blit(self.image, self.rect)

    def check_edges(self):
        # 如果碰到边缘就返回ture
        screen_rect = self.screen.get_rect()
        if self.rect.right >= screen_rect.right:
            return True
        elif self.rect.left <= 0:
            return True

    def update(self):
        # 向右移动外星人(或者向左)
        self.x += (self.ai_settings.alien_speed_factor *
                   self.ai_settings.fleet_direction)
        self.rect.x = self.x