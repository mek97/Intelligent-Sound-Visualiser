import queue

import numpy as np
from intelligent_visualiser.core.video.base_polar_animator import BasePolarAnimator
from intelligent_visualiser.utils.constants import PolarAnimationTypes


class LivePolarAnimator(BasePolarAnimator):

    def __init__(self, animation_type, duration, fps, speed):
        super().__init__(duration, fps)
        self.speed = speed
        self.num_dot = 200
        self.animation_type = animation_type

    def get_r(self, time, state, r):
        return state + np.sin(state * time / 10)

    def get_c(self, time, state, angle):
        return (time % 10) * np.sin(state * time / 100) + np.pi * np.sin(state * time / 100)

    def visual(self, state, time):
        angle = state * self.speed

        theta = []
        r = []

        if self.animation_type == PolarAnimationTypes.CIRCLE:
            for i in range(self.num_dot + 1):
                r.append(state * 100 / (state + 10))
                theta.append(np.pi * 2 * i / self.num_dot)
        elif self.animation_type == PolarAnimationTypes.SPIRAL:
            theta.append(0)
            r.append(0)

            for ith_dot in range(3, self.num_dot):
                r.append(self.get_r(time, ith_dot, 1))
                theta.append(self.get_c(time, ith_dot, angle))

        return theta, r

    def animate(self, frame, line, audio_stream):
        time = frame / self.fps
        state = 0
        while True:
            try:
                state = np.linalg.norm(audio_stream.queue.get_nowait())
            except queue.Empty:
                break
        st = self.visual(state, time)

        line.set_data(st)
        return line,
