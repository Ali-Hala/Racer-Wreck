'''
Assignment - Final Project
Authors: AP, AH, BR, XZ
Due Date: 01/21/22
Question & Problem description: 
Class: ICS3UI-01
'''
#screen size is 810x810 (do not touch this comment)

# importing libraries - BR, Day 3
import pygame
import math
import time # for stopwatch - BR, Overtime

# initializing the constructor - XZ, Day 4
pygame.init()

# code for resizing images (initial images are a bit small) - BR, Day 3
# part of loading images 
def image_scale(image, factor):
    newsize = (image.get_width() * factor, image.get_height() * factor)
    return pygame.transform.scale(image, newsize)

# choice for loading in backgrounds - BR Day 4
grass = "grass.jpg"
mountain = "mountain.jpg"
dirt = "dirt.jpg"

#loading in background and the track since the track has no background - BR, Day 3
# scaling image is used (background can be a lot bigger since the screen will just show the track anyways)
background = image_scale(pygame.image.load(dirt), 2.5)
track = image_scale(pygame.image.load("track.png"), 0.9)

# loading in track border for mask (nessasary for collision checking) - BR, Day 4
track_border = image_scale(pygame.image.load("track-border.png"), 0.9)
track_mask = pygame.mask.from_surface(track_border)

# loading in finish line (for levels) - BR, Day 4
finish = pygame.image.load("finish.png")
finish_mask = pygame.mask.from_surface(finish)
finish_pos = (130, 250)

# setting up screen using the dimensions of the track image - BR, Day 3
WIDTH, HEIGHT = track.get_width(), track.get_height()
screen = pygame.display.set_mode((WIDTH, HEIGHT))

# setting a caption for the pygame window - BR, Day 3
game_name = "Racer Wreck"
pygame.display.set_caption(game_name)

# load in car images (finalized) - BR, Day 4
car1 = "grey-car.png" #use 0.5 scale (computer car)
car2 = "racecar.png" #use 0.1 scale
car_image = image_scale(pygame.image.load(car2), 0.1)
computer_car_image = image_scale(pygame.image.load(car1), 0.5)

# set up FPS limitation (will be called in main game loop) - BR, Day 3
FPS = 60

# get fonts - XZ, BR
font1 = pygame.font.SysFont("helvetica", 44)
smallfont = pygame.font.SysFont('Corbel',35)

# set up colours - XZ, Day 6
white = (255, 255, 255)
black = (0, 0, 0)
red = (255, 0, 0)
# light shade of the button - XZ
color_light = (170,170,170)
# dark shade of the button - XZ
color_dark = (100,100,100)

#button class - XZ
class Button():
  def __init__(self,x,y,image):
    self.image=image
    self.rect=self.image.get_rect()
    self.rect.topleft=(x,y)

  def draw(self):
    screen.blit(self.image,(self.rect.x, self.rect.y))

  def pressed(self):
    action = False
    for event in pygame.event.get():
    #get mouse position
      pos=pygame.mouse.get_pos()
    #check mouseover and clicked condition
      if event.type == pygame.MOUSEBUTTONDOWN: # is some button clicked
        if event.button == 1: # is left button clicked
          if self.rect.collidepoint(pos):
            action=True
    return action

# game start, end, level control - AH, BR (Day 5/6)
class GameControl:
  gamelevels = 10 # 10 levels in game before the player wins
  def __init__(self, level=1): #when calling function, always call "level" by AH, Day 5
    self.level = level
    self.start = False

  def levelup(self):
    self.level += 1
    self.start = False
  
  def level_start(self):
    self.start = True
    self.start_time = time.time() #to find out the time when the player starts actually playing the level - BR, Overtime

  def level_time(self):
    if not self.start:
        return 0
    return round(time.time() - self.start_time) # to return how long the player has been playing the level in seconds

  # for when the game is restarted
  def reset(self):
    self.level = 1
    self.start = False
    self.start_time = 0

  def game_end(self):
    return self.level > self.gamelevels

# path of the computer car (coordinates gained through trial and error) - BR, Day 5
path = [(175, 119), (110, 70), (56, 133), (70, 481), (318, 731), (404, 680), (418, 521), (507, 475), (600, 551), (613, 715), (736, 713),(734, 399), (611, 357), (409, 343), (433, 257), (697, 258), (738, 123), (581, 71), (303, 78), (275, 377), (176, 388), (178, 260)]
# code for rotating an image on the screen (car movement) - BR, Day 3
def blit_rotate(screen, image, top_left, angle):
    rotated_image = pygame.transform.rotate(image, angle)
    new_rect = rotated_image.get_rect(
        center=image.get_rect(topleft=top_left).center)
    screen.blit(rotated_image, new_rect.topleft)

