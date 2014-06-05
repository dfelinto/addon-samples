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
# Shape Alignment Addon
#
# Organize the selected objects in specific shapes.
#
# Dalai Felinto
#
# dalaifelinto.com
# Rio de Janeiro, June 2014
#
# ########################################


import bpy
import math
from mathutils import Euler, Vector


bl_info = {
    "name": "Shape Alignment",
    "author": "Dalai Felinto (dfelinto)",
    "version": (1,0),
    "blender": (2, 7, 1),
    "location": "Tool Panel",
    "description": "",
    "warning": "",
    "wiki_url": "https://github.com/dfelinto/addon-samples",
    "tracker_url": "",
    "category": "Object"}


def get_angle(base_dir, ob, center):
    angle = base_dir.angle_signed(ob.location.xy - center.xy, 0)
    if angle < 0:
        angle += math.pi * 2
    return angle


def get_xy_corner(vector2d):
    """return a vector that points to the closest corner:
       1,1; 1,-1; -1,-1, -1, 1
       """

    diagonal = vector2d.length
    half_side = 0.5 * math.sqrt(2 * (diagonal ** 2))

    angle = vector2d.angle_signed(Vector((1,1)), 0)
    if angle < 0:
        angle += math.pi * 2

    if angle <= math.radians(45) or \
       angle >  math.radians(360 - 45):
        return Vector((half_side, half_side))
    elif angle > math.radians(45) and \
        angle <= math.radians(90 + 45):
        return Vector((-half_side, half_side))
    elif angle > math.radians(90 + 45) and \
         angle <= math.radians(180 + 45):
        return Vector((-half_side, -half_side))
    else:
        return Vector((half_side, -half_side))


def get_xy(vector2d):
    """return a vector that points to the closest direction:
       1,0; 0,-1; -1,0; 0,1
       """

    length = vector2d.length
    angle = vector2d.angle_signed(Vector((1,0)), 0)

    if angle < 0:
        angle += math.pi * 2

    if angle <= math.radians(45) or \
       angle >  math.radians(360 - 45):
        return Vector((length, 0))
    elif angle > math.radians(45) and \
        angle <= math.radians(90 + 45):
        return Vector((0, length))
    elif angle > math.radians(90 + 45) and \
         angle <= math.radians(180 + 45):
        return Vector((-length, 0))
    else:
        return Vector((0, -length))


def shape_circle(context, orientation):
    center = context.scene.cursor_location
    active = context.active_object
    zed = active.location[2]

    base_dir = active.location.xy - center.xy

    if orientation == 'XY':
        zero_dir = get_xy(base_dir).resized(3)
    else:
        zero_dir = base_dir.xy.resized(3)

    num_objects = len(context.selected_objects)
    delta_angle = 2 * math.pi / num_objects

    # sort objects based on angle to center
    sorted_objects = sorted(context.selected_objects, key=lambda ob: get_angle(base_dir, ob, center))

    for i in range(num_objects):
        angle = delta_angle * i
        euler = Euler((0, 0, -angle))

        direction = Vector(zero_dir)
        direction.rotate(euler)

        sorted_objects[i].location = center + direction
        sorted_objects[i].location[2] = zed


def shape_line(context, orientation):
    center = context.scene.cursor_location
    active = context.active_object
    zed = active.location[2]
    origin = active.location.xy

    base_dir = active.location.xy - center.xy
    length = base_dir.length
    #ortho_dir = Vector(base_dir).rotate(Euler((0, 0, math.pi * 0.5)))

    if orientation == 'XY':
        line_dir = get_xy(base_dir).resized(3)
    else:
        line_dir = base_dir.xy.resized(3)

    line_dir.normalize()

    pre_objects = [ob for ob in context.selected_objects if ob != active and math.fabs(base_dir.angle_signed(ob.location.xy - origin, 0)) < math.pi * 0.5]
    post_objects = [ob for ob in context.selected_objects if ob != active and ob not in pre_objects]

    num_objects = len(context.selected_objects)
    if len(post_objects) > 1:
        step = length / len(post_objects)
    else:
        step = length

    #XXX should use cross or dot instead
    pre_objects = sorted(pre_objects, key=lambda ob: (ob.location.xy - origin).length)
    post_objects = sorted(post_objects, key=lambda ob: (ob.location.xy - origin).length)

    for i, ob in enumerate(pre_objects):
        ob.location.xy = origin + (line_dir.xy * (i + 1) * step)

    for i, ob in enumerate(post_objects):
        ob.location.xy = origin - (line_dir.xy * (i + 1) * step)


