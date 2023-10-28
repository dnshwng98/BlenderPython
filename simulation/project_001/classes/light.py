import bpy


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