import bpy


class Material:
    @classmethod
    def register_material(cls, material_name):
        material = bpy.data.materials.get(material_name)

        if material == None:
            material = bpy.data.materials.new(name = material_name)
    
        material.use_nodes = True
        
        return material