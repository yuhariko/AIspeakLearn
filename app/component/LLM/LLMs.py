class ChatLLMs:
    def __init__(self, model):
        self.model = model

    def get_message(self, message, max_tokens=100, temperature=0.5):
        result = self.model.create_chat_completion(
            max_tokens=max_tokens,
            temperature=temperature,
            messages=message
        )
        text_result = result['choices'][0]['message']['content']
        return text_result


if __name__ == "__main__":
    from llama_cpp import Llama

    llm = Llama(
        model_path="/home/huy/Downloads/Meta-Llama-3.1-8B-Instruct-Q4_K_M.gguf",
        chat_format="llama-3"
    )

    messages = [
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
    llm = ChatLLMs(llm)
    result = llm.get_message(messages)
    print(result)
