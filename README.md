# LLM and VTK Driven Environment Visualization System

## Overview

This project demonstrates a prototype system for visualizing environmental components (like atmosphere, water bodies, and ecosystems) in a 3D scene using the Visualization Toolkit (VTK). The unique aspect of this system is its natural language interface, powered by a Large Language Model (LLM), allowing users to command the visualization through text prompts.

The system parses user commands, interprets the intent using an LLM (currently 'microsoft/DialoGPT-small'), and then triggers corresponding actions to render or modify objects in the VTK scene.

## Features

*   **LLM-Driven Interaction**: Control the visualization using natural language commands.
*   **3D Visualization**: Utilizes VTK for rendering environmental components.
*   **Modular Components**: Separate Python classes for:
    *   `Atmosphere`: Visualized as a sphere, properties can be customized via a JSON file.
    *   `WaterBody`: Visualized as a flat plane.
    *   `Ecosystem`: Visualized as a flat plane representing land/vegetation.
*   **Basic Data Persistence**: Atmosphere visualization can be customized by editing `data/atmosphere_properties.json`.
*   **Example Scripts**: Includes a main application (`src/llm_driven_visualization.py`) and an initial VTK example (`src/initial_vtk_example.py`).

## Project Structure

```
.
├── data/
│   └── atmosphere_properties.json  # Sample data for atmosphere
├── docs/
│   ├── README.md                   # Documentation main page
│   ├── architecture.md             # System architecture details
│   ├── components.md               # Visualization component details
│   └── llm_interaction.md          # LLM interaction specifics
├── src/
│   ├── visualization/
│   │   ├── __init__.py
│   │   ├── atmosphere.py
│   │   ├── ecosystem.py
│   │   └── water_body.py
│   ├── llm_driven_visualization.py # Main application
│   ├── llm_interaction_example.py  # Standalone LLM example
│   └── initial_vtk_example.py      # Standalone VTK example
├── requirements.txt                # Project dependencies
└── README.md                       # This file
```

## Setup Instructions

1.  **Clone the Repository** (if applicable)
    ```bash
    # git clone <repository_url>
    # cd <repository_directory>
    ```

2.  **Create a Python Virtual Environment**
    It's highly recommended to use a virtual environment:
    ```bash
    python -m venv venv
    source venv/bin/activate  # On Windows: venv\Scripts\activate
    ```

3.  **Install Dependencies**
    Install the required Python packages using pip:
    ```bash
    pip install -r requirements.txt
    ```
    This will install `vtk`, `transformers`, `torch`, and their dependencies. Note that `torch` can be a large download.

## How to Run

1.  **Navigate to the Source Directory or Project Root**:
    Ensure your terminal is in the project's root directory. The main script handles path adjustments for imports.

2.  **Run the Main Application**:
    ```bash
    python src/llm_driven_visualization.py
    ```
    *   The first time you run this, it might take a while to download the LLM model files (e.g., 'microsoft/DialoGPT-small', ~350MB).
    *   A VTK window will open, and you'll be prompted in the console for commands.

3.  **Example Commands**:
    Once the application is running, try typing these commands in the console:
    *   `"Hello"`
    *   `"Show me the atmosphere"` (this will use properties from `data/atmosphere_properties.json`)
    *   `"Display a large ocean"`
    *   `"Add some vegetation"`
    *   `"What can you show me?"` (LLM response might not always be useful for commands)
    *   `"exit"` (to close the application)

## Further Documentation

For more detailed information on the system architecture, components, and LLM interaction, please refer to the documents in the `docs/` directory. Start with `docs/README.md`.

## Future Enhancements (Potential)
* More sophisticated LLM command parsing and state management.
* Advanced VTK rendering (textures, lighting, more complex geometries).
* Data-driven customization for all components.
* UI for easier interaction beyond the console.
* Support for more diverse environmental phenomena.
