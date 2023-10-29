import bpy


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