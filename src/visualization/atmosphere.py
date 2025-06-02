"""
Defines the Atmosphere class for visualizing an atmospheric component.

This module provides the `Atmosphere` class, which is responsible for creating
and managing a 3D representation of an atmosphere (typically a large sphere)
in a VTK scene. It supports customization through an external JSON data file.
"""
import vtk
import json # Added for JSON parsing
import os # Added to check file existence

class Atmosphere:
    """
    Represents the atmospheric component of the visualization.

    This class handles the creation of a spherical VTK actor to represent
    the atmosphere. It can load properties such as name, color, radius, and
    opacity from a specified JSON data file, falling back to defaults if
    the file or specific properties are not found or are invalid.
    """
    def __init__(self, name="DefaultAtmosphere", data_path=None):
        """
        Initializes the Atmosphere object.

        Args:
            name (str, optional): Default name for the atmosphere instance. This
                                  name can be overridden if a "name" key is
                                  present in the loaded JSON data.
                                  Defaults to "DefaultAtmosphere".
            data_path (str, optional): Path to a JSON file containing properties
                                       for the atmosphere (e.g., color, radius,
                                       opacity). If None, default properties are used.
                                       Defaults to None.
        """
        self.name = name # Default name, can be overridden by load_data
        self.actor = None # Holds the vtkActor for this atmosphere
        self.data_path = data_path

        # Initialize attributes for custom properties, to be loaded from JSON
        self.custom_color = None
        self.custom_radius = None
        self.custom_opacity = None

        # Load data if data_path is provided
        if self.data_path:
            self.load_data()
        
        # Print after attempting to load data, so self.name might be updated
        print(f"Atmosphere component '{self.name}' initialized.")


    def load_data(self):
        """
        Loads atmosphere properties from the JSON file specified in `self.data_path`.

        If the file is found and valid, it updates `self.name`, `self.custom_color`,
        `self.custom_radius`, and `self.custom_opacity` with values from the JSON.
        Includes error handling for file not found, JSON parsing errors, and
        basic data type validation for the loaded properties. If loading fails or
        a property is invalid, a message is printed, and the affected property
        will remain None (causing fallback to defaults in `render`).
        """
        if not self.data_path:
            print(f"No data path provided for Atmosphere '{self.name}', using defaults.")
            return

        if not os.path.exists(self.data_path):
            print(f"Data file not found: {self.data_path} for Atmosphere '{self.name}'. Using defaults.")
            return

        try:
            with open(self.data_path, 'r') as f:
                data = json.load(f)
            
            self.name = data.get("name", self.name) # Update name from JSON if present
            self.custom_color = data.get("color")
            self.custom_radius = data.get("radius")
            self.custom_opacity = data.get("opacity")
            
            # Basic validation for loaded data types
            if self.custom_color and not (isinstance(self.custom_color, list) and len(self.custom_color) == 3):
                print(f"Warning: Invalid color format in {self.data_path}. Must be a list of 3 numbers. Using default.")
                self.custom_color = None
            if self.custom_radius and not isinstance(self.custom_radius, (int, float)):
                print(f"Warning: Invalid radius format in {self.data_path}. Must be a number. Using default.")
                self.custom_radius = None
            if self.custom_opacity and not isinstance(self.custom_opacity, (int, float)):
                print(f"Warning: Invalid opacity format in {self.data_path}. Must be a number. Using default.")
                self.custom_opacity = None

            print(f"Atmosphere data loaded from {self.data_path} for '{self.name}'.")
            if self.custom_radius is not None: print(f"  - Loaded radius: {self.custom_radius}")
            if self.custom_color is not None: print(f"  - Loaded color: {self.custom_color}")
            if self.custom_opacity is not None: print(f"  - Loaded opacity: {self.custom_opacity}")

        except json.JSONDecodeError:
            print(f"Error decoding JSON from {self.data_path} for Atmosphere '{self.name}'. Using defaults.")
        except Exception as e:
            print(f"An error occurred while loading data for Atmosphere '{self.name}': {e}. Using defaults.")

    def render(self, vtk_renderer):
        """
        Renders the atmosphere as a large, semi-transparent sphere in the VTK scene.

        If an existing actor for this atmosphere is present in the renderer, it is
        removed and replaced. The sphere's properties (radius, color, opacity)
        are taken from loaded data (`self.custom_...` attributes) if available and valid,
        otherwise, predefined default values are used.

        Args:
            vtk_renderer (vtk.vtkRenderer): The VTK renderer to add the atmosphere actor to.
        """
        if self.actor is not None:
            vtk_renderer.RemoveActor(self.actor)
            self.actor = None

        # Use loaded properties or fall back to defaults
        radius = self.custom_radius if self.custom_radius is not None else 15.0
        color = self.custom_color if self.custom_color is not None else [0.53, 0.81, 0.92] # LightSkyBlue
        opacity = self.custom_opacity if self.custom_opacity is not None else 0.3

        print(f"Rendering Atmosphere: {self.name} (Radius: {radius}, Color: {color}, Opacity: {opacity})")

        sphere_source = vtk.vtkSphereSource()
        sphere_source.SetRadius(radius)
        sphere_source.SetPhiResolution(32)
        sphere_source.SetThetaResolution(32)
        sphere_source.Update()

        mapper = vtk.vtkPolyDataMapper()
        mapper.SetInputConnection(sphere_source.GetOutputPort())

        self.actor = vtk.vtkActor()
        self.actor.SetMapper(mapper)

        prop = self.actor.GetProperty()
        prop.SetColor(color[0], color[1], color[2])
        prop.SetOpacity(opacity)

        vtk_renderer.AddActor(self.actor)
        print(f"Atmosphere actor for '{self.name}' added to the renderer.")

    def remove(self, vtk_renderer):
        """
        Removes the atmosphere's VTK actor from the specified renderer.

        If the actor exists (i.e., `self.actor` is not None), it is removed
        from the renderer, and `self.actor` is set to None.

        Args:
            vtk_renderer (vtk.vtkRenderer): The VTK renderer from which to remove
                                           the atmosphere actor.
        """
        if self.actor is not None:
            vtk_renderer.RemoveActor(self.actor)
            self.actor = None
            print(f"Atmosphere actor for '{self.name}' removed from the renderer.")
