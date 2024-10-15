import json
import os

from langchain.chains.question_answering.map_reduce_prompt import messages


def find_or_create_temp_dir():
    current_path = os.path.dirname(os.path.abspath(__file__))

    app_dir = os.path.dirname(current_path)
    project_root = os.path.dirname(app_dir)

    # Define the temp directory path relative to the project root
    temp_dir = os.path.join(project_root, "temp")

    # Check if the temp directory exists, if not, create it
    if not os.path.exists(temp_dir):
        os.makedirs(temp_dir, exist_ok=True)

    return temp_dir


def get_llm_format(role, content):
    return {
        'role': role,
        'content': content
    }


def get_message_from_json(file_path):
    if os.path.isdir(file_path):
        with open(file_path, 'r') as file:
            data = json.load(file)
    else:
        data = []
        json_object = json.dumps(data, indent=4)
        with open(file_path, "w") as outfile:
            outfile.write(json_object)
    return data


def write_message_to_cache(dp):
    """
    Write the history message to temp.
    :param dp: get id, llm_message, user_text
    :return:
    """
    message = dp.message
    llm_response = get_llm_format(role='assistant', content=dp.llm_message)
    message.append(llm_response)

    json_object = json.dumps(message, indent=4)
    with open(dp.llm_file_path, "w") as outfile:
        outfile.write(json_object)


if __name__ == "__main__":
    temp_directory = find_or_create_temp_dir()
    print(f"Using temp directory: {temp_directory}")
