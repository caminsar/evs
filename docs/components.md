# Visualization Components

This document provides details on the individual visualization components used in the LLM and VTK Driven Environment Visualization System. These components are Python classes responsible for creating and managing specific visual elements within the 3D scene.

All visualization components are located in the `src/visualization/` directory.

## Common Structure

Each component generally follows this pattern:
*   An `__init__(self, name, ...)` method for initialization, often accepting a name and optionally a path to a data file for customization.
*   A `load_data(self)` method if the component supports external data configuration (e.g., from JSON).
*   A `render(self, vtk_renderer)` method that:
    *   Checks if a previous actor for this component exists and removes it to allow for updates.
    *   Creates VTK sources (e.g., `vtkSphereSource`, `vtkPlaneSource`).
    *   Creates VTK mappers and actors.
    *   Sets properties of the actor (color, opacity, size, etc.), potentially using loaded data.
    *   Adds the actor to the provided `vtk_renderer`.
    *   Stores the actor in an instance variable (e.g., `self.actor`).
*   A `remove(self, vtk_renderer)` method to explicitly remove the component's actor from the scene.

---

## 1. Atmosphere

*   **Module**: `src/visualization/atmosphere.py`
*   **Class**: `Atmosphere`
*   **Purpose**: Represents the Earth's atmosphere or a sky dome.
*   **Visual Representation**:
    *   Rendered as a large `vtkSphereSource`.
    *   Typically semi-transparent to allow viewing of other objects.
*   **Default Properties**:
    *   Radius: 15.0
    *   Color: Light Blue ([0.53, 0.81, 0.92])
    *   Opacity: 0.3
*   **Data-Driven Customization**:
    *   The `Atmosphere` class can load its properties from a JSON file.
    *   **Data File**: `data/atmosphere_properties.json` (by default, as configured in `llm_driven_visualization.py`).
    *   **Constructor**: `Atmosphere(name="DefaultAtmosphere", data_path=None)`
    *   **Loaded Properties**:
        *   `name` (string): Name of the atmosphere instance.
        *   `color` (list of 3 floats, e.g., `[0.0, 0.7, 0.9]`): RGB color.
        *   `radius` (float): Radius of the sphere.
        *   `opacity` (float): Opacity of the sphere (0.0 to 1.0).
    *   If the data file is not found, is invalid, or a specific property is missing, the component falls back to its default values for those properties.

---

## 2. WaterBody

*   **Module**: `src/visualization/water_body.py`
*   **Class**: `WaterBody`
*   **Purpose**: Represents a body of water, such as an ocean, lake, or large river.
*   **Visual Representation**:
    *   Rendered as a flat `vtkPlaneSource`.
    *   Positioned at Z=0 by default.
*   **Default Properties**:
    *   Size: 20x20 units (defined by `SetOrigin`, `SetPoint1`, `SetPoint2` of the plane source).
    *   Color: Blue ([0.1, 0.3, 0.7])
    *   Opacity: 1.0 (opaque)
*   **Data-Driven Customization**:
    *   Currently, the `WaterBody` component does not implement loading properties from an external data file. Customization would require direct modification of its class or instantiation parameters.

---

## 3. Ecosystem

*   **Module**: `src/visualization/ecosystem.py`
*   **Class**: `Ecosystem`
*   **Purpose**: Represents a patch of land, vegetation, or a general terrestrial ecosystem.
*   **Visual Representation**:
    *   Rendered as a flat `vtkPlaneSource`.
    *   Positioned slightly above Z=0 (e.g., Z=0.1) to avoid Z-fighting if a `WaterBody` is also present at Z=0.
*   **Default Properties**:
    *   Size: 16x16 units.
    *   Color: Green ([0.0, 0.6, 0.2])
    *   Opacity: 1.0 (opaque)
*   **Data-Driven Customization**:
    *   Currently, the `Ecosystem` component does not implement loading properties from an external data file. Customization would require direct modification of its class or instantiation parameters.

---

These components form the foundational visual elements of the simulation. Future work could involve making them more complex (e.g., using textures, more detailed geometries, animations) and expanding data-driven customization to all components.
