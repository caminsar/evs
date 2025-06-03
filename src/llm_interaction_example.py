"""
A standalone example script for interacting with a Large Language Model (LLM).

This script demonstrates:
1. Loading a pre-trained conversational LLM (e.g., 'microsoft/DialoGPT-small')
   using the `transformers` library.
2. Sending text prompts to the LLM, including attention masks.
3. Receiving and printing the LLM's textual responses.
4. Maintaining a basic conversation history (input_ids and attention_mask)
   to provide context to the LLM.
5. An interactive loop for continuous conversation with the LLM.

This script is intended for testing LLM interaction independently of the main
VTK visualization application.
"""
from transformers import AutoModelForCausalLM, AutoTokenizer
import torch

# Global variables to store the tokenizer, model, and chat history
tokenizer = None
model = None
# chat_history_ids and chat_history_attention_mask will store the concatenated history
chat_history_input_ids = None
chat_history_attention_mask = None


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
        # Ensure tokenizer adds padding token if it doesn't have one, for consistent attention mask handling
        tokenizer = AutoTokenizer.from_pretrained(model_name)
        if tokenizer.pad_token is None:
            tokenizer.pad_token = tokenizer.eos_token # Common practice for models like GPT

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

    Maintains a simple conversation history by appending new input tokens and
    their attention masks to previously generated chat history. This provides
    context and proper padding information to the LLM.

    Args:
        prompt_text (str): The user's input text to send to the LLM.

    Returns:
        str: The LLM's generated response as a string. Returns an error message
             if the model is not initialized or if an error occurs during generation.
    """
    global tokenizer, model, chat_history_input_ids, chat_history_attention_mask

    if not tokenizer or not model:
        return "Model not initialized. Please call initialize_model() first."

    try:
        # Encode the new user input, add the eos_token, and return tensors & attention_mask
        # Using __call__ method of the tokenizer
        new_input = tokenizer(
            prompt_text + tokenizer.eos_token,
            return_tensors='pt',
            return_attention_mask=True,
            # padding=True, # Usually not needed here as we are encoding a single sequence
            # truncation=True # Optional: if prompts can be very long
        )
        new_user_input_ids = new_input.input_ids
        new_user_attention_mask = new_input.attention_mask

        # Append the new user input tokens and attention mask to the chat history
        if chat_history_input_ids is not None:
            bot_input_ids = torch.cat([chat_history_input_ids, new_user_input_ids], dim=-1)
            bot_attention_mask = torch.cat([chat_history_attention_mask, new_user_attention_mask], dim=-1)
        else:
            bot_input_ids = new_user_input_ids
            bot_attention_mask = new_user_attention_mask

        # Generate a response
        # Parameters are set to encourage diverse and coherent responses.
        # The model.generate call now includes the attention_mask
        generated_ids = model.generate(
            input_ids=bot_input_ids,
            attention_mask=bot_attention_mask,
            max_length=1024,          # Max length of the entire conversation history (input + output)
            max_new_tokens=100,       # Max length for the newly generated part of the response
            pad_token_id=tokenizer.pad_token_id, # Use tokenizer.pad_token_id
            eos_token_id=tokenizer.eos_token_id,
            no_repeat_ngram_size=3,
            do_sample=True,
            top_k=50,
            top_p=0.95,
            temperature=0.7
        )

        # Update chat history with the full sequence generated (including prompt and response)
        chat_history_input_ids = generated_ids
        # Recreate attention mask for the generated history (everything is attended to)
        chat_history_attention_mask = torch.ones_like(generated_ids)


        # Decode only the newly generated part of the response
        # This is the part of generated_ids that comes after bot_input_ids
        response_ids = generated_ids[:, bot_input_ids.shape[-1]:]
        response = tokenizer.decode(response_ids[0], skip_special_tokens=True)

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
            # Reset history for next independent prompt in this demo part
            if i < len(prompts) - 1: # Not for the last predefined prompt
                 chat_history_input_ids = None
                 chat_history_attention_mask = None


        print("\nNote: The LLM maintains conversation history for the following interactive session.")
        print("Try asking follow-up questions!")
        print("Type 'exit' to end the conversation.")
        # Reset history before starting interactive loop for a fresh conversation
        chat_history_input_ids = None
        chat_history_attention_mask = None

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
