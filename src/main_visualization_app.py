import vtk
from visualization import Atmosphere, WaterBody, Ecosystem # src.visualization should be in PYTHONPATH

def main():
    # --- VTK Setup ---
    # Create a renderer
    renderer = vtk.vtkRenderer()
    renderer.SetBackground(0.1, 0.2, 0.4)  # Dark blue background

    # Create a render window
    render_window = vtk.vtkRenderWindow()
    render_window.AddRenderer(renderer)
    render_window.SetSize(1000, 800)
    render_window.SetWindowName("Main Visualization Application")

    # Create a render window interactor
    render_window_interactor = vtk.vtkRenderWindowInteractor()
    render_window_interactor.SetRenderWindow(render_window)
    render_window_interactor.SetInteractorStyle(vtk.vtkInteractorStyleTrackballCamera())

    print("--- VTK Setup Complete ---")

    # --- Instantiate Visualization Components ---
    print("\n--- Initializing Visualization Components ---")
    atmosphere_component = Atmosphere(name="GlobalAtmosphereLayer")
    water_component = WaterBody(name="ArcticOcean")
    ecosystem_component = Ecosystem(name="AmazonRainforest")
    print("--- Visualization Components Initialized ---")

    # --- Call Render Methods ---
    # In a real application, these render methods would add VTK actors to the renderer.
    # For now, they will just print messages.
    print("\n--- Calling Render Methods ---")
    atmosphere_component.render(renderer)
    water_component.render(renderer)
    ecosystem_component.render(renderer)
    print("--- Render Methods Called ---")

    # --- Start VTK Visualization ---
    print("\n--- Starting VTK Interactor ---")
    print("A VTK window should appear. Close it to exit the application.")
    render_window.Render()
    render_window_interactor.Initialize()
    render_window_interactor.Start()
    print("--- VTK Interactor Stopped ---")

if __name__ == "__main__":
    print("Executing main_visualization_app.py")
    # Add current directory to python path to allow imports from src.visualization
    # This is often handled by IDEs or by setting PYTHONPATH environment variable
    import sys
    import os
    # Assuming the script is run from the root of the project or inside src
    # Adjust if necessary. If run from /app (root), 'src' needs to be in path.
    # If run from /app/src, '.' (current dir) needs to be in path for 'visualization'.
    # For `python src/main_visualization_app.py` from `/app`:
    sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))


    main()
    print("main_visualization_app.py finished.")
