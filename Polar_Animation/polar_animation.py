from math import pi
import numpy as np
from matplotlib import pyplot as plt
from matplotlib import animation
import wave
import struct
import pygame

class anisimu:

	def __init__(self, duration, FPS, speed):
		self.duration = duration
		self.FPS = FPS
		self.speed = speed
		self.inter = 1000/ self.FPS
		self.fr = self.duration * self.FPS
		self.num_dot = 200;
		self.dest = 10
	

	def return_r(self,time,i,r):
		return i+np.sin(i*time/10)



	def return_c(self,time,i,angle):
		return time*np.sin(i*time/100)+np.pi*np.sin(i*time/100)

	def visual(self,i1,time):


		angle = i1 * self.speed

		theta = []
		r = []
		theta.append(0)
		r.append(0)

		for i in range(3,self.num_dot):
			r.append(self.return_r(time,i,1))
			theta.append(self.return_c(time,i,angle))
		return (theta,r)

	


def fft_from_wav(fname,CHANNELS,SAMPLE_SIZE,RATE,nFFT,FPS):

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

BLACK = (0,  0,  0)
WHITE = (255, 255, 255)
GOLD = (255,215,0)
RED =   (232, 62,  62)
ORANGE = (237 , 140, 37)
ORANGE1 = (240,240,240)
GREEN =   (152, 224, 89)
BLUE = (91 , 192, 229)

def run(AS):

	fig = plt.figure()
	plt.style.use('dark_background')
	fig.set_size_inches(10, 10, True)

	ax = plt.subplot(111, projection='polar')
	line, = ax.plot([], [], lw=2, color= "gold")
	ax.set_rmax(200)
	ax.set_yticklabels([])
	ax.set_xticklabels([])
	ax.set_theta_zero_location('N')
	ax.get_xaxis().set_visible(False)
	ax.get_yaxis().set_visible(False)


	ax.set_facecolor("black")


	def init():
		line.set_data([], [])
		return line,

	def animate(i):
		time = i/AS.FPS

		st = AS.visual(i,time)

		line.set_data(st)
		return line,

	anim = animation.FuncAnimation(fig, animate, init_func = init,
			frames = AS.fr, interval = AS.inter, blit = True)

	#anim.save('basic_animation.mp4', fps=AS.FPS, extra_args=['-vcodec', 'libx264'])

	plt.show()

def main():

	fname = "IM"

	# pygame.init()
	# pygame.mixer.init()
	# pygame.mixer.music.load(fname+'.wav')
	# pygame.mixer.music.play()

	nFFT = 512
	SAMPLE_SIZE = 2
	CHANNELS = 2
	RATE = 44100

	S = anisimu(120,40,0.005)
	run(S)

	avgfreq = fft_from_wav(fname,CHANNELS,SAMPLE_SIZE,RATE,nFFT,S.FPS)
	# pygame.quit()


if __name__== "__main__":
	main()















