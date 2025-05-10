from pygame import *
import os
import sys


class GameSprite(sprite.Sprite):
    def __init__(self, player_image, player_x, player_y, size_x, size_y):
        sprite.Sprite.__init__(self)
        self.image_normal = transform.scale(image.load(player_image), (size_x, size_y))
        self.image = self.image_normal
        self.rect = self.image.get_rect()
        self.rect.x = player_x
        self.rect.y = player_y

    def update(self, mouse_pos, player_image_hover, size_x, size_y):
        if self.rect.collidepoint(mouse_pos):
            self.image_hover = transform.scale(image.load(player_image_hover), (size_x, size_y))
            self.image = self.image_hover
        else:
            self.image = self.image_normal

    def reset(self):
        window.blit(self.image, (self.rect.x, self.rect.y))


class Player(GameSprite):
    def __init__(self, player_image, player_x, player_y, size_x, size_y, player_x_speed, player_y_speed):
        GameSprite.__init__(self, player_image, player_x, player_y, size_x, size_y)
        self.x_speed = player_x_speed
        self.y_speed = player_y_speed

    def update(self, barriers):
        if self.rect.x <= win_width - 80 and self.x_speed > 0 or self.rect.x >= 0 and self.x_speed < 0:
            self.rect.x += self.x_speed
        platforms_touched = sprite.spritecollide(self, barriers, False)
        if self.x_speed > 0:
            for p in platforms_touched:
                self.rect.right = min(self.rect.right, p.rect.left)
        elif self.x_speed < 0:
            for p in platforms_touched:
                self.rect.left = max(self.rect.left, p.rect.right)

        if self.rect.y <= win_height - 80 and self.y_speed > 0 or self.rect.y >= 0 and self.y_speed < 0:
            self.rect.y += self.y_speed
        platforms_touched = sprite.spritecollide(self, barriers, False)
        if self.y_speed > 0:
            for p in platforms_touched:
                self.rect.bottom = min(self.rect.bottom, p.rect.top)
        elif self.y_speed < 0:
            for p in platforms_touched:
                self.rect.top = max(self.rect.top, p.rect.bottom)

    def fire(self):
        bullet = Bullet('images/bullet.png', self.rect.centerx, self.rect.top, 15, 20, 15)
        bullets.add(bullet)


class Enemy_h(GameSprite):
    side = "left"

    def __init__(self, player_image, player_x, player_y, size_x, size_y, player_speed, x1, x2):
        GameSprite.__init__(self, player_image, player_x, player_y, size_x, size_y)
        self.speed = player_speed
        self.x1 = x1
        self.x2 = x2

    def update(self):
        if self.rect.x <= self.x1:
            self.side = "right"
        if self.rect.x >= self.x2:
            self.side = "left"
        if self.side == "left":
            self.rect.x -= self.speed
        else:
            self.rect.x += self.speed


class Enemy_v(GameSprite):
    side = "up"

    def __init__(self, player_image, player_x, player_y, size_x, size_y, player_speed, y1, y2):
        GameSprite.__init__(self, player_image, player_x, player_y, size_x, size_y)
        self.speed = player_speed
        self.y1 = y1
        self.y2 = y2

    def update(self):
        if self.rect.y <= self.y1:
            self.side = "down"
        if self.rect.y >= self.y2:
            self.side = "up"
        if self.side == "up":
            self.rect.y -= self.speed
        else:
            self.rect.y += self.speed


class Bullet(GameSprite):
    def __init__(self, player_image, player_x, player_y, size_x, size_y, player_speed):
        GameSprite.__init__(self, player_image, player_x, player_y, size_x, size_y)
        self.speed = player_speed

    def update(self):
        self.rect.x += self.speed
        if self.rect.x > win_width + 10:
            self.kill()


def fade(screen, width, height):
    fade_surface = Surface((width, height))
    fade_surface.fill((0, 0, 0))
    for alpha in range(0, 255, 5):
        fade_surface.set_alpha(alpha)
        screen.blit(fade_surface, (0, 0))
        display.update()
        time.delay(30)


def save_progress(amount):
    with open("save.txt", "w") as f:
        f.write(str(amount))


