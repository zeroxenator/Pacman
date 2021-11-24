# Pacman in Python with PyGame
# https://github.com/hbokmann/Pacman
# Changes for vaxman by https://github.com/zeroxenator/Pacman

from constants import *
from player import Player, Ghost
from wall import Wall
from block import Block

# Import the pygame module
import pygame

# Import pygame.locals for easier access to key coordinates
# Updated to conform to flake8 and black standards
from pygame.locals import (
    K_UP,
    K_DOWN,
    K_LEFT,
    K_RIGHT,
    K_ESCAPE,
    KEYDOWN,
    QUIT,
)

# Initialize pygame
pygame.init()

# Define constants for the screen width and height
SCREEN_WIDTH = 606
SCREEN_HEIGHT = 606

# Create the screen object
# The size is determined by the constant SCREEN_WIDTH and SCREEN_HEIGHT
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))

# --------------------------------------------------
# Set Game Variables
# --------------------------------------------------
# Title
pygame.display.set_caption('Vaxman')

# --- Directories
image_dir = "assets/images"
audio_dir = "assets/audio"
font_dir = "assets/fonts"

# --- Icon
image_icon = pygame.image.load(f'{image_dir}/pacman.png')
pygame.display.set_icon(image_icon)

# --- Music
pygame.mixer.init()
pygame.mixer.music.load(f'{audio_dir}/ES_Press_X_Twice-Lexica.mp3')
pygame.mixer.music.set_volume(0.3)
pygame.mixer.music.play(-1, 0.0)

# --- Font
pygame.font.init()
font = pygame.font.Font(f"{font_dir}/freesansbold.ttf", 24)

# --- Background
# Create a surface we can draw on
background = pygame.Surface(screen.get_size())
background = background.convert()
background.fill(COLOR_BLACK)

# --- Clock
clock = pygame.time.Clock()
clock_sec = 10

# --- User Events
EVENT_MUTATE = pygame.USEREVENT + 0
run_every = 30
pygame.time.set_timer(EVENT_MUTATE, run_every * 1000)


