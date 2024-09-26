class TextToSpeach:
    def __init__(self, model):
        self.model = model

    def get_text(self, audio_path):
        result = self.model.transcribe(audio_path)
        text_result = result["text"]
        return text_result


if __name__ == "__main__":
    import whisper

    model = whisper.load_model("tiny.en")
    tts = TextToSpeach(model)
    result = tts.get_text("/home/huy/Downloads/test_000000/ZBA040416CL19/ZBA040416CL19/ZBA_040416-CL19_DOT_flac_00005.flac")
    print(result)