def load_progress():
    if os.path.exists("save.txt"):
        with open("save.txt", "r") as f:
            return int(f.read())
    return 0



win_width = 1200
win_height = 700
window = display.set_mode((win_width, win_height))
display.set_caption("Лабіринт")

back_m = transform.scale(image.load("images/menu.png"), (win_width, win_height))
start_but = GameSprite("images/start.png", 1000, 10, 200, 80)
exit_but = GameSprite("images/exit.png", 0, 10, 200, 80)
mus_but = GameSprite("images/musicb.png", 1000, 600, 80, 80)

mixer.init()
mixer.music.load("sounds/main.wav")
mixer.music.set_volume(0.02)
mixer.music.play(-1)
lose = mixer.Sound("sounds/over.wav")
lose.set_volume(0.02)
win = mixer.Sound("sounds/win.wav")
win.set_volume(0.02)

total_amount = load_progress()

############## 1 lvl #####################
amount = 0

font.init()
text = font.SysFont(None, 36).render("Coins: " + str(amount), True, (255, 255, 0))

back = transform.scale(image.load("images/display.jpg"), (win_width, win_height))
bullets = sprite.Group()
barriers = sprite.Group()
monsters = sprite.Group()
coins = sprite.Group()

w1 = GameSprite('images/wall2.png', 0, 200, 300, 50)
w2 = GameSprite('images/wall1.png', 250, 200, 50, 400)
barriers.add(w1)
barriers.add(w2)



hero = Player('images/hero.png', 5, win_height - 80, 80, 80, 0, 0)
final_sprite = GameSprite('images/door.png', win_width - 85, win_height - 100, 80, 80)

monster1 = Enemy_v('images/enemy.png', 1000, 200, 80, 80, 5, 200, 420)
monster2 = Enemy_h('images/enemy.png', 0, 90, 80, 80, 5, 0, 200)
monsters.add(monster1)
monsters.add(monster2)

coin1 = GameSprite('images/coin.png', 400, 200, 80, 80)
coin2 = GameSprite('images/coin.png', 200, 600, 80, 80)
coins.add(coin1)
coins.add(coin2)

############## 2 lvl #####################
amount_2 = 0

back_2 = transform.scale(image.load("images/back_2.png"), (win_width, win_height))
barriers_2 = sprite.Group()
monsters_2 = sprite.Group()
coins_2 = sprite.Group()


hero_2 = Player('images/hero.png', 5, 5, 80, 80, 0, 0)
final_sprite_2 = GameSprite('images/door.png', win_width - 85, 500, 80, 80)

monster1_2 = Enemy_v('images/enemy.png', 1000, 200, 80, 80, 5, 200, 420)
monster2_2 = Enemy_h('images/enemy.png', 0, 90, 80, 80, 5, 0, 200)
monsters_2.add(monster1_2)
monsters_2.add(monster2_2)

coin1_2 = GameSprite('images/coin.png', 1000, 300, 80, 80)
coin2_2 = GameSprite('images/coin.png', 100, 600, 80, 80)
coins_2.add(coin1_2)
coins_2.add(coin2_2)

finish = False
run = True
a = "menu"
music = "on"

