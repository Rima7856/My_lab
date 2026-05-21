import pygame
import random
import math
import sys

# --- CONFIGURATION & CONSTANTS ---
SCREEN_WIDTH = 1000
SCREEN_HEIGHT = 650
FPS = 60

# Colors
COLOR_BG = (30, 100, 30)
COLOR_LAWN_1 = (100, 200, 50)
COLOR_LAWN_2 = (90, 190, 40)
COLOR_HOUSE = (180, 100, 80)
COLOR_ROOF = (140, 60, 50)
COLOR_UI_BG = (80, 60, 40)
COLOR_SUN = (255, 215, 0)
COLOR_ZOMBIE_SKIN = (150, 200, 150)
COLOR_ZOMBIE_SUIT = (60, 60, 80)
COLOR_PEA = (0, 255, 0)
COLOR_CHERRY = (200, 0, 0)
COLOR_NUT = (180, 140, 50)
COLOR_ICE_BLOOM = (0, 150, 255)
COLOR_WIN = (100, 200, 255)
COLOR_LOSE = (150, 50, 50)
COLOR_WAVE_MARKER = (255, 100, 100)

# Grid Settings
GRID_ROWS = 5
GRID_COLS = 9
CELL_SIZE = 80
GRID_OFFSET_X = 180
GRID_OFFSET_Y = 200 

# Game Settings
SUN_VALUE = 25
STARTING_SUN = 150
GAME_DURATION = 10800  # 3 минуты

# Wave Settings - ДОБАВЛЕНА ТРЕТЬЯ ВОЛНА
WAVE_1_START = 3000    # 50 секунд
WAVE_1_END = 4200      # 70 секунд
BREAK_START = 4200     # Начало перерыва
BREAK_END = 5400       # Конец перерыва (90 секунд)
WAVE_2_START = 5400    # 90 секунд
WAVE_2_END = 7200      # 120 секунд
WAVE_3_START = 9000    # 150 секунд (30 секунд до конца)
WAVE_3_END = 10200     # 170 секунд (20 секунд длительность)

# --- ASSET GENERATION ---

def draw_house_facade(surface, rect):
    x, y, w, h = rect
    pygame.draw.rect(surface, (200, 160, 140), (x, y, w, h))
    roof_points = [(x - 10, y), (x + w + 10, y), (x + w/2, y - 60)]
    pygame.draw.polygon(surface, COLOR_ROOF, roof_points)
    for i in range(0, w + 20, 15):
        for j in range(0, 60, 10):
            shingle_y = y - 10 - j
            shingle_x = x - 5 + i + (j % 20)
            pygame.draw.rect(surface, (100, 40, 30), (shingle_x, shingle_y, 14, 8))
    win_rect = pygame.Rect(x + 30, y + 40, 50, 60)
    pygame.draw.rect(surface, (100, 150, 255), win_rect)
    pygame.draw.rect(surface, (255, 255, 255), win_rect, 4)
    pygame.draw.line(surface, (255, 255, 255), (win_rect.left+5, win_rect.top+5), (win_rect.right-5, win_rect.top+5), 2)
    door_rect = pygame.Rect(x + 100, y + 60, 50, 90)
    pygame.draw.rect(surface, (100, 60, 40), door_rect)
    pygame.draw.circle(surface, (255, 215, 0), (door_rect.right - 10, door_rect.centery), 4)
    pygame.draw.rect(surface, (50, 50, 50), (x + w - 5, y, 5, h))

def draw_lawn_grid(surface):
    for r in range(GRID_ROWS):
        for c in range(GRID_COLS):
            x = GRID_OFFSET_X + c * CELL_SIZE
            y = GRID_OFFSET_Y + r * CELL_SIZE
            color = COLOR_LAWN_1 if (r + c) % 2 == 0 else COLOR_LAWN_2
            pygame.draw.rect(surface, color, (x, y, CELL_SIZE, CELL_SIZE))
            if random.random() > 0.8:
                pygame.draw.line(surface, (80, 180, 30), (x+10, y+70), (x+15, y+60), 1)

# --- CLASSES ---

