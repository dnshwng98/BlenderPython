class Animation:
    @classmethod
    def orientation(cls, object, data_paths, keyframe):
        for data_path in data_paths:
            object.state.keyframe_insert(data_path, frame = keyframe)
    
    @classmethod
    def base_color(cls, object, data_paths, keyframe):
        for data_path in data_paths:
            object.material.node_tree.nodes['Principled BSDF'].inputs[0].keyframe_insert(data_path, frame = keyframe)
