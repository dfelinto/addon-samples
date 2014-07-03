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
#
# ########################################

import bpy
import bmesh

bl_info = {
    "name": "Materials Purge",
    "author": "Dalai Felinto (dfelinto)",
    "version": (1,0),
    "blender": (2, 7, 1),
    "location": "Material Special Menu",
    "description": "Remove the materials that are note used in the selected object",
    "warning": "",
    "wiki_url": "https://github.com/dfelinto/addon-samples",
    "tracker_url": "",
    "category": "Material"}


class OBJECT_OT_MaterialPurge(bpy.types.Operator):
    """Remove the materials that are note used in the selected object"""
    bl_idname = "object.material_purge"
    bl_label = "Purge Material"

    @classmethod
    def poll(cls, context):
        return context.active_object and context.active_object.type == 'MESH'

    def execute(self, context):
        obj = context.active_object
        tot_purged = 0
        used = [] #
        lookup = []

        material_slots = obj.material_slots

        for material_slot in material_slots:
            used.append(False)

        mesh = obj.data
        bm = bmesh.new()
        bm.from_mesh(mesh)

        for face in bm.faces:
            used[face.material_index] = True

        # unassign not-used materials
        if mesh.users > 1 or \
           not bpy.ops.object.material_slot_remove.poll():

            for i, material_slot in enumerate(material_slots):
                if not used[i]:
                    material_slot.material = None
                    tot_purged += 1
        else:
            # remove/re-map materials
            active_material_index = obj.active_material_index
            used_len = len(used)

            for i in range(used_len):
                # remove them from the last to the first
                remove_i = (used_len - 1) - i
                if not used[remove_i]:
                    obj.active_material_index = remove_i
                    bpy.ops.object.material_slot_remove()

                    tot_purged += 1
                    if remove_i < active_material_index:
                        active_material_index = max(0, active_material_index -1)

            # restore corrected active material index
            obj.active_material_index = active_material_index

        # garbage cleanup
        bm.free()

        if tot_purged > 0:
            self.report({'INFO'}, "Purged {0} material{1}".format(tot_purged, "s" if tot_purged > 1 else ""))
        else:
            self.report({'INFO'}, "No material to be purged")
        return {'FINISHED'}

    def invoke(self, context, event):
        wm = context.window_manager
        return context.window_manager.invoke_confirm(self, event)


def MATERIAL_PT_purge(self, context):
    self.layout.operator("object.material_purge", icon='RADIO')


def register():
    bpy.utils.register_class(OBJECT_OT_MaterialPurge)
    bpy.types.MATERIAL_MT_specials.append(MATERIAL_PT_purge)


def unregister():
    bpy.utils.unregister_class(OBJECT_OT_MaterialPurge)
    bpy.types.MATERIAL_MT_specials.remove(MATERIAL_PT_purge)


if __name__ == "__main__":
    register()

    # test call
    bpy.ops.object.material_purge()