# Car class with everything that is needed for bliting the car on the screen, moving the image, rotating the image, etc. (can add more to this class) - BR, Day 3
# Tested by A.H.
class Car:
  def __init__(self, max_velocity, rotation_velocity):
      self.image = self.IMAGE
      self.max_velocity = max_velocity
      self.velocity = 0 #starting velocity 
      self.rotation_velocity = rotation_velocity
      self.angle = 0 #starting angle (no angle change) 
      self.x, self.y = self.start_pos
      self.acceleration = 0.1 #acceleration rate

  def rotate(self, left=False, right=False):
      if left==True:
          self.angle += self.rotation_velocity
      elif right==True:
          self.angle -= self.rotation_velocity

  def draw(self, screen):
      blit_rotate(screen, self.image, (self.x, self.y), self.angle)

  def move_forward(self):
      self.velocity = min(self.velocity + self.acceleration, self.max_velocity)
      self.move()

  # moving backwards code
  def move_backward(self):
      self.velocity = max(self.velocity - self.acceleration, -self.max_velocity/2)
      self.move()

  # borrowed code idea from: https://pretagteam.com/question/how-to-move-a-sprite-according-to-an-angle-in-pygame for cosine and sine calculations when moving at an angle - BR, Day 3
  def move(self):
      radians = math.radians(self.angle)
      vertical = math.cos(radians) * self.velocity
      horizontal = math.sin(radians) * self.velocity

      self.y -= vertical
      self.x -= horizontal

  # collision code idea source: http://renesd.blogspot.com/2017/03/pixel-perfect-collision-detection-in.html
  def collision(self, mask, x=0, y=0):
    car_mask = pygame.mask.from_surface(self.image)
    offset = (int(self.x - x), int(self.y-y))
    p = mask.overlap(car_mask, offset)
    return p

  def reset(self):
    self.x, self.y = self.start_pos
    self.angle = 0
    self.velocity = 0

# another Car class - BR, Day 3
class PlayerCar(Car):
  IMAGE = car_image
  start_pos = (180, 200)

  def reduce_speed(self):
      self.velocity = max(self.velocity - self.acceleration / 2, 0)
      self.move()

  def bouncing(self): #for when there is a collision -BR, Day 4
    self.velocity = -self.velocity
    self.move()

#class for computer car movement - BR, Day 5
class ComputerCar(Car):
  IMAGE = computer_car_image
  start_pos = (150, 200)

  def __init__(self, max_velocity, rotation_velocity, path=[]):
        super().__init__(max_velocity, rotation_velocity)
        self.path = path
        self.current = 0
        self.velocity = max_velocity
        self.inital_vel = max_velocity

  def draw_points(self, win):
    for point in self.path:
      pygame.draw.circle(win, (255, 0, 0), point, 5)

  def draw(self, win):
    super().draw(win)
    # self.draw_points(win)

  def calculate_angle(self):
      xpoint, ypoint = self.path[self.current]
      xdiff = xpoint - self.x
      ydiff = ypoint - self.y

      if ydiff == 0:
          radian_angle = math.pi / 2
      else:
          radian_angle = math.atan(xdiff / ydiff)

      if ypoint > self.y:
          radian_angle += math.pi

      angle_diff = self.angle - math.degrees(radian_angle)
      if angle_diff >= 180:
          angle_diff -= 360

      if angle_diff > 0:
          self.angle -= min(self.rotation_velocity, abs(angle_diff))
      else:
          self.angle += min(self.rotation_velocity, abs(angle_diff))

  def update_path_point(self):
      point = self.path[self.current]
      rect = pygame.Rect(self.x, self.y, self.image.get_width(), self.image.get_height())
      if rect.collidepoint(*point):
          self.current += 1

  def move(self):
      if self.current >= len(self.path):
          return

      self.calculate_angle()
      self.update_path_point()
      super().move()

  def levelup(self, level):
        self.reset()
        self.velocity = self.max_velocity + (level - 1) * 0.2
        self.current = 0

  def resetend(self):
    self.reset()
    self.current = 0
    self.velocity = self.inital_vel

def big_center_text(screen, font, text):
  render = font.render(text, 1, red)
  screen.blit(render, (WIDTH/2 - render.get_width()/2, HEIGHT/2 - render.get_height()/2))

# Day 7 - Text rendering for Start and End screens - BR
def big_high_text(screen, font, text):
  render = font.render(text, 1, white)
  screen.blit(render, (275, 100))

# drawing all nessasary images - BR, Day 3
# adding text for level and time info
def draw(screen, images, player_car, computer_car, gamecontrol):
    for image, position in images:
        screen.blit(image, position)

    level_text = font1.render("Level {}".format(gamecontrol.level), 1, white)
    screen.blit(level_text, (10, HEIGHT - level_text.get_height() - 70))

    time_text = font1.render("Time: {}s".format(gamecontrol.level_time()), 1, white)
    screen.blit(time_text, (10, HEIGHT - time_text.get_height() - 30))

    player_car.draw(screen)
    computer_car.draw(screen)
    pygame.display.update()

