class BaseAnimator:

    def __init__(self, duration, fps):
        self.duration = duration
        self.fps = fps
        self.interval = 1000 / self.fps
        self.frames = self.duration * self.fps

    def generate(self, audio_stream, save=False, output_path=None):
        return NotImplementedError
