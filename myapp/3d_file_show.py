import vtk

# Create a reader to read the .obj file 
reader = vtk.vtkOBJReader()
reader.SetFileName("myapp\\static\\building_model.obj")
reader.Update()

# Create a mapper
mapper = vtk.vtkPolyDataMapper()
mapper.SetInputConnection(reader.GetOutputPort())

# Create an actor
actor = vtk.vtkActor()
actor.SetMapper(mapper)

# Apply shading properties to the actor (for material)
actor.GetProperty().SetColor(1, 1, 1)  # Default to white if no colors are loaded
actor.GetProperty().SetDiffuse(0.8)  # Diffuse reflection (how much light scatters)
actor.GetProperty().SetSpecular(0.5)  # Specular reflection (how shiny the surface is)
actor.GetProperty().SetSpecularPower(30)  # Shininess

# Create a renderer, render window, and interactor
renderer = vtk.vtkRenderer()
render_window = vtk.vtkRenderWindow()
render_window.AddRenderer(renderer)
render_window_interactor = vtk.vtkRenderWindowInteractor()
render_window_interactor.SetRenderWindow(render_window)

# Add the actor to the scene
renderer.AddActor(actor)
renderer.SetBackground(0.1, 0.1, 0.1)  # Background color dark gray

# Create a light source (to properly show material and textures)
light = vtk.vtkLight()
light.SetPosition(1, 1, 1)
light.SetFocalPoint(0, 0, 0)
renderer.AddLight(light)

# Render and interact
render_window.Render()
render_window_interactor.Start()