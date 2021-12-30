import pygame
import random
import os
from pygame.locals import *

WIDTH = 400
HEIGHT = 640
FPS = 60

# definisi warna
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)
BG = (150, 150, 150)

# variabel untuk menyimpan posisi mouse
mouse_pos = (0, 0)
show_mouse_pos = True

# set up path untuk assets
game_folder = os.path.dirname(__file__)  # mengembalikan letak file car.py
# menggabungkan letak file car.py dengan assets
img_folder = os.path.join(game_folder, 'assets')
# menggabungkan letak file assets dengan car, lifebar, dan object
car_folder = os.path.join(img_folder, 'car')
life_folder = os.path.join(img_folder, 'lifebar')
object_folder = os.path.join(img_folder, 'object')


def draw_text(text, font_size, font_color, x, y):
    # deklarasi font (jenis dan ukuran)
    font = pygame.font.SysFont(None, font_size)
    # merubah / merender font menjadi surface
    img_font = font.render(text, True, font_color)
    # manampilkan font yang sudah dirender ke screen
    screen.blit(img_font, (x, y))


# inisialisasi pygame
pygame.init()
pygame.mixer.init()  # menambahkan suara
# membuat lebar window dari game
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption('Game Mobil')  # caption window
clock = pygame.time.Clock()  # untuk mengatur fps

# class untuk inherit terhadap pygame.sprite.Sprite untuk menampilkan karakter


class Player(pygame.sprite.Sprite):
    def __init__(self, x, y):
        super().__init__()
        # untuk load karakter dan mengconvert bagian transparan
        self.image = pygame.image.load(os.path.join(
            car_folder, "car_blue_3.png")).convert_alpha()
        # untuk membuat rectangle berguna untuk mengecek coalision atau rintangan jika karakter menabrak
        self.orig_image = self.image
        self.rect = self.image.get_rect(center=(x, y))
        self.rect.x = x
        self.rect.y = y
        self.speed = 4

        self.angle = 0

    def update(self):
        key = pygame.key.get_pressed()  # untuk mendeteksi penekanan keyboard

        # ketika keyboard panah kanan ditekan
        if key[pygame.K_RIGHT] and self.rect.right < 355:
            # move in place
            self.rect.move_ip(self.speed, 0)
            # self.rect.x += self.speed

        # ketika keyboard panah kiri ditekan
        if key[pygame.K_LEFT] and self.rect.left > 49:
            # move in place
            self.rect.move_ip(-self.speed, 0)
            # self.rect.x -= self.speed
        if self.rect.right > 352:
            self.angle = 0
            if key[pygame.K_LEFT]:
                self.angle = 15

        if self.rect.left < 47:
            self.angle = 0
            if key[pygame.K_RIGHT]:
                self.angle = -15

        self.image = pygame.transform.rotozoom(
            self.orig_image, self.angle, 1)
        self.rect = self.image.get_rect(center=self.rect.center)


class PanahJalan(pygame.sprite.Sprite):
    def __init__(self, x, y):
        super().__init__()
        self.image = pygame.transform.scale(pygame.image.load(os.path.join(
            object_folder, "arrow_white.png")).convert_alpha(), (100, 50))
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y

    def update(self):
        if self.rect.y > HEIGHT:
            self.kill()


class Car(pygame.sprite.Sprite):
    def __init__(self, x, img):
        super().__init__()
        self.image = img
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = -250
        self.hit = False

    def update(self):
        if self.rect.y > HEIGHT:
            self.kill()


class Batu(pygame.sprite.Sprite):
    def __init__(self, x, img):
        super().__init__()
        self.image = img
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = -250
        self.hit = False

    def update(self):
        if self.rect.y > HEIGHT:
            self.kill()


# load tribune
tribune = pygame.transform.rotate(pygame.image.load(
    os.path.join(object_folder, "tribune.png")).convert_alpha(), 90)
tribune_kanan = pygame.transform.scale(tribune, (144, HEIGHT))
tribune_kiri = pygame.transform.scale(tribune, (144, HEIGHT))

# load cars
car_list = []  # array untuk menyimpan mobil npc (non player character)
for i in range(4):  # men-load seluruh mobil
    img = pygame.image.load(os.path.join(
        car_folder, "car_{}.png".format(i))).convert_alpha()
    car_list.append(img)

# load batu
batu_list = []
for i in range(3):
    img = pygame.image.load(os.path.join(
        object_folder, f"rock_{i}.png")).convert_alpha()
    batu_list.append(img)

all_sprites = pygame.sprite.Group()  # untuk menyimpan seluruh sprite
panahGroup = pygame.sprite.Group()  # untuk menyimpan seluruh sprite panah
cars = pygame.sprite.Group()  # untuk menyimpan seluruh sprite car
batus = pygame.sprite.Group()  # untuk menyimpan seluruh sprite batu

b = Batu(random.randrange(46, 286), random.choice(batu_list))
batus.add(b)

mobil = Car(random.randrange(46, 286), random.choice(car_list))
cars.add(mobil)

