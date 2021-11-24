import pygame


class Player(pygame.sprite.Sprite):
    # Set speed vector
    change_x = 0
    change_y = 0

    # Constructor function
    def __init__(self, x, y, filename):

        # Call the parent's constructor
        pygame.sprite.Sprite.__init__(self)

        self.spawn_x = x
        self.spawn_y = y
        self.filename = filename

        # Set height, width
        self.image = pygame.image.load(filename).convert()

        # Make our top-left corner the passed-in location.
        self.rect = self.image.get_rect()
        self.rect.top = y
        self.rect.left = x
        self.prev_x = x
        self.prev_y = y

    # Clear the speed of the player
    def prev_direction(self):
        self.prev_x = self.change_x
        self.prev_y = self.change_y

    # Change the speed of the player
    def move(self, x=None, y=None):
        self.change_x += x
        self.change_y += y

    # Find a new position for the player
    def update(self, walls, gate):

        # Get the old position, in case we need to go back to it
        old_x = self.rect.left
        new_x = old_x + self.change_x
        prev_x = old_x + self.prev_x
        self.rect.left = new_x

        old_y = self.rect.top
        new_y = old_y + self.change_y
        prev_y = old_y + self.prev_y

        # Did this update cause us to hit a wall?
        x_collide = pygame.sprite.spritecollide(self, walls, False)
        if x_collide:
            # Whoops, hit a wall. Go back to the old position
            self.rect.left = old_x
        else:
            self.rect.top = new_y

            # Did this update cause us to hit a wall?
            y_collide = pygame.sprite.spritecollide(self, walls, False)
            if y_collide:
                # Whoops, hit a wall. Go back to the old position
                self.rect.top = old_y

        if gate:
            gate_hit = pygame.sprite.spritecollide(self, gate, False)
            if gate_hit:
                self.rect.left = old_x
                self.rect.top = old_y

    def hit(self, enemies):
        return pygame.sprite.spritecollideany(self, enemies)


# Inherit Player class
class Ghost(Player):

    def __init__(self, x, y, filename, enemy_id, name, directions, wait=0):
        super().__init__(x, y, filename)
        self.enemy_id = enemy_id
        self.name = name
        self.directions = directions
        self.turn = 0
        self.steps = 0
        self.wait = wait
        self.dir_len = len(directions) - 1

    # Change the speed of the ghost
    def move(self, x=None, y=None):
        if self.wait == 0:
            total_steps = self.directions[self.turn][2]
            if self.steps < total_steps:
                self.steps += 1
            else:
                # Reset or Update Turns
                if self.turn < self.dir_len:
                    self.turn += 1
                elif self.name == "Clyde":
                    self.turn = 2
                else:
                    self.turn = 0
                self.steps = 0
            self.change_x = self.directions[self.turn][0]
            self.change_y = self.directions[self.turn][1]
        else:
            self.wait -= 1

