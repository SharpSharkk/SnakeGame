import pygame
import sys
import random

# Initialize Pygame
pygame.init()

# Set up display
width,height=800,600
window=pygame.display.set_mode((width,height))
pygame.display.set_caption("Snake Game")
start=True

# Drawing Text
def drawer(text,font,col,x,y):
  img=font.render(text,True,col)
  window.blit(img,(x,y))

# Fonts
menuf=pygame.font.SysFont("comicsans",30)
scoref=pygame.font.SysFont("comicsans",20)
endscreen=pygame.font.SysFont("comicsans",50)

# Colors
black=(0,0,0)
white=(255,255,255)
red=(255,0,0)
gray=(104,104,104)
dark_gray=(15,15,15)

# Snake
snake_size=20
snake_speed=15
snake=[(width//2,height//2)]
snake_direction=(0,0)
snake_head = pygame.image.load('snakehead.png')
head = snake_head
switch=0

#Score Tracker
count=0
countmax=0

#Head Rotator
def headrot(img,angle):
  return pygame.transform.rotate(img,angle)

# Food
def foodmaker():
  return (random.randrange(1,(width//food_size)-1)*food_size,
          random.randrange(1,(height//food_size)-1)*food_size)

food_size=20
food_position=foodmaker()

# Clock to control the speed of the game
clock=pygame.time.Clock()

# Game loop
while True:
  for event in pygame.event.get():
    if event.type==pygame.QUIT:
      pygame.quit()
      sys.exit()
    
    elif event.type==pygame.KEYDOWN:
      if event.key==pygame.K_r and not start:
        snake=[(width//2,height//2)]
        start=True
        countmax=max(count,countmax)
        count=0
      
      if (event.key==pygame.K_UP or event.key==pygame.K_w) and snake_direction!=(0,1) and start:
        snake_direction=(0,-1)
        head = headrot(snake_head,270)
      elif (event.key==pygame.K_DOWN or event.key==pygame.K_s) and snake_direction!=(0,-1) and start:
        snake_direction=(0,1)
        head = headrot(snake_head,90)
      elif (event.key==pygame.K_LEFT or event.key==pygame.K_a) and snake_direction!=(1,0) and start:
        snake_direction=(-1,0)
        head = headrot(snake_head,180)
      elif (event.key==pygame.K_RIGHT or event.key==pygame.K_d) and snake_direction!=(-1,0) and start:
        snake_direction=(1,0)
        head = headrot(snake_head,0)
  
  # Move the snake
  x,y=snake[0]
  x+=snake_direction[0]*snake_size
  y+=snake_direction[1]*snake_size
  snake.insert(0,(x,y))
  
  # Check for collisions with the food
  if x==food_position[0] and y==food_position[1]:
    count+=1
    food_position=foodmaker()
  else:
    snake.pop()
  
  # Check for collisions with the walls
  if x<1 or x>=width-snake_size or y<1 or y>=height-snake_size:
    snake_direction=(0,0)
    start=False
  
  # Check for collisions with itself
  if len(snake)>1 and (x,y) in snake[1:]:
    snake_direction=(0,0)
    start=False
  
  # Draw everything
  window.fill(black)
  
  for ycoord in range(snake_size,height-snake_size,2*snake_size):
    for xcoord in range(snake_size,width-snake_size,2*snake_size):
      pygame.draw.rect(window,dark_gray,(xcoord,ycoord,snake_size,snake_size))
  
  for ycoord in range(snake_size*2,height-snake_size,2*snake_size):
    for xcoord in range(snake_size*2,width-snake_size,2*snake_size):
      pygame.draw.rect(window,dark_gray,(xcoord,ycoord,snake_size,snake_size))
  
  pygame.draw.rect(window,gray,(0,0,snake_size,height))
  pygame.draw.rect(window,gray,(0,0,width,snake_size))
  pygame.draw.rect(window,gray,(width-snake_size,0,snake_size,height))
  pygame.draw.rect(window,gray,(0,height-snake_size,width,snake_size))
  
  if start:
    window.blit(head,snake[0])
    for segment in range(1, len(snake)):
      pygame.draw.rect(window,white,(snake[segment][0],snake[segment][1],snake_size,snake_size))
    pygame.draw.rect(window,red,(food_position[0],food_position[1],food_size,food_size))
  
  drawer(f"Score: {count}",scoref,white,width-(8*snake_size),2*snake_size)
  drawer(f"Highscore: {countmax}",scoref,white,width-(9*snake_size),3*snake_size)
  
  if snake_direction==(0,0):
    if start:
      pygame.draw.rect(window,gray,(width//6,height//4,width//1.5,height//2))
      drawer("Welcome!",menuf,white,width//2-(3.5*snake_size),height//2-(5*snake_size))
      drawer("Press an arrow key to begin.",menuf,white,width//2-(9*snake_size),height//2-(2*snake_size))
      drawer("Made by: Shahzaib S.",menuf,white,width//2-(7.5*snake_size),height//1.75)
    else:
      pygame.draw.rect(window,gray,(width//6,height//4,width//1.5,height//2))
      drawer("You Lost...",endscreen,white,width//2-(5*snake_size),height//2-(3*snake_size))
      drawer("Press R to Restart",menuf,white,width//2-(6*snake_size),height//2+(2*snake_size))
      drawer("Press R to Restart",menuf,white,width//2-(6*snake_size),height//2+(2*snake_size))
  
  # Update the display
  pygame.display.flip()
  
  # Cap the frame rate
  clock.tick(snake_speed)