import pygame, sys, time
from settings import *
from sprites import BG, Ground, Plane, Obstacle


class Game:
    def __init__(self):
        # setup
        pygame.init()
        self.display_surface = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
        pygame.display.set_caption('Flappy Cat')
        self.clock = pygame.time.Clock()
        self.active = True

        # sprite groups
        self.all_sprites = pygame.sprite.Group()
        self.collision_sprites = pygame.sprite.Group()

        # scale factor
        bg_height = pygame.image.load('graphics/environment/background.png').get_height()
        self.scale_factor = WINDOW_HEIGHT / bg_height

        # sprite setup
        BG(self.all_sprites, self.scale_factor)
        Ground([self.all_sprites, self.collision_sprites], self.scale_factor)
        # Plane is the cat
        self.plane = Plane(self.all_sprites, self.scale_factor / 25)

        # timer
        self.obstacle_timer = pygame.USEREVENT + 1
        pygame.time.set_timer(self.obstacle_timer, 1400)

        # text
        self.font = pygame.font.Font('graphics/font/BD_Cartoon_Shout.ttf', 30)
        self.score = 0
        self.start_offset = 0

        # menu
        self.menu_surf = pygame.image.load('graphics/ui/menu.png').convert_alpha()
        self.manu_rect = self.menu_surf.get_rect(center=(WINDOW_WIDTH / 2, WINDOW_HEIGHT / 2 ))

        # music
        self.background_music = pygame.mixer.Sound('sounds/Monkeys-Spinning-Monkeys(chosic.com).mp3')
        self.background_music.set_volume(0.2)
        self.background_music.play(-1)

        self.collision_effect = pygame.mixer.Sound('sounds/vine-boom-sound-effect_KT89XIq.mp3')
        self.collision_effect.set_volume(0.5)



    def collisions(self):
        if pygame.sprite.spritecollide(self.plane, self.collision_sprites, False, pygame.sprite.collide_mask) or self.plane.rect.top <= -50:
            for sprite in self.collision_sprites.sprites():
                if sprite.sprite_type == 'obstacle':
                    sprite.kill()
            self.background_music.stop()
            self.collision_effect.play()
            self.active = False
            self.plane.kill()


    def display_score(self):
        if self.active:
            self.score = (pygame.time.get_ticks() - self.start_offset) // 1000
            y = WINDOW_HEIGHT / 10
        else:
            y = (WINDOW_HEIGHT / 2) + (self.manu_rect.height / 1.5)

        score_surf = self.font.render(str(self.score), True, 'black')
        score_rect = score_surf.get_rect(midtop=(WINDOW_WIDTH / 2, y))
        self.display_surface.blit(score_surf, score_rect)

    def run(self):
        last_time = time.time()
        while True:

            # delta time
            dt = time.time() - last_time
            last_time = time.time()
            # event loop
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                if event.type == pygame.MOUSEBUTTONDOWN:
                    if self.active:
                        self.plane.jump()
                    else: # restart the game
                        self.background_music.play(loops=-1)
                        self.active = True
                        self.plane = Plane(self.all_sprites, self.scale_factor / 25)
                        self.start_offset = pygame.time.get_ticks()

                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_SPACE:
                        self.plane.jump()
                if event.type == self.obstacle_timer and self.active:
                    Obstacle([self.all_sprites, self.collision_sprites], self.scale_factor * 1.1)


            # game logic
            self.display_surface.fill('black')
            self.all_sprites.update(dt)
            self.all_sprites.draw(self.display_surface)
            self.display_score()

            if self.active:
                self.collisions()
            else:
                self.display_surface.blit(self.menu_surf, self.manu_rect)

            pygame.display.update()
            self.clock.tick(FRAME_RATE)




if __name__ == '__main__':
    game = Game()
    game.run()