# --------------------------------------------------
# Start Game
# --------------------------------------------------
class Pacman(object):
    def __init__(self):
        self.sprites_list = pygame.sprite.RenderPlain()
        self.block_list = pygame.sprite.RenderPlain()
        self.player_list = pygame.sprite.RenderPlain()
        self.enemies_list = pygame.sprite.RenderPlain()

        # Make the walls. (x_pos, y_pos, width, height)
        self.wall_list = pygame.sprite.RenderPlain()
        self.gate_list = pygame.sprite.RenderPlain()

        self.player_obj = None
        self.enemy_objs = {}

        self.player_score = 0

        self.run()

    def run(self):
        if self.setup_game():
            self.run_game()

    def setup_game(self):

        # Create Player Object
        self.player_obj = Player(PLAYER_X, PLAYER_Y, f"{image_dir}/pacman.png")
        self.sprites_list.add(self.player_obj)
        self.player_list.add(self.player_obj)

        # Create Enemies Objects
        for i in range(4):
            ghost_obj = self.create_enemy_sprite(
                x=ENEMY_SPAWNS[i].x, y=ENEMY_SPAWNS[i].y,
                filename=f"{image_dir}/enemy{i}.png",
                enemy_id=i,
                name=ENEMY_NAMES[i],
                directions=ENEMY_DIRECTIONS[i])

            self.enemy_objs[i] = ghost_obj

        self.setup_walls()
        self.setup_gate()
        self.setup_coins()

        return True

    def setup_walls(self):
        # Loop through the list. Create the wall, add it to the list
        for item in WALLS_LIST:
            wall = Wall(item[0], item[1], item[2], item[3], COLOR_BLUE)
            self.wall_list.add(wall)
            self.sprites_list.add(wall)

    def setup_gate(self):
        self.gate_list.add(Wall(282, 242, 42, 2, COLOR_WHITE))
        self.sprites_list.add(self.gate_list)

    def setup_coins(self):

        # Draw the grid
        for row in range(19):
            for column in range(19):
                if (row == 7 or row == 8) and (column == 8 or column == 9 or column == 10):
                    continue
                else:
                    block = Block(COLOR_YELLOW, 4, 4)

                    # Set a random location for the block
                    block.rect.x = (30 * column + 6) + 26
                    block.rect.y = (30 * row + 6) + 26

                    b_collide = pygame.sprite.spritecollide(block, self.wall_list, False)
                    p_collide = pygame.sprite.spritecollide(block, self.player_list, False)
                    if b_collide:
                        continue
                    elif p_collide:
                        continue
                    else:
                        # Add the block to the list of objects
                        self.block_list.add(block)
                        self.sprites_list.add(block)

    def create_enemy_sprite(self, x, y, filename, enemy_id, name, directions):
        ghost_obj = Ghost(x, y, filename, enemy_id, name, directions, wait=enemy_id)
        self.enemies_list.add(ghost_obj)
        self.sprites_list.add(ghost_obj)
        return ghost_obj

    def commence_mutation(self):
        enemy_id_counter = max(self.enemy_objs.keys()) + 1
        new_enemy_objs = {}

        for key, enemy_obj in self.enemy_objs.items():
            new_enemy_objs[enemy_id_counter] = self.create_enemy_sprite(
                x=enemy_obj.spawn_x, y=enemy_obj.spawn_y,
                filename=enemy_obj.filename,
                enemy_id=enemy_id_counter,
                name=enemy_obj.name,
                directions=enemy_obj.directions)
            enemy_id_counter += 1

        self.enemy_objs.update(new_enemy_objs)

    def monitor_player_input(self):

        # ALL EVENT PROCESSING SHOULD GO BELOW THIS COMMENT
        # Look at every event in the queue
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return False

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_LEFT:
                    self.player_obj.move(-30, 0)
                if event.key == pygame.K_RIGHT:
                    self.player_obj.move(30, 0)
                if event.key == pygame.K_UP:
                    self.player_obj.move(0, -30)
                if event.key == pygame.K_DOWN:
                    self.player_obj.move(0, 30)
                if event.key == K_ESCAPE:
                    return False

            if event.type == pygame.KEYUP:
                if event.key == pygame.K_LEFT:
                    self.player_obj.move(30, 0)
                if event.key == pygame.K_RIGHT:
                    self.player_obj.move(-30, 0)
                if event.key == pygame.K_UP:
                    self.player_obj.move(0, 30)
                if event.key == pygame.K_DOWN:
                    self.player_obj.move(0, -30)

            if event.type == EVENT_MUTATE:
                self.commence_mutation()
        # ALL EVENT PROCESSING SHOULD GO ABOVE THIS COMMENT
        return True

    def update_game_objects(self):

        # ALL GAME LOGIC SHOULD GO BELOW THIS COMMENT
        self.player_obj.update(self.wall_list, self.gate_list)

        # Check if player hit any enemies
        enemy_hit = self.player_obj.hit(self.enemies_list)
        if enemy_hit:
            enemy_id = enemy_hit.enemy_id
            enemy_hit.kill()
            self.enemy_objs.pop(enemy_id)

        # Update enemies
        for key, enemy_obj in self.enemy_objs.items():
            enemy_obj.move()
            enemy_obj.update(self.wall_list, False)

        # See if the player_obj block has collided with anything.
        blocks_hit_list = pygame.sprite.spritecollide(self.player_obj, self.block_list, True)

        # Check the list of collisions.
        if len(blocks_hit_list) > 0:
            self.player_score += len(blocks_hit_list)

        # ALL GAME LOGIC SHOULD GO ABOVE THIS COMMENT

    def draw_game_objects(self):
        # ALL CODE TO DRAW SHOULD GO BELOW THIS COMMENT
        screen.fill(COLOR_BLACK)

        self.wall_list.draw(screen)
        self.gate_list.draw(screen)
        self.sprites_list.draw(screen)
        self.enemies_list.draw(screen)

        text = font.render("Score: " + str(self.player_score) + "/" + str(len(self.block_list)), True, COLOR_RED)
        screen.blit(text, [10, 10])

        # Player won if all coins collected and enemies are lesser than 128
        if len(self.block_list) == 0 and len(self.enemy_objs) < 128:
            self.game_over("Congratulations, you won!", 145)
        elif len(self.enemy_objs) == 128:
            self.game_over("Game Over!", 235)

        # enemy_hit_list = pygame.sprite.spritecollide(self.player_obj, self.enemies_list, False)
        #
        # if enemy_hit_list:
        #     self.game_over("Game Over!", 235)

        # ALL CODE TO DRAW SHOULD GO ABOVE THIS COMMENT

    def reset_game(self):
        self.sprites_list = pygame.sprite.RenderPlain()
        self.block_list = pygame.sprite.RenderPlain()
        self.player_list = pygame.sprite.RenderPlain()
        self.enemies_list = pygame.sprite.RenderPlain()
        self.wall_list = pygame.sprite.RenderPlain()
        self.gate_list = pygame.sprite.RenderPlain()

        self.player_obj = None
        self.enemy_objs = {}

        self.player_score = 0

        self.run()

    def game_over(self, message, left):

        while True:
            # ALL EVENT PROCESSING SHOULD GO BELOW THIS COMMENT
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_ESCAPE:
                        pygame.quit()
                    if event.key == pygame.K_RETURN:
                        self.reset_game()

            # Grey background
            w = pygame.Surface((400, 200))  # the size of your rect
            w.set_alpha(10)  # alpha level
            w.fill((128, 128, 128))  # this fills the entire surface
            screen.blit(w, (100, 200))  # (0,0) are the top-left coordinates

            # Won or lost
            text1 = font.render(message, True, COLOR_WHITE)
            screen.blit(text1, [left, 233])

            text2 = font.render("To play again, press ENTER.", True, COLOR_WHITE)
            screen.blit(text2, [135, 303])
            text3 = font.render("To quit, press ESCAPE.", True, COLOR_WHITE)
            screen.blit(text3, [165, 333])

            pygame.display.flip()
            clock.tick(clock_sec)

    def run_game(self):

        while self.monitor_player_input():
            self.update_game_objects()
            self.draw_game_objects()

            pygame.display.flip()
            clock.tick(clock_sec)

        pygame.quit()


Pacman()