class Sun:
    def __init__(self, x, y, is_natural=True):
        self.x = x
        self.y = y
        self.target_y = y
        self.radius = 25
        self.value = SUN_VALUE
        self.is_natural = is_natural
        self.spawn_time = pygame.time.get_ticks()
        self.lifetime = 8000
        self.collected = False
        self.velocity = 0
        self.max_velocity = 3
        self.float_offset = 0
        if is_natural:
            self.y = -50

    def update(self):
        self.float_offset = math.sin(pygame.time.get_ticks() / 200) * 3
        if self.is_natural and self.y < self.target_y:
            self.velocity += 0.2
            if self.velocity > self.max_velocity: self.velocity = self.max_velocity
            self.y += self.velocity
        elif not self.is_natural:
            if self.y > self.target_y - 20:
                self.y -= 1

    def draw(self, surface):
        if self.collected: return
        draw_y = self.y + self.float_offset
        pygame.draw.circle(surface, COLOR_SUN, (int(self.x), int(draw_y)), self.radius)
        for i in range(8):
            angle = i * (360 / 8)
            rad = math.radians(angle)
            sx = self.x + math.cos(rad) * (self.radius + 5)
            sy = draw_y + math.sin(rad) * (self.radius + 5)
            ex = self.x + math.cos(rad) * (self.radius + 15)
            ey = draw_y + math.sin(rad) * (self.radius + 15)
            pygame.draw.line(surface, (255, 255, 200), (sx, sy), (ex, ey), 3)

    def check_click(self, pos):
        dist = math.hypot(pos[0] - self.x, pos[1] - (self.y + self.float_offset))
        if dist < self.radius + 10:
            self.collected = True
            return True
        return False

    def is_expired(self):
        return pygame.time.get_ticks() - self.spawn_time > self.lifetime

class Projectile:
    def __init__(self, x, y, row):
        self.x = x
        self.y = y
        self.row = row
        self.speed = 7
        self.damage = 20
        self.radius = 8
        self.active = True

    def update(self):
        self.x += self.speed
        if self.x > SCREEN_WIDTH:
            self.active = False

    def draw(self, surface):
        pygame.draw.circle(surface, COLOR_PEA, (int(self.x), int(self.y)), self.radius)
        pygame.draw.circle(surface, (200, 255, 200), (int(self.x)-2, int(self.y)-2), 3)

class Particle:
    def __init__(self, x, y, color):
        self.x = x
        self.y = y
        self.color = color
        self.vx = random.uniform(-3, 3)
        self.vy = random.uniform(-3, 3)
        self.life = 30
        self.size = random.randint(3, 6)

    def update(self):
        self.x += self.vx
        self.y += self.vy
        self.life -= 1
        self.size = max(0, self.size - 0.2)

    def draw(self, surface):
        if self.life > 0:
            pygame.draw.circle(surface, self.color, (int(self.x), int(self.y)), int(self.size))

class Lawnmower:
    def __init__(self, row):
        self.row = row
        self.x = GRID_OFFSET_X - 60
        self.y = GRID_OFFSET_Y + row * CELL_SIZE + 10
        self.width = 50
        self.height = 60
        self.active = True
        self.speed = 0
        self.max_speed = 8
        self.triggered = False

    def update(self):
        if self.triggered:
            self.speed = min(self.speed + 0.5, self.max_speed)
            self.x += self.speed
            if self.x > SCREEN_WIDTH:
                self.active = False

    def draw(self, surface):
        if not self.active: return
        pygame.draw.rect(surface, (200, 50, 50), (self.x, self.y, self.width, self.height))
        pygame.draw.line(surface, (100, 100, 100), (self.x + 10, self.y), (self.x - 20, self.y - 40), 5)
        pygame.draw.circle(surface, (50, 50, 50), (int(self.x + 10), int(self.y + self.height)), 10)
        pygame.draw.circle(surface, (50, 50, 50), (int(self.x + self.width - 10), int(self.y + self.height)), 10)
        if self.triggered:
             pygame.draw.line(surface, (255, 255, 255), (self.x, self.y-10), (self.x-10, self.y-20), 2)

    def check_collision(self, zombie):
        if self.triggered and zombie.row == self.row:
            zombie.health = 0
            zombie.dead = True
            return True
        if not self.triggered and zombie.x < self.x + self.width and zombie.row == self.row:
            self.triggered = True
            return True
        return False

