#====================== BEGIN GPL LICENSE BLOCK ======================
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
#======================= END GPL LICENSE BLOCK ========================

# <pep8 compliant>
bl_info = {
    "name": "Super Camera",
    "author": "Dalai Felinto",
    "version": (1, 0),
    "blender": (2, 7, 5),
    "location": "Search Menu",
    "description": "",
    "warning": "",
    "wiki_url": "",
    "tracker_url": "",
    "category": "3D View"}


import bpy


def get_context_3dview (context):
    """returns area and space"""
    screen = context.screen

    for area in screen.areas:
        if area.type == 'VIEW_3D':
            for region in area.regions:
                if region.type == 'WINDOW':
                    return area, region

    return None, None


def get_space_3dview(context):
    area = context.area
    for space in area.spaces:
        if space.type == 'VIEW_3D':
            return space
    return None


class SuperCameraOperator(bpy.types.Operator):
    """"""
    bl_idname = "view3d.super_camera"
    bl_label = "Super Camera"
    bl_description = "Set viewport view to camera, and view all"

    _space = None

    @classmethod
    def poll(cls, context):
        camera = context.scene.camera
        return camera and camera.type == 'CAMERA'


    def invoke(self, context, event):
        if context.area.type == 'VIEW_3D':
            space = get_space_3dview(context)
            space.region_3d.view_perspective = 'CAMERA'

            # if you uncomment the next lines, viewport camera fails
            if bpy.ops.view3d.view_center_camera.poll():
                bpy.ops.view3d.view_center_camera()

            return {'FINISHED'}
        else:
            self.report({'WARNING'}, "View3D not found, cannot run operator")
            return {'CANCELLED'}


def register():
    bpy.utils.register_class(SuperCameraOperator)


def unregister():
    bpy.utils.unregister_class(SuperCameraOperator)


if __name__ == '__main__':
    register()
