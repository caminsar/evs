"""
A simple standalone VTK example script.

This script demonstrates the basic steps to create a 3D scene using VTK:
1. Create a source object (a sphere in this case).
2. Create a mapper to map the geometric data to graphics primitives.
3. Create an actor to represent the object in the scene (with properties like color).
4. Create a renderer to manage the scene.
5. Create a render window to display the scene.
6. Create a render window interactor to handle user interaction (mouse, keyboard).

This example renders a single sphere with a light blue background.
It serves as a basic test and illustration of VTK usage.
"""
import vtk

def main():
    """
    Sets up and displays a simple VTK scene with a 3D sphere.

    The sphere is rendered in a window with a light blue background.
    The window remains open until manually closed by the user.
    """
    # Create a sphere source
    sphere_source = vtk.vtkSphereSource()
    sphere_source.SetCenter(0.0, 0.0, 0.0)
    sphere_source.SetRadius(5.0)
    sphere_source.SetPhiResolution(100)  # Higher resolution for a smoother sphere
    sphere_source.SetThetaResolution(100)

    # Create a mapper to convert the sphere data to graphics primitives
    mapper = vtk.vtkPolyDataMapper()
    mapper.SetInputConnection(sphere_source.GetOutputPort())

    # Create an actor to represent the sphere in the scene
    actor = vtk.vtkActor()
    actor.SetMapper(mapper)
    # Note: Default color for actor is often white.

    # Create a renderer to manage the actors and camera
    renderer = vtk.vtkRenderer()
    renderer.AddActor(actor)
    # Set background color to light blue (LightSkyBlue)
    renderer.SetBackground(0.53, 0.81, 0.92)

    # Create a render window to host the renderer
    render_window = vtk.vtkRenderWindow()
    render_window.AddRenderer(renderer)
    render_window.SetSize(800, 600)
    render_window.SetWindowName("VTK Sphere Example")

    # Create a render window interactor to handle user inputs (mouse interaction)
    render_window_interactor = vtk.vtkRenderWindowInteractor()
    render_window_interactor.SetRenderWindow(render_window)
    # Default interactor style is vtkInteractorStyleTrackballCamera

    # Initialize the interactor and start the rendering loop
    render_window.Render()  # Initial render
    render_window_interactor.Initialize() # Prepare for interaction
    render_window_interactor.Start()      # Start event loop (blocks until window closed)

if __name__ == "__main__":
    main()
