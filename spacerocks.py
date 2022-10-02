 #importing the random, math, and arcade libraries.
import random
import math
import arcade
 
 #importing the keybroad for movement
from typing import cast
 
 #Setting up the game window
 
STARTING_SPACEROCK_COUNT =3
SCALE = 0.5
OFFSCREEN_SPACE = 300
SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600
SCREEN_TITLE = "SPACE ROCKS"
LEFT_LIMIT = -OFFSCREEN_SPACE
RIGHT_LIMIT = SCREEN_WIDTH + OFFSCREEN_SPACE
BOTTOM_LIMIT = -OFFSCREEN_SPACE
TOP_LIMIT = SCREEN_HEIGHT + OFFSCREEN_SPACE
 
    # this is so the sprites turn as the input keys are pressed
class TurningSprite(arcade.Sprite):
     def update(self):
         super().update()
         self.angle = math.degrees(math.atan2(self.change_y, self.change_x))
 
    # This is where the ship comes from        
class ShipSprite(arcade.Sprite):
    def __init__(self, filename, scale):
        super().__init__(filename, scale)
        self.thrust = 0
        self.speed = 0
        self.max_speed = 4
        self.drag  = 0.05
        self.respawning = 0
        self.respawn()
        
    #what happens when you die and respawn
    def respawn(self):
        self.respawning = 1
        self.center_x = SCREEN_WIDTH / 2
        self.center_y = SCREEN_HEIGHT / 2
        self.angle = 0
        
    #updates location as well as speed and drag on ship
    def update(self):
        if self.respawning:
            self.respawning += 1
            self.alpha = self.respawning
            if self.respawning > 250:
                self.respawning = 0
                self.alpha = 255
        if self.speed > 0:
            self.speed -= self.drag
            if self.speed < 0:
                self.speed = 0
                
        if self.speed < 0:
            self.speed += self.drag
            if self.speed > 0:
                self.speed = 0
                
        self.speed += self.thrust
        if self.speed > self.max_speed:
            self.speed = self.max_speed
        if self.speed < -self.max_speed:
            self.speed = -self.speed
            
        self.change_x = -math.sin(math.radians(self.angle)) * self.speed
        self.change_y = math.cos(math.radians(self.angle)) * self.speed

        self.center_x += self.change_x
        self.center_y += self.change_y
        
        #move ship from one side of the screen to the other
        if self.right < 0:
            self.left = SCREEN_WIDTH

        if self.left > SCREEN_WIDTH:
            self.right = 0

        if self.bottom < 0:
            self.top = SCREEN_HEIGHT

        if self.top > SCREEN_HEIGHT:
            self.bottom = 0
        
            #gets the parent class
        super().update()
    
    #spacerock class    
class SpacerockSprite(arcade.Sprite):
    def __init__(self, image_file_name, scale):
        super().__init__(image_file_name, scale=scale)
        self.size = 0
        
    def update(self):
        #moving the spacerocks around
        super().update()
        if self.center_x < LEFT_LIMIT:
            self.center_x = RIGHT_LIMIT
        if self.center_x > RIGHT_LIMIT:
            self.center_x = LEFT_LIMIT
        if self.center_y > TOP_LIMIT:
            self.center_y = BOTTOM_LIMIT
        if self.center_y < BOTTOM_LIMIT:
            self.center_y = TOP_LIMIT
            
    # Main game class       
