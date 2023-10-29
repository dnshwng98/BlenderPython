import bpy
from .animation import Animation
from .material import Material


class Particle:
    def __init__(self, speed, location, rotation, scale, material_name):
        self.speed = speed
        self.location = location
        self.rotation = rotation
        self.scale = scale
        self.material = Material.register_material(material_name)

    def update_state(self):
        bpy.context.view_layer.objects.active = bpy.data.objects[self.name]
        self.state = bpy.context.active_object
        self.state.location = self.location
        self.state.rotation_euler = self.rotation
        
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

class Cube(Particle):
    def __init__(self, name, size, *args, **kwargs) -> None:
        super(Cube, self).__init__(*args, **kwargs, material_name = name)
        self.name = name
        self.size = size
        bpy.ops.mesh.primitive_cube_add(size = self.size, enter_editmode = False, align = 'WORLD',
                                        location = self.location, rotation = self.rotation, scale = self.scale)
        self.state = bpy.context.active_object
        self.state.name = self.name
        self.state.data.materials.append(self.material)

class Plane(Particle):
    def __init__(self, name, size, *args, **kwargs):
        super(Plane, self).__init__(*args, **kwargs, material_name = name)
        self.name = name
        self.size = size
        bpy.ops.mesh.primitive_plane_add(size = self.size, enter_editmode = False, align = 'WORLD',
                                        location = self.location, rotation = self.rotation, scale = self.scale)
        self.state = bpy.context.active_object
        self.state.name = self.name
        self.state.data.materials.append(self.material)