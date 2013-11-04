import bpy

class OrganizerOperator(bpy.types.Operator):
    """Tooltip"""
    bl_idname = "object.organizer"
    bl_label = "Organize the Objects per Type"

    factor = bpy.props.FloatProperty(default=10.0)

    @classmethod
    def poll(cls, context):
        return context.active_object is not None

    def execute(self, context):
        factor = self.factor
        for object in context.selected_objects:
            if object.type == 'MESH':
                object.location[2] = 0.0 * factor
            elif object.type == 'CAMERA':
                object.location[2] = 2.0 * factor
            elif object.type == 'FONT':
                object.location = (0,0,0)
            else:
                object.location[2] = 1.0 * factor

        return {'FINISHED'}

    def invoke(self, context, event):
        return context.window_manager.invoke_props_dialog(self)


def register():
    bpy.utils.register_class(OrganizerOperator)


def unregister():
    bpy.utils.unregister_class(OrganizerOperator)


if __name__ == "__main__":
    register()

    # test call
    bpy.ops.object.organizer()
