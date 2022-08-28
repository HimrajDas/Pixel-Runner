import pygame, sys, random

pygame.init()

class Player(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()

        player_walk_1  = pygame.image.load("graphics/player/player_walk_1.png").convert_alpha()
        player_walk_2 = pygame.image.load("graphics/player/player_walk_2.png").convert_alpha()
        self.player_walk = [player_walk_1, player_walk_2]
        self.player_index = 0
        self.player_jump = pygame.image.load("graphics/player/jump.png").convert_alpha()
        self.image = self.player_walk[self.player_index]
        self.rect = self.image.get_rect(midbottom = (80, 300))
        self.gravity = 0
        self.jump_sound = pygame.mixer.Sound('audio/audio_jump.mp3')
        self.jump_sound.set_volume(0.5)
    

    def player_input(self):
        keys = pygame.key.get_pressed()
        if keys[pygame.K_SPACE] and self.rect.bottom >= 300:
            self.gravity = -20
            self.jump_sound.play()


    def apply_gravity(self):
        self.gravity += 1
        self.rect.y += self.gravity
        if self.rect.bottom >= 300:
            self.rect.bottom = 300


    def animation_state(self):
        if self.rect.bottom < 300:
            self.image = self.player_jump
        else:
            self.player_index += 0.1
            if self.player_index >= len(self.player_walk):
                self.player_index = 0
            self.image = self.player_walk[int(self.player_index)]


    def update(self):
        self.player_input()
        self.apply_gravity()
        self.animation_state()


class Obstacle(pygame.sprite.Sprite):
    def __init__(self, type):
        super().__init__()

        if type == 'fly':
            fly_frame_1 = pygame.image.load("graphics/fly/Fly1.png").convert_alpha()
            fly_frame_2 = pygame.image.load("graphics/fly/Fly2.png").convert_alpha()
            self.frames = [fly_frame_1, fly_frame_2]
            y_pos = random.randint(130, 210)
        else:
            snail_frame_1 = pygame.image.load('graphics/snail/snail1.png').convert_alpha()
            snail_frame_2 = pygame.image.load('graphics/snail/snail2.png').convert_alpha()
            self.frames = [snail_frame_1, snail_frame_2]
            y_pos = 300

        self.animation_index = 0
        self.image = self.frames[self.animation_index]
        self.rect = self.image.get_rect(midbottom = (random.randint(900, 1100), y_pos))


    def animation_state(self):
        self.animation_index += 0.1
        if self.animation_index >= len(self.frames):
            self.animation_index = 0
        self.image  = self.frames[int(self.animation_index)]


    def update(self):
        self.animation_state()
        self.rect.x -= 6
        self.destroy_object()

    
    def destroy_object(self):
        if self.rect.x <= -100:
            self.kill()


def display_score():
    current_time = int(pygame.time.get_ticks() / 1000)  - start_time
    score_surface = test_font.render(f"Score: {current_time}", True, (64, 64, 64))
    score_rect = score_surface.get_rect(center = (400, 30))
    screen.blit(score_surface, score_rect)
    return current_time


def collisions(player, obstacles):
    if obstacles:
        for obstacle_rect in obstacles:
            if player.colliderect(obstacle_rect):
                return False
    return True


def collision_sprite():
    if pygame.sprite.spritecollide(player.sprite, obstacle_group, False):
        obstacle_group.empty()
        return False
    else:
        return True


pygame.display.set_caption("Runner")
clock = pygame.time.Clock()
screen = pygame.display.set_mode((800, 400))
test_font = pygame.font.Font('font/Pixeltype.ttf', 50)
bg_music = pygame.mixer.Sound("audio/music.wav")
bg_music.set_volume(0.1)
bg_music.play(loops = -1)

ground_surface = pygame.image.load("graphics/ground.png").convert()
sky_surface = pygame.image.load("graphics/Sky.png").convert()

# Intro screen.
player_stand = pygame.image.load("graphics/player/player_stand.png").convert_alpha()
player_stand = pygame.transform.rotozoom(player_stand, 0, 2)
player_stand_rect = player_stand.get_rect(center = (400, 200))
game_title = test_font.render("Pixel Runner", True, (255, 255, 255))
game_title_rect = game_title.get_rect(center = (400, 50))
game_instruction = test_font.render("Press SPACE to run", True, (255, 255, 255))
game_instruction_rect =  game_instruction.get_rect(center = (400, 380))

# Timer.
obstacle_timer = pygame.USEREVENT + 1
pygame.time.set_timer(obstacle_timer, 1500)

snail_animation_timer = pygame.USEREVENT + 2
pygame.time.set_timer(snail_animation_timer, 500)

fly_animation_timer = pygame.USEREVENT + 3
pygame.time.set_timer(fly_animation_timer, 200)

start_time = 0
score = 0
game_active = False

# Groups.
player = pygame.sprite.GroupSingle()
player.add(Player())
obstacle_group = pygame.sprite.Group()

while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            sys.exit()

        if game_active:
            if event.type == obstacle_timer:
                obstacle_group.add(Obstacle(random.choice(['fly', 'fly', 'fly','snail', 'snail','snail', 'snail'])))
            
        else:
            if event.type == pygame.KEYDOWN and event.key == pygame.K_SPACE:
                game_active = True
                start_time = int(pygame.time.get_ticks() / 1000)

    if game_active:
        screen.blit(sky_surface, (0, 0))
        screen.blit(ground_surface, (0, 300))
        score = display_score()

        player.draw(screen)
        player.update()

        obstacle_group.draw(screen)
        obstacle_group.update()

        game_active = collision_sprite()
    else:
        screen.fill((94, 129, 162))

        screen.blit(player_stand, player_stand_rect)
        screen.blit(game_title, game_title_rect)
       
        score_message = test_font.render(f"Score: {score}", True, (255, 255, 255))
        score_message_rect = score_message.get_rect(center = (700, 50))

        if score == 0:
            screen.blit(game_instruction, game_instruction_rect)
        else:
            screen.blit(game_instruction, game_instruction_rect)
            screen.blit(score_message, score_message_rect)

    pygame.display.update()
    clock.tick(60)