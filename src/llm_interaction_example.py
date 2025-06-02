"""
A standalone example script for interacting with a Large Language Model (LLM).

This script demonstrates:
1. Loading a pre-trained conversational LLM (e.g., 'microsoft/DialoGPT-small')
   using the `transformers` library.
2. Sending text prompts to the LLM.
3. Receiving and printing the LLM's textual responses.
4. Maintaining a basic conversation history to provide context to the LLM.
5. An interactive loop for continuous conversation with the LLM.

This script is intended for testing LLM interaction independently of the main
VTK visualization application.
"""
from transformers import AutoModelForCausalLM, AutoTokenizer
import torch

# Global variables to store the tokenizer, model, and chat history
# These are used to maintain state across multiple calls to get_llm_response
tokenizer = None
model = None
chat_history_ids = None

def initialize_model():
    """
    Loads the pre-trained conversational LLM and its tokenizer.

    Uses 'microsoft/DialoGPT-small' by default. Sets global variables
    `tokenizer` and `model`. Handles potential errors during loading,
    such as network issues or incorrect model names.
    """
    global tokenizer, model
    try:
        model_name = 'microsoft/DialoGPT-small'
        tokenizer = AutoTokenizer.from_pretrained(model_name)
        model = AutoModelForCausalLM.from_pretrained(model_name)
        print(f"Model '{model_name}' loaded successfully.")
    except Exception as e:
        print(f"Error loading model: {e}")
        print("Please ensure you have an active internet connection and the model name is correct.")
        print("You might need to install additional dependencies like 'sentencepiece'.")
        tokenizer = None
        model = None

def get_llm_response(prompt_text: str) -> str:
    """
    Sends a text prompt to the loaded LLM and returns its textual response.

    Maintains a simple conversation history by appending new input tokens to
    previously generated chat history IDs. This provides some context to the LLM.

    Args:
        prompt_text (str): The user's input text to send to the LLM.

    Returns:
        str: The LLM's generated response as a string. Returns an error message
             if the model is not initialized or if an error occurs during generation.
    """
    global tokenizer, model, chat_history_ids

    if not tokenizer or not model:
        return "Model not initialized. Please call initialize_model() first."

    try:
        # Encode the new user input, add the eos_token and return a tensor in Pytorch
        new_user_input_ids = tokenizer.encode(prompt_text + tokenizer.eos_token, return_tensors='pt')

        # Append the new user input tokens to the chat history
        if chat_history_ids is not None:
            bot_input_ids = torch.cat([chat_history_ids, new_user_input_ids], dim=-1)
        else:
            bot_input_ids = new_user_input_ids

        # Generate a response
        # Parameters are set to encourage diverse and coherent responses.
        chat_history_ids = model.generate(
            bot_input_ids,
            max_length=1024,          # Max length of the entire conversation history
            new_tokens_max_length=100, # Max length for the newly generated part of the response
            pad_token_id=tokenizer.eos_token_id,
            no_repeat_ngram_size=3, # Helps prevent repetitive phrases
            do_sample=True,         # Enables sampling for less deterministic responses
            top_k=50,               # Considers the top_k most probable tokens at each step
            top_p=0.95,             # Nucleus sampling: considers smallest set of tokens whose cumulative probability exceeds top_p
            temperature=0.7         # Controls randomness: lower is more deterministic, higher is more random
        )

        # Decode only the newly generated part of the response
        response = tokenizer.decode(chat_history_ids[:, bot_input_ids.shape[-1]:][0], skip_special_tokens=True)
        return response
    except Exception as e:
        return f"Error during LLM interaction: {e}"

if __name__ == "__main__":
    """
    Main execution block for the LLM interaction example.

    Initializes the LLM, then runs a sequence of predefined prompts followed by
    an interactive loop allowing the user to chat with the LLM.
    """
    # Initialize the model first
    initialize_model()

    if model and tokenizer: # Proceed only if model initialization was successful
        print("\nLLM Interaction Example:")
        print("------------------------")
        # Demonstrate with a few predefined prompts
        prompts = [
            "Hello, how are you?",
            "What is VTK?",
            "Tell me a joke related to programming."
        ]

        for i, prompt in enumerate(prompts):
            print(f"\nUser Prompt {i+1}: {prompt}")
            response = get_llm_response(prompt)
            print(f"LLM Response {i+1}: {response}")
            if i < len(prompts) - 1:
                print("---") # Separator

        print("\nNote: The LLM maintains conversation history for this session.")
        print("Try asking follow-up questions!")
        print("Type 'exit' to end the conversation.")

        # Interactive loop for continuous conversation
        while True:
            user_prompt = input("\nYour prompt: ")
            if user_prompt.lower() == 'exit':
                print("Exiting interactive session.")
                break
            llm_reply = get_llm_response(user_prompt)
            print(f"LLM: {llm_reply}")
    else:
        print("\nSkipping LLM interaction example due to model initialization failure.")
