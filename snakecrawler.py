import pygame
import random
import os
from sys import exit

pygame.init()

screen_width = 400
screen_height = 600
screen = pygame.display.set_mode((screen_width,screen_height),pygame.RESIZABLE)
pygame.display.set_caption("Snake Crawler")
directory = os.getcwd()
clock = pygame.time.Clock()
fps = 60

original_coins = 0
coins = 0
items = ""
#Checking if savefile exist with os import and if it exist, read it then apply it to the game ,
if os.path.exists(f"{directory}\savefile.txt"):
    with open(f"{directory}\savefile.txt","r") as file:
        stats = file.readline()
        if len(stats) >= 3 : #Making sure the length of first line is atleast 3 as a default value of saving
            seperate = stats.index(":")
            high_score = int(stats[ 0 : seperate])
            original_coins = int(stats[ seperate + 1 : ])
            coins += original_coins

            items = file.read() #Reading the rest of the file as shop items 
        else:
            high_score = 0
            coins = 0
            items = "" 
        file.close()
else:
    high_score = 0
    coins = 0
    items = ""

#Some global variables to be used later on
score = 0
game_time = 0
away_time = 0
counter_fade = 0
extra_life = 0
scroll_thres = 200
background_scroll = 0
fps = 60
game_active = False 
first_game = True
shop_game = False


#Minecraft font imports
small_font = pygame.font.SysFont(f"{directory}\Minecraft.ttf" , 25)
large_font = pygame.font.SysFont(f"{directory}\Minecraft.ttf" , 28)

class Shop():
    def __init__(self):
        #Importing images of shop and their item images
        shop_background1 = pygame.image.load(f"{directory}\sprite\shop_background.png").convert_alpha()
        shop_background2 = pygame.image.load(f"{directory}\sprite\shop_background2.png").convert_alpha() 
        self.shop_background = [shop_background1,shop_background2]
        self.shop_index = 0
        self.image = self.shop_background
        self.rect = self.image[self.shop_index].get_rect()

        #Using the Button for when buying an item
        self.item1_button = Button(50,100,4)
        self.item2_button = Button(130,100,5)
        self.item3_button = Button(210,100,6)
        self.item4_button = Button(290,100,7)
    def draw(self):
        #Update the item sprite
        global extra_life
        if "shop_background2" in items : self.shop_index = 1
        screen.blit(self.image[self.shop_index],self.rect)
        draw_text("Coins: "+ str(coins), large_font, "Black", 175, 0)
        
        self.item1_button.buy("shop_background2",500)
        draw_text("500",large_font,"Black",65,180)

        self.item2_button.buy("extra_life",2000)
        draw_text("2000",large_font,"Black",140,180)

        self.item3_button.buy("extra_life2",3000)
        draw_text("3000",large_font,"Black",220,180)

        self.item4_button.buy("extra_life3",5000)
        draw_text("5000",large_font,"Black",295,180)

class Background():
    def __init__(self):
        self.background = pygame.image.load(f"{directory}\sprite\sky.png").convert_alpha()
        self.image = self.background
        self.rect = self.image.get_rect() 

    def draw_background(self,background_scrolls): 
        screen.blit(self.background,(0, 0 + background_scrolls))
        screen.blit(self.background,(0, -600 + background_scrolls))

