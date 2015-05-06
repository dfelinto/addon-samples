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
    "name": "Add Pixel Plane",
    "author": "Dalai Felinto",
    "version": (1, 0),
    "blender": (2, 7, 5),
    "location": "Add Mesh Menu",
    "description": "Creates a plane made of quads forming a pixel grid",
    "warning": "",
    "wiki_url": "",
    "tracker_url": "",
    "category": "Mesh"}


import bpy

from bpy.props import (
        BoolProperty,
        IntProperty,
        FloatProperty,
        FloatVectorProperty,
        )

import bmesh


def add_pixel_plane(plane_width, pixels_width, pixels_height):
    """"""
    verts = []
    faces = []

    w = plane_width / pixels_width
    h = w / (pixels_width / pixels_height)

    for i in range(pixels_width):
        for j in range(pixels_height):
            verts.append(((i + 1) * w,       j * h, 0.0))
            verts.append((      i * w,       j * h, 0.0))
            verts.append((      i * w, (j + 1) * h, 0.0))
            verts.append(((i + 1) * w, (j + 1) * h, 0.0))

            # the id of the first vertex
            _id = ((i * pixels_height)  + j) * 4
            faces.append((_id, _id + 1, _id + 2, _id + 3))

    return verts, faces


def set_pixel_plane_uv(bm):
    """"""
    from mathutils import Vector

    uv_layer = bm.loops.layers.uv.verify()
    bm.faces.layers.tex.verify()  # currently blender needs both layers.

    # adjust UVs
    for f in bm.faces:
        coords = Vector((0.0, 0.0))
        for l in f.loops:
            coords += l.vert.co.xy * 0.25

        for l in f.loops:
            luv = l[uv_layer]
            luv.uv = coords


class AddPixelPlaneOperator(bpy.types.Operator):
    """Add a simple box mesh"""
    bl_idname = "mesh.pixel_plane_add"
    bl_label = "Add Pixel Plane"
    bl_options = {'REGISTER', 'UNDO'}

    plane_width = FloatProperty(
            name="Width",
            default=1.0,
            min = 0.1,
            max=10.0,
            )

    pixels_width = IntProperty(
            name="Pixels Width",
            default=640,
            min = 2,
            max=4096,
            )

    pixels_height = IntProperty(
            name="Pixels Height",
            default=480,
            min = 2,
            max=4096,
            )

    # generic transform props
    view_align = BoolProperty(
            name="Align to View",
            default=False,
            )

    location = FloatVectorProperty(
            name="Location",
            subtype='TRANSLATION',
            )

    rotation = FloatVectorProperty(
            name="Rotation",
            subtype='EULER',
            )

    @classmethod
    def poll(cls, context):
        return True

    def execute(self, context):

        verts_loc, faces = add_pixel_plane(
                self.plane_width,
                self.pixels_width,
                self.pixels_height,
                )

        mesh = bpy.data.meshes.new('Pixel Plane')
        bm = bmesh.new()

        for v_co in verts_loc:
            bm.verts.new(v_co)

        bm.verts.ensure_lookup_table()
        for f_idx in faces:
            bm.faces.new([bm.verts[i] for i in f_idx])

        set_pixel_plane_uv(bm)

        bm.to_mesh(mesh)
        mesh.update()

        # add the mesh as an object into the scene with this utility module
        from bpy_extras import object_utils
        object_utils.object_data_add(context, mesh, operator=self)

        return {'FINISHED'}

    def invoke(self, context, event):
        wm = context.window_manager
        return wm.invoke_props_dialog(self, width=200)

    def draw(self, context):
        layout = self.layout
        col = layout.column()

        col.prop(self, "plane_width", "Plane Width")
        col.separator()

        col.label(text="Pixels")
        row = col.row(align=True)
        row.prop(self, "pixels_width", text="Width")
        row.prop(self, "pixels_height", text="Height")


def menu_func(self, context):
    self.layout.operator(AddPixelPlaneOperator.bl_idname, icon='IMAGE_RGB')


def register():
    bpy.utils.register_class(AddPixelPlaneOperator)
    bpy.types.INFO_MT_mesh_add.append(menu_func)


def unregister():
    bpy.utils.unregister_class(AddPixelPlaneOperator)
    bpy.types.INFO_MT_mesh_add.remove(menu_func)


if __name__ == "__main__":
    register()

    # test call
    bpy.ops.mesh.pixel_plane_add()
