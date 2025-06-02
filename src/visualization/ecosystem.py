"""
Defines the Ecosystem class for visualizing a patch of land or vegetation.

This module provides the `Ecosystem` class, responsible for creating and
managing a 3D representation of a terrestrial ecosystem (typically a flat,
green plane) in a VTK scene.
"""
import vtk

class Ecosystem:
    """
    Represents an ecosystem (e.g., forest, desert, grassland) in the visualization.

    This class handles the creation of a flat plane VTK actor to represent a
    patch of land or vegetation. Its properties (like color and size) are
    currently defined by default values within the class. It is typically rendered
    slightly above the Z=0 plane to avoid Z-fighting with water bodies.
    """
    def __init__(self, name="DefaultEcosystem"):
        """
        Initializes the Ecosystem object.

        Args:
            name (str, optional): The name for this ecosystem instance.
                                  Defaults to "DefaultEcosystem".
        """
        self.name = name
        self.actor = None # Holds the vtkActor for this ecosystem
        print(f"Ecosystem component '{self.name}' initialized.")

    def render(self, vtk_renderer):
        """
        Renders the ecosystem as a flat green plane in the VTK scene.

        If an existing actor for this ecosystem is present, it is removed and
        replaced. The plane's size, position (slightly above Z=0), and color
        are set to predefined default values.

        Args:
            vtk_renderer (vtk.vtkRenderer): The VTK renderer to add the ecosystem
                                           actor to.
        """
        # If an old actor exists, remove it first
        if self.actor is not None:
            vtk_renderer.RemoveActor(self.actor)
            self.actor = None

        print(f"Rendering Ecosystem: {self.name} with actual VTK plane.")

        # Create a plane source to represent a patch of land/vegetation
        plane_source = vtk.vtkPlaneSource()
        # Set Z to 0.1 to be slightly above a potential water plane at Z=0, preventing Z-fighting
        z_level = 0.1
        # Defines a 16x16 unit plane
        plane_source.SetOrigin(-8.0, -8.0, z_level)
        plane_source.SetPoint1(8.0, -8.0, z_level)
        plane_source.SetPoint2(-8.0, 8.0, z_level)
        
        plane_source.SetXResolution(10) # Number of cells in X
        plane_source.SetYResolution(10) # Number of cells in Y
        plane_source.Update()

        # Create a mapper for the plane source
        mapper = vtk.vtkPolyDataMapper()
        mapper.SetInputConnection(plane_source.GetOutputPort())

        # Create an actor for the mapper
        self.actor = vtk.vtkActor()
        self.actor.SetMapper(mapper)

        # Set appearance properties
        prop = self.actor.GetProperty()
        prop.SetColor(0.0, 0.6, 0.2)  # A shade of green for vegetation/land

        # Add the actor to the renderer
        vtk_renderer.AddActor(self.actor)
        print(f"Ecosystem actor for '{self.name}' added to the renderer.")

    def remove(self, vtk_renderer):
        """
        Removes the ecosystem's VTK actor from the specified renderer.

        If the actor exists (i.e., `self.actor` is not None), it is removed
        from the renderer, and `self.actor` is set to None.

        Args:
            vtk_renderer (vtk.vtkRenderer): The VTK renderer from which to remove
                                           the ecosystem actor.
        """
        if self.actor is not None:
            vtk_renderer.RemoveActor(self.actor)
            self.actor = None
            print(f"Ecosystem actor for '{self.name}' removed from the renderer.")
