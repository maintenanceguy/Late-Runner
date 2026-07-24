# player.py
# player class, keeps track of position, gravity and animation

import settings


class Player:
    def __init__(self, walk_frames, jump_frame):
        self.walk_frames = walk_frames
        self.jump_frame = jump_frame
        self.frame_index = 0
        self.image = self.walk_frames[0]
        self.rect = self.image.get_rect(bottomleft=(30, settings.GROUND_Y))
        self.gravity = 0

    def jump(self, jump_sound=None):
        # can only jump if standing on ground
        if self.rect.bottom >= settings.GROUND_Y:
            self.gravity = settings.JUMP_POWER
            if jump_sound is not None:
                jump_sound.play()

    def update(self):
        self.gravity += settings.GRAVITY
        self.rect.y += self.gravity

        if self.rect.bottom > settings.GROUND_Y:
            self.rect.bottom = settings.GROUND_Y

        self.animate()

    def animate(self):
        if self.rect.bottom < settings.GROUND_Y:
            self.image = self.jump_frame
        else:
            self.frame_index += 0.3
            if self.frame_index >= len(self.walk_frames):
                self.frame_index = 0
            self.image = self.walk_frames[int(self.frame_index)]

    def reset(self):
        self.rect.bottomleft = (80, settings.GROUND_Y)
        self.gravity = 0
        self.frame_index = 0
        self.image = self.walk_frames[0]

    def draw(self, screen):
        screen.blit(self.image, self.rect)