class Plant:
    def __init__(self, col, row, p_type):
        self.col = col
        self.row = row
        self.x = GRID_OFFSET_X + col * CELL_SIZE + CELL_SIZE // 2
        self.y = GRID_OFFSET_Y + row * CELL_SIZE + CELL_SIZE // 2
        self.type = p_type
        self.health = 100
        self.max_health = 100
        self.timer = 0
        self.shoot_timer = 0
        self.dead = False
        
        if self.type == 'sunflower':
            self.max_health = 8000
            self.health = 8000
        elif self.type == 'wallnut':
            self.max_health = 400
            self.health = 40000
        elif self.type == 'cherrybomb':
            self.max_health = 100000
            self.timer = 1
        elif self.type == 'icebloom':
            self.max_health = 1000000
            self.timer = 1

    def update(self, zombies, projectiles, particles):
        self.timer += 1
        if self.type == 'peashooter':
            zombie_in_lane = any(z.row == self.row and z.x > self.x for z in zombies)
            if zombie_in_lane and self.shoot_timer > 90:
                projectiles.append(Projectile(self.x + 20, self.y, self.row))
                self.shoot_timer = 0
            self.shoot_timer += 1
        elif self.type == 'sunflower':
            if self.timer % 500 == 0: 
                game.suns.append(Sun(self.x, self.y - 40, is_natural=False))
        elif self.type == 'cherrybomb':
            if self.timer >= 60:
                for _ in range(30):
                    particles.append(Particle(self.x, self.y, (255, 100, 0)))
                    particles.append(Particle(self.x, self.y, (50, 50, 50)))
                for z in zombies:
                    z_col = (z.x - GRID_OFFSET_X) // CELL_SIZE
                    z_row = z.row
                    if abs(z_col - self.col) <= 1 and abs(z_row - self.row) <= 1:
                        z.health -= 1000
                        z.flash_time = 10
                        z.dead = True
                self.dead = True
        elif self.type == 'icebloom':
            if self.timer >= 60:
                for _ in range(40):
                    particles.append(Particle(self.x, self.y, (0, 200, 255)))
                    particles.append(Particle(self.x, self.y, (200, 255, 255)))
                for z in zombies:
                    z_col = (z.x - GRID_OFFSET_X) // CELL_SIZE
                    z_row = z.row
                    if abs(z_col - self.col) <= 1 and abs(z_row - self.row) <= 1:
                        z.frozen = True
                        z.freeze_timer = 300
                self.dead = True

    def draw(self, surface):
        if self.dead: return
        cx, cy = int(self.x), int(self.y)
        if self.type == 'peashooter':
            pygame.draw.rect(surface, (0, 150, 0), (cx - 5, cy, 10, 30))
            pygame.draw.circle(surface, (0, 200, 0), (cx, cy - 10), 20)
            pygame.draw.circle(surface, (0, 180, 0), (cx + 15, cy - 10), 12)
            pygame.draw.circle(surface, (0, 100, 0), (cx + 20, cy - 10), 8)
            pygame.draw.circle(surface, (255, 255, 255), (cx - 5, cy - 15), 5)
            pygame.draw.circle(surface, (0, 0, 0), (cx - 5, cy - 15), 2)
        elif self.type == 'icebloom':
            pygame.draw.rect(surface, (0, 100, 150), (cx - 4, cy, 8, 25))
            pygame.draw.circle(surface, (0, 180, 255), (cx, cy - 10), 18)
            for i in range(6):
                angle = i * 60
                rad = math.radians(angle)
                px = cx + math.cos(rad) * 24
                py = (cy - 10) + math.sin(rad) * 24
                pygame.draw.ellipse(surface, (150, 230, 255), (px-10, py-5, 20, 10))
            pygame.draw.circle(surface, (200, 255, 255), (cx, cy - 10), 8)
            ratio = self.timer / 60.0
            pygame.draw.circle(surface, (255, 255, 255), (cx, cy - 10), int(18 * ratio), 2)
        elif self.type == 'sunflower':
            pygame.draw.rect(surface, (0, 150, 0), (cx - 4, cy, 8, 30))
            pygame.draw.circle(surface, (255, 200, 0), (cx, cy - 10), 22)
            for i in range(8):
                angle = i * 45
                rad = math.radians(angle)
                px = cx + math.cos(rad) * 28
                py = (cy - 10) + math.sin(rad) * 28
                pygame.draw.ellipse(surface, (255, 220, 0), (px-8, py-4, 16, 8))
            pygame.draw.arc(surface, (0, 0, 0), (cx - 10, cy - 15, 20, 15), 3.14, 0, 2)
            pygame.draw.circle(surface, (0, 0, 0), (cx - 8, cy - 15), 3)
            pygame.draw.circle(surface, (0, 0, 0), (cx + 8, cy - 15), 3)
        elif self.type == 'wallnut':
            pygame.draw.ellipse(surface, COLOR_NUT, (cx - 15, cy - 20, 30, 40))
            if self.health < 200:
                pygame.draw.line(surface, (50, 30, 0), (cx, cy), (cx+5, cy+5), 2)
            if self.health < 100:
                pygame.draw.line(surface, (50, 30, 0), (cx-5, cy-5), (cx+5, cy+10), 2)
            pygame.draw.circle(surface, (255, 255, 255), (cx - 8, cy - 10), 4)
            pygame.draw.circle(surface, (255, 255, 255), (cx + 8, cy - 10), 4)
            pygame.draw.circle(surface, (0, 0, 0), (cx - 8, cy - 10), 1)
            pygame.draw.circle(surface, (0, 0, 0), (cx + 8, cy - 10), 1)
        elif self.type == 'cherrybomb':
            ratio = self.timer / 60.0
            radius = int(20 * ratio)
            pygame.draw.circle(surface, COLOR_CHERRY, (cx, cy), radius)
            pygame.draw.line(surface, (100, 100, 100), (cx, cy-20), (cx+10, cy-30), 3)
            if self.timer % 10 < 5:
                pygame.draw.circle(surface, (255, 255, 0), (cx+10, cy-30), 3)

