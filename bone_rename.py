import bpy

bones_names_lookup = {
    "old_name":"new_name",
    "Bone.001":"Bone.one",
    "Bone.002":"Bone.two",
    }

objects = [obj for obj in bpy.context.selected_objects if obj.type == 'ARMATURE']
for obj in objects:
    armature_name = obj.name

    for bone in obj.data.bones:
        new_name = bones_names_lookup.get(bone.name)
        if new_name:
            print("{0} > {1} renamed to {2}".format(armature_name, bone.name, new_name))
            bone.name = new_name
