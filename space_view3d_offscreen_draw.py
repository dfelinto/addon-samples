# ##### BEGIN GPL LICENSE BLOCK #####
#
#  This program is free software; you can redistribute it and/or
#  modify it under the terms of the GNU General Public License
#  as published by the Free Software Foundation; either version 2
#  of the License, or (at your option) any later version.
#
#  This program is distributed in the hope that it will be useful,
#  but WITHOUT ANY WARRANTY; without even the implied warranty of
#  MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#  GNU General Public License for more details.
#
#  You should have received a copy of the GNU General Public License
#  along with this program; if not, write to the Free Software Foundation,
#  Inc., 51 Franklin Street, Fifth Floor, Boston, MA 02110-1301, USA.
#
# ##### END GPL LICENSE BLOCK #####


# ########################################
# Object Material Purge Addon
#
# Remove the materials that are not assigned to any face
# for the selected objects.
#
# Dalai Felinto
#
# dalaifelinto.com
# Rio de Janeiro, July 2014
# ########################################

bl_info = {
    "name": "Offscreen draw",
    "author": "Dalai Felinto (dfelinto)",
    "version": (1,0),
    "blender": (2, 7, 7),
    "location": "Toolshelf",
    "description": "",
    "warning": "",
    "wiki_url": "https://github.com/dfelinto/addon-samples",
    "tracker_url": "",
    "category": "Material"}


import bpy

from bpy.props import BoolProperty

class VIEW3D_OT_OffScreenDraw(bpy.types.Operator):
    ''''''
    bl_idname = "view3d.offscreen_draw"
    bl_label = "Offscreen Draw"

    _handle_calc = None
    _handle_draw = None
    is_enabled = False

    @classmethod
    def poll(cls, context):
        return context.area.type == 'VIEW_3D'

    @staticmethod
    def handle_add(self, context):
        VIEW3D_OT_OffScreenDraw._handle_draw = bpy.types.SpaceView3D.draw_handler_add(
            draw_callback_px, (self, context), 'WINDOW', 'POST_PIXEL')

    @staticmethod
    def handle_remove():
        if VIEW3D_OT_OffScreenDraw._handle_draw is not None:
            bpy.types.SpaceView3D.draw_handler_remove(VIEW3D_OT_OffScreenDraw._handle_draw, 'WINDOW')

        VIEW3D_OT_OffScreenDraw._handle_draw = None

    def modal(self, context, event):
        if context.area:
            context.area.tag_redraw()

        return {'PASS_THROUGH'}

    def invoke(self, context, event):
        if VIEW3D_OT_OffScreenDraw.is_enabled:
            VIEW3D_OT_OffScreenDraw.handle_remove()
            VIEW3D_OT_OffScreenDraw.is_enabled = False

            if context.area:
                context.area.tag_redraw()

            return {'FINISHED'}

        else:
            VIEW3D_OT_OffScreenDraw.handle_add(self, context)
            VIEW3D_OT_OffScreenDraw.is_enabled = True

            if context.area:
                context.area.tag_redraw()

            context.window_manager.modal_handler_add(self)
            return {'RUNNING_MODAL'}


# draw in 3d-view
def draw_callback_px(self, context):
    print('print')


def register():
    bpy.utils.register_class(VIEW3D_OT_OffScreenDraw)


def unregister():
    bpy.utils.unregister_class(VIEW3D_OT_OffScreenDraw)


if __name__ == "__main__":
    register()