while run:
    if a == "menu":
        for e in event.get():
            if e.type == QUIT:
                run = False
            elif e.type == MOUSEBUTTONDOWN:
                if exit_but.rect.collidepoint(e.pos):
                    run = False
                if mus_but.rect.collidepoint(e.pos):
                    if music == "on":
                        mixer.music.pause()
                        music = "off"
                    else:
                        mixer.music.unpause()
                        music = "on"
                if start_but.rect.collidepoint(e.pos):
                    mixer.music.stop()
                    fade(window, win_width, win_height)
                    a = "lvl1"
                    mixer.music.load("sounds/lvl1.wav")
                    mixer.music.play(-1)

        window.blit(back_m, (0, 0))
        start_but.reset()
        mus_but.reset()
        exit_but.reset()
        mouse_pos = mouse.get_pos()
        exit_but.update(mouse_pos, "images/exit_2.png", 200, 80)

    elif a == "lvl1":
        for e in event.get():
            if e.type == QUIT:
                run = False
            elif e.type == KEYDOWN:
                if e.key == K_LEFT:
                    hero.x_speed = -8
                if e.key == K_RIGHT:
                    hero.x_speed = 8
                if e.key == K_UP:
                    hero.y_speed = -8
                if e.key == K_DOWN:
                    hero.y_speed = 8
                if e.key == K_SPACE:
                    hero.fire()

            elif e.type == KEYUP:
                if e.key == K_LEFT:
                    hero.x_speed = 0
                if e.key == K_RIGHT:
                    hero.x_speed = 0
                if e.key == K_UP:
                    hero.y_speed = 0
                if e.key == K_DOWN:
                    hero.y_speed = 0

        if not finish:
            window.blit(back, (0, 0))
            window.blit(text, (270, 0))

            hero.update(barriers)
            hero.reset()
            bullets.draw(window)
            bullets.update()

            barriers.draw(window)
            final_sprite.reset()

            sprite.groupcollide(monsters, bullets, True, True)
            monsters.update()
            monsters.draw(window)
            sprite.groupcollide(bullets, barriers, True, False)

            coins.draw(window)
            if sprite.spritecollide(hero, coins, True):
                amount += 1
                total_amount += 1
                save_progress(total_amount)
            text = font.SysFont(None, 36).render("Coins: " + str(amount), True, (255, 255, 0))

            if sprite.spritecollide(hero, monsters, False):
                finish = True
                lose.play()
                mixer.music.stop()
                img = image.load('images/game_over.png')
                window.blit(transform.scale(img, (win_width, win_height)), (0, 0))

            if sprite.collide_rect(hero, final_sprite):
                fade(window, win_width, win_height)
                a = "pause"

    elif a == "pause":
        ################ вікно між рівнями або для паузи #####################
        for e in event.get():
            if e.type == QUIT:
                run = False
            elif e.type == MOUSEBUTTONDOWN:
                if start_but.rect.collidepoint(e.pos):
                    a = "lvl2"
        window.blit(back_m, (0, 0))
        start_but.reset()

    elif a == "lvl2":
        for e in event.get():
            if e.type == QUIT:
                run = False
            elif e.type == KEYDOWN:
                if e.key == K_LEFT:
                    hero_2.x_speed = -8
                if e.key == K_RIGHT:
                    hero_2.x_speed = 8
                if e.key == K_UP:
                    hero_2.y_speed = -8
                if e.key == K_DOWN:
                    hero_2.y_speed = 8
                if e.key == K_SPACE:
                    hero_2.fire()

            elif e.type == KEYUP:
                if e.key == K_LEFT:
                    hero_2.x_speed = 0
                if e.key == K_RIGHT:
                    hero_2.x_speed = 0
                if e.key == K_UP:
                    hero_2.y_speed = 0
                if e.key == K_DOWN:
                    hero_2.y_speed = 0

        if not finish:
            window.blit(back_2, (0, 0))
            window.blit(text, (270, 0))

            hero_2.update(barriers_2)
            hero_2.reset()
            bullets.draw(window)
            bullets.update()

            barriers_2.draw(window)
            final_sprite_2.reset()

            sprite.groupcollide(monsters_2, bullets, True, True)
            monsters_2.update()
            monsters_2.draw(window)
            sprite.groupcollide(bullets, barriers_2, True, False)

            coins_2.draw(window)
            if sprite.spritecollide(hero_2, coins_2, True):
                amount_2 += 1
                total_amount += 1
                save_progress(total_amount)
            text = font.SysFont(None, 36).render("Coins: " + str(amount_2), True, (255, 255, 0))

            if sprite.spritecollide(hero_2, monsters_2, False):
                finish = True
                lose.play()
                mixer.music.stop()
                img = image.load('images/game_over.png')
                window.blit(transform.scale(img, (win_width, win_height)), (0, 0))

            if sprite.collide_rect(hero_2, final_sprite_2):
                finish = True
                win.play()
                mixer.music.stop()
                img = image.load('images/winner.png')
                window.blit(transform.scale(img, (win_width, win_height)), (0, 0))

    time.delay(20)
    display.update()