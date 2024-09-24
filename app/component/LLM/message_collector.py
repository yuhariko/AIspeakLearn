import os
import json


class MessageCollector:
    def __init__(self, id, message_path):
        self.id = id
        self.message_path = message_path
        self.file_path = os.path.join(self.message_path, self.id + ".json")

    def get_message_from_json(self):
        with open(self.file_path, 'r') as file:
            data = json.load(file)
        return data

    def write_message_to_cache(self, contents):
        """contents: A list of dict include data format {'role':'user'/'assistant'/'system', 'content':text data}"""
        for content in contents:
            if content['role'] not in ['user', 'assistant', 'system']:
                raise f'The role excepted are user and assistant but get {content["role"]}'
        if os.path.isfile(self.file_path):
            with open(self.file_path, 'r') as file:
                data = json.load(file)

            data.extend(contents)
        else:
            data = contents

        json_object = json.dumps(data, indent=4)
        with open(self.file_path, "w") as outfile:
            outfile.write(json_object)

    def get_chat_message(self, number_maximum_message=10):
        """if the length of chat too long we need to summary it to run faster."""
        messages = self.get_message_from_json()
        number_message = len(messages)

        if number_message < 10:
            return messages
        else:
            return messages


if __name__ == "__main__":
    mc = MessageCollector("abcdedfg", "/home/huy/project/AIspeakLearn/temp")
    contents = [
        {"role": "system", "content": "You are an assistant who is English foreigner."},
        {
            "role": "assistant",
            "content": "conversation talk about tet holiday."
        },
        {
            "role": "user",
            "content": "when it start?"
        }
    ]
    mc.write_message_to_cache(contents)

