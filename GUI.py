# Stephanie Torres/Joseph Quarshie/Arpit Singh 
# COMP 259: Character Animation 
# Final Project: Animation Tool 


import pygame
import pygame_gui
import random
import os
import tkinter as tk
from tkinter import filedialog
import time

# initialized Tkinter & Pygame 
root = tk.Tk()
root.withdraw()  # hide the main window
pygame.init()

# setting the dimensions of the main window
width, height = 800, 600
screen = pygame.display.set_mode((width, height))
pygame.display.set_caption('MotionCraft: Visual Animation & Control Interface')

# created GUI Manager
manager = pygame_gui.UIManager((width, height))

# GUI elements defined
play_button = pygame_gui.elements.UIButton(relative_rect=pygame.Rect((50, 550), (100, 50)),
                                           text='Play',
                                           manager=manager)
pause_button = pygame_gui.elements.UIButton(relative_rect=pygame.Rect((160, 550), (100, 50)),
                                            text='Pause',
                                            manager=manager)
stop_button = pygame_gui.elements.UIButton(relative_rect=pygame.Rect((270, 550), (100, 50)),
                                           text='Stop',
                                           manager=manager)
reset_button = pygame_gui.elements.UIButton(relative_rect=pygame.Rect((380, 550), (100, 50)),
                                            text='Reset',
                                            manager=manager)
load_button = pygame_gui.elements.UIButton(relative_rect=pygame.Rect((490, 550), (100, 50)),
                                           text='Load',
                                           manager=manager)
camera_left_button = pygame_gui.elements.UIButton(relative_rect=pygame.Rect((width - 150, 10), (30, 30)),
                                                  text='<',
                                                  manager=manager)
camera_right_button = pygame_gui.elements.UIButton(relative_rect=pygame.Rect((width - 110, 10), (30, 30)),
                                                   text='>',
                                                   manager=manager)
camera_up_button = pygame_gui.elements.UIButton(relative_rect=pygame.Rect((width - 70, 10), (30, 30)),
                                                text='^',
                                                manager=manager)
camera_down_button = pygame_gui.elements.UIButton(relative_rect=pygame.Rect((width - 30, 10), (30, 30)),
                                                  text='v',
                                                  manager=manager)
speed_slider = pygame_gui.elements.UIHorizontalSlider(relative_rect=pygame.Rect((600, 550), (150, 50)),
                                                      start_value=2.5,
                                                      value_range=(0.1, 10.0),
                                                      manager=manager)
# future work will entail to get these blending elements drop down menus to function correct 
animation_select_1 = pygame_gui.elements.UIDropDownMenu(
    options_list=["Bouncing Ball", "Rotating Square", "Scaling Triangle"],
    starting_option="Bouncing Ball",
    relative_rect=pygame.Rect((50, 500), (200, 30)),
    manager=manager
)
animation_select_2 = pygame_gui.elements.UIDropDownMenu(
    options_list=["Bouncing Ball", "Rotating Square", "Scaling Triangle"],
    starting_option="Bouncing Ball",
    relative_rect=pygame.Rect((260, 500), (200, 30)),
    manager=manager
)

BLACK = (0, 0, 0) # colors for animation
WHITE = (255, 255, 255)
RED = (255, 0, 0)

# animation state
animation_paused = True  # animation starts paused
animation_playing = False

# all animation properties
ball_radius = 20
ball_x = width // 2
ball_y = height // 2
ball_speed_x = random.randint(2, 5)
ball_speed_y = random.randint(2, 5)

square_size = 50
square_x = width // 2
square_y = height // 2
square_angle = 0
square_rotation_speed = 2

triangle_size = 40
triangle_x = width // 2
triangle_y = height // 2
triangle_scale = 1.0
triangle_scale_speed = 0.01

# dropdown menu for selecting animations
animation_dropdown = pygame_gui.elements.UIDropDownMenu(options_list=["Bouncing Ball", "Rotating Square", "Scaling Triangle"],
                                                        starting_option="Bouncing Ball",
                                                        relative_rect=pygame.Rect((600, 450), (150, 50)),
                                                        manager=manager)

selected_animation = "Bouncing Ball" # default

# camera properties
camera_x, camera_y = 0, 0
camera_speed = 5

# clock for controlling frame rate
clock = pygame.time.Clock()

# function to reset the object's location
def reset_object_location():
    global ball_x, ball_y, square_x, square_y, triangle_x, triangle_y, triangle_scale, square_angle 
    ball_x, ball_y = width // 2, height // 2 # reseting
    square_x, square_y = width // 2, height // 2
    triangle_x, triangle_y = width // 2, height // 2
    triangle_scale = 1.0
    square_angle = 0

loaded_image = None
loaded_image_rect = None

