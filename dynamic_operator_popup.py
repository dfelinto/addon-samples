# ########################################
#
# Sample to demonstrate dynamic operator menus
# It requires https://developer.blender.org/D578
# (patch by Campbell Barton)
#
# CODE SAMPLE, SNIPPETS FOR MY OWN REFERENCE
# NO COPYRIGHT APPLIES
#
# Dalai Felinto
#
# dalaifelinto.com
# Rio de Janeiro, June 2014
#
# ########################################

import bpy

bl_info = {
    "name": "Polygon Creator",
    "author": "Dalai Felinto (dfelinto)",
    "version": (1,0),
    "blender": (2, 7, 2),
    "location": "Operator Search",
    "description": "",
    "warning": "Sample addon to test dynamic menu drawing, requires a patched Blender",
    "wiki_url": "https://github.com/dfelinto/addon-samples",
    "tracker_url": "",
    "category": "Object"}


def create_circle(context, radius, verts):
    print('create circle')
    return {'FINISHED'}


def create_square(context, side_verts, side_length):
    print('create square')
    return {'FINISHED'}


class OBJECT_OT_PolygonCreate(bpy.types.Operator):
    """Tooltip"""
    bl_idname = "object.polygon_create"
    bl_label = "Create Polygon"

    polygon_mode = bpy.props.EnumProperty(
        name="Polygon Mode",
        description= "",
        items=(
            ('SQUARE', "Square", ""),
            ('CIRCLE', "Circle", ""),
            ),
        default='SQUARE')

    circle_radius = bpy.props.FloatProperty(
            name="Radius",
            subtype='DISTANCE',
            min=0.001,
            max=100.0,
            default=1.0)

    circle_verts = bpy.props.IntProperty(
            name="Vertices",
            min=3,
            max=360,
            default=32)

    square_side_verts = bpy.props.IntProperty(
            name="Size Vertices",
            min=2,
            max=100,
            default=4)

    square_side_length = bpy.props.FloatProperty(
            name="Size Length",
            subtype='DISTANCE',
            min=0.1,
            max=100.0,
            default=1.0)

    @classmethod
    def poll(cls, context):
        return True

    def execute(self, context):
        if self.polygon_mode == 'CIRCLE':
            return create_circle(context, self.circle_radius, self.circle_verts)
        else: #SQUARE
            return create_square(context, self.square_side_verts, self.square_side_length)

        return {'FINISHED'}

    def invoke(self, context, event):
        wm = context.window_manager
        return wm.invoke_props_dialog(self, width=200)

    def draw(self, context):
        layout = self.layout
        layout.prop(self, "polygon_mode", text="")

        if self.polygon_mode == 'CIRCLE':
            row = layout.row(align=True)
            row.prop(self, "circle_radius")
            row.prop(self, "circle_verts")
        else: #SQUARE
            row = layout.row(align=True)
            row.prop(self, "square_side_verts")
            row.prop(self, "square_side_length")


def register():
    bpy.utils.register_class(OBJECT_OT_PolygonCreate)


def unregister():
    bpy.utils.unregister_class(OBJECT_OT_PolygonCreate)


if __name__ == "__main__":
    register()

    # test call
    bpy.ops.object.polygon_create()

