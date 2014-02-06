# ########################################
#
# Populates the ENUM of an operator dynamically
# (and focus the view in the selected object)
#
# CODE SAMPLE, SNIPPETS FOR MY OWN REFERENCE
# NO COPYRIGHT APPLIES
#
# Dalai Felinto
#
# dalaifelinto.com
# Rio de Janeiro, February 2014
#
# ########################################

import bpy

def items_dynamic(self, context):
    names = {object.name: object.name for object in context.scene.objects}
    return [(name, name.title(), "") for name in names]


class OBJECT_OT_Focus(bpy.types.Operator):
    ''''''
    bl_idname = "object.focus"
    bl_label = "Object Focus"
    bl_description = "Select Object for Focus View"

    object = bpy.props.EnumProperty(
        name="Object",
        description= "",
        items=items_dynamic,
        )

    def execute(self, context):
        self.report({'INFO'}, "Selected: \"{0}\"".format(self.object))

        object = context.scene.objects[self.object]

        if bpy.ops.object.select_all.poll():
            bpy.ops.object.select_all(action='DESELECT')

        object.select = True
        if bpy.ops.view3d.view_selected.poll():
            return bpy.ops.view3d.view_selected()

        return {'CANCELLED'}

    def invoke(self, context, event):
        wm = context.window_manager
        return wm.invoke_props_dialog(self)


def register():
    bpy.utils.register_class(OBJECT_OT_Focus)


def unregister():
    bpy.utils.unregister_class(OBJECT_OT_Focus)


if __name__ == "__main__":
    register()

    # test call
    bpy.ops.object.focus()
