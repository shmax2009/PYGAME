import pygame
import math
import random
import math

# Define some colors.
BLACK = pygame.Color('black')
WHITE = pygame.Color('white')
random.seed()
pygame.init()
width_s = 600
height_s = 600
screen = pygame.display.set_mode((width_s, height_s))
pygame.display.set_caption("My Game")
done = False
clock = pygame.time.Clock()
pygame.joystick.init()

width = 50
height = 50
t = 0
x = width_s // 2
y = height_s // 2
speed = 10
mana = 20
font = pygame.font.Font('ArialRegular.ttf', 32)
text = font.render('INC. : {}'.format(mana), True, BLACK, WHITE)
textRect = text.get_rect()
check_a = 0
check_x = 0
textRect.center = (75, 40)
speed_fall = 0
facing = -1


class eat():
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.r = 50

    def draw(self, screen):
        pygame.draw.rect(screen, (15, 175, 15), (self.x, self.y, 20, 20))


class bullet():
    def __init__(self, x, y, width, height, speed_y_b, speed_x_b):
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.speed_y_b = speed_y_b
        self.speed_x_b = speed_x_b

    def draw(self, screen):
        pygame.draw.rect(screen, BLACK, (self.x, self.y, self.width, self.height))


bullets = []
eat = eat(100, 120)
# -------- Main Program Loop -----------
while not done:
    screen.fill(WHITE)
    screen.blit(text, textRect)
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            done = True
    for b in bullets:
        if b.x < width_s and b.x > 0:
            b.x -= b.speed_x_b
            b.speed_y_b += 0.6

            b.y += b.speed_y_b
            if b.y <= 0 or b.y >= height_s:
                bullets.pop(bullets.index(b))
        else:
            bullets.pop(bullets.index(b))

    joystick_count = pygame.joystick.get_count()

    for i in range(joystick_count):
        joystick = pygame.joystick.Joystick(i)
        joystick.init()
        ax_a = joystick.get_axis(2)
        # print(speed_fall)
        # print(ax_a)
        y -= speed_fall
        if y < height_s - height and y > 0 and round(ax_a) == 0:
            speed_fall -= 1
        else:
            if round(ax_a) == 0:

                if y > height_s - height:
                    y = height_s - height - 1
                elif y < 0:
                    y = 0 + 1
                speed_fall = 0
            else:
                if y < 0:
                    y = 0 + 1
                elif y > height_s - height:
                    y = height_s - height - 3
                speed_fall += (abs(ax_a)) / 2

        r = round(joystick.get_axis(0))
        if r != 0:
            if r > 0:
                facing = 1
            elif r < 0:
                facing = -1
        axes = joystick.get_numaxes()
        x += math.trunc(joystick.get_axis(0) * speed)
        ax1 = joystick.get_axis(4)
        ax2 = joystick.get_axis(3)
        buttons = joystick.get_numbuttons()
        button_a = joystick.get_button(0)
        a = (eat.x - (x + width // 2))
        b = (eat.y - (y + height // 2))

        qr = round(ax1) != 0 or round(ax2) != 0
        # print(qr)
        # button X
        # print(qr)
        if qr and check_x == 0 and mana >= 2 + 2:
            qr = ax1 != 0 or ax2 != 0
            check_x = 1
            mana -= 2
            width -= 4
            height -= 4
            eat.r -= 4
            x += 2
            y -= 2
            bullets.append(
                bullet(x + width // 2, y + height // 2, 15, 15, speed * 2 * round(ax2), speed * 2 * round(ax1) * -1))
            text = font.render('INC. : {}'.format(mana), True, BLACK, WHITE)

        elif check_x == 1 and round(ax1) == 0 and round(ax2) == 0:
            check_x = 0
        if math.sqrt(a * a + b * b) <= eat.r:
            if mana < 60:
                mana += 1
                width += 2
                height += 2
                eat.r += 2
                x -= 2
                y += 2
                text = font.render('INC. : {}'.format(mana), True, BLACK, WHITE)
                eat.x = (random.random() * 1000 + 50) % (height_s - 50)
                eat.y = (random.random() * 1000 + 50) % (height_s - 50)

        # button A

    pygame.draw.rect(screen, BLACK, (x, y, width, height))
    screen.blit(text, textRect)
    for b in bullets:
        b.draw(screen)
    eat.draw(screen)
    pygame.display.update()
    clock.tick(60)

pygame.quit()