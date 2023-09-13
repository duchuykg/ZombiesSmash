import pygame
import random

from pygame import *
import math as mp
import asyncio

class ZombiesSmash:
    def __init__(self):
        self.SCREEN_WIDTH = 1200
        self.SCREEN_HEIGHT = 670
        self.FPS = 60
        self.MOLE_WIDTH = 90
        self.MOLE_HEIGHT = 81
        self.FONT_SIZE = 31
        self.FONT_TOP_MARGIN = 26
        self.LEVEL_SCORE_GAP = 4
        self.LEFT_MOUSE_BUTTON = 1
        
        # Initialize player's score, number of missed hits and level
        self.score = 0
        self.misses = 0
        self.level = 1
        # Initialize screen
        self.screen = pygame.display.set_mode((self.SCREEN_WIDTH, self.SCREEN_HEIGHT))
        pygame.display.set_caption("Zombies Smash")
        self.background = pygame.image.load("img/bg3.png")
        icon = pygame.image.load(r'img\logo.webp')
        pygame.display.set_icon(icon)

        # Font object for displaying text
        self.font_obj = pygame.font.Font('./fonts/Purple Smile.ttf', self.FONT_SIZE)
        # Initialize the zombies's sprite sheet
        sprite_sheet = pygame.image.load("img/zombies.png")
        self.zombies = []
        self.zombies.append(sprite_sheet.subsurface(853, 0, 120, 100))
        self.zombies.append(sprite_sheet.subsurface(310, 0, 120, 100))
        self.zombies.append(sprite_sheet.subsurface(455, 0, 120, 100))
        self.zombies.append(sprite_sheet.subsurface(580, 0, 120, 100))
        self.zombies.append(sprite_sheet.subsurface(722, 0, 120, 100))
        self.zombies.append(sprite_sheet.subsurface(853, 0, 120, 100))
        
        self.hammer_mouse  = pygame.image.load("img/hammer_mouse.png")
        self.hammer_smash  = pygame.image.load("img/hammer_smash.png")
        # hammer_sprite_sheet  = pygame.image.load("img/sahammer.png")
        # self.hammers = []
        # self.hammers.append(hammer_sprite_sheet.subsurface(42, 10, 100, 168))
        # self.hammers.append(hammer_sprite_sheet.subsurface(223, 12, 140, 165))
        # self.hammers.append(hammer_sprite_sheet.subsurface(407, 40, 169, 132))
        # self.hammers.append(hammer_sprite_sheet.subsurface(573, 50, 178, 105))

        # Positions of the holes in background
        self.hole_positions = []
        self.hole_positions.append((324, 386))
        self.hole_positions.append((232, 519))
        self.hole_positions.append((489, 447))
        self.hole_positions.append((641, 523))
        self.hole_positions.append((788, 448))
        self.hole_positions.append((1012, 409))
        
        self.soundEffect = SoundEffect()

    # Calculate the player level according to his current score & the LEVEL_SCORE_GAP constant
    def get_player_level(self):
        newLevel = 1 + int(self.score / self.LEVEL_SCORE_GAP)
        if newLevel != self.level:
            # if player get a new level play this sound
            self.soundEffect.playLevelUp()
        return 1 + int(self.score / self.LEVEL_SCORE_GAP)

    # Get the new duration between the time the mole pop up and down the holes
    # It's in inverse ratio to the player's current level
    def get_interval_by_level(self, initial_interval):
        new_interval = initial_interval - self.level * 0.15
        if new_interval > 0:
            return new_interval
        else:
            return 0.05

    # Check whether the mouse click hit the mole or not
    def is_mole_hit(self, mouse_position, current_hole_position):
        mouse_x = mouse_position[0]
        mouse_y = mouse_position[1]
        current_hole_x = current_hole_position[0]
        current_hole_y = current_hole_position[1]
        if (mouse_x > current_hole_x) and (mouse_x < current_hole_x + self.MOLE_WIDTH) and (mouse_y > current_hole_y) and (mouse_y < current_hole_y + self.MOLE_HEIGHT):
            return True
        else:
            return False      
        
    # Update the game states, re-calculate the player's score, misses, level
    def update(self):
        # Update the player's score
        current_score_string = "SCORE: " + str(self.score)
        score_text = self.font_obj.render(current_score_string, True, (255, 255, 255))
        score_text_pos = score_text.get_rect()
        score_text_pos.centerx = self.SCREEN_WIDTH / 5 * 4
        score_text_pos.centery = self.FONT_TOP_MARGIN
        self.screen.blit(score_text, score_text_pos)
        # Update the player's misses
        current_misses_string = "MISSES: " + str(self.misses)
        misses_text = self.font_obj.render(current_misses_string, True, (255, 255, 255))
        misses_text_pos = misses_text.get_rect()
        misses_text_pos.centerx = self.SCREEN_WIDTH / 5 * 3
        misses_text_pos.centery = self.FONT_TOP_MARGIN
        self.screen.blit(misses_text, misses_text_pos)
        # Update the player's level
        current_level_string = "LEVEL: " + str(self.level)
        level_text = self.font_obj.render(current_level_string, True, (255, 255, 255))
        level_text_pos = level_text.get_rect()
        level_text_pos.centerx = self.SCREEN_WIDTH / 5 * 1
        level_text_pos.centery = self.FONT_TOP_MARGIN
        self.screen.blit(level_text, level_text_pos)

    # Start the game's main loop
    # Contains some logic for handling animations, mole hit events, etc..
    async def start(self):
        hole_num = 0
        cycle_time = 0
        num = -1
        loop = True
        is_down = True
        interval = 0.1
        initial_interval = 1
        # Time control variables
        clock = pygame.time.Clock()
        pic = None

        while loop:
            for event in pygame.event.get():
                click = False
                if event.type == pygame.QUIT:
                    loop = False
                
                if event.type == MOUSEBUTTONDOWN and event.button == self.LEFT_MOUSE_BUTTON:  
                    click = True                
                    self.soundEffect.playFire()
                    if self.is_mole_hit(mouse.get_pos(), self.hole_positions[hole_num]) and num > 0 and is_down == True:
                        num = 3
                        is_down = False
                        interval = 0
                        self.score += 1  # Increase player's score
                        self.level = self.get_player_level()  # Calculate player's level
                        # Stop popping sound effect
                        self.soundEffect.stopPop()
                        # Play hurt sound
                        self.soundEffect.playHurt()
                        self.update()
                    else:
                        self.misses += 1
                        self.update()
            
            mil = clock.tick(self.FPS)
            self.screen.fill((0, 0, 0))
            self.screen.blit(self.background, (0, 0))
            pygame.mouse.set_visible(False)
            if pic is not None:
                self.screen.blit(pic, (self.hole_positions[hole_num][0], self.hole_positions[hole_num][1]))
            if click == True:
                self.screen.blit(self.hammer_smash, pygame.mouse.get_pos())
            else:
                self.screen.blit(self.hammer_mouse, pygame.mouse.get_pos())
                
            self.update()
            

            if num > 5:
                num = -1
                pic = None
                is_down = False

            if num == -1:
                num = 0
                is_down = False
                interval = 0.5
                hole_num = random.randint(0, 5)
                
            sec = mil / 1000.0
            cycle_time += sec
            if cycle_time > interval:
                # self.update_background()
                pic = self.zombies[num]
                self.screen.blit(self.background, (0, 0)) 
                self.screen.blit(pic, (self.hole_positions[hole_num][0], self.hole_positions[hole_num][1]))
                self.screen.blit(self.hammer_mouse, pygame.mouse.get_pos())
                self.update()
                if is_down is False:
                    num += 1
                else:
                    num -= 1
                if num == 4:
                    interval = 0.3
                elif num == 3:
                    num -= 1
                    is_down = True
                    self.soundEffect.playPop()
                    interval = self.get_interval_by_level(initial_interval)  # get the newly decreased interval value
                else:
                    interval = 0.1
                cycle_time = 0
            # Update the display
            pygame.display.flip()
            await asyncio.sleep(0)

class SoundEffect:
    def __init__(self):
        self.mainTrack = pygame.mixer.music.load("sounds/themesong.wav")
        self.fireSound = pygame.mixer.Sound("sounds/fire.wav")
        self.fireSound.set_volume(1.0)
        self.popSound = pygame.mixer.Sound("sounds/pop.wav")
        self.hurtSound = pygame.mixer.Sound("sounds/hurt.wav")
        self.levelSound = pygame.mixer.Sound("sounds/point.wav")
        pygame.mixer.music.play(-1)

    def playFire(self):
        self.fireSound.play()

    def stopFire(self):
        self.fireSound.sop()

    def playPop(self):
        self.popSound.play()

    def stopPop(self):
        self.popSound.stop()

    def playHurt(self):
        self.hurtSound.play()

    def stopHurt(self):
        self.hurtSound.stop()

    def playLevelUp(self):
        self.levelSound.play()

    def stopLevelUp(self):
        self.levelSound.stop()

# Initialize the game
pygame.mixer.init(frequency=22050, size=-16, channels=2, buffer=512)
pygame.init()

my_game = ZombiesSmash()
asyncio.run(my_game.start())

pygame.quit()
