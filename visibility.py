import bpy

def visibility(objects, is_hide):
    for ob in objects:
        ob.hide = ob.hide_render = is_hide
        ob.keyframe_insert(data_path = "hide")
        ob.keyframe_insert(data_path = "hide_render")

objects = bpy.context.selected_objects
visibility(objects, True)
