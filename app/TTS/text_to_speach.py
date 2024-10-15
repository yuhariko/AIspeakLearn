import os

from utils.utils import find_or_create_temp_dir


class TextToSpeak:
    def __init__(self, model):
        self.model = model
        self.speaker_ids = self.model.hps.data.spk2id

    def get_speak(self, dp, speed=1.0, ids='EN-US'):
        path_temp = find_or_create_temp_dir()
        voice_out_path = os.path.join(path_temp, 'voice_out')
        if not os.path.exists(voice_out_path):
            os.makedirs(voice_out_path, exist_ok=True)
        output_path = os.path.join(voice_out_path, dp.id + ".wav")

        self.model.tts_to_file(dp.llm_message, self.speaker_ids[ids], output_path, speed=speed)
        dp.speak = output_path


if __name__ == "__main__":
    from melo.api import TTS
    from pipeline.dataclass import DataPoint

    dp = DataPoint()

    dp.id = "212321132123"
    dp.llm_message = "A little more moderation would be good. Of course, my life hasn't exactly been one of moderation."
    device = 'auto'
    model = TTS(language='EN', device=device, use_hf=False,
                ckpt_path="/home/huy/project/AIspeakLearn/model/checkpoint.pth")
    tts = TextToSpeak(model)
    print("success loading model")
    tts.get_speak(dp)
