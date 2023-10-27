import bpy, math, random


class Camera:
    def __init__(self, location, rotation, name):
        self.location = location
        self.rotation = rotation
        self.name = name
        bpy.ops.object.camera_add(enter_editmode = False, align = 'VIEW', location = self.location,
                                    rotation = self.rotation)
        self.state = bpy.context.active_object
        self.state.name = self.name
                            
    def update_state(self):
        bpy.context.view_layer.objects.active = bpy.data.objects[self.name]
        self.state = bpy.context.active_object
        self.state.location = self.location
        self.state.rotation_euler = self.rotation
        
class Light:
    def __init__(self, type, location, name):
        self.type = type
        self.location = location
        self.name = name
        bpy.ops.object.light_add(type = type, align = 'WORLD', location = location)
        self.state = bpy.context.active_object
        self.state.name = self.name
        self.color = self.state.data.color
        self.power = self.state.data.energy
        self.max_bounces = self.state.data.cycles.max_bounces
        
    def update_state(self):
        raise NotImplementedError()
        
class Point(Light):
    def __init__(self, radius, *args, **kwargs):
        super(Point, self).__init__(*args, **kwargs)
        self.radius = radius
    
    def update_state(self):
        bpy.context.view_layer.objects.active = bpy.data.objects[self.name]
        self.state = bpy.context.active_object
        self.state.location = self.location
        self.state.data.color = self.color
        self.state.data.energy = self.power
        self.state.data.shadow_soft_size = self.radius
        self.state.data.cycles.max_bounces = self.max_bounces
        
class Material:
    @classmethod
    def register_material(cls, material_name):
        material = bpy.data.materials.get(material_name)

        if material == None:
            material = bpy.data.materials.new(name = material_name)
    
        material.use_nodes = True
        
        return material
    
class Animation:
    @classmethod
    def orientation(cls, object, data_paths, keyframe):
        for data_path in data_paths:
            object.state.keyframe_insert(data_path, frame = keyframe)
    
    @classmethod
    def base_color(cls, object, data_paths, keyframe):
        for data_path in data_paths:
            object.material.node_tree.nodes['Principled BSDF'].inputs[0].keyframe_insert(data_path, frame = keyframe)

class Mesh:
    def __init__(self, location, rotation, scale, material_name):
        self.location = location
        self.rotation = rotation
        self.scale = scale
        self.material = Material.register_material(material_name)
        
    def update_material_base_color(self, base_color):
        self.material.node_tree.nodes['Principled BSDF'].inputs[0].default_value = base_color
        
    def update_material_roughness(self, roughness):
        self.material.node_tree.nodes['Principled BSDF'].inputs[9].default_value = roughness
        
    def insert_keyframe(self, data_paths, keyframe):
        for data_path in data_paths:
            for key in data_path: 
                if key == Animation.orientation.__name__:
                    Animation.orientation(self, data_path[key], keyframe)
                elif key == Animation.base_color.__name__:
                    Animation.base_color(self, data_path[key], keyframe)
            
class Cube(Mesh):
    def __init__(self, name, size, *args, **kwargs):
        super(Cube, self).__init__(*args, **kwargs, material_name = "Cube")
        self.name = name
        self.size = size
        bpy.ops.mesh.primitive_cube_add(size = self.size, enter_editmode = False, align = 'WORLD', 
                                        location = self.location, rotation = self.rotation, scale = self.scale)
        self.state = bpy.context.active_object
        self.state.name = self.name
        self.state.data.materials.append(self.material)

class Sphere(Mesh):
    def __init__(self, name, radius, *args, **kwargs):
        super(Sphere, self).__init__(*args, **kwargs, material_name = name)
        self.name = name
        self.radius = radius
        bpy.ops.mesh.primitive_uv_sphere_add(radius = self.radius, enter_editmode = False, align = 'WORLD',
                                        location = self.location, rotation = self.rotation, scale = self.scale)
        self.state = bpy.context.active_object
        self.state.name = self.name
        self.state.data.materials.append(self.material)

class Plane(Mesh):
    def __init__(self, name, size, *args, **kwargs):
        super(Plane, self).__init__(*args, **kwargs, material_name = name)
        self.name = name
        self.size = size
        bpy.ops.mesh.primitive_plane_add(size = self.size, enter_editmode = False, align = 'WORLD',
                                        location = self.location, rotation = self.rotation, scale = self.scale)
        self.state = bpy.context.active_object
        self.state.name = self.name
        self.state.data.materials.append(self.material)

    
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