# movement code moved out of game loop into a function - BR, Day 4
def movement(player_car):
  pressed = pygame.key.get_pressed()
  moved = False

  # car movement with WAD keys so that player can control it - BR, Day 3
  if pressed[pygame.K_a]:
    game_car.rotate(left=True)
  if pressed[pygame.K_d]:
    game_car.rotate(right=True)
  if pressed[pygame.K_w]:
    moved = True
    game_car.move_forward()
  if pressed[pygame.K_s]:
    moved = True
    game_car.move_backward()
    
  if not moved:
    game_car.reduce_speed()

loss = False

def handle_collision(player_car, computer_car, gamecontrol):
  # collision check code - BR, Day 4
  # moved out of game loop into a function - BR, Day 5
  # added finish line collision for computer car - BR, Day 5
  # collision code idea source: http://renesd.blogspot.com/2017/03/pixel-perfect-collision-detection-in.html
  # informative video about pygame mask: https://www.youtube.com/watch?v=Dspz3kaTKUg
  
  if game_car.collision(track_mask) != None:
    player_car.reset()

  # Code for if the computer makes it to the finish before the player - BR, Overtime
  computer_finish = computer_car.collision(finish_mask, *finish_pos)
  if computer_finish != None:
    loss = True
    while loss:
      
      # end screen code by AP, Day 6
      screen.fill(black) 

      # stores the (x,y) coordinates into the variable as a tuple 
      mouse = pygame.mouse.get_pos() 

      # if mouse is hovered on a button it changes to lighter shade 
      if WIDTH/2 <= mouse[0] <= WIDTH/2+140 and HEIGHT/2 <= mouse[1] <= HEIGHT/2+40: 
        pygame.draw.rect(screen,color_light,[WIDTH/2,HEIGHT/2,140,40])      
      else: 
        pygame.draw.rect(screen,color_dark,[WIDTH/2,HEIGHT/2,140,40]) 

      if WIDTH/2-200 <= mouse[0] <= WIDTH/2-60 and HEIGHT/2 <= mouse[1] <= HEIGHT/2+40: 
        pygame.draw.rect(screen,color_light,[WIDTH/4,HEIGHT/2,140,40])       
      else:
        pygame.draw.rect(screen,color_dark,[WIDTH/4,HEIGHT/2,140,40]) 
      
      screen.blit(textquit , (WIDTH/2+50,HEIGHT/2)) 
      screen.blit(textretry , (WIDTH/2-140,HEIGHT/2))
      screen.blit(textlose , (WIDTH/2-70,HEIGHT/4))

      pygame.display.update()

      for ev in pygame.event.get(): 
        if ev.type == pygame.QUIT: 
          return False
                  
        #checks if a mouse is clicked 
        if ev.type == pygame.MOUSEBUTTONDOWN:       
        #if the mouse is clicked on the button the game is terminated 
          if WIDTH/2 <= mouse[0] <= WIDTH/2+140 and HEIGHT/2 <= mouse[1] <= HEIGHT/2+40: 
            return False
          
          elif WIDTH/2-200 <= mouse[0] <= WIDTH/2-60 and HEIGHT/2 <= mouse[1] <= HEIGHT/2+40: 
            gamecontrol.reset()
            player_car.reset()
            computer_car.resetend()
            loss = False

    pygame.display.update()

  finish_collision = game_car.collision(finish_mask, *finish_pos)
  if finish_collision != None:
    if finish_collision[1] == 0:
      game_car.bouncing()
      big_center_text(screen, font1, "Don't try to cheat!")
      pygame.display.update()
      pygame.time.wait(3000)
    else:
      gamecontrol.levelup()
      player_car.reset()
      computer_car.levelup(gamecontrol.level)

# setup needed for main game loop - BR, Day 3
# added trackborder+finish line
origin = (0, 0)
running = True
clock = pygame.time.Clock()
images = [(background, origin), (track, origin),(finish, finish_pos), (track_border, origin)]
game_car = PlayerCar(4, 4)
computer_car = ComputerCar(2, 4, path)
game_info = GameControl()

# start screen implementation - code by XZ, implmentation by BR
startscreen = True # for startscreen
startquit = False
startbackground = pygame.image.load("startbackground.jpg")
start1=pygame.image.load("Start.png").convert_alpha()
start2=pygame.transform.scale(start1, (150, 80))
quit1=pygame.image.load("Quit.png").convert_alpha()
quit2=pygame.transform.scale(quit1, (150,80))
#Create Button Instances - XZ
start_button = Button(210,300, start2)
quit_button = Button(450,300, quit2)

