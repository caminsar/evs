# System Architecture

This document outlines the architecture of the LLM and VTK Driven Environment Visualization System.

## Overview

The system is designed to interpret natural language commands from a user, process these commands to understand the user's intent, and then manipulate a 3D scene rendered by the Visualization Toolkit (VTK) to reflect that intent. It integrates three main areas: Natural Language Processing (NLP) via an LLM, a Python application backend for logic and control, and 3D graphics via VTK.

```mermaid
graph TD
    A[User Input (Text Prompt)] --> B{LLM Interaction Module};
    B -- Raw Text Response --> C{Command Parser};
    C -- Parsed Command --> D{Visualization Logic};
    D -- Updates --> E[VTK Rendering Engine];
    E -- Renders --> F[3D Scene (Window)];

    G[Visualization Components Registry] -.-> D;
    H[Data Files (e.g., JSON)] -.-> G;

    subgraph Core Application
        B
        C
        D
        G
    end

    subgraph External Libraries/Services
        E
        %% LLM Model can be here if considered external
    end
```

*(Mermaid diagram illustrating the flow from user input to 3D scene update. This might not render in all Markdown viewers but describes the flow.)*

## Key Components and Flow

1.  **User Input**: The user provides a text prompt via a console interface.

2.  **LLM Interaction Module (`src/llm_driven_visualization.py` - `get_llm_response` function)**:
    *   The user's prompt is sent to a pre-trained Large Language Model (e.g., 'microsoft/DialoGPT-small').
    *   The LLM processes the input and generates a textual response. This response is fairly raw and conversational.

3.  **Command Parser (`src/llm_driven_visualization.py` - `parse_llm_command` function)**:
    *   The raw text response from the LLM is then parsed.
    *   Currently, this is a simple keyword-based parser that looks for terms like "atmosphere", "water", "ecosystem", etc., to map the LLM's output to a predefined set of internal commands (e.g., "show_atmosphere").

4.  **Visualization Logic (`src/llm_driven_visualization.py` - main loop)**:
    *   Based on the parsed command, the main application logic decides which action to take.
    *   This typically involves instantiating or interacting with one of the visualization component classes.

5.  **Visualization Components (`src/visualization/` package)**:
    *   **`Atmosphere`**: Manages the creation and rendering of an atmospheric representation (currently a sphere). It can load properties like color, radius, and opacity from `data/atmosphere_properties.json`.
    *   **`WaterBody`**: Manages the creation and rendering of water surfaces (currently a flat plane).
    *   **`Ecosystem`**: Manages the creation and rendering of land or vegetation areas (currently a flat plane).
    *   Each component has a `render(vtk_renderer)` method that creates VTK actors and adds them to the main VTK renderer. They also manage their state (e.g., storing their VTK actor) to allow for updates or removal.

6.  **VTK Rendering Engine**:
    *   A standard VTK setup (`vtkRenderer`, `vtkRenderWindow`, `vtkRenderWindowInteractor`) is used.
    *   The visualization components add their VTK actors to this renderer.
    *   The `vtkRenderWindow` displays the 3D scene, and the `vtkRenderWindowInteractor` allows for camera manipulation (orbit, pan, zoom).

## Core Scripts

*   **`src/llm_driven_visualization.py`**:
    *   The main entry point of the application.
    *   Initializes the LLM, VTK environment, and visualization components.
    *   Contains the primary interaction loop (prompt user, get LLM response, parse, act).
*   **`src/visualization/atmosphere.py`**, **`src/visualization/water_body.py`**, **`src/visualization/ecosystem.py`**:
    *   Define the classes for the individual visual components. They encapsulate the VTK object creation and properties for that specific element.
*   **`src/visualization/__init__.py`**:
    *   Makes the `visualization` directory a Python package and exposes the component classes for easy importing.

## Data Flow for Customization

*   Currently, the `Atmosphere` component demonstrates data-driven customization.
*   If a `data_path` is provided to its constructor, it attempts to load `name`, `color`, `radius`, and `opacity` from the specified JSON file (`data/atmosphere_properties.json`).
*   These loaded values then override the default parameters when rendering the atmosphere.

This architecture allows for a separation of concerns, where the LLM handles natural language, the main script orchestrates, and the visualization components manage their specific VTK representations.
