import pygame
import random

from pygame import *
import math as mp
import asyncio

class ZombiesSmash:
    def __init__(self):
        self.START_SCREEN_WIDTH = 1200 
        self.START_SCREEN_HEIGHT = 673
        self.SCREEN_WIDTH = 1200 
        self.SCREEN_HEIGHT = 670
        self.FPS = 60
        self.ZOMBIE_WIDTH = 100
        self.ZOMBIE_HEIGHT = 80
        self.FONT_SIZE = 32
        self.FONT_TOP_MARGIN = 35
        self.LEVEL_SCORE_GAP = 5
        self.LEFT_MOUSE_BUTTON = 1
        
        # Initialize player's score, number of missed hits and level
        self.score = 0
        self.total = -1
        self.misszombie = 0
        self.misses = 0
        self.level = 1
        self.is_playing = False
        self.status = 0
        # Initialize screen
        self.screen = pygame.display.set_mode((self.SCREEN_WIDTH, self.SCREEN_HEIGHT))
        pygame.display.set_caption("Zombies Smash")
        self.start_bg = pygame.image.load("img/start1.jpg")
        self.background = pygame.image.load("img/bg3.png")
        icon = pygame.image.load("img/logo.webp")
        pygame.display.set_icon(icon)
        self.start_button_x = 510
        self.start_button_y = 230
        self.start_button_width = 140
        self.start_button_height = 58
        self.con_button_width = 220
        self.con_button_height = 58

        # Font object for displaying text
        self.font_obj = pygame.font.Font("./fonts/PS.ttf", self.FONT_SIZE)
        self.font_start = pygame.font.Font("./fonts/BW.ttf", 50)
        # Initialize the zombies's sprite sheet
        sprite_sheet = pygame.image.load("img/zombies.png")
        self.zombies = []
        self.zombies.append(sprite_sheet.subsurface(853, 0, 10, 10))
        self.zombies.append(sprite_sheet.subsurface(310, 0, 120, 100))
        self.zombies.append(sprite_sheet.subsurface(455, 0, 120, 100))
        self.zombies.append(sprite_sheet.subsurface(580, 0, 120, 100))
        self.zombies.append(sprite_sheet.subsurface(722, 0, 120, 100))
        self.zombies.append(sprite_sheet.subsurface(853, 0, 120, 100))
        
        self.hammer_mouse = pygame.image.load("img/hammer_mouse.png")
        self.hammer_smash = pygame.image.load("img/hammer_smash.png")
        self.star_point = pygame.image.load("img/star.png")
        # hammer_sprite_sheet  = pygame.image.load("img/sahammer.png")
        # self.hammers = []
        # self.hammers.append(hammer_sprite_sheet.subsurface(42, 10, 100, 168))
        # self.hammers.append(hammer_sprite_sheet.subsurface(223, 12, 140, 165))
        # self.hammers.append(hammer_sprite_sheet.subsurface(407, 40, 169, 132))
        # self.hammers.append(hammer_sprite_sheet.subsurface(573, 50, 178, 105))

        # Positions of the holes in background
        self.hole_positions = []
        # for i in range(6):
        #     self.hole_positions.append((324, 386))
        self.hole_positions.append((324, 386))
        self.hole_positions.append((232, 519))
        self.hole_positions.append((489, 447))
        self.hole_positions.append((641, 523))
        self.hole_positions.append((788, 448))
        self.hole_positions.append((1012, 409))
        
        self.soundEffect = SoundEffect()

    # Calculate the player level according to his current score & the LEVEL_SCORE_GAP constant    
    def is_point_inside_rect(self, point_x, point_y, rect_x, rect_y, rect_width, rect_height):
        return rect_x <= point_x <= rect_x + rect_width and rect_y <= point_y <= rect_y + rect_height
    
    def draw_start_screen(self):
        if self.status == 0:
            mouse_x, mouse_y = pygame.mouse.get_pos()
            self.screen.blit(self.start_bg, (0, 0))
            if self.check_start_button_click(mouse_x, mouse_y):
                start_text_surface = self.font_start.render("Start", True, (255, 0, 0))
            else:
                start_text_surface = self.font_start.render("Start", True, (220, 220, 220))
            self.screen.blit(start_text_surface, (self.start_button_x, self.start_button_y))
            pygame.display.flip()
        elif self.status == 1:
            mouse_x, mouse_y = pygame.mouse.get_pos()
            self.screen.blit(self.start_bg, (0, 0))
            if self.check_con_button_click(mouse_x, mouse_y):
                start_text_surface = self.font_start.render("Continue", True, (220, 220, 220))
            else:
                start_text_surface = self.font_start.render("Continue", True, (255, 0, 0))
            self.screen.blit(start_text_surface, (self.start_button_x, self.start_button_y))                
            pygame.display.flip()
        elif self.status == 2:
            mouse_x, mouse_y = pygame.mouse.get_pos()
            self.screen.blit(self.background, (0, 0))
            current_score_string = "GAME OVER - SCORE: " + str(self.score)
            score_text = self.font_obj.render(current_score_string, True, (255, 255, 0))
            score_text_pos = score_text.get_rect()
            score_text_pos.centerx = self.SCREEN_WIDTH / 8 * 4
            score_text_pos.centery = self.SCREEN_HEIGHT / 4 * 2
            self.screen.blit(score_text, score_text_pos)
            if self.check_con_button_click(mouse_x, mouse_y):
                start_text_surface = self.font_start.render("Play again", True, (220, 220, 220))
            else:
                start_text_surface = self.font_start.render("Play again", True, (255, 0, 0))
            self.screen.blit(start_text_surface, (self.start_button_x, self.start_button_y))
            self.update()
            pygame.display.flip()

    def check_start_button_click(self, mouse_x, mouse_y):
        if self.is_point_inside_rect(mouse_x, mouse_y, self.start_button_x, self.start_button_y, self.start_button_width, self.start_button_height):
            return True
        return False
    
    def check_con_button_click(self, mouse_x, mouse_y):
        if self.is_point_inside_rect(mouse_x, mouse_y, self.start_button_x, self.start_button_y, self.con_button_width, self.con_button_height):
            return True
        return False
    

    def get_player_level(self):
        newLevel = 1 + int(self.score / self.LEVEL_SCORE_GAP)
        if newLevel != self.level:
            # if player get a new level play this sound
            self.soundEffect.playLevelUp()
        return 1 + int(self.score / self.LEVEL_SCORE_GAP)

    # Get the new duration between the time the zombie pop up and down the holes
    # It's in inverse ratio to the player's current level
    def get_interval_by_level(self, initial_interval):
        new_interval = initial_interval - self.level * 0.15
        if new_interval > 0.12:
            return new_interval
        else:
            return 0.12

    # Check whether the mouse click hit the zombie or not
    def is_zombie_hit(self, mouse_position, current_hole_position):
        mouse_x = mouse_position[0]
        mouse_y = mouse_position[1]
        current_hole_x = current_hole_position[0]
        current_hole_y = current_hole_position[1]
        if (mouse_x > current_hole_x) and (mouse_x < current_hole_x + self.ZOMBIE_WIDTH) and (mouse_y > current_hole_y - 50) and (mouse_y < current_hole_y + self.ZOMBIE_HEIGHT):
            return True
        else:
            return False      
        
    # Update the game states, re-calculate the player's score, misses, level
    def update(self):
        # Update the player's miss zombie
        current_score_string = "MISSED ZOMBIE: " + str(self.misszombie)
        score_text = self.font_obj.render(current_score_string, True, (128, 128, 128))
        score_text_pos = score_text.get_rect()
        score_text_pos.centerx = self.SCREEN_WIDTH / 5 * 4
        score_text_pos.centery = self.FONT_TOP_MARGIN
        self.screen.blit(score_text, score_text_pos)
        # Update the player's score
        current_score_string = "SCORE: " + str(self.score)
        score_text = self.font_obj.render(current_score_string, True, (255, 255, 0))
        score_text_pos = score_text.get_rect()
        score_text_pos.centerx = self.SCREEN_WIDTH / 5 * 3
        score_text_pos.centery = self.FONT_TOP_MARGIN
        self.screen.blit(score_text, score_text_pos)
        # Update the player's misses
        current_misses_string = "MISSES: " + str(self.misses)
        misses_text = self.font_obj.render(current_misses_string, True, (255, 0, 0))
        misses_text_pos = misses_text.get_rect()
        misses_text_pos.centerx = self.SCREEN_WIDTH / 5 * 2
        misses_text_pos.centery = self.FONT_TOP_MARGIN
        self.screen.blit(misses_text, misses_text_pos)
        # Update the player's level
        current_level_string = "LEVEL: " + str(self.level)
        level_text = self.font_obj.render(current_level_string, True, (0, 0, 255))
        level_text_pos = level_text.get_rect()
        level_text_pos.centerx = self.SCREEN_WIDTH / 5 * 1
        level_text_pos.centery = self.FONT_TOP_MARGIN
        self.screen.blit(level_text, level_text_pos)

    async def start(self):
        if self.status == 2 or self.status == 0:
            self.score = 0
            self.total = -1
            self.misszombie = 0
            self.misses = 0
            self.level = 1 
        hole_num = 0
        cycle_time = 0
        num = -1
        # num = 1, 2 zombie getup, num = 3, 4 smash zombie
        is_down = True
        interval = 0.1
        initial_interval = 1

        clock = pygame.time.Clock()
        pic = None
        click = False
        click_point = False     
                
        while self.is_playing:
            # misszombie - 1
            if self.misszombie == 10 or self.misses == 100:
                self.soundEffect.playGameover()
                self.status = 2
                self.is_playing = False
            mil = clock.tick(self.FPS)
            
            for event in pygame.event.get():                                   
                if event.type == pygame.QUIT:
                    pygame.mixer.music.load("sounds/rung.mp3")
                    pygame.mixer.music.play(-1)
                    self.status = 0
                    self.screen = pygame.display.set_mode((self.START_SCREEN_WIDTH, self.START_SCREEN_HEIGHT))
                    self.is_playing = False
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_ESCAPE:  
                        self.is_playing = False
                        self.status = 1

                click = False
                click_point = False
                
                pygame.mouse.set_visible(False)
                if event.type == MOUSEBUTTONDOWN and event.button == self.LEFT_MOUSE_BUTTON:  
                    self.soundEffect.playFire()
                    click = True               
                    self.screen.blit(self.zombies[4], pygame.mouse.get_pos())
                    
                    if self.is_zombie_hit(mouse.get_pos(), self.hole_positions[hole_num]) and num > 0 and is_down == True:
                        click = True  
                        click_point = True
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
            
            self.screen.fill((0, 0, 0))
            self.screen.blit(self.background, (0, 0))
            if pic is not None:
                self.screen.blit(pic, (self.hole_positions[hole_num][0], self.hole_positions[hole_num][1]))
            if click == True:
                self.screen.blit(self.hammer_smash, pygame.mouse.get_pos())
                # if click_point == True:
                #     self.screen.blit(self.star_point, (pygame.mouse.get_pos()[0] - 50, pygame.mouse.get_pos()[1] - 90))
            else:
                self.screen.blit(self.hammer_mouse, pygame.mouse.get_pos()) 
            
            self.update()
            # Start cycle
            if num > 5:
                num = -1
                pic = None
                is_down = False

            if num == -1:
                num = 0
                is_down = False
                interval = 0.5
                hole_num = random.randint(0, 5)
                self.total += 1
                self.misszombie = self.total - self.score
                
            sec = mil / 1000.0
            cycle_time += sec
            
            if cycle_time > interval:
                pic = self.zombies[num]
                self.screen.blit(self.background, (0, 0)) 
                self.screen.blit(pic, (self.hole_positions[hole_num][0], self.hole_positions[hole_num][1])) 
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
                    interval = 0.12
                cycle_time = 0
                
                if click == True:
                    self.screen.blit(self.hammer_smash, pygame.mouse.get_pos())
                    # if click_point == True:
                    #     self.screen.blit(self.star_point, (pygame.mouse.get_pos()[0] - 50, pygame.mouse.get_pos()[1] - 90))
                else:
                    self.screen.blit(self.hammer_mouse, pygame.mouse.get_pos()) 
                    
                self.update()

                
            # Update the display
                
            pygame.display.flip()

    async def menu(self):
        running = True

        while running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False
                elif event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                    if not self.is_playing:
                        mouse_x, mouse_y = pygame.mouse.get_pos()
                        if self.check_start_button_click(mouse_x, mouse_y) and self.status == 0: 
                            pygame.mixer.music.load("sounds/silent.mp3")
                            pygame.mixer.music.play(-1)                         
                            self.is_playing = True
                        elif self.check_con_button_click(mouse_x, mouse_y) and (self.status == 1 or self.status == 2):
                            if self.status == 2:
                                pygame.mixer.music.load("sounds/silent.mp3")
                                pygame.mixer.music.play(-1)
                            self.is_playing = True
            self.screen.fill((0, 0, 0))
            if self.is_playing:
                self.screen = pygame.display.set_mode((self.SCREEN_WIDTH, self.SCREEN_HEIGHT))
                await self.start()
            else:
                pygame.mouse.set_visible(True)
                self.draw_start_screen()
            
        pygame.quit()


class SoundEffect:
    def __init__(self):
        self.mainTrack = pygame.mixer.Sound("sounds/silent.mp3")
        self.startSound = pygame.mixer.Sound("sounds/start.mp3")
        self.rungSound = pygame.mixer.music.load("sounds/rung.mp3")
        self.fireSound = pygame.mixer.Sound("sounds/fire.wav")
        self.fireSound.set_volume(1)
        self.popSound = pygame.mixer.Sound("sounds/pop.wav")
        self.hurtSound = pygame.mixer.Sound("sounds/point.wav")
        self.levelSound = pygame.mixer.Sound("sounds/levelup.mp3")
        self.gameOver = pygame.mixer.Sound("sounds/gameover.wav")
        pygame.mixer.music.play(-1)

    def playGameover(self):
        self.gameOver.play()
    def playStart(self):
        self.startSound.play()
    def stopStart(self):
        self.startSound.stop()
        
    def playRung(self):
        self.rungSound.play()
    def stopRung(self):
        self.rungSound.stop()
        
    def playFire(self):
        self.fireSound.play()

    # def stopFire(self):
    #     self.fireSound.stop()

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

asyncio.run(my_game.menu())

pygame.quit()
