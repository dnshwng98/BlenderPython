import bpy


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