def load_image(image_path):
    global loaded_image, loaded_image_rect
    try:
        loaded_image = pygame.image.load(image_path)

        desired_width = 800
        desired_height = 600
        loaded_image = pygame.transform.scale(loaded_image, (desired_width, desired_height))
        loaded_image_rect = loaded_image.get_rect()
        loaded_image_rect.center = (width // 2, height // 2)
    except pygame.error as e:
        print(f"Error loading image: {e}")

start_time = 0
current_time = 0
timer_active = False

selected_animation_1 = "Bouncing Ball"
selected_animation_2 = "Bouncing Ball"

# main event loop
running = True
while running:
    time_delta = clock.tick(60) / 1000.0

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

        # process GUI events
        manager.process_events(event)

        if event.type == pygame.USEREVENT:
            if event.user_type == pygame_gui.UI_HORIZONTAL_SLIDER_MOVED:
              if event.ui_element == speed_slider:
                # here we adjust the ball's speed
                ball_speed_x = event.value
                ball_speed_y = event.value
                square_rotation_speed = event.value
                triangle_scale_speed = event.value / 100 
            if event.user_type == pygame_gui.UI_BUTTON_PRESSED:
                if event.ui_element == play_button:
                    animation_paused = False
                    animation_playing = True
                    if not timer_active:  
                      start_time = pygame.time.get_ticks() - current_time
                      timer_active = True
                elif event.ui_element == pause_button:
                    animation_paused = True
                    timer_active = False
                elif event.ui_element == stop_button:
                    animation_paused = True
                    animation_playing = False
                    timer_active = False
                    start_time = 0
                    current_time = 0
                elif event.ui_element == reset_button:
                    reset_object_location()
                elif event.ui_element == load_button:
                    # open a file dialog to select an image or animation clip
                    file_path = filedialog.askopenfilename()
                    if os.path.exists(file_path):
                        load_image(file_path)

            elif event.user_type == pygame_gui.UI_DROP_DOWN_MENU_CHANGED:
                if event.ui_element == animation_dropdown:
                    selected_animation = event.text  # update the selected animation
                if event.ui_element == camera_left_button:
                   camera_x -= camera_speed
                elif event.ui_element == camera_right_button:
                   camera_x += camera_speed
                elif event.ui_element == camera_up_button:
                   camera_y -= camera_speed
                elif event.ui_element == camera_down_button:
                   camera_y += camera_speed
            if event.user_type == pygame_gui.UI_BUTTON_PRESSED:
                if event.ui_element == play_button:
                    animation_paused = False
                    animation_playing = True
                    if not timer_active:
                        start_time = pygame.time.get_ticks()
                        timer_active = True
                elif event.ui_element == pause_button:
                    animation_paused = True
                    timer_active = False
            # handling camera button presses
            if event.ui_element == camera_left_button:
                camera_x -= camera_speed
            elif event.ui_element == camera_right_button:
                camera_x += camera_speed
            elif event.ui_element == camera_up_button:
                camera_y -= camera_speed
            elif event.ui_element == camera_down_button:
                camera_y += camera_speed
            # blending drop down menu with animations 
            elif event.user_type == pygame_gui.UI_DROP_DOWN_MENU_CHANGED:
             if event.ui_element == animation_select_1:
               selected_animation_1 = event.text
            elif event.ui_element == animation_select_2:
              selected_animation_2 = event.text

    if timer_active:
        current_time = pygame.time.get_ticks() - start_time

    # updating the GUI
    manager.update(time_delta)
    screen.fill(BLACK)
    if loaded_image is not None:
        screen.blit(loaded_image, loaded_image_rect.topleft)

    # updating & rendering the selected animation
    if animation_playing:
        if selected_animation == "Bouncing Ball":
            if not animation_paused:
                ball_x += ball_speed_x
                ball_y += ball_speed_y

                if ball_x - ball_radius + camera_x < 0 or ball_x + ball_radius + camera_x > width:
                   ball_speed_x *= -1
                if ball_y - ball_radius + camera_y < 0 or ball_y + ball_radius + camera_y > height:
                   ball_speed_y *= -1

            pygame.draw.circle(screen, RED, (int(ball_x + camera_x), int(ball_y + camera_y)), ball_radius)

        elif selected_animation == "Rotating Square":
            if not animation_paused:
             square_angle += square_rotation_speed

            rotated_square = pygame.Surface((square_size, square_size), pygame.SRCALPHA)
            pygame.draw.rect(rotated_square, RED, (0, 0, square_size, square_size))
            rotated_square = pygame.transform.rotate(rotated_square, square_angle)
            rotated_square_rect = rotated_square.get_rect(center=(square_x + camera_x, square_y + camera_y))
            screen.blit(rotated_square, rotated_square_rect.topleft)


        elif selected_animation == "Scaling Triangle":
            if not animation_paused:
               triangle_scale += triangle_scale_speed

            triangle_points = [(triangle_x, triangle_y - triangle_size * triangle_scale),
                               (triangle_x - triangle_size * triangle_scale, triangle_y + triangle_size * triangle_scale),
                               (triangle_x + triangle_size * triangle_scale, triangle_y + triangle_size * triangle_scale)]
            adjusted_triangle_points = [(x + camera_x, y + camera_y) for x, y in triangle_points]
            pygame.draw.polygon(screen, RED, adjusted_triangle_points)

    timer_surface = pygame.font.Font(None, 36).render(str(current_time // 1000), True, WHITE)
    screen.blit(timer_surface, ((10, 10)))

    # drawing GUI
    manager.draw_ui(screen)

    pygame.display.flip()

pygame.quit()