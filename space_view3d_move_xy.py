import bpy

from bpy_extras.view3d_utils import (
    region_2d_to_location_3d,
    )

from mathutils import (
    Vector,
    )

class MoveXYOperator(bpy.types.Operator):
    """Translate the view using mouse events"""
    bl_idname = "view3d.move_xy"
    bl_label = "Move XY"

    @classmethod
    def poll(cls, context):
        return context.object
    
    def modal(self, context, event):
        if event.type == 'MOUSEMOVE':
            self.move(context, event)

        elif event.type in {'LEFTMOUSE', 'RIGHTMOUSE', 'ESC'}:
            return {'FINISHED'}

        return {'RUNNING_MODAL'}

    def invoke(self, context, event):
        if context.space_data.type == 'VIEW_3D':
            self.ob = context.object
            context.window_manager.modal_handler_add(self)
            return {'RUNNING_MODAL'}
        else:
            self.report({'WARNING'}, "Active space must be a View3d")
            return {'CANCELLED'}

    def move(self, context, event):
        xy = region_2d_to_location_3d(
                context.region,
                context.space_data.region_3d,
                (event.mouse_region_x, event.mouse_region_y),
                Vector(),
                ).xy

        self.ob.location.xy = xy


def register():
    bpy.utils.register_class(MoveXYOperator)


def unregister():
    bpy.utils.unregister_class(MoveXYOperator)


if __name__ == "__main__":
    register()
