import os

from utils.utils import find_or_create_temp_dir


class TextToSpeak:
    def __init__(self, model):
        self.model = model
        self.speaker_ids = self.model.hps.data.spk2id

    def get_speak(self, id, text, speed=1.0, ids='EN-US'):
        path_temp = find_or_create_temp_dir()
        output_path = os.path.join(path_temp, id + ".wav")
        self.model.tts_to_file(text, self.speaker_ids[ids], output_path, speed=speed)


if __name__ == "__main__":
    from melo.api import TTS

    text = "Did you ever hear a folk tale about a giant turtle?"
    device = 'auto'
    model = TTS(language='EN', device=device)
    tts = TextToSpeak(model)
    print("success loading model")
    tts.get_speak("abc", text)
