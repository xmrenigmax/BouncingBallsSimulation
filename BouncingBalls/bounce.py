import pygame
import sys
import random
import math
import time

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
initial_num_balls = 50
positions = []
velocities = []
colors = []
last_duplication_times = []
boundary_stuck_times = []  # Track how long each ball has been near the boundary
duplication_delay = 2  # 2 seconds delay

# Black hole properties
black_hole_radius = 20
black_hole_position = [random.uniform(center_x - radius + black_hole_radius, center_x + radius - black_hole_radius),
                       random.uniform(center_y - radius + black_hole_radius, center_y + radius - black_hole_radius)]
black_hole_velocity = [random.uniform(2, 16), random.uniform(2, 16)]  # Increased initial velocity
gravity = 0.2  # Gravity effect
velocity_gain = 0.2  # Velocity gain upon collision
wall_bounce_gain = 0.8  # Ricochet effect, gain some momentum
random_bounce_factor = 1  # Random perturbation factor

# Timers for fluctuating wall_bounce_gain and changing direction
last_wall_bounce_gain_change = time.time()
last_direction_change = time.time()

# Initialize balls
for _ in range(initial_num_balls):
    angle = random.uniform(0, 2 * math.pi)
    distance = random.uniform(0, radius - ball_radius)
    x = center_x + distance * math.cos(angle)
    y = center_y + distance * math.sin(angle)
    positions.append([x, y])
    velocities.append([random.uniform(-1, 1), random.uniform(-1, 1)])
    colors.append([random.randint(0, 255), random.randint(0, 255), random.randint(0, 255)])
    last_duplication_times.append(time.time())
    boundary_stuck_times.append(0)  # Initialize boundary stuck times

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

    # Draw the black hole with a white outline
    pygame.draw.circle(screen, (255, 255, 255), (int(black_hole_position[0]), int(black_hole_position[1])), black_hole_radius, 1)
    pygame.draw.circle(screen, (0, 0, 0), (int(black_hole_position[0]), int(black_hole_position[1])), black_hole_radius - 1)

    # Update ball positions
    for i in range(len(positions)):
        positions[i][0] += velocities[i][0]
        positions[i][1] += velocities[i][1]

        # Check for collisions with the circular boundary
        distance_from_center = math.sqrt((positions[i][0] - center_x) ** 2 + (positions[i][1] - center_y) ** 2)
        if distance_from_center + ball_radius > radius:
            if boundary_stuck_times[i] == 0:
                boundary_stuck_times[i] = time.time()  # Start the timer when the ball first touches the boundary

            # If the ball has been near the boundary for more than 2 seconds, push it towards the center
            if time.time() - boundary_stuck_times[i] > 2:
                dx = center_x - positions[i][0]
                dy = center_y - positions[i][1]
                distance_to_center = math.sqrt(dx ** 2 + dy ** 2)
                if distance_to_center > 0:
                    velocities[i][0] += 0.1 * (dx / distance_to_center)
                    velocities[i][1] += 0.1 * (dy / distance_to_center)
        else:
            boundary_stuck_times[i] = 0  # Reset the timer if the ball is not near the boundary

        # Double the ball upon collision with the boundary if delay has passed
        current_time = time.time()
        if current_time - last_duplication_times[i] >= duplication_delay:
            new_ball_position = [positions[i][0], positions[i][1]]
            new_ball_velocity = [random.uniform(-1, 1), random.uniform(-1, 1)]
            new_ball_color = [random.randint(0, 255), random.randint(0, 255), random.randint(0, 255)]
            positions.append(new_ball_position)
            velocities.append(new_ball_velocity)
            colors.append(new_ball_color)
            last_duplication_times.append(current_time)
            boundary_stuck_times.append(0)  # Initialize boundary stuck time for the new ball
            last_duplication_times[i] = current_time

    # Update black hole position and velocity
    black_hole_position[0] += black_hole_velocity[0]
    black_hole_position[1] += black_hole_velocity[1]

    # Apply gravitational pull downwards
    black_hole_velocity[1] += gravity

    # Check for collisions with the circular boundary
    distance_from_center = math.sqrt((black_hole_position[0] - center_x) ** 2 + (black_hole_position[1] - center_y) ** 2)
    if distance_from_center + black_hole_radius > radius:
        angle = math.atan2(black_hole_position[1] - center_y, black_hole_position[0] - center_x)
        black_hole_velocity[0] = -black_hole_velocity[0] * wall_bounce_gain
        black_hole_velocity[1] = -black_hole_velocity[1] * wall_bounce_gain
        black_hole_velocity[0] += random.uniform(-random_bounce_factor, random_bounce_factor)
        black_hole_velocity[1] += random.uniform(-random_bounce_factor, random_bounce_factor)
        black_hole_position[0] = center_x + (radius - black_hole_radius) * math.cos(angle)
        black_hole_position[1] = center_y + (radius - black_hole_radius) * math.sin(angle)

    # Check for collisions with balls
    for i in range(len(positions) - 1, -1, -1):
        dx = black_hole_position[0] - positions[i][0]
        dy = black_hole_position[1] - positions[i][1]
        distance = math.sqrt(dx ** 2 + dy ** 2)
        if distance < black_hole_radius + ball_radius:
            # Eat the ball, regain velocity, and increase size
            black_hole_velocity[0] += velocity_gain * random.uniform(-1, 1)
            black_hole_velocity[1] += velocity_gain * random.uniform(-1, 1)
            black_hole_radius += 1  # Increase the size of the black hole
            positions.pop(i)
            velocities.pop(i)
            colors.pop(i)
            last_duplication_times.pop(i)
            boundary_stuck_times.pop(i)

    # Randomly fluctuate wall_bounce_gain every 3 seconds
    if time.time() - last_wall_bounce_gain_change >= 3:
        wall_bounce_gain = random.uniform(0.6, 1.1)
        last_wall_bounce_gain_change = time.time()

    # Change black hole direction every 8 seconds
    if time.time() - last_direction_change >= 8:
        black_hole_velocity[0] = random.uniform(-16, 16)
        black_hole_velocity[1] = random.uniform(-16, 16)
        last_direction_change = time.time()

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