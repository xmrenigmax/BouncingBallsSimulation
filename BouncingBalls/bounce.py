import pygame
import sys
import random
import math

# Initialize pygame
pygame.init()

# Screen dimensions
screen_width = 800
screen_height = 600
screen = pygame.display.set_mode((screen_width, screen_height))
pygame.display.set_caption("Bouncing Balls")

# Circle boundary
center_x = screen_width // 2
center_y = screen_height // 2
radius = min(screen_width, screen_height) // 2 - 50  # Slightly smaller than half the screen size

# Ball properties
ball_radius = 10
initial_num_balls = 5
positions = []
velocities = []
colors = []

# Initialize balls
for _ in range(initial_num_balls):
    angle = random.uniform(0, 2 * math.pi)
    distance = random.uniform(0, radius - ball_radius)
    x = center_x + distance * math.cos(angle)
    y = center_y + distance * math.sin(angle)
    positions.append([x, y])
    velocities.append([random.uniform(-1, 1), random.uniform(-1, 1)])
    colors.append([random.randint(0, 255), random.randint(0, 255), random.randint(0, 255)])

# Main loop
running = True
clock = pygame.time.Clock()

while running:
    screen.fill((0, 0, 0))

    # Draw the circular boundary
    pygame.draw.circle(screen, (255, 255, 255), (center_x, center_y), radius, 1)

    # Draw the balls
    for i in range(len(positions)):
        pygame.draw.circle(screen, colors[i], (int(positions[i][0]), int(positions[i][1])), ball_radius)

    # Update ball positions
    for i in range(len(positions)):
        positions[i][0] += velocities[i][0]
        positions[i][1] += velocities[i][1]

        # Check for collisions with the circular boundary
        distance_from_center = math.sqrt((positions[i][0] - center_x) ** 2 + (positions[i][1] - center_y) ** 2)
        if distance_from_center + ball_radius > radius:
            angle = math.atan2(positions[i][1] - center_y, positions[i][0] - center_x)
            velocities[i][0] = -velocities[i][0]
            velocities[i][1] = -velocities[i][1]
            positions[i][0] = center_x + (radius - ball_radius) * math.cos(angle)
            positions[i][1] = center_y + (radius - ball_radius) * math.sin(angle)

            # Double the ball upon collision with the boundary
            new_ball_position = [positions[i][0], positions[i][1]]
            new_ball_velocity = [random.uniform(-1, 1), random.uniform(-1, 1)]
            new_ball_color = [random.randint(0, 255), random.randint(0, 255), random.randint(0, 255)]
            positions.append(new_ball_position)
            velocities.append(new_ball_velocity)
            colors.append(new_ball_color)

    # Handle events
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    # Update the display
    pygame.display.flip()

    # Cap the frame rate
    clock.tick(60)

# Quit pygame
pygame.quit()
sys.exit()