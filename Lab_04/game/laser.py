import pygame

LASER_SPEED = 10
LASER_LENGTH = 18
LASER_WIDTH = 4

class Laser:
    def __init__(self, x, y):
        # (x, y) is the muzzle: the bottom end of the beam
        self.x = x
        self.y = y

    @property
    def rect(self):
        return pygame.Rect(int(self.x) - LASER_WIDTH // 2, int(self.y) - LASER_LENGTH,
                           LASER_WIDTH, LASER_LENGTH)

    def update(self):
        self.y -= LASER_SPEED

    def off_screen(self):
        return self.y < 0

    def hits(self, meteor):
        # circle (meteor) vs rectangle (laser): find the closest point on the beam
        r = self.rect
        nx = max(r.left, min(meteor.x, r.right))
        ny = max(r.top, min(meteor.y, r.bottom))
        return (meteor.x - nx) ** 2 + (meteor.y - ny) ** 2 < meteor.radius ** 2

    def draw(self, screen):
        r = self.rect
        pygame.draw.rect(screen, (90, 255, 140), r, border_radius=2)
        pygame.draw.rect(screen, (230, 255, 235), r.inflate(-2, 0), border_radius=2)