class Button():
    def __init__(self, x, y, type):
        start_image1 = pygame.image.load(f"{directory}\sprite\start_button.png").convert_alpha()
        start_image2 = pygame.image.load(f"{directory}\sprite\start_button_hover.png").convert_alpha()

        shop_image1 = pygame.image.load(f"{directory}\sprite\shop_button.png").convert_alpha()
        shop_image2 = pygame.image.load(f"{directory}\sprite\shop_button_hover.png").convert_alpha()

        retry_image1 = pygame.image.load(f"{directory}\sprite\etry_button.png").convert_alpha()
        retry_image2 = pygame.image.load(f"{directory}\sprite\etry_button_hover.png").convert_alpha()

        back_image1 = pygame.image.load(f"{directory}\sprite\ck_button.png").convert_alpha()
        back_image2 = pygame.image.load(f"{directory}\sprite\ck_button_hover.png").convert_alpha()

        shop_background2_icon = pygame.image.load(f"{directory}\sprite\shop_background2_icon.png").convert_alpha()
        extra_life_icon = pygame.image.load(f"{directory}\sprite\life.png").convert_alpha()

        soldout = pygame.image.load(f"{directory}\sprite\soldout.png").convert_alpha()

        self.available = True
        self.type_index = type
        self.number_index = 0
        image = [[start_image1,start_image2],[shop_image1,shop_image2],[retry_image1,retry_image2],[back_image1,back_image2],[shop_background2_icon,soldout],[extra_life_icon,soldout],[extra_life_icon,soldout],[extra_life_icon,soldout]]
        self.image = image
        self.rect = self.image[self.type_index][self.number_index].get_rect()
        self.rect.topleft = (x,y)

    def draw(self):
        self.mouse_pos = pygame.mouse.get_pos()
        if self.rect.collidepoint(self.mouse_pos):
            self.number_index = 1
            if pygame.mouse.get_pressed()[0] == 1 : return True
        else :  self.number_index = 0
        screen.blit(self.image[self.type_index][self.number_index], (self.rect.x, self.rect.y))
    
    def buy(self,shop_item,price):
        global coins, items
        self.mouse_pos = pygame.mouse.get_pos()
        if self.rect.collidepoint(self.mouse_pos):
            self.number_index = 0
            if pygame.mouse.get_pressed()[0] == 1 and coins >= price :
                if shop_item not in items :
                    items = f"{items}{shop_item}\n"
                    coins -= price
                    savetxt(f"{directory}\savefile.txt","w")
        if shop_item in items : self.number_index = 1

        screen.blit(self.image[self.type_index][self.number_index], (self.rect.x, self.rect.y))
        return coins

class Player():
    def __init__(self,x,y):
        #Imports of player images for animation purposes, used in line 177
        player1 = pygame.image.load(f"{directory}\sprite\snakeleft1.png").convert_alpha()
        player1 = pygame.transform.scale(player1,(40,20))
        player2 = pygame.image.load(f"{directory}\sprite\snakeleft2.png").convert_alpha()
        player2 = pygame.transform.scale(player2,(40,20))
        self.player = [player1,player2]
        self.player_index = 0
        self.image = self.player[self.player_index]
        self.facing = True

        #Creating more defined rect for the player
        self.width = 40
        self.height = 20
        self.rect = pygame.Rect(0,0, self.width, self.height)
        self.rect.center = (x,y)

        #Players speed
        self.speed_y = 0


    def player_input(self):
        global extra_life
        scroll = 0
        changed_x = 0
        changed_y = 0

        #Changes the horizontal movement of player and their corresponding images
        keys = pygame.key.get_pressed()
        if keys[pygame.K_a] : 
            changed_x -= 10
            self.facing = False
        if keys[pygame.K_d] : 
            changed_x += 10
            self.facing = True

        #Animation loop for the player
        self.player_index += 0.125
        if self.player_index >= len(self.player) : self.player_index = 0
        self.image = self.player[int(self.player_index)]

        #Gravity affecting the player speed
        self.speed_y += 1
        changed_y += self.speed_y

        #Boundaries for player in screen
        if self.rect.left + changed_x < 0 : changed_x = 0 - self.rect.left
        if self.rect.right + changed_x > screen_width : changed_x = screen_width - self.rect.right

        #No collision to move player up when jumping and collision when falling
        for plat in platform_group:
            if plat.rect.colliderect(self.rect.x, self.rect.y + changed_y , self.width, self.height) :   
                if self.rect.bottom < plat.rect.centery :
                    if self.speed_y > 0 :
                        self.rect.bottom = plat.rect.top
                        changed_y = 0 
                        self.speed_y = -20


        #When the player touches the bottom of the screen with an extra life, they would bounce back up and minus the life
        if (self.rect.bottom + changed_y > screen_height) and extra_life >= 1: 
            changed_y = 0 
            self.speed_y = -35
            extra_life -=1

        #When above a certain scrolling point, the player wont move
        if self.rect.top <= scroll_thres : 
            if self.speed_y < 0 : scroll = -changed_y
            
        #After everything above, finally the movement of player is updated as the last one
        self.rect.x += changed_x
        self.rect.y += changed_y + scroll

        self.mask = pygame.mask.from_surface(self.image) #Used in line 410 where it helps pixel perfect image of player

        return scroll #Used in line 349

    def display_score(self):
        pygame.draw.rect(screen, "White", (0,0,screen_width, 12))
        pygame.draw.line(screen, "White", (0,12),(screen_width, 12),2)

        if "extra_life" in items : 
            draw_text("Score: "+ str(score), small_font, "Black", 5, 0)
            draw_text("Life: "+ str(extra_life), small_font, "Black", 125, 0)
            draw_text("Coins: "+ str(coins), small_font, "Black", 205, 0)
            draw_text("Time: "+ str(game_time), small_font, "Black", 333, 0)
        else :
            draw_text("Score: "+ str(score), small_font, "Black", 5, 0)
            draw_text("Coins: "+ str(coins), small_font, "Black", 155, 0)
            draw_text("Time: "+ str(game_time), small_font, "Black", 335, 0)

    def draw(self):
        screen.blit(pygame.transform.flip(self.image, self.facing, False), (self.rect.x, self.rect.y) )
        pygame.draw.rect(screen,"White",(self.rect), 1)

    def update(self):
        self.display_score()
        self.draw()

