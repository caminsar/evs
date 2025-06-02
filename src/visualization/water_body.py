"""
Defines the WaterBody class for visualizing a body of water.

This module provides the `WaterBody` class, which is responsible for creating
and managing a 3D representation of a water surface (typically a flat plane)
in a VTK scene.
"""
import vtk

class WaterBody:
    """
    Represents a water body (e.g., ocean, lake) in the visualization.

    This class handles the creation of a flat plane VTK actor to represent
    a water surface. Its properties (like color and size) are currently
    defined by default values within the class.
    """
    def __init__(self, name="DefaultWaterBody"):
        """
        Initializes the WaterBody object.

        Args:
            name (str, optional): The name for this water body instance.
                                  Defaults to "DefaultWaterBody".
        """
        self.name = name
        self.actor = None # Holds the vtkActor for this water body
        print(f"WaterBody component '{self.name}' initialized.")

    def render(self, vtk_renderer):
        """
        Renders the water body as a flat blue plane in the VTK scene.

        If an existing actor for this water body is present, it is removed and
        replaced. The plane's size and color are set to predefined default values.

        Args:
            vtk_renderer (vtk.vtkRenderer): The VTK renderer to add the water body
                                           actor to.
        """
        # If an old actor exists, remove it first
        if self.actor is not None:
            vtk_renderer.RemoveActor(self.actor)
            self.actor = None

        print(f"Rendering WaterBody: {self.name} with actual VTK plane.")

        # Create a plane source to represent a flat water surface
        plane_source = vtk.vtkPlaneSource()
        # Defines a 20x20 unit plane on the Z=0 plane
        plane_source.SetOrigin(-10.0, -10.0, 0.0)
        plane_source.SetPoint1(10.0, -10.0, 0.0)
        plane_source.SetPoint2(-10.0, 10.0, 0.0)
        
        plane_source.SetXResolution(20) # Number of cells in X direction
        plane_source.SetYResolution(20) # Number of cells in Y direction
        plane_source.Update()

        # Create a mapper for the plane source
        mapper = vtk.vtkPolyDataMapper()
        mapper.SetInputConnection(plane_source.GetOutputPort())

        # Create an actor for the mapper
        self.actor = vtk.vtkActor()
        self.actor.SetMapper(mapper)

        # Set appearance properties
        prop = self.actor.GetProperty()
        prop.SetColor(0.1, 0.3, 0.7)  # A shade of blue for water

        # Add the actor to the renderer
        vtk_renderer.AddActor(self.actor)
        print(f"WaterBody actor for '{self.name}' added to the renderer.")

    def remove(self, vtk_renderer):
        """
        Removes the water body's VTK actor from the specified renderer.

        If the actor exists (i.e., `self.actor` is not None), it is removed
        from the renderer, and `self.actor` is set to None.

        Args:
            vtk_renderer (vtk.vtkRenderer): The VTK renderer from which to remove
                                           the water body actor.
        """
        if self.actor is not None:
            vtk_renderer.RemoveActor(self.actor)
            self.actor = None
            print(f"WaterBody actor for '{self.name}' removed from the renderer.")
