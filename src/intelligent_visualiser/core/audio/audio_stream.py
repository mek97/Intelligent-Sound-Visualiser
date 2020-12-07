import queue
import sys
import threading

import sounddevice as sd
import soundfile as sf


class AudioStream(threading.Thread):

    def __init__(self, duration, record=False, record_conf=None):
        threading.Thread.__init__(self)

        default_record_conf = {
            "mode": 'w',
            "samplerate": int(sd.query_devices()[0]['default_samplerate']),
            "channels": 1
        }

        if record_conf is None:
            record_conf = {}
        record_conf = {**default_record_conf, **record_conf}

        self.queue = queue.Queue()
        self.record = record
        self.record_conf = record_conf
        self.duration = duration

    def run(self):
        file = None
        try:
            if self.record:
                file = sf.SoundFile(**self.record_conf)

            def audio_callback(indata, frames, time, status):
                if status:
                    print(status, file=sys.stderr)
                self.queue.put(indata)

                if self.record:
                    file.write(indata)

            with sd.InputStream(callback=audio_callback) as stream:  # noqa: F841
                sd.sleep(self.duration * 1000)

        finally:
            if self.record and file is not None:
                file.close()
