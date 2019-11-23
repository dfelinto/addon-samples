import bpy


def create_action_modifier(fcurve, frame_offset):
    if fcurve.data_path[-5:] not in {'ation', 'scale'}:
        return

    modifier = fcurve.modifiers.new('STEPPED')
    modifier.frame_offset = frame_offset
    return modifier


for ob in bpy.context.selected_objects:
    if not ob.animation_data:
        continue
    
    if not ob.animation_data.action:
        continue

    for fcurve in ob.animation_data.action.fcurves:
        #while fcurve.modifiers:
        #    fcurve.modifiers.remove(fcurve.modifiers[0])
        create_action_modifier(fcurve, 3)
