import random

# dictionary that says where each enemy type spawns
ENEMY_SPAWN_DATA = {
    "snail": {"x_range": (1100, 1400), "bottom": 300},
    "fly": {"x_range": (900, 1100), "bottom": 210},
}


class Enemy:
    def __init__(self, enemy_type, frames, x, bottom):
        self.type = enemy_type
        self.frames = frames
        self.frame_index = 0
        self.image = frames[0]
        self.rect = self.image.get_rect(bottomright=(x, bottom))

    def update(self, speed):
        self.rect.left -= speed

    def animate(self):
        self.frame_index = 1 - self.frame_index
        self.image = self.frames[self.frame_index]

    def draw(self, screen):
        screen.blit(self.image, self.rect)

    def off_screen(self):
        return self.rect.left <= -100


def spawn_enemy(frame_bank, seen_types):
    enemy_type = random.choice(list(ENEMY_SPAWN_DATA.keys()))
    seen_types.add(enemy_type)

    data = ENEMY_SPAWN_DATA[enemy_type]
    x = random.randint(*data["x_range"])
    bottom = data["bottom"]
    frames = frame_bank[enemy_type]

    return Enemy(enemy_type, frames, x, bottom)
