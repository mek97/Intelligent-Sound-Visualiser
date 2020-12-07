#Python Visualizer
# Authors -- Keerthana S, Mehul Kumar

import struct
import wave

import matplotlib.animation as animation
import matplotlib.pyplot as plt
import numpy as np
import pygame,time
from math import pi
import numpy as np

import csv
import json
import requests
import random

# Insert API Key here (within quotes, like a string)

apiKey = ''

# Insert lrc file name here 

lrcname = ''

# Insert wav file name here 

wavname = 'TY'

CONST_W = int(1280)
CONST_H = int(720)

BLACK = (0,  0,  0)
WHITE = (255, 255, 255)
GOLD = (255,215,0)
RED =   (232, 62,  62)
ORANGE = (237 , 140, 37)
ORANGE1 = (240,240,240)
GREEN =   (152, 224, 89)
BLUE = (91 , 192, 229)

TITLE = ''
WIDTH = 1280
HEIGHT = 720
FPS = int(21)

FREQ_LIST = []

def pol2cart(x,y,rho, phi):
  phi = (pi*phi/180)
  x1 = x + rho * np.cos(phi)
  y1 = y + rho * np.sin(phi)
  return(int(x1), int(y1))

def r_2(n1,angle1):
  return pi*(angle1%(360/n1) - (360/(2*n1)))/180

def init(line):

  # This data is a clear frame for animation
  line.set_ydata(np.zeros(nFFT - 1))
  return line,

nFFT = 512
BUF_SIZE = 4 * nFFT
SAMPLE_SIZE = 2
CHANNELS = 2
RATE = 44100

# parses the song time from a line of the lyrics file
def gettime(line):
  return int(line[1:3])*60 + float(line[4:6])

def main():

  # Frequency range
  MAX_y = 2.0 ** (SAMPLE_SIZE * 8 - 1)
  wf = wave.open(wavname+'.wav', 'rb')
  assert wf.getnchannels() == CHANNELS
  assert wf.getsampwidth() == SAMPLE_SIZE
  assert wf.getframerate() == RATE

  frames = wf.getnframes()
  print(frames)

  for i in range(0,int((frames/RATE)*FPS) ):
    N = (int((i + 1) * RATE / FPS) - wf.tell()) / nFFT
    if not N:
      return
    N = N * nFFT
    data = wf.readframes(int(N))

    y = np.array(struct.unpack("%dh" % (len(data) / SAMPLE_SIZE), data)) / MAX_y
    y_L = y[::2]
    y_R = y[1::2]

    Y_L = np.fft.fft(y_L, nFFT)
    Y_R = np.fft.fft(y_R, nFFT)


    Y = abs(np.hstack((Y_L[int(-nFFT / 2):-1], Y_R[:int(nFFT / 2)])))

    FREQ_LIST.append(Y)

  wf.close()

  avgfreq = []

  # FREQ_LIST[i][j] i is the n th frame and j is a particular frequency

  # Should capture the rate at which song vibrates or differs from the previous frame
  for i in range(0,-1+len(FREQ_LIST)):
    x = []
    for j in range(0,-1+len(FREQ_LIST[i])):

      #x.append((FREQ_LIST[i][j]-FREQ_LIST[i][j+1])**2)
      x.append((FREQ_LIST[i+1][j]-FREQ_LIST[i][j])**2)
    avgfreq.append(np.sum(x)/len(x))


  pygame.init()
  size = [CONST_W, CONST_H]
  screen = pygame.display.set_mode(size)
  pygame.display.set_caption(wavname)
  clock = pygame.time.Clock()

  def visual(t,angle,angle_e,num_dot,dest,val, flicker):
    fr = 0.0
    fre = 0
    cc = 0
    t = t - 90
    tick = 60
    st = []
    done = False
    start_time = time.time()
    C1 = WHITE
    C2 = BLACK
    while not done:
      if angle>=angle_e:
        done = False

      for event in pygame.event.get():
        if event.type == pygame.QUIT:
          done=True

      clock.tick(tick)

      x = random.randrange(1,100)/100

      if(flicker and cc >= 35/(avgfreq[fre]+1)):
        cc = 0
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
      fr += 1.0
      cc += 1
      if(fr == 3): # Set to FPS
        fre += 1
        cc = 0
        val = (avgfreq[fre] + 1)/50
        print('Duration ' + str(fre) + '--' + str(time.time() - start_time));
        fr = 0
        start_time = time.time()

      for i in range(3,num_dot+1):
        st.append(pol2cart(CONST_W/2,CONST_H/2,dest/(np.cos(r_2(i,angle*(num_dot+1-i)-180/i))*np.tan(pi/i)),angle*(num_dot+1-i)+t))

      st.append((CONST_W/2,CONST_H/2))
      pygame.draw.polygon(screen,C2,st,2)
      pygame.display.flip()
      st.clear()


url = 'https://southeastasia.api.cognitive.microsoft.com/text/analytics/v2.0/sentiment'

lyrics = []
with open('lyrics.lrc', newline='\n') as inputfile:
  for row in csv.reader(inputfile):
    lyrics.append(row)
lyrics = lyrics[4:]

documents = []
for i in range(len(lyrics)):
  d = {}
  d['language'] = 'en'
  d['id'] = i+1
  d['text'] = lyrics[i][0][7:]
  documents.append(d)

j = {}
j['documents'] = documents
data = json.dumps(j)

print(len(lyrics))

headers = {'Content-Type' : 'application/json', 'Ocp-Apim-Subscription-Key' : '22835c7c256b423580c564f2524e4910', 'Accept' : 'application/json'}

response = requests.post(url, headers=headers, data=data)
results = response.json()['documents']

print(len(results))

sentiments = []
cur = 0.5
time = 0
for i in range(len(lyrics)):
  now = gettime(lyrics[i][0])
  while(time < now):
    sentiments.append(cur)
    time += 0.04
  # Update cur
    cur = results[i]['score']

print(time)
print(now)
print(sentiments)

  pygame.mixer.init()
  pygame.mixer.music.load(wavname+'.wav')
  pygame.mixer.music.play()


  start_time = time.time()
  j=0

  print(len(avgfreq))
  for i in range(0,(len(FREQ_LIST)-1),25):



    # C1 = BLACK
    # C2 = GOLD

    k = 1+avgfreq[i]
    # time to run 1 visual should be the frame length
    st_disp = 0
    st_angle = j
    st_stop = j+k*k
    num_dot = 100+int(k*100)
    #num_dot = 80+int(random.randrange(2,70))
    dist = 20 + k*25
    angle_change = k/30
    visual(st_disp,st_angle,st_stop,num_dot,dist,angle_change, True)
    j+=k*k

  # print("--- %s seconds ---" % (time.time() - start_time))


  # visual(180,0,40,500,10,0.05)
  # visual(180,40,60,2000,20,0.05)
  # visual(180,60,110,500,10,0.1)
  # visual(180,110,130,500,20,0.025)
  # visual(180,130,180,500,20,0.1)

  time.sleep(7)
  pygame.quit()


main()