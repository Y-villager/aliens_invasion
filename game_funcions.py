import sys, pygame
from bullet import Bullet
from alien import Alien
from time import sleep


def check_keydown_events(event, ai_settings, stats, screen, ship, bullets,
                         music1):
    '''响应按键'''
    if event.key == pygame.K_RIGHT:
        ship.moving_right = True

    elif event.key == pygame.K_LEFT:
        ship.moving_left = True

    elif event.key == pygame.K_SPACE:
        #创建一颗子弹，并将其加入到编组bullets中
        fire_bullet(ai_settings, stats, screen, ship, bullets, music1)

    elif event.key == pygame.K_ESCAPE:  #按Esc退出
        sys.exit()


#如果还没有达到限制，就发射一颗子弹
def fire_bullet(ai_settings, stats, screen, ship, bullets, music1):
    if len(bullets) < ai_settings.bullet_allowed and stats.game_active:
        new_bullet = Bullet(ai_settings, screen, ship)
        bullets.add(new_bullet)
        music1.play()


def check_keyup_events(event, ship):
    # 响应松开
    if event.key == pygame.K_RIGHT:
        ship.moving_right = False
    elif event.key == pygame.K_LEFT:
        ship.moving_left = False


def check_events(ai_settings, screen, stats, play_button, ship, aliens,
                 bullets, music1, sb):
    # 监视键盘和鼠标事件
    for event in pygame.event.get():
        if event.type == pygame.QUIT:  #如果鼠标点击关闭，就退出窗口
            sys.exit()

        elif event.type == pygame.KEYDOWN:  #对KEYDOWN事件作出响应
            check_keydown_events(event, ai_settings, stats, screen, ship,
                                 bullets, music1)

        elif event.type == pygame.KEYUP:  #对KEYUP事件做出响应
            check_keyup_events(event, ship)

        elif event.type == pygame.MOUSEBUTTONDOWN:  #对点击play按钮做出回应
            mouse_x, mouse_y = pygame.mouse.get_pos()
            check_play_button(ai_settings, screen, stats, play_button, ship,
                              aliens, bullets, mouse_x, mouse_y, sb)


def check_play_button(ai_settings, screen, stats, play_button, ship, aliens,
                      bullets, mouse_x, mouse_y, sb):
    '''在玩家单击Play按钮时开始新游戏'''
    button_clicked = play_button.rect.collidepoint(mouse_x, mouse_y)
    if button_clicked and not stats.game_active:
        #重置游戏设置
        ai_settings.initialize_dynamic_settings()

        #隐藏光标
        pygame.mouse.set_visible(False)

        #重置游戏信息
        stats.reset_stats()
        stats.game_active = True

        #把分数0显示出来
        sb.prep_score()
        sb.show_score()
        sb.prep_level()
        sb.prep_ships()

        #清空外星人列表和子弹列表
        aliens.empty()
        bullets.empty()

        #创建一群新的外星人，并让飞船居中
        create_fleet(ai_settings, screen, ship, aliens)
        ship.center_ship()


def update_bullets(ai_settings, screen, stats, sb, ship, aliens, bullets):
    bullets.update()
    # 删除已消失的子弹
    for bullet in bullets.copy():
        if bullet.rect.bottom <= 0:
            bullets.remove(bullet)
        # print(len(bullets))
    check_bullet_alien_collisions(ai_settings, screen, stats, sb, ship, aliens,
                                  bullets)


def check_bullet_alien_collisions(ai_settings, screen, stats, sb, ship, aliens,
                                  bullets):
    collisions = pygame.sprite.groupcollide(bullets, aliens, True, True)

    #当外星人群被消灭后，删除现有的子弹并新建一群外星人, 同时加快游戏速度
    if len(aliens) == 0:
        bullets.empty()

        ai_settings.increase_speed()
        # 提高等级
        stats.level += 1
        sb.prep_level()
        create_fleet(ai_settings, screen, ship, aliens)
    if collisions:  #记分
        for aliens in collisions.values():
            stats.score += ai_settings.alien_points * len(aliens)
            sb.prep_score()
        check_high_score(stats, sb)


