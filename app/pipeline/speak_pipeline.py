import os
import whisper
from llama_cpp import Llama
from melo.api import TTS

from pipeline.dataclass import DataPoint, Result
from utils.utils import write_message_to_cache
from STT.speak_to_text import SpeakToText
from TTS.text_to_speach import TextToSpeak
from LLM.LLMs import ChatLLMs
from LLM.message_collector import MessageCollector


class SpeakAI:
    def __init__(self, llm_model=None, tts_model=None):
        ai_model_path = os.environ['MODEL_PATH']
        try:
            stt_model = whisper.load_model("tiny.en")
            self.stt = SpeakToText(stt_model)
            print("Load TTS successful!")
        except:
            raise "Can not load Speak to text model!"

        if llm_model is None:
            llm_model = "Llama-3.2-1B-Instruct-Q6_K_L.gguf"
        try:
            llm_path = os.path.join(ai_model_path, llm_model)
            llm = Llama(
                model_path=llm_path,
                chat_format="llama-3"
            )
            self.llms = ChatLLMs(llm)
            print("Load LLM successful!")
        except:
            raise "Can not load LLM!"
        self.mc = MessageCollector()
        if tts_model is None:
            tts_model = "checkpoint.pth"
        try:
            tts_path = os.path.join(ai_model_path, tts_model)
            device = 'auto'
            model = TTS(language='EN', device=device, use_hf=False, ckpt_path=tts_path)
            self.tts = TextToSpeak(model)
            print("Load TTS successful!")
        except:
            raise "Can not load TTS!"

        self.config = ['user_text', 'llm_message', 'speak']

    def serve(self, id, audio, topic):
        """
        Get user speech text and llm response
        :param id: id of chat
        :param audio: path of audio input
        :param topic: topic of chat
        :return: text of user, llm response, response audio
        """
        dp = DataPoint()
        dp.id = id
        dp.audio = audio
        dp.topic = topic

        self.stt.get_user_text(dp)
        print('speech to text done')
        self.mc.get_chat_message(dp)
        self.llms.get_llm_message(dp)
        print('llm done')
        self.tts.get_speak(dp)
        print('text to speech done')
        write_message_to_cache(dp)

        result = Result(self.config)
        final_result = result.to_dict(dp)
        return final_result


if __name__ == "__main__":
    spk = SpeakAI()
    result = spk.serve('abc', "/home/huy/project/AIspeakLearn/temp/voice_in/test.wav", 'toys')
    print(result)
    print('succesful!!!')
