import bpy, math, random


# Deleting all objects in the scene.
# This step is to prevent the creation of the same object every time the script is run.
bpy.ops.object.select_all(action = 'SELECT')
bpy.ops.object.delete(use_global = False)

# Create a camera.
# This is the object that will capture the image or animation.
camera_x_degrees = 90
camera_x_radians = math.radians(camera_x_degrees)
bpy.ops.object.camera_add(enter_editmode = False, align = 'VIEW', location = (0, 4, 0),
                            rotation = (camera_x_radians, 0, 0))

# Create a light of type Point.
bpy.ops.object.light_add(type = 'POINT', align = 'WORLD', location = (0, 6, 3), scale = (1, 1, 1))
bpy.context.view_layer.objects.active = bpy.data.objects["Point"]
point = bpy.context.active_object
point.data.energy = 5

# Create a plane.
# It will be used as a still backdrop.
backdrop_x_degrees = 90
backdrop_x_radians = math.radians(backdrop_x_degrees)
bpy.ops.mesh.primitive_plane_add(size = 5, enter_editmode = False, align = 'WORLD', location = (0, 10, 0), 
                                rotation = (backdrop_x_radians, 0, 0), scale = (1, 1, 1))                
backdrop_material = bpy.data.materials.get("Backdrop")

if backdrop_material == None:
    backdrop_material = bpy.data.materials.new(name = "Backdrop")
    
backdrop_material.use_nodes = True
backdrop_material.node_tree.nodes['Principled BSDF'].inputs[0].default_value = (40, 10, 11, 1)

bpy.context.view_layer.objects.active = bpy.data.objects["Plane"]
backdrop = bpy.context.active_object
backdrop.data.materials.append(backdrop_material)
                                
# Create cubes.
# These are the object that will be animated.
cube = None
for i in range(22):
    bpy.ops.mesh.primitive_cube_add(size = 1, enter_editmode = False, align = 'WORLD',location = (-2 + (i * 0.1904), 9, 0),
                                    scale = (.1, .1, .1))
                                        
    if i == 0:
        bpy.context.view_layer.objects.active = bpy.data.objects["Cube"]
    else:
        if len(str(i)) > 1:
            bpy.context.view_layer.objects.active = bpy.data.objects["Cube.0" + str(i)]
        else:
            bpy.context.view_layer.objects.active = bpy.data.objects["Cube.00" + str(i)]
            
    cube = bpy.context.active_object
    cube_material = bpy.data.materials.get("Cube")

    if cube_material == None:
        cube_material = bpy.data.materials.new(name = "Cube")
    
    cube_material.use_nodes = True
    cube_material.node_tree.nodes['Principled BSDF'].inputs[0].default_value = (50, 0, 0, 1)
    cube.data.materials.append(cube_material)
    
# Create spheres.
# These are the object that will be animated.
for i in range(51):
    rand_x = random.uniform(-2, 2.1)
    rand_z = random.uniform(-1, 1.1)
    bpy.ops.mesh.primitive_uv_sphere_add(radius = 1, enter_editmode = False, align = 'WORLD',location = (rand_x, 9.5, rand_z),
                                    scale = (.1, .1, .1))
                                        
    if i == 0:
        bpy.context.view_layer.objects.active = bpy.data.objects["Sphere"]
    else:
        if len(str(i)) > 1:
            bpy.context.view_layer.objects.active = bpy.data.objects["Sphere.0" + str(i)]
        else:
            bpy.context.view_layer.objects.active = bpy.data.objects["Cube.00" + str(i)]

# Animate cubes
for i in range(22):
    if i == 0:
        bpy.context.view_layer.objects.active = bpy.data.objects["Cube"]
    else:
        if len(str(i)) > 1:
            bpy.context.view_layer.objects.active = bpy.data.objects["Cube.0" + str(i)]
        else:
            bpy.context.view_layer.objects.active = bpy.data.objects["Cube.00" + str(i)]
            
    cube = bpy.context.active_object
    
    # Set the initial data of Cube.
    # In this context, we initialize the starting point of Cube.
    cube.location.z = -1

    # Insert a keyframe for the initial state of Cube.
    start_keyframe = 0
    cube.keyframe_insert("location", frame = start_keyframe)
    cube.keyframe_insert("rotation_euler", frame = start_keyframe)

    # Update Cube data.
    # In this context, we change the state of Cube.
    cube.location.z = 1
    cube.rotation_euler = (math.radians(180), math.radians(180), math.radians(180))

    # Insert another keyframe.
    # By doing this process we link this keyframe to the state of Cube we just updated
    mid_keyframe = 75 + (i * 2)
    cube.keyframe_insert("location", frame = mid_keyframe)
    cube.keyframe_insert("rotation_euler", frame = mid_keyframe)

    cube.location.z = -1
    cube.rotation_euler = (math.radians(360), math.radians(360), math.radians(360))

    end_keyframe = 150
    cube.keyframe_insert("location", frame = end_keyframe)
    cube.keyframe_insert("rotation_euler", frame = end_keyframe)

# Animate spheres
sphere = None
for i in range(51):
    if i == 0:
        bpy.context.view_layer.objects.active = bpy.data.objects["Sphere"]
    else:
        if len(str(i)) > 1:
            bpy.context.view_layer.objects.active = bpy.data.objects["Sphere.0" + str(i)]
        else:
            bpy.context.view_layer.objects.active = bpy.data.objects["Sphere.00" + str(i)]
            
    sphere = bpy.context.active_object
    sphere_material = bpy.data.materials.get("Sphere" + str(i))

    if sphere_material == None:
        sphere_material = bpy.data.materials.new(name = "Sphere" + str(i))
        
    sphere.data.materials.append(sphere_material)
    
    sphere.scale = (.1, .1, .1)
    sphere_material.use_nodes = True
    sphere_material.node_tree.nodes['Principled BSDF'].inputs[0].default_value = (0, 0, 0, 1)
    sphere_material.node_tree.nodes['Principled BSDF'].inputs[9].default_value = 1
    start_keyframe = 0
    sphere.keyframe_insert("scale", frame = start_keyframe)
    sphere_material.node_tree.nodes['Principled BSDF'].inputs[0].keyframe_insert("default_value", frame = start_keyframe)
    
    sphere.scale = (.5, .5, .5)
    sphere_material.node_tree.nodes['Principled BSDF'].inputs[0].default_value = (random.randint(0, 51), random.randint(0, 51), 
                                                                                random.randint(0, 51), 1)
    sphere_material.node_tree.nodes['Principled BSDF'].inputs[9].default_value = 1
    mid_keyframe = 75 + i
    sphere.keyframe_insert("scale", frame = mid_keyframe)
    sphere_material.node_tree.nodes['Principled BSDF'].inputs[0].keyframe_insert("default_value", frame = mid_keyframe)
    
    sphere.scale = (.1, .1, .1)
    sphere_material.node_tree.nodes['Principled BSDF'].inputs[0].default_value = (0, 0, 0, 1)
    sphere_material.node_tree.nodes['Principled BSDF'].inputs[9].default_value = 1
    end_keyframe = 150
    sphere.keyframe_insert("scale", frame = end_keyframe)
    sphere_material.node_tree.nodes['Principled BSDF'].inputs[0].keyframe_insert("default_value", frame = end_keyframe)
    
bpy.context.scene.cycles.glossy_bounces = 4