def check_high_score(stats, sb):
    '''检查是否诞生了新的最高得分'''
    if stats.score > stats.high_score:
        stats.high_score = stats.score
        sb.prep_high_score()


def update_screen(ai_settings, screen, stats, sb, ship, aliens, bullets,
                  play_button):
    # 设置背景颜色
    screen.fill(ai_settings.bg_color)

    # 在飞船和外星人后面重绘所以子弹
    for bullet in bullets.sprites():
        bullet.draw_bullet()
    # aliens.blitem()
    sb.show_score()
    ship.blitem()
    aliens.draw(screen)
    if not stats.game_active:
        play_button.draw_button()
    # 让最近绘制的屏幕可见
    pygame.display.flip()


def create_fleet(ai_settings, screen, ship, aliens):
    alien = Alien(ai_settings, screen)
    number_aliens_x = get_number_aliens_x(ai_settings, alien.rect.width)
    number_rows = get_number_rows(ai_settings, ship.rect.height,
                                  alien.rect.height)
    for row_number in range(number_rows):
        for alien_number in range(number_aliens_x):
            create_alien(ai_settings, screen, aliens, alien_number, row_number)


def get_number_aliens_x(ai_settings, alien_width):
    available_space_x = ai_settings.screen_width - 2 * alien_width
    number_aliens_x = int(available_space_x / (2 * alien_width))
    return number_aliens_x


def create_alien(ai_settings, screen, aliens, alien_number, row_number):
    '''创建一个外星人将其放在当前行'''
    alien = Alien(ai_settings, screen)
    alien_width = alien.rect.width
    alien.x = alien_width + 2 * alien_width * alien_number
    alien.rect.x = alien.x
    alien.rect.y = alien.rect.height + 2 * alien.rect.height * row_number
    aliens.add(alien)


def get_number_rows(ai_settings, ship_height, alien_height):
    # 计算屏幕容纳多少行
    available_space_y = (
        ai_settings.screen_height - (3 * alien_height) - ship_height)
    nubmer_rows = int(available_space_y / (2 * alien_height))
    return nubmer_rows


def check_fleet_edges(ai_settings, aliens):
    # 到达边缘采取相应措施
    for alien in aliens.sprites():
        if alien.check_edges():
            change_fleet_direction(ai_settings, aliens)
            break


def change_fleet_direction(ai_settings, aliens):
    # 将整群下移，并改变他们的方向
    for alien in aliens.sprites():
        alien.rect.y += ai_settings.fleet_drop_speed
    ai_settings.fleet_direction *= -1


def check_aliens_bottom(ai_settings, stats, screen, sb, ship, aliens, bullets):
    '''检查是否有外星人到达了屏幕底端'''
    screen_rect = screen.get_rect()
    for alien in aliens.sprites():
        if alien.rect.bottom >= screen_rect.bottom:
            #像飞船被撞一样进行处理
            ship_hit(ai_settings, stats, screen, sb, ship, aliens, bullets)
            break


def update_aliens(ai_settings, stats, screen, sb, ship, aliens, bullets):
    # 检查是否位于屏幕边缘，并更新整群位置
    check_fleet_edges(ai_settings, aliens)
    aliens.update()
    # 检查外星人和飞船的碰撞
    if pygame.sprite.spritecollideany(ship, aliens):
        ship_hit(ai_settings, stats, screen, sb, ship, aliens, bullets)
        # print("ship hit!!!")

    check_aliens_bottom(ai_settings, stats, screen, sb, ship, aliens, bullets)


def ship_hit(ai_settings, stats, screen, sb, ship, aliens, bullets):
    if stats.ships_left > 0:
        stats.ships_left -= 1
        # 更新计分牌
        sb.prep_ships()
        aliens.empty()
        bullets.empty()
        create_fleet(ai_settings, screen, ship, aliens)
        ship.center_ship()
        sleep(0.5)
    else:
        stats.game_active = False
        pygame.mouse.set_visible(True)
