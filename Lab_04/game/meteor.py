import pygame
import random
import math

LARGE_RADIUS = 20   # meteors at or above this radius split when destroyed

class Meteor:
    def __init__(self, width, x=None, y=None, radius=None, vx=None, vy=None):
        # With no arguments this spawns a random meteor above the screen.
        # Fragments created by split() pass their own position/size/velocity.
        self.x = random.randint(0, width) if x is None else x
        self.y = -30 if y is None else y
        self.radius = random.randint(12, 28) if radius is None else radius
        if vx is None or vy is None:
            angle = random.uniform(70,110)
            speed = random.uniform(2,5)
            vx = math.cos(math.radians(angle))*speed
            vy = math.sin(math.radians(angle))*speed
        self.vx = vx
        self.vy = vy
        self.color = (
            random.randint(160,220),
            random.randint(80,120),
            random.randint(40,80)
        )
        self.rot = 0
        self.rot_speed = random.uniform(-3,3)

    def is_large(self):
        return self.radius >= LARGE_RADIUS

    def split(self):
        """Large meteors break into 2-3 smaller fragments that fly apart.
        Small meteors return an empty list (they dissolve completely)."""
        if not self.is_large():
            return []
        offsets = random.choice([[-40, 40], [-50, 0, 50]])
        child_radius = max(8, self.radius // 2)
        fragments = []
        for off in offsets:
            a = math.radians(off + random.uniform(-10, 10))
            # rotate the parent's velocity by 'a' so fragments diverge outwards
            vx = self.vx*math.cos(a) - self.vy*math.sin(a)
            vy = self.vx*math.sin(a) + self.vy*math.cos(a)
            boost = random.uniform(1.0, 1.4)
            frag = Meteor(0, x=self.x, y=self.y, radius=child_radius,
                          vx=vx*boost, vy=vy*boost)
            frag.color = self.color
            fragments.append(frag)
        return fragments

    def update(self):
        self.x+=self.vx; self.y+=self.vy
        self.rot=(self.rot+self.rot_speed)%360

    def off_screen(self, width, height):
        return self.y > height + 60 or self.x < -60 or self.x > width + 60

    def collides(self, rect):
        cx,cy=rect.centerx,rect.centery
        dx,dy=self.x-cx,self.y-cy
        return (dx**2+dy**2)**0.5 < self.radius + 16

    def draw(self, screen):
        import math
        pts=[]
        for i in range(7):
            angle=math.radians(self.rot+i*(360/7))
            r=self.radius*(0.8+0.2*(i%2))
            pts.append((int(self.x+r*math.cos(angle)),int(self.y+r*math.sin(angle))))
        pygame.draw.polygon(screen,self.color,pts)
        inner=[(int(self.x+(r*0.5)*math.cos(math.radians(self.rot+i*(360/7)))),
                int(self.y+(r*0.5)*math.sin(math.radians(self.rot+i*(360/7)))))
               for i,(cx,cy) in enumerate(pts)]
        pygame.draw.polygon(screen,tuple(max(0,c-40) for c in self.color),inner)


class ShieldOrb:
    """A glowing energy orb that drifts down the screen, swaying side to side."""
    def __init__(self, width):
        self.base_x = random.randint(60, width - 60)
        self.x = self.base_x
        self.y = -20
        self.vy = random.uniform(1.2, 2.0)
        self.t = random.uniform(0, 6.28)
        self.radius = 13

    def update(self):
        self.y += self.vy
        self.t += 0.05
        self.x = self.base_x + math.sin(self.t) * 40

    def off_screen(self, height):
        return self.y > height + 30

    def collides(self, rect):
        dx, dy = self.x - rect.centerx, self.y - rect.centery
        return (dx**2 + dy**2) ** 0.5 < self.radius + 16

    def draw(self, screen):
        pulse = 1 + 0.15 * math.sin(self.t * 3)
        r = int(self.radius * pulse)
        cx, cy = int(self.x), int(self.y)
        glow = pygame.Surface((r*4, r*4), pygame.SRCALPHA)
        pygame.draw.circle(glow, (80, 220, 255, 60), (r*2, r*2), r*2)
        screen.blit(glow, (cx - r*2, cy - r*2))
        pygame.draw.circle(screen, (80, 220, 255), (cx, cy), r)
        pygame.draw.circle(screen, (220, 250, 255), (cx, cy), max(2, r // 2))