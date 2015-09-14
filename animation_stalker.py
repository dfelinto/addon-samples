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
# Animation Stalker
#
# Copy the selected object position to the active object
# and bake it as animation.
#
# Dalai Felinto
#
# dalaifelinto.com
# Rio de Janeiro, September 2015
#
# ########################################

bl_info = {
    "name": "Animation Stalker",
    "author": "Dalai Felinto (dfelinto)",
    "version": (1,0),
    "blender": (2, 7, 6),
    "location": "View 3D Toolbar > Animation",
    "description": "Copy the transformations from the selected to the active object",
    "warning": "",
    "wiki_url": "https://github.com/dfelinto/addon-samples",
    "tracker_url": "",
    "category": "Animation"}


import bpy
from bpy.props import IntProperty

def stalker_create_action(context, active_object, frame_start, frame_end, frame_interval):
    """"""
    channels = {
            'location' : 3,
            'rotation_euler' : 3,
            'scale' : 3,
            }

    scene = context.scene
    wm = context.window_manager

    frame_current = scene.frame_current

    action = bpy.data.actions.new('Stalker')
    fcurves = {}

    for name, ids in channels.items():
        fcurves[name] = []

        for id in range(ids):
            fcurve = action.fcurves.new(name, index=id)
            fcurves[name].append(fcurve)

    wm.progress_begin(0, frame_end)
    for frame in range(frame_start, frame_end + 1, frame_interval):
        scene.frame_set(frame)

        mat = active_object.matrix_world
        loc = mat.to_translation()
        rot = mat.to_euler()
        sca = mat.to_scale()

        data = {
                'location' : loc,
                'rotation_euler' : rot,
                'scale' : sca,
                }

        for name, ids in channels.items():
            for id in range(ids):
                fcurves[name][id].keyframe_points.insert(frame, data[name][id])

        wm.progress_update(frame)

    wm.progress_end()
    scene.frame_set(frame_current)

    return action


class ANIM_OT_stalker(bpy.types.Operator):
    """Copy the transformations from the active to the selected objects"""
    bl_idname = "anim.stalker"
    bl_label = "Stalker"

    frame_start = IntProperty(
            name="Start",
            description="Start Frames",
            default=1,
            min=1,
            )

    frame_end = IntProperty(
            name="End",
            description="End Frame",
            default=1,
            min=1,
            )

    frame_interval = IntProperty(
            name="Interval",
            description="Skipped Frames",
            default=1,
            min=1,
            )

    @classmethod
    def poll(cls, context):
        return context.active_object

    def execute(self, context):
        active_object = context.active_object

        selected_objects = context.selected_objects
        objs = [ob for ob in selected_objects if ob != active_object]

        _len = len(objs)

        if _len == 0:
            self.report({'INFO'}, "It requires at least one selected object")
            return {'CANCELLED'}

        action = stalker_create_action(
                context,
                active_object,
                self.frame_start,
                self.frame_end,
                self.frame_interval,
                )

        for ob in objs:
            ob.animation_data_clear()
            ob.animation_data_create()
            ob.animation_data.action = action

        return {'FINISHED'}

    def invoke(self, context, event):
        scene = context.scene

        self.frame_start = scene.frame_start
        self.frame_end = scene.frame_end

        wm = context.window_manager
        return wm.invoke_props_dialog(self, width=200)


def VIEW3D_PT_stalker(self, context):
    self.layout.operator("anim.stalker", text="Bake Stalker")


def register():
    bpy.utils.register_class(ANIM_OT_stalker)
    bpy.types.VIEW3D_PT_tools_animation.append(VIEW3D_PT_stalker)


def unregister():
    bpy.utils.unregister_class(ANIM_OT_stalker)
    bpy.types.VIEW3D_PT_tools_animation.remove(VIEW3D_PT_stalker)


if __name__ == "__main__":
    register()

    # test call
    bpy.ops.anim.stalker()

