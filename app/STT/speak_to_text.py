class SpeakToText:
    def __init__(self, model):
        self.model = model

    def get_user_text(self, dp):
        result = self.model.transcribe(dp.audio)
        text = result["text"]
        dp.user_text = text


if __name__ == "__main__":
    import whisper
    from pipeline.dataclass import DataPoint

    dp = DataPoint()
    dp.audio = "/home/huy/project/AIspeakLearn/temp/abc.wav"
    model = whisper.load_model("tiny.en")
    tts = SpeakToText(model)
    result = tts.get_text(dp)
    print(dp.text_result)