class Platform(pygame.sprite.Sprite):
    def __init__(self, x, y, width, movement):
        super().__init__() #Inheriting all of from pygame Sprite

        #The platform images and their given value from others
        platform_image = pygame.image.load(f"{directory}\sprite\platform.png").convert_alpha()
        self.image = pygame.transform.scale(platform_image,(width,10))
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y
        self.movement = movement

        #Determining the movement and direction of platform with randomness
        self.counter_movement = random.randint(0,50)
        self.direction_movement = random.choice([-1,1])

    def update(self, scroll):
        #How the platform move and their speed
        self.counter_movement += 1 
        self.rect.x += self.direction_movement * self.movement

        #When the platform touches the screen or reach their movement limit, change direction
        if self.counter_movement >= 100 or self.rect.left < 0 or self.rect.right > screen_width : 
            self.direction_movement *= -1
            self.counter_movement = random.randint(0,50)

        #If the player cant see the platform in the screen, kill with pygame.Sprite function
        self.rect.y += scroll
        if self.rect.top > screen_height : self.kill()

class Enemy(pygame.sprite.Sprite):
    def __init__(self, screen_width, y, speed):
        super().__init__() #Inheriting all of from pygame Sprite

        #Importing the enemy image and their given speed and random direction movement
        enemy = pygame.image.load(f"{directory}\sprite\enemy.png").convert_alpha()
        self.enemy_direction = random.choice([-1,1])
        self.speed = speed

        #Making sure the movement direction correspond to the face of bird
        if self.enemy_direction == 1 : self.facing = True
        else : self.facing = False
        self.image = pygame.transform.flip(enemy,self.facing,False)
        self.rect = self.image.get_rect()
        if self.enemy_direction == 1 :  self.rect.x = 0
        else : self.rect.x = screen_width
        self.rect.y = y

    def update(self,screen_width, scroll):
        #The actual movement of the enemy with their speed and wont move vertically when scrolled up
        self.rect.x += self.enemy_direction * 2 * self.speed
        self.rect.y += scroll

        if self.rect.right < 0 or self.rect.left > screen_width : self.kill()

def draw_text(text, font, color, x, y): #A fucntion to draw text 
    image = font.render(text, False, color)
    screen.blit(image, (x,y))

def savetxt(path,mode): #A function to save file 
        global high_score, original_coins, coins, items
        #Will update the save file if either the high score updates or coin is spend
        with open(path, mode) as file:
            if score > high_score :
                high_score = score
                file.write(f"{str(high_score)}:{str(coins)}\n{str(items)}")
            if original_coins > coins :
                    file.write(f"{str(high_score)}:{str(coins)}\n{str(items)}")


#The calling of classes and Sprites
shop = Shop()

background = Background()

start_button = Button(25,400,0)
shop_button = Button(225,400,1)
retry_button = Button(25,400,2)
back_button = Button(125,500,3)