class Zombie:
    def __init__(self, row, wave_level=0):
        self.row = row
        self.x = SCREEN_WIDTH + random.randint(0, 100)
        self.y = GRID_OFFSET_Y + row * CELL_SIZE + 10
        self.width = 40
        self.height = 60
        # Скорость и здоровье зависят от уровня волны
        self.speed =  0.5
        self.base_speed = self.speed
        self.health = 100 + (wave_level * 20)
        self.max_health = self.health
        self.dead = False
        self.eating = False
        self.flash_time = 0
        self.wobble_offset = random.randint(0, 100)
        self.frozen = False
        self.freeze_timer = 0
        self.wave_level = wave_level

    def update(self, plants):
        if self.dead: return
        if self.frozen:
            self.freeze_timer -= 1
            if self.freeze_timer <= 0:
                self.frozen = False
                self.speed = self.base_speed
        self.eating = False
        moving = True
        for plant in plants:
            if plant.row == self.row and not plant.dead:
                if self.x < plant.x + 20 and self.x + self.width > plant.x - 20:
                    self.eating = True
                    moving = False
                    plant.health -= 0.5
                    if plant.health <= 0:
                        plant.dead = True
                    break
        if moving:
            if self.frozen:
                self.x -= self.speed * 0.2
            else:
                self.x -= self.speed
        self.wobble = math.sin((pygame.time.get_ticks() / 200) + self.wobble_offset) * 3
        if self.flash_time > 0:
            self.flash_time -= 1

    def draw(self, surface):
        if self.dead: return
        cx = int(self.x + self.width/2)
        cy = int(self.y + self.height/2)
        color = COLOR_ZOMBIE_SKIN
        # Разные цвета для разных уровней волн
        if self.wave_level == 1:
            color = (140, 190, 140)
        elif self.wave_level == 2:
            color = (130, 180, 130)
        elif self.wave_level >= 3:
            color = (120, 170, 120)  # Самый тёмный для волны 3
        if self.frozen:
            color = (150, 200, 255)
        if self.flash_time > 0:
            color = (255, 0, 0)
        pygame.draw.rect(surface, COLOR_ZOMBIE_SUIT, (self.x + self.wobble, self.y + 20, self.width, 40))
        pygame.draw.polygon(surface, (200, 50, 50), [(cx + self.wobble, 25), (cx - 5 + self.wobble, 40), (cx + 5 + self.wobble, 40)])
        head_y = self.y + self.wobble
        pygame.draw.ellipse(surface, color, (self.x + 5 + self.wobble, head_y - 10, 30, 30))
        pygame.draw.circle(surface, (255, 255, 255), (int(self.x + 15 + self.wobble), int(head_y)), 6)
        pygame.draw.circle(surface, (255, 255, 255), (int(self.x + 25 + self.wobble), int(head_y)), 6)
        pygame.draw.circle(surface, (0, 0, 0), (int(self.x + 15 + self.wobble), int(head_y)), 2)
        pygame.draw.circle(surface, (0, 0, 0), (int(self.x + 25 + self.wobble), int(head_y)), 2)
        if self.frozen:
            pygame.draw.circle(surface, (200, 255, 255), (int(self.x + 15 + self.wobble), int(head_y)), 8)
            pygame.draw.circle(surface, (200, 255, 255), (int(self.x + 25 + self.wobble), int(head_y)), 8)
            for i in range(3):
                px = self.x + random.randint(0, self.width)
                py = self.y + random.randint(0, self.height)
                pygame.draw.circle(surface, (200, 255, 255), (int(px), int(py)), 2)
        arm_y = self.y + 30
        if self.eating:
            pygame.draw.line(surface, COLOR_ZOMBIE_SUIT, (self.x + 10 + self.wobble, arm_y), (self.x - 10, arm_y), 4)
        else:
            pygame.draw.line(surface, COLOR_ZOMBIE_SUIT, (self.x + 10 + self.wobble, arm_y), (self.x - 5, arm_y + 10), 4)

