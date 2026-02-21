import pygame, math, datetime, colorsys

pygame.init()
W, H = 800, 800
screen = pygame.display.set_mode((W, H))
pygame.display.set_caption("BMW Neon Clock")
clock = pygame.time.Clock()

CENTER, RADIUS = (W//2, H//2), 280
font_med = pygame.font.SysFont("Segoe UI", 40, bold=True)
font_small = pygame.font.SysFont("Segoe UI", 28, bold=True)
font_bmw = pygame.font.SysFont("Segoe UI", 60, bold=True)

def pakistan_time():
    return datetime.datetime.utcnow() + datetime.timedelta(hours=5)

def neon_color(t):
    r, g, b = colorsys.hsv_to_rgb(t % 1, 1, 1)
    return int(r*255), int(g*255), int(b*255)

def draw_neon_ring(t):
    for i in range(360):
        angle = math.radians(i)
        wave = math.sin(i*0.15 + t)*6
        x = CENTER[0] + math.cos(angle)*(RADIUS + wave + 40)
        y = CENTER[1] + math.sin(angle)*(RADIUS + wave + 40)
        pygame.draw.circle(screen, neon_color(i/360 + t*0.02), (int(x), int(y)), 5)

def draw_bmw_logo():
    # Outer black ring
    pygame.draw.circle(screen, (0,0,0), CENTER, 250)
    pygame.draw.circle(screen, (255,255,255), CENTER, 245, 10)

    # Blue and white quadrants using arcs
    rect = pygame.Rect(CENTER[0]-200, CENTER[1]-200, 400, 400)
    pygame.draw.arc(screen, (0,0,255), rect, math.radians(0), math.radians(90), 200)
    pygame.draw.arc(screen, (255,255,255), rect, math.radians(90), math.radians(180), 200)
    pygame.draw.arc(screen, (0,0,255), rect, math.radians(180), math.radians(270), 200)
    pygame.draw.arc(screen, (255,255,255), rect, math.radians(270), math.radians(360), 200)

    # Fill inner circle for smooth center
    pygame.draw.circle(screen, (0,0,0), CENTER, 60)
    pygame.draw.circle(screen, (255,255,255), CENTER, 55, 3)

    # BMW Text perfectly above the circle
    text = font_bmw.render("BMW", True, (255,255,255))
    text_rect = text.get_rect(center=(CENTER[0], CENTER[1]-250 - text.get_height()//2 + 5))
    screen.blit(text, text_rect)

def draw_hands(now):
    h, m, s = now.hour%12, now.minute, now.second
    hx = CENTER[0] + math.cos(math.radians(h*30 + m/2 - 90)) * RADIUS*0.45
    hy = CENTER[1] + math.sin(math.radians(h*30 + m/2 - 90)) * RADIUS*0.45
    pygame.draw.line(screen, (255,255,255), CENTER, (hx, hy), 14)
    mx = CENTER[0] + math.cos(math.radians(m*6 - 90)) * RADIUS*0.65
    my = CENTER[1] + math.sin(math.radians(m*6 - 90)) * RADIUS*0.65
    pygame.draw.line(screen, (255,255,255), CENTER, (mx, my), 10)
    sx = CENTER[0] + math.cos(math.radians(s*6 - 90)) * RADIUS*0.75
    sy = CENTER[1] + math.sin(math.radians(s*6 - 90)) * RADIUS*0.75
    pygame.draw.line(screen, (255,0,0), CENTER, (sx, sy), 4)
    pygame.draw.circle(screen, (255,255,255), CENTER, 12)

def draw_digital(now):
    t1 = font_med.render(now.strftime("%I:%M %p").lower(), True, (0,255,0))
    t2 = font_small.render(now.strftime("%b %d %a").upper(), True, (0,255,0))
    screen.blit(t1, (CENTER[0]-t1.get_width()//2, CENTER[1]+200))
    screen.blit(t2, (CENTER[0]-t2.get_width()//2, CENTER[1]+240))

t = 0
running = True
while running:
    for e in pygame.event.get():
        if e.type == pygame.QUIT:
            running = False
    screen.fill((0,0,0))
    t += 0.03
    now = pakistan_time()
    draw_neon_ring(t)
    draw_bmw_logo()
    draw_hands(now)
    draw_digital(now)
    pygame.display.update()
    clock.tick(60)

pygame.quit()
