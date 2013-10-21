import bpy

from bpy.props import BoolProperty

class VIEW3D_OT_DrawCube(bpy.types.Operator):
    ''''''
    bl_idname = "view3d.draw_cube"
    bl_label = "Draw Cube"

    _handle_calc = None
    _handle_draw = None

    @classmethod
    def poll(cls, context):
        return True

    @staticmethod
    def handle_add(self, context):
        VIEW3D_OT_DrawCube._handle_draw = bpy.types.SpaceView3D.draw_handler_add(
            draw_callback_px, (self, context), 'WINDOW', 'POST_PIXEL')

    @staticmethod
    def handle_remove():
        if VIEW3D_OT_DrawCube._handle_draw is not None:
            bpy.types.SpaceView3D.draw_handler_remove(VIEW3D_OT_DrawCube._handle_draw, 'WINDOW')

        VIEW3D_OT_DrawCube._handle_draw = None

    def modal(self, context, event):
        if not context.window_manager.cube:
            VIEW3D_OT_DrawCube.handle_remove()
            context.area.tag_redraw()
            return {'FINISHED'}

        if not context.area or not context.region or event.type == 'NONE':
            context.area.tag_redraw()
            return {'PASS_THROUGH'}

        if context.area: # not available if other window-type is fullscreen
            context.area.tag_redraw()

        return {'PASS_THROUGH'}

    def invoke(self, context, event):
        if context.area.type == 'VIEW_3D':
            if not context.window_manager.cube:
                # enable
                self.perspective = context.region_data.perspective_matrix

                VIEW3D_OT_DrawCube.handle_add(self, context)
                context.window_manager.cube = True

                if context.area:
                    context.area.tag_redraw()

                context.window_manager.modal_handler_add(self)
                return {'RUNNING_MODAL'}

            else:
                # disable
                VIEW3D_OT_DrawCube.handle_remove()
                context.window_manager.cube = False

                if context.area:
                    context.area.tag_redraw()

                return {'FINISHED'}

        else:
            self.report({'WARNING'}, "View3D not found, cannot run operator")
            return {'CANCELLED'}


# draw in 3d-view
def draw_callback_px(self, context):
    if not context.window_manager.cube:
        return

    print('print')
    return


def register():
    bpy.utils.register_class(VIEW3D_OT_DrawCube)
    bpy.types.WindowManager.cube = BoolProperty(default=False)


def unregister():
    bpy.utils.unregister_class(VIEW3D_OT_DrawCube)
    del bpy.types.WindowManager.cube


if __name__ == "__main__":
    register()