class VictoryFirework:
    def __init__(self):
        self.x = random.randint(100, SCREEN_WIDTH - 100)
        self.y = SCREEN_HEIGHT
        self.vy = -random.randint(5, 10)
        self.color = random.choice([(255, 0, 0), (0, 255, 0), (0, 0, 255), (255, 255, 0), (255, 0, 255)])
        self.exploded = False
        self.particles = []
        self.timer = 0

    def update(self):
        if not self.exploded:
            self.y += self.vy
            self.vy += 0.2
            if self.vy >= 0:
                self.exploded = True
                for _ in range(50):
                    self.particles.append(Particle(self.x, self.y, self.color))
        else:
            self.timer += 1
            for p in self.particles[:]:
                p.update()
                if p.life <= 0:
                    self.particles.remove(p)

    def draw(self, surface):
        if not self.exploded:
            pygame.draw.circle(surface, self.color, (int(self.x), int(self.y)), 5)
        else:
            for p in self.particles:
                p.draw(surface)

# --- GAME ENGINE ---

class Game:
    def __init__(self):
        pygame.init()
        self.screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
        pygame.display.set_caption("Plants vs. Zombies Clone (Python/PyGame)")
        self.clock = pygame.time.Clock()
        self.font = pygame.font.SysFont('Arial', 20, bold=True)
        self.big_font = pygame.font.SysFont('Arial', 40, bold=True)
        self.reset_game()

    def reset_game(self):
        self.sun_count = STARTING_SUN
        self.suns = []
        self.plants = []
        self.zombies = []
        self.projectiles = []
        self.particles = []
        self.lawnmowers = [Lawnmower(r) for r in range(GRID_ROWS)]
        self.grid_occupied = [[False for _ in range(GRID_COLS)] for _ in range(GRID_ROWS)]
        self.selected_plant = None
        # ИЗМЕНЕНИЕ: Уменьшена стоимость Ice Bloom с 75 до 50
        self.plant_costs = {'peashooter': 100, 'sunflower': 50, 'wallnut': 50, 'cherrybomb': 150, 'icebloom': 50}
        self.game_over = False
        self.game_won = False
        self.game_timer = GAME_DURATION
        self.wave_timer = 0
        self.spawn_interval = 1000
        self.huge_wave_active = False
        self.current_wave = 0
        self.fireworks = []
        self.end_screen_timer = 0
        
    def get_wave_status(self):
        elapsed = GAME_DURATION - self.game_timer
        if WAVE_1_START <= elapsed < WAVE_1_END:
            return 1
        elif BREAK_START <= elapsed < BREAK_END:
            return 2
        elif WAVE_2_START <= elapsed < WAVE_2_END:
            return 3
        elif WAVE_3_START <= elapsed < WAVE_3_END:
            return 4  # Волна 3
        return 0
        
    def handle_input(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return False
            if event.type == pygame.MOUSEBUTTONDOWN:
                mx, my = pygame.mouse.get_pos()
                if self.game_over or self.game_won:
                    keys = pygame.key.get_pressed()
                    if keys[pygame.K_r]:
                        self.reset_game()
                    return True
                if my < GRID_OFFSET_Y:
                    if 180 < mx < 245: self.selected_plant = 'peashooter'
                    elif 255 < mx < 320: self.selected_plant = 'sunflower'
                    elif 330 < mx < 395: self.selected_plant = 'wallnut'
                    elif 405 < mx < 470: self.selected_plant = 'cherrybomb'
                    elif 480 < mx < 545: self.selected_plant = 'icebloom'
                elif self.selected_plant:
                    if GRID_OFFSET_X <= mx < SCREEN_WIDTH and GRID_OFFSET_Y <= my < SCREEN_HEIGHT:
                        col = (mx - GRID_OFFSET_X) // CELL_SIZE
                        row = (my - GRID_OFFSET_Y) // CELL_SIZE
                        if 0 <= col < GRID_COLS and 0 <= row < GRID_ROWS:
                            if not self.grid_occupied[row][col]:
                                cost = self.plant_costs[self.selected_plant]
                                if self.sun_count >= cost:
                                    self.sun_count -= cost
                                    self.plants.append(Plant(col, row, self.selected_plant))
                                    self.grid_occupied[row][col] = True
                                    self.selected_plant = None
                for sun in self.suns:
                    if sun.check_click((mx, my)):
                        self.sun_count += sun.value
        return True

    def update(self):
        if self.game_over or self.game_won:
            self.end_screen_timer += 1
            if self.game_won and self.end_screen_timer % 30 == 0:
                self.fireworks.append(VictoryFirework())
            for fw in self.fireworks[:]:
                fw.update()
                if fw.exploded and fw.timer > 60:
                    self.fireworks.remove(fw)
            return
            
        self.game_timer -= 1
        if self.game_timer <= 0:
            self.game_won = True
            return
            
        self.wave_timer += 1
        wave_status = self.get_wave_status()
        
        if wave_status != self.current_wave:
            self.current_wave = wave_status
        
        # Логика спавна зомби
        if wave_status == 1:  # Волна 1
            if not self.huge_wave_active:
                self.huge_wave_active = True
                for _ in range(3):
                    r = random.randint(0, GRID_ROWS - 1)
                    self.zombies.append(Zombie(r, wave_level=1))
            if self.wave_timer % 150 == 0:
                r = random.randint(0, GRID_ROWS - 1)
                self.zombies.append(Zombie(r, wave_level=1))
                
        elif wave_status == 2:  # Перерыв
            self.huge_wave_active = False
            
        elif wave_status == 3:  # Волна 2
            if not self.huge_wave_active:
                self.huge_wave_active = True
                for _ in range(6):
                    r = random.randint(0, GRID_ROWS - 1)
                    self.zombies.append(Zombie(r, wave_level=2))
            if self.wave_timer % 90 == 0:
                r = random.randint(0, GRID_ROWS - 1)
                self.zombies.append(Zombie(r, wave_level=2))
                
        elif wave_status == 4:  # Волна 3 - САМАЯ СЛОЖНАЯ
            if not self.huge_wave_active:
                self.huge_wave_active = True
                # ИЗМЕНЕНИЕ: 8 зомби в начале волны 3
                for _ in range(8):
                    r = random.randint(0, GRID_ROWS - 1)
                    self.zombies.append(Zombie(r, wave_level=3))
            # ИЗМЕНЕНИЕ: Очень частый спавн (каждые 60 кадров = 1 секунда)
            if self.wave_timer % 60 == 0:
                r = random.randint(0, GRID_ROWS - 1)
                self.zombies.append(Zombie(r, wave_level=3))
        else:  # Обычное время
            self.huge_wave_active = False
            if self.wave_timer % self.spawn_interval == 0:
                r = random.randint(0, GRID_ROWS - 1)
                self.zombies.append(Zombie(r, wave_level=0))

        for sun in self.suns[:]:
            sun.update()
            if sun.is_expired() or sun.collected:
                self.suns.remove(sun)
        for plant in self.plants:
            plant.update(self.zombies, self.projectiles, self.particles)
            if plant.dead:
                self.grid_occupied[plant.row][plant.col] = False
                self.plants.remove(plant)
        for proj in self.projectiles[:]:
            proj.update()
            if not proj.active:
                self.projectiles.remove(proj)
            else:
                for z in self.zombies:
                    if z.row == proj.row and abs(z.x - proj.x) < 30:
                        z.health -= proj.damage
                        z.flash_time = 5
                        proj.active = False
                        if z.health <= 0:
                            z.dead = True
                            for _ in range(5):
                                self.particles.append(Particle(z.x, z.y, (100, 200, 100)))
                        break
        for z in self.zombies[:]:
            z.update(self.plants)
            if z.dead:
                self.zombies.remove(z)
            elif z.x < GRID_OFFSET_X - 50:
                self.game_over = True
        for mower in self.lawnmowers:
            mower.update()
            for z in self.zombies:
                if mower.check_collision(z):
                    pass
            if not mower.active:
                self.lawnmowers.remove(mower)
        for p in self.particles[:]:
            p.update()
            if p.life <= 0:
                self.particles.remove(p)

    def draw(self):
        self.screen.fill(COLOR_BG)
        draw_house_facade(self.screen, (0, 0, GRID_OFFSET_X, GRID_OFFSET_Y + GRID_ROWS * CELL_SIZE))
        draw_lawn_grid(self.screen)
        for mower in self.lawnmowers:
            mower.draw(self.screen)
        for plant in self.plants:
            plant.draw(self.screen)
        for z in self.zombies:
            z.draw(self.screen)
        for proj in self.projectiles:
            proj.draw(self.screen)
        for p in self.particles:
            p.draw(self.screen)
        for sun in self.suns:
            sun.draw(self.screen)
            
        # UI Bar
        pygame.draw.rect(self.screen, COLOR_UI_BG, (0, 0, SCREEN_WIDTH, GRID_OFFSET_Y))
        pygame.draw.line(self.screen, (0,0,0), (0, GRID_OFFSET_Y), (SCREEN_WIDTH, GRID_OFFSET_Y), 3)
        
        # Sun Counter
        sun_text = self.big_font.render(f"Sun: {self.sun_count}", True, (255, 255, 0))
        self.screen.blit(sun_text, (20, 5))
        
        # Timer Display
        minutes = self.game_timer // 3600
        seconds = (self.game_timer % 3600) // 60
        timer_text = self.big_font.render(f"Time: {minutes}:{seconds:02d}", True, (255, 255, 255))
        self.screen.blit(timer_text, (SCREEN_WIDTH - 280, 5))
        
        # Progress Bar
        progress_width = 280
        progress_height = 22
        progress_x = (SCREEN_WIDTH - progress_width) // 2
        progress_y = 100
        pygame.draw.rect(self.screen, (100, 100, 100), (progress_x, progress_y, progress_width, progress_height))
        progress_filled = int(progress_width * (1 - self.game_timer / GAME_DURATION))
        pygame.draw.rect(self.screen, (0, 200, 0), (progress_x, progress_y, progress_filled, progress_height))
        pygame.draw.rect(self.screen, (255, 255, 255), (progress_x, progress_y, progress_width, progress_height), 2)
        
        # Закрашенные промежутки волн на шкале прогресса
        # Волна 1 секция
        wave1_start_x = progress_x + int(progress_width * (WAVE_1_START / GAME_DURATION))
        wave1_end_x = progress_x + int(progress_width * (WAVE_1_END / GAME_DURATION))
        wave1_width = wave1_end_x - wave1_start_x
        wave_surface = pygame.Surface((wave1_width, progress_height), pygame.SRCALPHA)
        wave_surface.fill((255, 100, 100, 150))
        self.screen.blit(wave_surface, (wave1_start_x, progress_y))
        
        # Волна 2 секция
        wave2_start_x = progress_x + int(progress_width * (WAVE_2_START / GAME_DURATION))
        wave2_end_x = progress_x + int(progress_width * (WAVE_2_END / GAME_DURATION))
        wave2_width = wave2_end_x - wave2_start_x
        wave_surface2 = pygame.Surface((wave2_width, progress_height), pygame.SRCALPHA)
        wave_surface2.fill((255, 50, 50, 180))
        self.screen.blit(wave_surface2, (wave2_start_x, progress_y))
        
        # ИЗМЕНЕНИЕ: Волна 3 секция (самая тёмная)
        wave3_start_x = progress_x + int(progress_width * (WAVE_3_START / GAME_DURATION))
        wave3_end_x = progress_x + int(progress_width * (WAVE_3_END / GAME_DURATION))
        wave3_width = wave3_end_x - wave3_start_x
        wave_surface3 = pygame.Surface((wave3_width, progress_height), pygame.SRCALPHA)
        wave_surface3.fill((200, 0, 0, 200))  # Очень тёмный красный для финальной волны
        self.screen.blit(wave_surface3, (wave3_start_x, progress_y))
        
        # Перерыв секция (зелёная)
        break_start_x = progress_x + int(progress_width * (BREAK_START / GAME_DURATION))
        break_end_x = progress_x + int(progress_width * (BREAK_END / GAME_DURATION))
        break_width = break_end_x - break_start_x
        break_surface = pygame.Surface((break_width, progress_height), pygame.SRCALPHA)
        break_surface.fill((100, 255, 100, 100))
        self.screen.blit(break_surface, (break_start_x, progress_y))
        
        # Маркеры волн
        pygame.draw.line(self.screen, COLOR_WAVE_MARKER, (wave1_start_x, progress_y - 5), (wave1_start_x, progress_y + progress_height + 5), 2)
        pygame.draw.line(self.screen, COLOR_WAVE_MARKER, (wave2_start_x, progress_y - 5), (wave2_start_x, progress_y + progress_height + 5), 2)
        pygame.draw.line(self.screen, COLOR_WAVE_MARKER, (wave3_start_x, progress_y - 5), (wave3_start_x, progress_y + progress_height + 5), 2)
        
        # Seed Cards
        cards = [
            ('peashooter', (0, 200, 0)), 
            ('sunflower', (255, 200, 0)), 
            ('wallnut', (180, 140, 50)), 
            ('cherrybomb', (200, 0, 0)),
            ('icebloom', (0, 180, 255))
        ]
        start_x = 170
        for i, (p_type, color) in enumerate(cards):
            x = start_x + i * 75
            rect = pygame.Rect(x, 15, 68, 55)
            pygame.draw.rect(self.screen, (60, 60, 60), rect)
            pygame.draw.rect(self.screen, (100, 100, 100), rect, 2)
            if self.selected_plant == p_type:
                pygame.draw.rect(self.screen, (255, 255, 0), rect, 3)
            if p_type == 'peashooter':
                pygame.draw.circle(self.screen, (0, 255, 0), (x + 34, 35), 10)
            elif p_type == 'sunflower':
                pygame.draw.circle(self.screen, (255, 200, 0), (x + 34, 35), 10)
            elif p_type == 'wallnut':
                pygame.draw.ellipse(self.screen, (180, 140, 50), (x + 22, 25, 25, 20))
            elif p_type == 'cherrybomb':
                pygame.draw.circle(self.screen, (200, 0, 0), (x + 27, 35), 8)
                pygame.draw.circle(self.screen, (200, 0, 0), (x + 42, 35), 8)
            elif p_type == 'icebloom':
                pygame.draw.circle(self.screen, (0, 180, 255), (x + 34, 35), 10)
                for j in range(4):
                    angle = j * 90
                    rad = math.radians(angle)
                    lx = x + 34 + math.cos(rad) * 14
                    ly = 35 + math.sin(rad) * 14
                    pygame.draw.circle(self.screen, (200, 255, 255), (int(lx), int(ly)), 4)
            cost_text = self.font.render(str(self.plant_costs[p_type]), True, (255, 255, 255))
            self.screen.blit(cost_text, (x + 24, 48))

        # Отображение статуса волны
        wave_status = self.get_wave_status()
        if wave_status == 1:
            wave_text = self.big_font.render("HUGE WAVE 1!", True, (255, 0, 0))
            self.screen.blit(wave_text, (SCREEN_WIDTH//2 - 140, GRID_OFFSET_Y + 50))
        elif wave_status == 2:
            wave_text = self.big_font.render("BREAK - REGROUP!", True, (0, 255, 0))
            self.screen.blit(wave_text, (SCREEN_WIDTH//2 - 150, GRID_OFFSET_Y + 50))
            break_remaining = BREAK_END - (GAME_DURATION - self.game_timer)
            break_seconds = break_remaining // 60
            break_timer_text = self.font.render(f"Next wave in: {break_seconds}s", True, (255, 255, 0))
            self.screen.blit(break_timer_text, (SCREEN_WIDTH//2 - 80, GRID_OFFSET_Y + 100))
        elif wave_status == 3:
            wave_text = self.big_font.render("HUGE WAVE 2!", True, (255, 0, 0))
            self.screen.blit(wave_text, (SCREEN_WIDTH//2 - 140, GRID_OFFSET_Y + 50))
        elif wave_status == 4:  # ИЗМЕНЕНИЕ: Сообщение для волны 3
            wave_text = self.big_font.render("FINAL WAVE!", True, (255, 50, 50))
            self.screen.blit(wave_text, (SCREEN_WIDTH//2 - 120, GRID_OFFSET_Y + 50))
            # Таймер до конца игры
            remaining = self.game_timer // 60
            final_timer_text = self.font.render(f"Survive: {remaining}s", True, (255, 255, 0))
            self.screen.blit(final_timer_text, (SCREEN_WIDTH//2 - 70, GRID_OFFSET_Y + 100))
            
        if self.game_won:
            overlay = pygame.Surface((SCREEN_WIDTH, SCREEN_HEIGHT))
            overlay.set_alpha(200)
            overlay.fill(COLOR_WIN)
            self.screen.blit(overlay, (0, 0))
            for fw in self.fireworks:
                fw.draw(self.screen)
            win_text = self.big_font.render("VICTORY!", True, (255, 255, 255))
            sub_text = self.font.render("You survived the zombie attack!", True, (255, 255, 255))
            restart_text = self.font.render("Press R to Play Again", True, (255, 255, 255))
            self.screen.blit(win_text, (SCREEN_WIDTH//2 - 100, SCREEN_HEIGHT//2 - 80))
            self.screen.blit(sub_text, (SCREEN_WIDTH//2 - 140, SCREEN_HEIGHT//2 - 20))
            self.screen.blit(restart_text, (SCREEN_WIDTH//2 - 110, SCREEN_HEIGHT//2 + 40))
            
        if self.game_over:
            overlay = pygame.Surface((SCREEN_WIDTH, SCREEN_HEIGHT))
            overlay.set_alpha(200)
            overlay.fill(COLOR_LOSE)
            self.screen.blit(overlay, (0, 0))
            go_text = self.big_font.render("GAME OVER", True, (255, 255, 255))
            sub_text = self.font.render("The zombies ate your brains!", True, (255, 255, 255))
            restart_text = self.font.render("Press R to Try Again", True, (255, 255, 255))
            self.screen.blit(go_text, (SCREEN_WIDTH//2 - 130, SCREEN_HEIGHT//2 - 80))
            self.screen.blit(sub_text, (SCREEN_WIDTH//2 - 130, SCREEN_HEIGHT//2 - 20))
            self.screen.blit(restart_text, (SCREEN_WIDTH//2 - 110, SCREEN_HEIGHT//2 + 40))

        pygame.display.flip()

    def run(self):
        running = True
        while running:
            running = self.handle_input()
            self.update()                       
            self.draw()
            self.clock.tick(FPS)
        pygame.quit()
        sys.exit()

if __name__ == "__main__":
    game = Game()
    game.run()
