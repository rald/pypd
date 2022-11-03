import pygame
from PIL import Image,ImageDraw 


from pygame.locals import (
    K_UP,
    K_DOWN,
    K_LEFT,
    K_RIGHT,
    K_ESCAPE,
    KEYDOWN,
    QUIT,
)



GAME_TITLE = "Pixel Dancer"
SCREEN_WIDTH = 640
SCREEN_HEIGHT = 480



palette = {
  "c":0,
  "p":[
    (26, 28, 44), 
    (93, 39, 93),   
    (177, 62, 83), 
    (239, 125, 87), 
    (255, 205, 117), 
    (167, 240, 112), 
    (56, 183, 100), 
    (37, 113, 121), 
    (41, 54, 111), 
    (59, 93, 201), 
    (65, 166, 246), 
    (115, 239, 247), 
    (244, 244, 244), 
    (148, 176, 194), 
    (86, 108, 134), 
    (51, 60, 87),
    (255, 255, 255)
  ]
}



canvas={
  "w":32,"h":32,"z":12,
  "t":len(palette["p"])-1
}



draw=False
prev_x=0
prev_y=0



def canvas_draw(cvs,x,y,z,pal):
  for j in range(cvs["w"]):
    for i in range(cvs["h"]):
      k=cvs["p"][j][i]
      pygame.draw.rect(screen,pal["p"][k],pygame.Rect(i*z+x,j*z+y,z,z))      



def canvas_draw_point(cvs,x,y,c):
  if x>=0 and x<cvs["w"] and y>=0 and y<cvs["h"]:
    cvs["p"][y][x]=c



def canvas_draw_line(cvs,x0,y0,x1,y1,c):
  dx = abs(x1 - x0)
  dy = abs(y1 - y0)
  x, y = x0, y0
  sx = -1 if x0 > x1 else 1
  sy = -1 if y0 > y1 else 1
  if dx > dy:
    err = dx / 2.0
    while x != x1:
      canvas_draw_point(cvs,x,y,c)
      err -= dy
      if err < 0:
        y += sy
        err += dx
      x += sx
  else:
    err = dy / 2.0
    while y != y1:
      canvas_draw_point(cvs,x,y,c)
      err -= dx
      if err < 0:
        x += sx
        err += dy
      y += sy        
  canvas_draw_point(cvs,x,y,c)



def canvas_save(name,cvs,pal):
  image = Image.new("RGB",(cvs["w"]*cvs["z"],cvs["h"]*cvs["z"]),"white")
  draw = ImageDraw.Draw(image)
  for j in range(cvs["h"]):
    for i in range(cvs["w"]):
      k=cvs["p"][j][i]
      if k!=len(pal["p"])-1:
        draw.rectangle(
          [
            i*cvs["z"],j*cvs["z"],
            i*cvs["z"]+cvs["z"],
            j*cvs["z"]+cvs["z"]
          ],
          fill=pal["p"][k])
  image.save(name,format="GIF")



def grid_draw(x,y,w,h,z,c):
  global screen
  for i in range(w+1):
    pygame.draw.line(screen,c,(i*z,y),(i*z,y+h*z))
  for j in range(h+1):
    pygame.draw.line(screen,c,(x,j*z),(x+w*z,j*z))



def palette_draw(pal,x,y,z):

  global screen
  global mouse_x, mouse_y
  global mouse_button1, mouse_button2, mouse_button3

  if mouse_button1:
    rect=pygame.Rect(x,y,len(pal["p"])*z,z)
    if rect.collidepoint(mouse_x,mouse_y):
      pal["c"]=int((mouse_x-x)/z)
      
  for i in range(len(pal["p"])):
    pygame.draw.rect(screen,pal["p"][i],pygame.Rect(i*z+x,y,z,z))

    if i==len(pal["p"])-1:
      pygame.draw.line(screen,(0,0,0),(i*z+z+x,y),(i*z+x,y+z),2)      

    if i==pal["c"]:
      pygame.draw.rect(screen,pal["p"][12],pygame.Rect(i*z+x,y,z,z),2)
      pygame.draw.rect(screen,pal["p"][0],pygame.Rect(i*z+x+2,y+2,z-4,z-4),2)      



def main():

  global screen
  global canvas
  global mouse_x, mouse_y
  global mouse_button1, mouse_button2, mouse_button3
  global draw
  global prev_x,prev_y

  canvas["p"] = [[len(palette["p"])-1 for col in range(canvas["w"])] for row in range(canvas["h"])]

  pygame.init()

  pygame.display.set_caption(GAME_TITLE)

  screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))

  running = True
  while running:
    for event in pygame.event.get():
      if event.type == pygame.QUIT:
        running = False
      elif event.type == KEYDOWN:
        if event.key == K_ESCAPE:
          running = False

    mouse_x, mouse_y = pygame.mouse.get_pos()

    mouse_button1, mouse_button2, mouse_button3 = pygame.mouse.get_pressed(3)

    screen.fill((0,0,0))

    canvas_draw(canvas,0,0,canvas["z"],palette)

    canvas_draw(canvas,SCREEN_WIDTH-canvas["w"]*2,0,2,palette)

    grid_draw(0,0,canvas["w"],canvas["h"],canvas["z"],palette["p"][15])

    palette_draw(palette,0,SCREEN_HEIGHT-32,32)

    if not draw:
      if mouse_button1:
        rect=pygame.Rect(0,0,canvas["w"]*canvas["z"],canvas["h"]*canvas["z"])
        if rect.collidepoint(mouse_x,mouse_y):
          prev_x=int(mouse_x/canvas["z"])
          prev_y=int(mouse_y/canvas["z"])
          draw=True
    else:
      if mouse_button1:
        rect=pygame.Rect(0,0,canvas["w"]*canvas["z"],canvas["h"]*canvas["z"])
        if rect.collidepoint(mouse_x,mouse_y):
          x=int(mouse_x/canvas["z"])
          y=int(mouse_y/canvas["z"])
          canvas_draw_line(canvas,prev_x,prev_y,x,y,palette["c"])  
          prev_x=x
          prev_y=y
      else:
        draw=False
          
    pygame.display.flip()

  canvas_save("output.gif",canvas,palette)

  pygame.quit()



if __name__ == "__main__":
  main()


