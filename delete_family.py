# ########################################
#
# Delete all the objects relative to the
# selected objects (children and parents)
#
# Reference documentation:
# http://www.blender.org/documentation/
#    blender_python_api_2_68_release/bpy.ops.html
#    #overriding-context
#
#
# CODE SAMPLE, SNIPPETS FOR MY OWN REFERENCE
# NO COPYRIGHT APPLIES
#
# Dalai Felinto
#
# dalaifelinto.com
# Rio de Janeiro, October 2013
#
# ########################################

import bpy


def get_children(object):
    """
    returns all the children of the object
    recursively
    """
    objects = []
    for child in object.children:
        objects.append(child)
        objects.extend(get_children(child))

    return objects


def get_parent(object):
    """
    returns the top parent of the object
    """
    if object.parent:
        return get_parent(object.parent)
    else:
        return object


class OBJECT_OT_DeleteFamily(bpy.types.Operator):
    """Tooltip"""
    bl_idname = "object.delete_family"
    bl_label = "Delete All Related Objects"

    @classmethod
    def poll(cls, context):
        return context.active_object is not None

    def execute(self, context):
        scene = context.scene

        parents = []
        # collect all parents
        for object in context.selected_objects:
            parents.append(get_parent(object))

        # remove duplicates
        parents = list(set(parents))
        family = parents[:]

        # collect all children
        for parent in parents:
            family.extend(get_children(parent))

        family_base = []
        # we need the object base
        for object in family:
            family_base.append(scene.object_bases[object.name])

        # delete the objects
        override = context.copy()
        override['selected_bases'] = family_base
        bpy.ops.object.delete(override)

        return {'FINISHED'}


def register():
    bpy.utils.register_class(OBJECT_OT_DeleteFamily)


def unregister():
    bpy.utils.unregister_class(OBJECT_OT_DeleteFamily)


if __name__ == "__main__":
    register()

    # test call
    bpy.ops.object.delete_family()

