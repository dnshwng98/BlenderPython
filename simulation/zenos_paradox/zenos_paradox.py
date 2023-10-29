import sys
sys.path.insert(0, "C:\Projects\Python\BlenderPython\simulation")

from zenos_paradox.classes.camera import Camera
from zenos_paradox.classes.light import Point
from zenos_paradox.classes.particle import Cube, Plane
import bpy, math

# Deleting all objects in the scene.
# This step is to prevent the creation of the same object every time the script is run.
bpy.ops.object.select_all(action = 'SELECT')
bpy.ops.object.delete(use_global = False)

# Create camera.
# This is the object that will capture the image or animation.
camera_a_x_degrees = 90
camera_a_x_radians = math.radians(camera_a_x_degrees)
camera_a_z_degrees = 270
camera_a_z_radians = math.radians(camera_a_z_degrees)
camera_a = Camera((-2, 0, .1), (camera_a_x_radians, 0, camera_a_z_radians), "CameraA")

camera_a.state.keyframe_insert("location", frame = 0)
camera_a.state.keyframe_insert("rotation_euler", frame = 0)

camera_a.location = ((8, 0, .1))
camera_a.update_state()
camera_a.state.keyframe_insert("location", frame = 37.5)
camera_a.state.keyframe_insert("rotation_euler", frame = 37.5)

camera_a.location = ((10.5, 0, 1))
camera_a.rotation = ((math.radians(35), 0, camera_a.rotation[2]))
camera_a.update_state()
camera_a.state.keyframe_insert("location", frame = 75)
camera_a.state.keyframe_insert("rotation_euler", frame = 75)

camera_a.location = ((11.1, 0, 1))
camera_a.rotation = ((math.radians(0), 0, camera_a.rotation[2]))
camera_a.update_state()
camera_a.state.keyframe_insert("location", frame = 112.5)
camera_a.state.keyframe_insert("rotation_euler", frame = 112.5)

camera_a.location = ((11.2, .1, .3))
camera_a.rotation = ((math.radians(0), 0, camera_a.rotation[2]))
camera_a.update_state()
camera_a.state.keyframe_insert("location", frame = 150)
camera_a.state.keyframe_insert("rotation_euler", frame = 150)


# Create light of type Point.
light_a = Point(.2, 'POINT', (5, 0, 5), "LightA")
light_a.power = 1000
light_a.update_state()

# Create a plane.
# It will be used as a ground.
groud_a_x_degrees = 0
ground_a_x_radians = math.radians(groud_a_x_degrees)
ground_a = Plane("GroundA", 30, 0, (0, 0, 0), (ground_a_x_radians, 0, 0), (1, 1, 1)) 

ground_a.update_material_base_color((0.793802, 0.125434, 0.394829, 1))

# Defining particles with initial position(in metric units)
cube_a = Cube("CubeA", 1, 1, (10.05, 0, .1), (0, 0, 0), (.1, .1, .1))
cube_a.update_material_base_color((50, 50, 0, 1))
data_paths = [{"orientation": ("location", "rotation_euler")}]
cube_a.insert_keyframe(data_paths, 0)

cube_b = Cube("CubeB", 1, 10, (0, 0, .1), (0, 0, 0), (.1, .1, .1))
cube_b.update_material_base_color((50, 0, 0, 1))
cube_b.insert_keyframe(data_paths, 0)

for index in range(1, 5):
    # Phase 1.
    # Calculating Particle B's time to approach Particle A's position
    cube_a_dimension = bpy.data.objects[cube_a.name].dimensions
    cube_b_dimension = bpy.data.objects[cube_b.name].dimensions
    cube_b_time = ((cube_a.location[0] - cube_a_dimension[0] / 2) - (cube_b.location[0] + cube_b_dimension[0] / 2)) / cube_b.speed
    cube_b.location = (float(f"{cube_a.location[0] - cube_a_dimension[0] / 2 - cube_b_dimension[0] / 2:.4f}"), 0, .1)
    cube_b.rotation = (math.radians(720) * index, 0, 0)
    cube_b.update_state()
    cube_b.insert_keyframe(data_paths, index * 37.5)

    # Phase 2.
    # At this phase, Particle B is already at Particle A'previous location
    # Now, let's calculate and update Particle A's current location
    cube_a.location = (float(f"{cube_a.location[0] + cube_b_time * cube_a.speed:.4f}"), 0, .1)
    cube_a.update_state()
    cube_a.insert_keyframe(data_paths, index * 37.5)
