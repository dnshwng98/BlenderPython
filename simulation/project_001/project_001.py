import bpy, math, random
from simulation.project_001.classes.camera import Camera
from simulation.project_001.classes.light import Point
from simulation.project_001.classes.mesh import Plane, Cube, Sphere

    
# Deleting all objects in the scene.
# This step is to prevent the creation of the same object every time the script is run.
bpy.ops.object.select_all(action = 'SELECT')
bpy.ops.object.delete(use_global = False)

# Create camera.
# This is the object that will capture the image or animation.
camera_a_x_degrees = 90
camera_a_x_radians = math.radians(camera_a_x_degrees)
camera_a = Camera((0, 3.1, 0), (camera_a_x_radians, 0, 0), "CameraA")

camera_a.state.keyframe_insert("location", frame = 0)
camera_a.state.keyframe_insert("rotation_euler", frame = 0)

camera_a.location = ((0, 7, 0))
camera_a_y_degrees = 180
camera_a_y_radians = math.radians(camera_a_y_degrees)
camera_a.rotation = ((camera_a_x_radians, camera_a_y_radians, 0))
camera_a.update_state()

camera_a.state.keyframe_insert("location", frame = 150)
camera_a.state.keyframe_insert("rotation_euler", frame = 150)

# Create light of type Point.
light_a = Point(.3, 'POINT', (0, 6, 3), "LightA")
light_a.power = 200
light_a.update_state()

# Create a plane.
# It will be used as a still backdrop.
backdrop_a_x_degrees = 90
backdrop_a_x_radians = math.radians(backdrop_a_x_degrees)
backdrop_a = Plane("BackdropA", 6, (0, 10, 0), (backdrop_a_x_radians, 0, 0), (1, 1, 1)) 

backdrop_a.update_material_base_color((0.793802, 0.125434, 0.394829, 1))
                                
# Create cubes and animate.
for i in range(22):
    cube = Cube("Cube" + str(i), 1, (-2 + (i * 0.1904), 9, 0), (0, 0, 0), (.1, .1, .1))
    cube.update_material_base_color((50, 0, 0, 1))
    
    cube.state.location.z = -1
    data_paths = [{"orientation": ("location", "rotation_euler")}]
    cube.insert_keyframe(data_paths, 0)
    
    cube.state.location.z = 1
    cube.state.rotation_euler = (math.radians(180), math.radians(180), math.radians(180))
    cube.insert_keyframe(data_paths, 75 + (i * 2))
    
    cube.state.location.z = -1
    cube.state.rotation_euler = (math.radians(360), math.radians(360), math.radians(360))
    cube.insert_keyframe(data_paths, 150)
    
# Create spheres and animate.
for i in range(81):
    rand_x = random.uniform(-3, 3.1)
    rand_z = random.uniform(-2, 2.1)
    sphere = Sphere("Sphere" + str(i), 1, (rand_x, 9.5, rand_z), (0, 0, 0), (.1, .1, .1))
    
    sphere.state.scale = (.1, .1, .1)
    sphere.update_material_base_color((0, 0, 0, 1))
    sphere.update_material_roughness(1)
    data_paths = [{"orientation": ("scale",)}, {"base_color": ("default_value",)}]
    sphere.insert_keyframe(data_paths, 0)
    
    sphere.state.scale = (.5, .5, .5)
    sphere.update_material_base_color((random.randint(0, 51), random.randint(0, 51), random.randint(0, 51), 1))
    sphere.insert_keyframe(data_paths, 75 + 1)
    
    sphere.state.scale = (.1, .1, .1)
    sphere.update_material_base_color((0, 0, 0, 1))
    sphere.insert_keyframe(data_paths, 150)
