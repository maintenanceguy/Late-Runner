import os
import sys
import pygame
import settings
from player import Player
from enemy import spawn_enemy
from file_manager import load_scores, save_score, get_high_score, get_average_score

class GameManager:
    def __init__(self):
        pygame.init()
        self.screen = pygame.display.set_mode((settings.SCREEN_WIDTH, settings.SCREEN_HEIGHT))
        pygame.display.set_caption("Late Runner")
        self.clock = pygame.time.Clock()

        self.load_assets()

        self.scores = load_scores(settings.SCORE_FILE)

        self.player = Player(self.player_walk_imgs, self.player_jump_img)
        self.enemies = []
        self.seen_enemy_types = set()

        self.running = True
        self.game_active = False
        self.start_time = 0
        self.current_score = 0

        self.spawn_event = pygame.USEREVENT + 1
        self.snail_anim_event = pygame.USEREVENT + 2
        self.fly_anim_event = pygame.USEREVENT + 3
        pygame.time.set_timer(self.spawn_event, settings.SPAWN_TIME)
        pygame.time.set_timer(self.snail_anim_event, settings.SNAIL_ANIM_TIME)
        pygame.time.set_timer(self.fly_anim_event, settings.FLY_ANIM_TIME)

    def load_image(self, path, size=(40, 40)):
        try:
            return pygame.image.load(path).convert_alpha()
        except (pygame.error, FileNotFoundError) as e:
            print("could not load image", path, e)
            image = pygame.Surface(size)
            image.fill((200, 50, 50))
            return image

    def load_sound(self, path):
        try:
            return pygame.mixer.Sound(path)
        except (pygame.error, FileNotFoundError) as e:
            print("could not load sound", path, e)
            return None

    def load_font(self, path, size):
        try:
            if not os.path.exists(path):
                raise FileNotFoundError(path)
            return pygame.font.Font(path, size)
        except (pygame.error, FileNotFoundError) as e:
            print("could not load font", path, e)
            return pygame.font.SysFont("arial", size)

    def load_assets(self):
        self.font = self.load_font(settings.FONT_PATH, 25)
        self.sky_img = self.load_image(settings.SKY_IMG, (800, 300))
        self.ground_img = self.load_image(settings.GROUND_IMG, (800, 100))

        self.player_walk_imgs = [self.load_image(p) for p in settings.PLAYER_WALK_IMGS]
        self.player_jump_img = self.load_image(settings.PLAYER_JUMP_IMG)
        self.player_stand_img = self.load_image(settings.PLAYER_STAND_IMG)

        self.frame_bank = {
            "snail": [self.load_image(p) for p in settings.SNAIL_IMGS],
            "fly": [self.load_image(p) for p in settings.FLY_IMGS],
        }

        self.music = self.load_sound(settings.MUSIC_PATH)
        if self.music is not None:
            self.music.play(loops=-1)
            self.music.set_volume(0.2)

        self.jump_sound = self.load_sound(settings.JUMP_SOUND_PATH)
        if self.jump_sound is not None:
            self.jump_sound.set_volume(0.1)

    # game logic helpers
    def get_current_score(self):
        return int(pygame.time.get_ticks() / 1000) - self.start_time

    def get_enemy_speed(self, score):
        return settings.BASE_SPEED + (score // settings.SPEED_DIVIDER)

    def spawn_new_enemy(self):
        enemy = spawn_enemy(self.frame_bank, self.seen_enemy_types)
        self.enemies.append(enemy)

    def update_enemies(self, score):
        speed = self.get_enemy_speed(score)
        for enemy in self.enemies:
            enemy.update(speed)
            enemy.draw(self.screen)
        self.enemies = [e for e in self.enemies if not e.off_screen()]

    def check_collision(self):
        for enemy in self.enemies:
            if self.player.rect.colliderect(enemy.rect):
                return True
        return False

    def start_run(self):
        self.game_active = True
        self.start_time = int(pygame.time.get_ticks() / 1000)

    def end_run(self):
        self.game_active = False
        self.scores.append(self.current_score)
        save_score(settings.SCORE_FILE, self.scores)
        self.enemies.clear()
        self.seen_enemy_types.clear()
        self.player.reset()

    # drawing
    def draw_gameplay(self):
        self.screen.blit(self.sky_img, (0, 0))
        self.screen.blit(self.ground_img, (0, settings.GROUND_Y))

        self.current_score = self.get_current_score()
        score_text = self.font.render(f"Point: {self.current_score}", False, settings.SCORE_COLOR)
        self.screen.blit(score_text, (35, 20))

        self.player.update()
        self.player.draw(self.screen)

        self.update_enemies(self.current_score)

        if self.check_collision():
            self.end_run()

    def draw_menu(self):
        self.screen.fill(settings.BG_COLOR)

        stand_rect = self.player_stand_img.get_rect(center=(400, 200))
        self.screen.blit(self.player_stand_img, stand_rect)

        title_text = self.font.render("Late Runner", False, settings.TEXT_COLOR)
        self.screen.blit(title_text, (330, 80))

        if not self.scores:
            prompt = self.font.render("Press space to start", False, settings.TEXT_COLOR)
            self.screen.blit(prompt, (280, 280))
        else:
            last_score = self.scores[-1]
            high_score = get_high_score(self.scores)
            avg_score = get_average_score(self.scores)

            last_text = self.font.render(f"Your score is: {last_score}", False, settings.TEXT_COLOR)
            self.screen.blit(last_text, (290, 290))

            high_text = self.font.render(f"Best: {high_score}", False, settings.TEXT_COLOR)
            self.screen.blit(high_text, (350, 250))

            avg_text = self.font.render(
                f"Games played: {len(self.scores)}  Avg: {avg_score}", False, settings.TEXT_COLOR
            )
            self.screen.blit(avg_text, (220, 330))

    # events
    def handle_events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.running = False

            elif event.type == pygame.KEYDOWN and event.key == pygame.K_SPACE:
                if self.game_active:
                    self.player.jump(self.jump_sound)
                else:
                    self.start_run()

            elif event.type == self.spawn_event and self.game_active:
                self.spawn_new_enemy()

            elif self.game_active and event.type == self.snail_anim_event:
                for enemy in self.enemies:
                    if enemy.type == "snail":
                        enemy.animate()

            elif self.game_active and event.type == self.fly_anim_event:
                for enemy in self.enemies:
                    if enemy.type == "fly":
                        enemy.animate()

    def run(self):
        while self.running:
            self.handle_events()

            if self.game_active:
                self.draw_gameplay()
            else:
                self.draw_menu()

            pygame.display.update()
            self.clock.tick(settings.FPS)

        pygame.quit()
        sys.exit()