class MyGame(arcade.Window):
    
    def __init__(self):
        super().__init__(SCREEN_WIDTH, SCREEN_HEIGHT, SCREEN_TITLE)
        
        self.game_over = False
        
        #self.background = arcade.load_textures("background.jpg")

        # Sprite lists
        self.player_sprite_list = arcade.SpriteList()
        self.spacerock_list = arcade.SpriteList()
        self.bullet_list = arcade.SpriteList()
        self.ship_life_list = arcade.SpriteList()

        # Set up the player
        self.score = 0
        self.player_sprite = None
        self.lives = 3
        
        # Text
        self.text_score = None
        self.text_spacerock_count = None
        
    def start_new_game(self):
        # Set up the game and initialize the variables

        self.game_over = False

        # Sprite lists
        self.player_sprite_list = arcade.SpriteList()
        self.spacerock_list = arcade.SpriteList()
        self.bullet_list = arcade.SpriteList()
        self.ship_life_list = arcade.SpriteList()
   
        # Set up the player
        self.score = 0
        self.player_sprite = ShipSprite("spaceship1.png", SCALE)
        self.player_sprite_list.append(self.player_sprite)
        self.lives = 3
        
        # Set up the little icons that represent the player lives.
        cur_pos = 10
        for i in range(self.lives):
            life = arcade.Sprite("spaceship1.png",
                                 SCALE)
            life.center_x = cur_pos + life.width
            life.center_y = life.height
            cur_pos += life.width
            self.ship_life_list.append(life)
            
        # Make the spacerocks
        image_list = ("spacerock.png")
        for i in range(STARTING_SPACEROCK_COUNT):
            image_no = random.randrange(4)
            enemy_sprite = SpacerockSprite(image_list[image_no], SCALE)
            enemy_sprite.guid = "Spacerock"

            enemy_sprite.center_y = random.randrange(BOTTOM_LIMIT, TOP_LIMIT)
            enemy_sprite.center_x = random.randrange(LEFT_LIMIT, RIGHT_LIMIT)

            enemy_sprite.change_x = random.random() * 2 - 1
            enemy_sprite.change_y = random.random() * 2 - 1

            enemy_sprite.change_angle = (random.random() - 0.5) * 2
            enemy_sprite.size = 4
            self.spacerock_list.append(enemy_sprite)
    
        # Create new text objects with initial values
        self.text_score = arcade.Text(
            f"Score: {self.score}",
            start_x=10,
            start_y=70,
            font_size=13,
        )
        self.text_spacerock_count = arcade.Text(
            f"Spacerock Count: {len(self.spacerock_list)}",
            start_x=10,
            start_y=50,
            font_size=13,
        )    
        
    def on_draw(self):
        # clears the screen and renders the window
        
        self.clear()

        # Draw all the sprites.
        self.spacerock_list.draw()
        self.ship_life_list.draw()
        self.bullet_list.draw()
        self.player_sprite_list.draw()

        # Draw the text
        self.text_score.draw()
        self.text_spacerock_count.draw()   
        
    def on_key_press(self, symbol, modifiers):
        
        # Shoot if the player hit the space bar and we aren't respawning.
        if not self.player_sprite.respawning and symbol == arcade.key.SPACE:
            bullet_sprite = TurningSprite(":resources:images/space_shooter/"
                                          "laserBlue01.png",
                                          SCALE)
            bullet_sprite.guid = "Bullet"

            bullet_speed = 30
            bullet_sprite.change_y = \
                math.cos(math.radians(self.player_sprite.angle)) * bullet_speed
            bullet_sprite.change_x = \
                -math.sin(math.radians(self.player_sprite.angle)) \
                * bullet_speed

            bullet_sprite.center_x = self.player_sprite.center_x
            bullet_sprite.center_y = self.player_sprite.center_y
            bullet_sprite.update()

            self.bullet_list.append(bullet_sprite)

        if symbol == arcade.key.LEFT:
            self.player_sprite.change_angle = 3
        elif symbol == arcade.key.RIGHT:
            self.player_sprite.change_angle = -3
        elif symbol == arcade.key.UP:
            self.player_sprite.thrust = 0.15
        elif symbol == arcade.key.DOWN:
            self.player_sprite.thrust = -.2
        
    def on_key_release(self, symbol, modifiers):
        # Called whenever a key is released
        if symbol == arcade.key.LEFT:
            self.player_sprite.change_angle = 0
        elif symbol == arcade.key.RIGHT:
            self.player_sprite.change_angle = 0
        elif symbol == arcade.key.UP:
            self.player_sprite.thrust = 0
        elif symbol == arcade.key.DOWN:
            self.player_sprite.thrust = 0
            
    def split_spacerock(self, spacerock: SpacerockSprite):
        
        # Split an spacerock into chunks. 
        x = spacerock.center_x
        y = spacerock.center_y
        self.score += 1

        if spacerock.size == 4:
            for i in range(3):
                image_no = random.randrange(2)
                image_list = [":resources:images/space_shooter/meteorGrey_med1.png",
                              ":resources:images/space_shooter/meteorGrey_med2.png"]

                enemy_sprite = SpacerockSprite(image_list[image_no],
                                              SCALE * 1.5)

                enemy_sprite.center_y = y
                enemy_sprite.center_x = x

                enemy_sprite.change_x = random.random() * 2.5 - 1.25
                enemy_sprite.change_y = random.random() * 2.5 - 1.25

                enemy_sprite.change_angle = (random.random() - 0.5) * 2
                enemy_sprite.size = 3

                self.spacerock_list.append(enemy_sprite)

        elif spacerock.size == 3:
            for i in range(3):
                image_no = random.randrange(2)
                image_list = [":resources:images/space_shooter/meteorGrey_small1.png",
                              ":resources:images/space_shooter/meteorGrey_small2.png"]

                enemy_sprite = SpacerockSprite(image_list[image_no],
                                              SCALE * 1.5)

                enemy_sprite.center_y = y
                enemy_sprite.center_x = x

                enemy_sprite.change_x = random.random() * 3 - 1.5
                enemy_sprite.change_y = random.random() * 3 - 1.5

                enemy_sprite.change_angle = (random.random() - 0.5) * 2
                enemy_sprite.size = 2

                self.spacerock_list.append(enemy_sprite)
                
        elif spacerock.size == 2:
            for i in range(3):
                image_no = random.randrange(2)
                image_list = [":resources:images/space_shooter/meteorGrey_tiny1.png",
                              ":resources:images/space_shooter/meteorGrey_tiny2.png"]

                enemy_sprite = SpacerockSprite(image_list[image_no],
                                              SCALE * 1.5)

                enemy_sprite.center_y = y
                enemy_sprite.center_x = x

                enemy_sprite.change_x = random.random() * 3.5 - 1.75
                enemy_sprite.change_y = random.random() * 3.5 - 1.75

                enemy_sprite.change_angle = (random.random() - 0.5) * 2
                enemy_sprite.size = 1

                self.spacerock_list.append(enemy_sprite)

    def on_update(self, x):
        """ Move everything """

        if not self.game_over:
            self.spacerock_list.update()
            self.bullet_list.update()
            self.player_sprite_list.update()

            for bullet in self.bullet_list:
                spacerocks = arcade.check_for_collision_with_list(bullet,
                                                                 self.spacerock_list)

                for spacerock in spacerocks:
                    # expected spacerockSprite, got Sprite instead
                    self.split_spacerock(cast(SpacerockSprite, spacerock))
                    spacerock.remove_from_sprite_lists()
                    bullet.remove_from_sprite_lists()

                # Remove bullet if it goes off-screen
                size = max(bullet.width, bullet.height)
                if bullet.center_x < 0 - size:
                    bullet.remove_from_sprite_lists()
                if bullet.center_x > SCREEN_WIDTH + size:
                    bullet.remove_from_sprite_lists()
                if bullet.center_y < 0 - size:
                    bullet.remove_from_sprite_lists()
                if bullet.center_y > SCREEN_HEIGHT + size:
                    bullet.remove_from_sprite_lists()

            if not self.player_sprite.respawning:
                spacerocks = arcade.check_for_collision_with_list(self.player_sprite,
                                                                 self.spacerock_list)
                if len(spacerocks) > 0:
                    if self.lives > 0:
                        self.lives -= 1
                        self.player_sprite.respawn()
                        self.split_spacerock(cast(SpacerockSprite, spacerocks[0]))
                        spacerocks[0].remove_from_sprite_lists()
                        self.ship_life_list.pop().remove_from_sprite_lists()
                        print("Crash")
                    else:
                        self.game_over = True
                        print("Game over")

        # Update the text objects
        self.text_score.text = f"Score: {self.score}"
        self.text_spacerock_count.text = f"Spacerock Count: {len(self.spacerock_list)}"   
     
            
def main():
    
    window = MyGame()
    window.start_new_game()
    arcade.run()
    
if __name__ == "__main__":
    main()
