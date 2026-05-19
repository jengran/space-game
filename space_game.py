import pygame
import random

# Start pygame
pygame.init()

# Create the window
screen = pygame.display.set_mode((800, 600))
pygame.display.set_caption("Space Game")

# Colors
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
BLUE = (76, 201, 240)
YELLOW = (255, 255, 0)
GRAY = (169, 169, 169)
RED = (255, 107, 107)
GREEN = (0, 255, 0)
PURPLE = (123, 47, 190)

# Create stars
stars = []
for i in range(100):
    x = random.randint(0, 800)
    y = random.randint(0, 600)
    size = random.randint(1, 3)
    stars.append((x, y, size))

# Spaceship settings
ship_x = 400
ship_y = 500
ship_speed = 5

# Asteroid settings
asteroids = []
for i in range(6):
    x = random.randint(0, 800)
    y = random.randint(-100, 0)
    size = random.randint(15, 35)
    speed = random.randint(2, 5)
    asteroids.append([x, y, size, speed])

# Bullet settings
bullets = []
bullet_speed = 8
bullet_cooldown = 0

# Score and lives
score = 0
lives = 3
font = pygame.font.SysFont(None, 36)
big_font = pygame.font.SysFont(None, 60)

# Paused state
paused = False

# Game loop
clock = pygame.time.Clock()
running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        # Toggle pause with P key
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_p:
                paused = not paused

    # If paused show pause screen and skip everything else
    if paused:
        screen.fill(BLACK)
        for star in stars:
            pygame.draw.circle(screen, WHITE, (star[0], star[1]), star[2])
        pause_title = big_font.render("PAUSED", True, BLUE)
        pause_sub = font.render("Press P to resume", True, PURPLE)
        screen.blit(pause_title, (320, 260))
        screen.blit(pause_sub, (290, 320))
        pygame.display.flip()
        clock.tick(60)
        continue

    # Move spaceship with arrow keys
    keys = pygame.key.get_pressed()
    if keys[pygame.K_LEFT] and ship_x > 20:
        ship_x -= ship_speed
    if keys[pygame.K_RIGHT] and ship_x < 780:
        ship_x += ship_speed
    if keys[pygame.K_UP] and ship_y > 20:
        ship_y -= ship_speed
    if keys[pygame.K_DOWN] and ship_y < 580:
        ship_y += ship_speed

    # Shoot bullet with spacebar
    if keys[pygame.K_SPACE] and bullet_cooldown == 0:
        bullets.append([ship_x, ship_y - 20])
        bullet_cooldown = 15

    # Reduce cooldown
    if bullet_cooldown > 0:
        bullet_cooldown -= 1

    # Move bullets up
    for bullet in bullets[:]:
        bullet[1] -= bullet_speed
        if bullet[1] < 0:
            bullets.remove(bullet)

    # Move asteroids down
    for asteroid in asteroids:
        asteroid[1] += asteroid[3]

        # If asteroid goes off screen reset it to top
        if asteroid[1] > 650:
            asteroid[0] = random.randint(0, 800)
            asteroid[1] = random.randint(-100, 0)
            asteroid[2] = random.randint(15, 35)
            asteroid[3] = random.randint(2, 5)
            score += 1

        # Check if asteroid hits spaceship
        dist_x = asteroid[0] - ship_x
        dist_y = asteroid[1] - ship_y
        distance = (dist_x**2 + dist_y**2) ** 0.5
        if distance < asteroid[2] + 15:
            lives -= 1
            asteroid[0] = random.randint(0, 800)
            asteroid[1] = random.randint(-100, 0)
            if lives <= 0:
                running = False

        # Check if bullet hits asteroid
        for bullet in bullets[:]:
            dist_x = asteroid[0] - bullet[0]
            dist_y = asteroid[1] - bullet[1]
            distance = (dist_x**2 + dist_y**2) ** 0.5
            if distance < asteroid[2] + 5:
                bullets.remove(bullet)
                asteroid[0] = random.randint(0, 800)
                asteroid[1] = random.randint(-100, 0)
                asteroid[2] = random.randint(15, 35)
                asteroid[3] = random.randint(2, 5)
                score += 5

    # Fill background black
    screen.fill(BLACK)

    # Draw stars
    for star in stars:
        pygame.draw.circle(screen, WHITE, (star[0], star[1]), star[2])

    # Draw bullets
    for bullet in bullets:
        pygame.draw.rect(screen, GREEN, (bullet[0] - 2, bullet[1], 4, 12))

    # Draw asteroids
    for asteroid in asteroids:
        pygame.draw.circle(screen, GRAY, (asteroid[0], asteroid[1]), asteroid[2])

    # Draw spaceship
    pygame.draw.polygon(screen, BLUE, [
        (ship_x, ship_y - 20),
        (ship_x - 15, ship_y + 15),
        (ship_x + 15, ship_y + 15)
    ])
    pygame.draw.polygon(screen, YELLOW, [
        (ship_x, ship_y + 15),
        (ship_x - 8, ship_y + 25),
        (ship_x + 8, ship_y + 25)
    ])

    # Draw score and lives
    score_text = font.render(f"Score: {score}", True, BLUE)
    lives_text = font.render(f"Lives: {lives}", True, RED)
    pause_hint = font.render("P = Pause", True, GRAY)
    screen.blit(score_text, (10, 10))
    screen.blit(lives_text, (10, 50))
    screen.blit(pause_hint, (650, 10))

    # Update display
    pygame.display.flip()
    clock.tick(60)

# Game over screen
screen.fill(BLACK)
game_over_text = big_font.render("GAME OVER!", True, RED)
score_text = font.render(f"Final Score: {score}", True, BLUE)
screen.blit(game_over_text, (220, 260))
screen.blit(score_text, (310, 330))
pygame.display.flip()
pygame.time.wait(3000)

pygame.quit()