for i in range(3):
    panah = PanahJalan(WIDTH // 2 - 50, i * 230 + 40)
    panahGroup.add(panah)

# membuat object player (tanda // artinya pembagian akan dibukatkan kebawah)
player = Player(WIDTH // 2 - 30, HEIGHT // 2 + 100)
# menambahkan sprite di object player ke all_sprite agar bisa langsung ditampilkan
all_sprites.add(player)

run = True  # untuk acuan memulai game
scene = {
    0: "PLAY",
    1: "GAMEOVER"
}

current_scene = 0

while run:  # game berjalan
    clock.tick(FPS)
    for event in pygame.event.get():  # mengecek seluruh event / inputan
        if event.type == pygame.QUIT:  # ketika quit maka run akan false sehingga...
            run = False  # ...run akan false
        if event.type == KEYUP:
            if event.key == pygame.K_r:
                # mengosongkan semua sprite didalam group
                all_sprites.empty()
                panahGroup.empty()
                cars.empty()
                batus.empty()

                # menambahkan kembali sprite kedalam group
                b = Batu(random.randrange(46, 286), random.choice(batu_list))
                batus.add(b)

                mobil = Car(random.randrange(46, 286), random.choice(car_list))
                cars.add(mobil)

                for i in range(3):
                    panah = PanahJalan(WIDTH // 2 - 50, i * 230 + 40)
                    panahGroup.add(panah)

                player = Player(WIDTH // 2 - 30, HEIGHT // 2 + 100)
                all_sprites.add(player)

                current_scene = 0
        if event.type == KEYDOWN:  # ketika keyboard ditekan
            if event.key == K_x:  # ketika huruf ditekan
                show_mouse_pos = not show_mouse_pos  # maka posisi koordinat mouse akan hilang
            if event.key == pygame.K_RIGHT:
                player.angle = -15
            elif event.key == pygame.K_LEFT:
                player.angle = 15
        elif event.type == pygame.KEYUP:
            # Stop rotating if the player releases the keys.
            if event.key == pygame.K_RIGHT and player.angle == -15:
                player.angle = 0
            elif event.key == pygame.K_LEFT and player.angle == 15:
                player.angle = 0

        # dapatin posisi mouse
        mouse_pos = pygame.mouse.get_pos()  # mengembalikan tuple posisi mouse

    if scene.get(current_scene) == "PLAY":
        for panah in panahGroup:
            panah.rect.y += 2

        for batu in batus:
            batu.rect.y += 2

        for car in cars:
            car.rect.y += 3

        while len(batus) < 1:
            b_new = Batu(random.randrange(46, 286), random.choice(batu_list))
            batus.add(b_new)

        while len(cars) < 1:
            mobil_new = Car(random.randrange(82, 322), random.choice(car_list))
            cars.add(mobil_new)

        while len(panahGroup) < 3:
            panah_new = PanahJalan(WIDTH // 2 - 50, -50)
            panahGroup.add(panah_new)

        # cek collision mobil
        nabrak_mobil = pygame.sprite.spritecollide(player, cars, False)

        if nabrak_mobil:
            for m in nabrak_mobil:
                if not m.hit:
                    m.hit = True
                    current_scene = 1

        # cek collision batu
        nabrak_batu = pygame.sprite.spritecollide(player, batus, False)
        if nabrak_batu:
            for b in nabrak_batu:
                if not b.hit:
                    b.hit = True
                    current_scene = 1

        all_sprites.update()  # mengupdate seluruh sprite yang dimiliki
        panahGroup.update()  # mengupdate seluruh sprite panah
        cars.update()  # mengupdate seluruh sprite car
        batus.update()  # mengupdate seluruh sprite batu

    # clear screen
    screen.fill(BG)
    # menampilkan sesuatu ke screen melalui cara manual
    # screen.blit(player.image, (player.rect))
    screen.blit(tribune_kiri, (-100, 0))
    screen.blit(tribune_kanan, (WIDTH - 40, 0))

    if scene.get(current_scene) == "PLAY":
        panahGroup.draw(screen)  # draw seluruh panah
        batus.draw(screen)  # draw seluruh batu
        cars.draw(screen)  # draw seluruh car
        all_sprites.draw(screen)  # draw seluruh sprite

    if scene.get(current_scene) == "GAMEOVER":
        draw_text("GAME OVER", 40, RED, WIDTH // 2 - 80, HEIGHT // 4)
        draw_text("Tekan \"R\" untuk restart", 30,
                  BLACK, WIDTH // 2 - 100, HEIGHT // 2)

    # tampilin posisi mouse di surface, untuk memudahkan saja dalam melihat posisi x dan y
    if show_mouse_pos:
        draw_text(f"x = {mouse_pos[0]}, y = {mouse_pos[1]}",
                  25, WHITE, mouse_pos[0] + 20, mouse_pos[1])

    pygame.display.flip()  # update keseluruhan display

pygame.quit()  # jika whilenya bernilai false maka pygamenya akan quit