def shape_square(context, orientation):
    center = context.scene.cursor_location
    active = context.active_object
    zed = active.location[2]

    base_dir = active.location.xy - center.xy
    diagonal = base_dir.length

    if orientation == 'XY':
        zero_dir = get_xy_corner(base_dir).resized(3)
    else:
        zero_dir = base_dir.xy.resized(3)

    num_objects = len(context.selected_objects)
    num_side_objects = (num_objects // 4) - 1
    ortho_angle = math.pi * 0.5

    ortho_dir = Vector(zero_dir)
    ortho_dir.rotate(Euler((0, 0, ortho_angle * 0.5)))
    ortho_dir.normalize()

    # sort objects based on angle to center
    sorted_objects = sorted(context.selected_objects, key=lambda ob: get_angle(base_dir, ob, center))

    corners = []
    for i in range(0, num_objects, num_side_objects + 1):
        corners.append(sorted_objects[i])

    assert(len(corners) == 4)

    sides = [ob for ob in sorted_objects if ob not in corners]
    side_step = math.sqrt(2 * (diagonal ** 2)) / (num_side_objects + 1)

    for i in range(4):
        # corner
        angle = ortho_angle * i
        euler = Euler((0, 0, -angle))

        direction = Vector(zero_dir)
        direction.rotate(euler)

        corners[i].location = center + direction
        corners[i].location[2] = zed

        side_dir = Vector(ortho_dir)
        side_dir.rotate(euler)

        for j in range(num_side_objects):
            ob = sides[(i * num_side_objects) + j]
            step = (j + 1) * side_step

            ob.location = center + direction
            ob.location.xy -= side_dir.xy * step

            ob.location[2] = zed


class OBJECT_OT_ShapeAlignment(bpy.types.Operator):
    """Align and distribute selected objects into shapes"""
    bl_idname = "object.shape_alignment"
    bl_label = "Shape Alignment"

    shape = bpy.props.EnumProperty(
            name="Shape",
            description="",
            items=(
                ('LINE', "Line", ""),
                ('SQUARE', "Square", ""),
                ('CIRCLE', "Circle", ""),
                ),
            default='LINE')

    orientation = bpy.props.EnumProperty(
            name="Orientation",
            description="",
            items=(
                ('XY', "XY", ""),
                ('NONE', "None", ""),
                ),
            default='NONE')

    @classmethod
    def poll(cls, context):
        return context.active_object and context.active_object.select

    def execute(self, context):
        error_message = self.check_errors(len(context.selected_objects), self.shape)
        if error_message:
            self.report({'ERROR'}, error_message)

        if self.shape == 'CIRCLE':
            shape_circle(context, self.orientation)

        elif self.shape == 'LINE':
            shape_line(context, self.orientation)

        elif self.shape == 'SQUARE':
            shape_square(context, self.orientation)

        return {'FINISHED'}

    def invoke(self, context, event):
        wm = context.window_manager
        return wm.invoke_props_dialog(self, width=200)

    def check_errors(self, num_objects, shape):
        if num_objects == 0:
            return "No selected object"

        if shape == 'SQUARE' and \
           num_objects % 4 != 0:
            return "Square shape requires selected objects to be a multiple of 4 (4, 8, 16, ...)"

        elif self.shape == 'LINE' and \
             num_objects < 2:
            return "Line shape requires at least 2 selected objects"

        elif self.shape == 'CIRCLE' and \
             num_objects < 3:
            return "Circle shape requires at least 3 selected objects"

        return None

    def draw(self, context):
        layout = self.layout

        col = layout.column()
        col.prop(self, "shape", text="")
        col.prop(self, "orientation")


class VIEW3D_PT_tools_shape(bpy.types.Panel):
    bl_category = "Tools"
    bl_context = "objectmode"
    bl_label = "Shape Alignment"
    bl_space_type = 'VIEW_3D'
    bl_region_type = 'TOOLS'

    def draw(self, context):
        layout = self.layout
        layout.operator_context = 'EXEC_REGION_WIN'

        scene = context.scene
        orientation = 'XY' if scene.use_shape_align_orientation else 'NONE'

        col = layout.column()
        row = col.row()

        ops = row.operator("object.shape_alignment", text="", icon='MESH_CIRCLE', emboss=False)
        ops.shape = 'CIRCLE'
        ops.orientation = orientation

        ops = row.operator("object.shape_alignment", text="", icon='MESH_PLANE', emboss=False)
        ops.shape = 'SQUARE'
        ops.orientation = orientation

        ops = row.operator("object.shape_alignment", text="", icon='ZOOMOUT', emboss=False)
        ops.shape = 'LINE'
        ops.orientation = orientation

        row = col.row()
        row.prop(scene, "use_shape_align_orientation")


def register():
    bpy.utils.register_class(OBJECT_OT_ShapeAlignment)
    bpy.utils.register_class(VIEW3D_PT_tools_shape)
    bpy.types.Scene.use_shape_align_orientation = bpy.props.BoolProperty(
            name="Align to XY",
            default=False,
            description="Align the shape to the scene axis")


def unregister():
    del bpy.types.Scene.use_shape_align_orientation
    bpy.utils.unregister_class(VIEW3D_PT_tools_shape)
    bpy.utils.unregister_class(OBJECT_OT_ShapeAlignment)


if __name__ == "__main__":
    register()

    # test call
    bpy.ops.object.shape_alignment()

