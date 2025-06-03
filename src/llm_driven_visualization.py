"""
Main application script for the LLM and VTK Driven Environment Visualization System.

This script integrates a Large Language Model (LLM) for natural language command
processing and the Visualization Toolkit (VTK) for 3D rendering of environmental
components like atmosphere, water bodies, and ecosystems.

It allows users to type commands in natural language, which are then interpreted
by an LLM. The LLM's response is parsed to identify visualization actions,
which are then executed to update a 3D scene.
"""
import vtk
from transformers import AutoModelForCausalLM, AutoTokenizer
import torch
import sys
import os

# --- Path Setup ---
# Ensures that the 'visualization' package can be imported correctly
# when the script is run from the project root or the 'src' directory.
SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
PROJECT_ROOT = os.path.abspath(os.path.join(SCRIPT_DIR, '..'))
sys.path.insert(0, PROJECT_ROOT)

from visualization import Atmosphere, WaterBody, Ecosystem

# --- LLM Setup ---
llm_tokenizer = None
llm_model = None
llm_chat_history_ids = None

def initialize_llm_model():
    """
    Loads the pre-trained conversational LLM and its tokenizer.

    Uses 'microsoft/DialoGPT-small' by default. Sets global variables
    `llm_tokenizer` and `llm_model`. Handles potential errors during loading,
    such as network issues or incorrect model names.
    """
    global llm_tokenizer, llm_model
    try:
        model_name = 'microsoft/DialoGPT-small'
        llm_tokenizer = AutoTokenizer.from_pretrained(model_name)
        llm_model = AutoModelForCausalLM.from_pretrained(model_name)
        print(f"LLM Model '{model_name}' loaded successfully.")
    except Exception as e:
        print(f"Error loading LLM model: {e}")
        print("Please ensure you have an active internet connection and the model name is correct.")
        llm_tokenizer = None
        llm_model = None

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
    global llm_tokenizer, llm_model, llm_chat_history_ids

    if not llm_tokenizer or not llm_model:
        return "LLM Model not initialized. Please call initialize_llm_model() first."

    try:
        # Encode the new user input, add the eos_token and return a tensor in Pytorch
        new_user_input_ids = llm_tokenizer.encode(prompt_text + llm_tokenizer.eos_token, return_tensors='pt')

        # Append the new user input tokens to the chat history
        if llm_chat_history_ids is not None:
            bot_input_ids = torch.cat([llm_chat_history_ids, new_user_input_ids], dim=-1)
        else:
            bot_input_ids = new_user_input_ids

        # Generate a response
        llm_chat_history_ids = llm_model.generate(
            bot_input_ids,
            max_length=1024,
            new_tokens_max_length=100, # Max tokens for the new response part
            pad_token_id=llm_tokenizer.eos_token_id,
            no_repeat_ngram_size=3,
            do_sample=True,
            top_k=50,
            top_p=0.95,
            temperature=0.7
        )
        # Decode only the newly generated tokens
        response = llm_tokenizer.decode(llm_chat_history_ids[:, bot_input_ids.shape[-1]:][0], skip_special_tokens=True)
        return response
    except Exception as e:
        return f"Error during LLM interaction: {e}"

# --- Command Parsing Logic ---
def parse_llm_command(llm_response: str) -> str:
    """
    Parses the LLM's raw text response to identify predefined visualization commands.

    This implementation uses simple case-insensitive keyword matching.

    Args:
        llm_response (str): The raw text output from the LLM.

    Returns:
        str: A string representing a recognized command (e.g., "show_atmosphere",
             "show_water", "show_ecosystem") or "unknown_command" if no
             keywords are matched.
    """
    response_lower = llm_response.lower()
    if "atmosphere" in response_lower or "air" in response_lower or "sky" in response_lower:
        return "show_atmosphere"
    elif "water" in response_lower or "ocean" in response_lower or \
         "lake" in response_lower or "river" in response_lower:
        return "show_water"
    elif "ecosystem" in response_lower or "eco" in response_lower or \
         "vegetation" in response_lower or "habitat" in response_lower or \
         "plant" in response_lower or "forest" in response_lower or "land" in response_lower:
        return "show_ecosystem"
    return "unknown_command"

# --- Main Application ---
def main():
    """
    Runs the main interactive loop for the LLM-driven visualization.

    Initializes the LLM and VTK environments. Then, enters a loop that:
    1. Prompts the user for a natural language command.
    2. Sends the command to the LLM.
    3. Parses the LLM's response to a known command.
    4. Executes the command by interacting with visualization components.
    The loop continues until the user types 'exit'.
    """
    print("--- Initializing LLM Driven Visualization ---")

    # Initialize LLM
    initialize_llm_model()
    if not llm_model or not llm_tokenizer:
        print("LLM initialization failed. Exiting.")
        return

    # --- VTK Setup ---
    renderer = vtk.vtkRenderer()
    renderer.SetBackground(0.2, 0.3, 0.5)

    render_window = vtk.vtkRenderWindow()
    render_window.AddRenderer(renderer)
    render_window.SetSize(1000, 800)
    render_window.SetWindowName("LLM Driven Visualization")

    render_window_interactor = vtk.vtkRenderWindowInteractor()
    render_window_interactor.SetRenderWindow(render_window)
    render_window_interactor.SetInteractorStyle(vtk.vtkInteractorStyleTrackballCamera())

    render_window.Render()
    render_window_interactor.Initialize()
    # Note: render_window_interactor.Start() is not called here to keep the CLI interactive.
    # The window will update via render_window.Render() calls after actions.

    print("--- VTK Setup Complete. Render window is active. ---")
    print("--- Type 'exit' to end the application. ---")

    # --- Main Loop ---
    while True:
        user_prompt = input("\nWhat do you want to see in the visualization? (e.g., 'show me the sky', 'display ocean', 'add forest')\n> ")

        if user_prompt.lower() == 'exit':
            print("Exiting application.")
            break

        if not user_prompt.strip():
            continue

        print(f"User prompt: {user_prompt}")
        llm_raw_response = get_llm_response(user_prompt)
        print(f"LLM raw response: {llm_raw_response}")

        command = parse_llm_command(llm_raw_response)
        print(f"Parsed command: {command}")

        # --- Action Mapping ---
        if command == "show_atmosphere":
            atmosphere_data_file = os.path.join(PROJECT_ROOT, "data", "atmosphere_properties.json")
            print(f"Attempting to load atmosphere data from: {atmosphere_data_file}")
            atmosphere_viz = Atmosphere(data_path=atmosphere_data_file)
            atmosphere_viz.render(renderer)
            render_window.Render()
            print(f"LLM command: show_atmosphere. Visualizing atmosphere: {atmosphere_viz.name}")
        elif command == "show_water":
            water_viz = WaterBody(name="LLM_WaterBody") # Using default name
            water_viz.render(renderer)
            render_window.Render()
            print(f"LLM command: show_water. Visualizing water body: {water_viz.name}")
        elif command == "show_ecosystem":
            eco_viz = Ecosystem(name="LLM_Ecosystem") # Using default name
            eco_viz.render(renderer)
            render_window.Render()
            print(f"LLM command: show_ecosystem. Visualizing ecosystem: {eco_viz.name}")
        elif command == "unknown_command":
            print(f"LLM response ('{llm_raw_response}') did not map to a known visualization command.")
        else: # Should not happen with current parse_llm_command logic
            print(f"Unprocessed command: {command}")

    print("--- Application Finished ---")

if __name__ == "__main__":
    main()
