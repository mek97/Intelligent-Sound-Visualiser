import struct
import wave
import pygame
import time,random
import numpy as np
from math import pi


CONST_W = int(1280)
CONST_H = int(720)
FPS = int(25)


BLACK = (0,  0,  0)
WHITE = (255, 255, 255)
GOLD = (255,215,0)
RED =   (232, 62,  62)
ORANGE = (237 , 140, 37)
ORANGE1 = (240,240,240)
GREEN =   (152, 224, 89)
BLUE = (91 , 192, 229)




def fft_from_wav(fname,CHANNELS,SAMPLE_SIZE,RATE,nFFT):

  MAX_y = 2.0 ** (SAMPLE_SIZE * 8 - 1)
  wf = wave.open(fname+'.wav', 'rb')
  assert wf.getnchannels() == CHANNELS
  assert wf.getsampwidth() == SAMPLE_SIZE
  assert wf.getframerate() == RATE

  frames = wf.getnframes()

  FREQ_LIST = []
  for i in range(0,int((frames/RATE)*FPS) ):
    N = (int((i + 1) * RATE / FPS) - wf.tell()) / nFFT
    if not N:
      return
    N = N * nFFT
    data = wf.readframes(N)

    y = np.array(struct.unpack("%dh" % (len(data) / SAMPLE_SIZE), data)) / MAX_y
    y_L = y[::2]
    y_R = y[1::2]

    Y_L = np.fft.fft(y_L, nFFT)
    Y_R = np.fft.fft(y_R, nFFT)


    Y = abs(np.hstack((Y_L[int(-nFFT / 2):-1], Y_R[:int(nFFT / 2)])))
    
    FREQ_LIST.append(Y)

  wf.close()

  avgfreq = []

  for i in range(0,-1+len(FREQ_LIST)):
    x = []
    for j in range(0,-1+len(FREQ_LIST[i])):
      x.append((FREQ_LIST[i][j]-FREQ_LIST[i][j+1])**2)
    avgfreq.append(np.sum(x)/len(x))

  return avgfreq


def pol2cart(x,y,rho, phi):
  phi = (pi*phi/180)
  x1 = x + rho * np.cos(phi)
  y1 = y + rho * np.sin(phi)
  return(int(x1), int(y1))    

def r_2(n1,angle1):
  return pi*(angle1%(360/n1) - (360/(2*n1)))/180

def visual(t,angle,angle_e,num_dot,dest,val,clock,screen):
  t = t - 90
  tick = FPS
  st = []
  done = False
  while not done:

    if angle>=angle_e:
      done = True

    for event in pygame.event.get():
      if event.type == pygame.QUIT:
        done=True

    clock.tick(tick)

    x = random.randrange(1,100)/100

    if(0<x<0.14):
      C1 = WHITE
      C2 = BLACK
    elif (0.14<=x<=0.28):
      C1 = RED
      C2 = WHITE
    elif (0.28<x<=0.42):
      C1 = ORANGE
      C2 = BLACK
    elif (0.42<x<=0.56):
      C1 = BLACK
      C2 = GOLD
    elif (0.56<x<=0.70):
      C1 = GREEN
      C2 = BLUE
    elif (0.70<x<=0.84):
      C1 = BLUE
      C2 = WHITE
    else:
      C1 = ORANGE1
      C2 = BLUE


    screen.fill(C1)

    angle += val
    
    for i in range(3,num_dot+1):    
      st.append(pol2cart(CONST_W/2,CONST_H/2,dest/(np.cos(r_2(i,angle*(num_dot+1-i)-180/i))*np.tan(pi/i)),angle*(num_dot+1-i)+t))
    
    st.append((CONST_W/2,CONST_H/2))
    pygame.draw.polygon(screen,C2,st,2)
    pygame.display.flip()
    st.clear()


def main():

  fname = "IM"

  nFFT = 512
  SAMPLE_SIZE = 2
  CHANNELS = 2
  RATE = 44100

  avgfreq = fft_from_wav(fname,CHANNELS,SAMPLE_SIZE,RATE,nFFT)
  # fh = open("hello.txt","w")
  # fh.write(avgfreq)
  # fh.close()
  print(avgfreq)
  pygame.init()
  size = [CONST_W, CONST_H]
  screen = pygame.display.set_mode(size) 
  pygame.display.set_caption(fname)
  clock = pygame.time.Clock()

  pygame.mixer.init()
  pygame.mixer.music.load(fname+'.wav')
  pygame.mixer.music.play()

  time.sleep(5)
  start_time = time.time()

  j=0
  i=0
  st_angle = 0
  while i < len(avgfreq):

    k = 1+avgfreq[i]
    s = 10
    st_disp = 0
    angle_change = k/100
    st_stop = st_angle+s*angle_change
    num_dot = 100+int(k*50)
    #num_dot = 80+int(random.randrange(2,70))
    dist = 100
    
    visual(st_disp,st_angle,st_stop,num_dot,dist,angle_change,clock,screen)

    st_angle = st_stop
    i = i + s


  print("--- %s seconds ---" % (time.time() - start_time))
  pygame.quit()


if __name__ == '__main__':
  main()