# rules screen implementation - BR
rulescreen = False 
rulesbackground= pygame.image.load("How_to_play_CarGame.png")
start_button2 = Button(325,650,start2)

# end screen implementation - BR (code by AP)
textquit = smallfont.render('Quit' , True , white) 
textretry = smallfont.render('Retry' , True , white)
textlose = smallfont.render('You Lost!' , True , white)

# credit screen implementation - BR, Overtime (code by AH)
credits = pygame.image.load('Credits_CarGame.png')

# main game loop started - BR, Day 3
while running:
  clock.tick(FPS)

  #bring in start screen - code by XZ
  # implemented into main loop - BR, Day 6
  while startscreen:
    screen.blit(startbackground, [0, 0])
    start_button.draw()
    quit_button.draw()
    big_high_text(screen, font1, "Racer Wreck!")

    for e in pygame.event.get():

      p=pygame.mouse.get_pos()
      if e.type == pygame.MOUSEBUTTONDOWN: 
        if e.button == 1: 
          if start_button.rect.collidepoint(p):
            startscreen = False
            rulescreen = True
            continue
          
          elif quit_button.rect.collidepoint(p):
            startscreen = False
            startquit = True
            break
  
    pygame.display.update()

  # implementing the quite button on the start screen - BR, Day 6
  if startquit:
    running = False
    break
  
  # rulescreen implementation - BR, Day 7
  while rulescreen:
    screen.fill(black)
    screen.blit(rulesbackground, [0, 0])
    start_button2.draw()

    if start_button2.pressed():
      rulescreen = False
      continue
    
    pygame.display.update()

  # game starting necessities - BR, Overtime 
  screen.fill(black) #clear the screen of previous start screen
  draw(screen, images, game_car, computer_car, game_info)
  while not game_info.start:
    big_center_text(screen, font1, "Press any key to start level {}!".format(game_info.level))
    pygame.display.update()
    #in case they want to quit the pygame window now
    for event in pygame.event.get():
      if event.type == pygame.QUIT:
        running = False
        break

      if event.type == pygame.KEYDOWN:
        game_info.level_start()

  movement(game_car)
  computer_car.move()

  handle_collision(game_car, computer_car, game_info)
  pygame.display.update()

  if handle_collision(game_car, computer_car, game_info) == False:
    running = False
    break

  # code to close cleanly if player quits the window - BR, Day 3
  for event in pygame.event.get():
      if event.type == pygame.QUIT:
          running = False
          break

  win = False

  # implemented game win code - BR, Overtime (credits screen made by AH)
  if game_info.game_end():
    win = True
    while win:
      screen.blit(credits,(0,0))

      # stores the (x,y) coordinates into the variable as a tuple 
      mouse = pygame.mouse.get_pos() 
      for event in pygame.event.get():
          if event.type == pygame.QUIT: 
              win = False
              running = False
              break
                
          #checks if a mouse is clicked 
          if event.type == pygame.MOUSEBUTTONDOWN:  
              #if the mouse is clicked on the button the game is terminated 
              if WIDTH/2 <= mouse[0] <= WIDTH/2+140 and HEIGHT/2+200 <= mouse[1] <= HEIGHT/2+240: 
                win = False
                running = False
                break 

              elif WIDTH/2-200 <= mouse[0] <= WIDTH/2-60 and HEIGHT/2 +200 <= mouse[1] <= HEIGHT/2+240:
                game_info.reset()
                game_car.reset()
                computer_car.resetend()
                win = False
        
      # if mouse is hovered on a button it changes to lighter shade 
      if WIDTH/2 <= mouse[0] <= WIDTH/2+140 and HEIGHT/2+200 <= mouse[1] <= HEIGHT/2+240: 
          pygame.draw.rect(screen,color_light,[WIDTH/2,HEIGHT/2+200,140,40]) 
            
      else: 
          pygame.draw.rect(screen,color_dark,[WIDTH/2,HEIGHT/2+200,140,40]) 
      if WIDTH/2-200 <= mouse[0] <= WIDTH/2-60 and HEIGHT/2 +200 <= mouse[1] <= HEIGHT/2+240: 
          pygame.draw.rect(screen,color_light,[WIDTH/4,HEIGHT/2+200,140,40]) 
            
      else: 
          pygame.draw.rect(screen,color_dark,[WIDTH/4,HEIGHT/2+200,140,40]) 
        
      # superimposing the text onto our screen 
      screen.blit(textquit, (WIDTH/2+50,HEIGHT/2+200)) 
      screen.blit(textretry, (WIDTH/2-150,HEIGHT/2+200))
        
      # updates the frames of the game in loop
      pygame.display.update() 
      
  # in case anything was missed
  pygame.display.update()

pygame.quit()