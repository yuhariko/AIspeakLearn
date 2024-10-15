import os

from LLM.prompt import system_prompt
from utils.utils import find_or_create_temp_dir, get_llm_format, get_message_from_json


class MessageCollector:
    def __init__(self):
        self.message_path = find_or_create_temp_dir()

    def get_chat_message(self, dp, number_maximum_message=10):
        """
        Prepare the message to put into LLMs.
        :param dp: datapoint
        :param number_maximum_message:length history of message to LLMs. It affects the speed and accurate of LLMs.
        :return: put message to datapoint
        """
        llm_chat_path = os.path.join(self.message_path, 'chat')
        if not os.path.exists(llm_chat_path):
            os.makedirs(llm_chat_path, exist_ok=True)
        llm_file_path = os.path.join(llm_chat_path, dp.id + ".json")
        dp.llm_file_path = llm_file_path
        messages = get_message_from_json(llm_file_path)

        if len(messages) == 0:
            system_prompt_with_topic = system_prompt.format(topic=dp.topic)
            system_role = get_llm_format(role='system', content=system_prompt_with_topic)
            messages.append(system_role)
        user_role = get_llm_format(role='user', content=dp.user_text)
        messages.append(user_role)
        dp.message = messages


if __name__ == "__main__":
    from pipeline.dataclass import DataPoint
    from utils.utils import write_message_to_cache

    dp = DataPoint()
    dp.id = "temp_id"
    dp.topic = "menu"
    dp.user_text = "You are number one"
    mc = MessageCollector()
    mc.get_chat_message(dp)
    dp.llm_message = {'role': 'assistant', 'content': 'abbcbcbcbc'}
    write_message_to_cache(dp)