player = Player(screen_width //2 , screen_height - 200 )

platform_group = pygame.sprite.Group()

platform = Platform(screen_width //2 - 50, screen_height - 50, 100, False)
platform_group.add(platform)
counter_platform = 10
plat_move = 0

enemy_group = pygame.sprite.Group()


                                                                                                                        # The main game loop
while True :
    for event in pygame.event.get():
        if event.type == pygame.QUIT :
            #Savefile the stats when its being closed
            savetxt(f"{directory}\savefile.txt","w")
            pygame.quit()
            exit()

                                                                                #Starting state check
    if first_game :
        screen.fill("Blue")
        if start_button.draw() : # Starting screen
            if "extra_life" in items : extra_life += 1 #Shop item check
            if "extra_life2" in items : extra_life += 1 #Shop item check
            if "extra_life3" in items : extra_life += 1 #Shop item check
            game_active = True 
            first_game = False
        elif shop_button.draw() or shop_game : # Go to shop screen
            shop_game = True
            shop.draw()
            if back_button.draw() : 
                shop_game = False   

        away_time = pygame.time.get_ticks() #The time spent outside of the actual game
    else :
        if game_active :                                                                                                                                    #Actual game state
            game_time = (pygame.time.get_ticks() - away_time) //1000 #Actual game time in seconds

            #How far the player had scroll up and add it to the background then repeat
            scroll = player.player_input()
            background_scroll += scroll
            if background_scroll >= 600 : background_scroll = 0
            Background.draw_background(background,background_scroll)

            #Numbers of platform allowed to be generated
            if len(platform_group) <= counter_platform :
                plat_y = platform.rect.y - random.randint(80,120)
                #Difficulties ramping with time
                if game_time < 10 : 
                    plat_type = 1
                    plat_x = random.randint(screen_width //2 - 75, screen_width //2 + 75)
                    plat_width = random.randint(80,100)
                elif 10 <= game_time < 20 :
                    plat_type = 2
                    plat_x = random.randint(screen_width //2 ,screen_width //2)
                    plat_width = random.randint(60,80)
                elif 20 <= game_time < 40 :
                    plat_type = 3
                    plat_width = random.randint(40,60)
                    plat_x = random.randint(0, screen_width - plat_width)
                else :
                    plat_type = 4
                    plat_width = random.randint(20,40)
                    plat_x = random.randint(0, screen_width)

                if   plat_type == 1 : plat_move = 0
                elif plat_type == 2 : plat_move = 1
                elif plat_type == 3 : plat_move = 2
                else :                plat_move = 3

                platform = Platform(plat_x, plat_y, plat_width, plat_move)
                platform_group.add(platform)

            platform_group.update(scroll)

            #Enemy bird spawning
            if len(enemy_group) == 0 :
                if plat_type >= 2 : 
                    bird = Enemy(screen_width, 120, 0.8)
                    enemy_group.add(bird)
                if plat_type >= 3 :
                    bird = Enemy(screen_width, 50, 1.5)
                    enemy_group.add(bird)
            enemy_group.update(screen_width,scroll)

                                                                    #The auto scrolling up the screen with value from before
            if scroll > 0:
                score += scroll
                coins += score//1000
            pygame.draw.line(screen, "White", (0, score - high_score + scroll_thres),(screen_width,score - high_score + scroll_thres),3)  #A line representing the high score
            draw_text("HIGH Score", small_font, "White", screen_width - 130, score - high_score + scroll_thres) # The text for high score

            #Updating the screen with new displays
            platform_group.draw(screen)
            enemy_group.draw(screen)
            player.update()

            #Checking if the collision of player and enemy_group is pixel perfect and ends the game if there are no life left, else minus the life
            if pygame.sprite.spritecollide(player, enemy_group, False) :
                if pygame.sprite.spritecollide(player, enemy_group, False, pygame.sprite.collide_mask) :
                    if extra_life >= 1 : 
                        extra_life -= 1
                        player.speed_y -= 35
                    else : game_active = False

            #End the game if the player is our of the screen
            if player.rect.top > screen_height : 
                game_active = False

                                                                                                                     #Game Over state
        else : 
            #Drawing the white game over screen until the display is fully covered
            if counter_fade < screen_height : 
                counter_fade += 7.5
                pygame.draw.rect(screen, "White", (0,0, screen_height, counter_fade))

            #Then continue
            else:
                #Save to txt
                savetxt(f"{directory}\savefile.txt","w")

                #Draw the text on screen
                draw_text(f"GAME OVER!", large_font, "Black", 125, 150)
                draw_text(f"Score: {score}", large_font, "Black", 125, 200)
                draw_text(f"Highscore: {high_score}", large_font, "Black", 125, 250)
                draw_text(f"Coins: {coins}", large_font, "Black", 125, 300)
            
                #The retry button will reset the game back to its default state to repeat the game
                if retry_button.draw() :
                    game_active = True 
                    game_active = True
                    score = 0
                    scroll = 0
                    counter_fade = 0
                    if "extra_life" in items : extra_life = 1
                    if "extra_life2" in items : extra_life = 1
                    if "extra_life3" in items : extra_life = 1
                    player.rect.center = (screen_width //2 , screen_height - 200 )
                    enemy_group.empty()
                    platform_group.empty()
                    platform = Platform(screen_width //2 - 50, screen_height - 50, 100,False)
                    platform_group.add(platform)
                    game_time = 0
                    away_time = pygame.time.get_ticks()

                #Or the player can move to the shop
                elif shop_button.draw() or shop_game : 
                    shop_game = True
                    shop.draw()

                    #When exiting, move back to the game over state but with faster drawing of white
                    if back_button.draw() : 
                        counter_fade = 100
                        game_time = 0
                        shop_game = False

    #The game fps and an update display
    clock.tick(fps)
    pygame.display.update()