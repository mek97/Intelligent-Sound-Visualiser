from intelligent_visualiser.core.video_profile.base_animator import BaseAnimator
from matplotlib import animation
from matplotlib import pyplot as plt


class BasePolarAnimator(BaseAnimator):

    def __init__(self, duration, fps):
        super().__init__(duration, fps)
        self.face_colour = 'black'
        self.background_colour = 'dark_background'
        self.pen_colour = 'gold'
        self.width = 20
        self.height = 20

    def animate(self, **kwargs):
        return NotImplementedError

    def generate(self, animate_arg, save=False, output_path=None):

        fig = plt.figure()
        plt.style.use(self.background_colour)
        fig.set_size_inches(self.width, self.height, True)

        ax = plt.subplot(111, projection='polar')
        line, = ax.plot([], [], lw=2, color=self.pen_colour)
        ax.set_rmax(200)
        ax.set_yticklabels([])
        ax.set_xticklabels([])
        ax.set_theta_zero_location('N')
        ax.get_xaxis().set_visible(False)
        ax.get_yaxis().set_visible(False)

        ax.set_facecolor(self.face_colour)

        def init():
            line.set_data([], [])
            return line,

        anim = animation.FuncAnimation(fig, self.animate, fargs=(line, animate_arg), init_func=init,
                                       frames=self.frames, interval=self.interval, blit=True)

        if save:
            anim.save(output_path, fps=self.fps, extra_args=['-vcodec', 'libx264'])
        else:
            plt.show()
