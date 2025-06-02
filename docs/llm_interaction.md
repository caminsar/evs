# LLM Interaction

This document explains how the system utilizes a Large Language Model (LLM) to process user commands and translate them into visualization actions.

## Overview

The goal of integrating an LLM is to provide a more natural and intuitive way for users to interact with the 3D visualization system. Instead of requiring specific syntax or GUI interactions, users can type commands in plain English.

## LLM Model Used

*   **Model**: `microsoft/DialoGPT-small`
*   **Library**: `transformers` by Hugging Face
*   **Reasoning**: `DialoGPT-small` is a relatively lightweight conversational model suitable for demonstrating the concept without requiring extensive computational resources. It's designed for dialogue and can generate coherent (though not always perfectly accurate or instruction-following) responses.

## Interaction Flow

The LLM interaction process is primarily managed within `src/llm_driven_visualization.py`:

1.  **Initialization (`initialize_llm_model`)**:
    *   The tokenizer and the pre-trained model (`AutoTokenizer`, `AutoModelForCausalLM`) are loaded when the application starts.
    *   If the model files are not present locally, they are downloaded from the Hugging Face model hub.

2.  **User Prompt**:
    *   The user types a command in the console (e.g., "Show me the sky", "Add some water").

3.  **Getting LLM Response (`get_llm_response`)**:
    *   The user's input string is encoded by the tokenizer.
    *   This encoded input is fed to the LLM model.
    *   The function maintains a basic chat history (`llm_chat_history_ids`) by concatenating new inputs with previous conversation turns. This allows the LLM to have some context, potentially leading to more relevant follow-up responses.
    *   The LLM generates a response based on the input and chat history.
    *   The response (which is initially in tokenized form) is decoded back into a human-readable string.

4.  **Command Parsing (`parse_llm_command`)**:
    *   The raw text string received from `get_llm_response` is then passed to `parse_llm_command`.
    *   **Current Approach**: This function implements a very simple keyword-based parsing strategy. It converts the LLM's response to lowercase and checks for the presence of specific keywords:
        *   `"atmosphere"`, `"air"` -> map to internal command `"show_atmosphere"`
        *   `"water"`, `"ocean"`, `"lake"`, `"river"` -> map to `"show_water"`
        *   `"ecosystem"`, `"eco"`, `"vegetation"`, `"habitat"`, `"plant"` -> map to `"show_ecosystem"`
        *   If no relevant keywords are found, it returns `"unknown_command"`.

5.  **Action Mapping (Main Loop in `llm_driven_visualization.py`)**:
    *   The internal command returned by `parse_llm_command` is then used in a series of `if/elif` statements to trigger the corresponding visualization action (e.g., creating an `Atmosphere` object and calling its `render` method).

## Limitations of Current Approach

*   **Simple Keyword Matching**: The parsing is naive. It doesn't understand grammar, context beyond keywords, or complex instructions. For example, "Don't show the atmosphere" might still trigger "show_atmosphere" if the LLM's response includes "atmosphere".
*   **LLM's Conversational Nature**: `DialoGPT-small` is designed for conversation, not necessarily for direct instruction following like some newer instruction-tuned models. Its responses can be verbose or conversational rather than direct commands. For instance, if you say "Show the sky", it might reply "Okay, I can try to show you what the sky looks like!" The parser then just looks for "sky" (or related terms like "atmosphere") in this response.
*   **No Complex State Management**: The system doesn't robustly track what's already visible or handle complex sequences of commands like "show X then remove Y then add Z". Each command is largely treated independently, though component `render` methods do replace existing actors of the same type.
*   **Limited Vocabulary**: The parser only understands a predefined set of keywords.

## Future Improvements

*   **More Sophisticated Parsing**:
    *   Using regular expressions for more flexible pattern matching.
    *   Employing NLP techniques like Named Entity Recognition (NER) to identify objects and actions.
    *   Using more advanced LLMs that are better at instruction-following or function calling.
*   **Intent Recognition**: Moving beyond simple keywords to a more robust intent recognition system.
*   **Parameter Extraction**: Enabling commands like "show a *small* blue sphere for atmosphere" by extracting parameters (size, color) from the LLM response.
*   **Better State Tracking**: Implementing a scene graph or state manager to have a clearer picture of what is currently displayed and how new commands should modify it.

Despite the current limitations, the integration demonstrates the potential of using LLMs for creating more user-friendly interfaces for complex visualization tools.
