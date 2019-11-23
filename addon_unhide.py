bl_info = {
    "name": "Unhide",
    "author": "Dalai Felinto",
    "version": (1, 0),
    "blender": (2, 80, 0),
    "location": "",
    "description": "Adds a new Mesh Object",
    "category": "Add Mesh",
}




import bpy
from bpy.types import Operator


class OBJECT_OT_Unhide(Operator):
    """Unhidew COnferen and schoool"""
    bl_idname = "object.unhide"
    bl_label = "Move Object Up"
    bl_options = {'REGISTER', 'UNDO'}
    
    factor = bpy.props.FloatProperty(
            name = "Factor",
            default = 1.0,
            description = "Quao pra cima sobe",
            options = {'SKIP_SAVE'}
            )

    up = bpy.props.BoolProperty(
            name = "Up",
            default = True,
            description = "Sobe ou desce")

    direction = bpy.props.EnumProperty(
            name = "Direction",
            default = 'UP',
            description = "The Direction ...",
            items = (
            ('UP', "Up", "Going UUUUUP"),
            ('DOWN', "Down", "Going downhile")),
            )


    def execute(self, context):
        print("EXECUTE")
        if context.scene.unhide == 'UP':
            context.object.location[2] += self.factor
        else:
            context.object.location[2] -= self.factor
        return {'FINISHED'}

    
    def invoke(self, context, events):
        wm = context.window_manager
        return wm.invoke_props_dialog(self, width=200)
    
    def draw(self, context):
        layout = self.layout
        layout.prop(context.scene, "unhide")



class UNHIDE_PT_hello(bpy.types.Panel):
    """Creates a Panel in the Object properties window"""
    bl_label = "Unhide Conference"
    bl_idname = "UNHIDE_PT_hello"
    bl_space_type = 'PROPERTIES'
    bl_region_type = 'WINDOW'
    bl_context = "object"

    def draw(self, context):
        layout = self.layout

        obj = context.object

        layout.label(text="Hello world!", icon='WORLD_DATA')
        layout.label(text="Active object is: " + obj.name)
        layout.prop(obj, "name")
        layout.operator("mesh.primitive_cube_add")
        layout.operator("object.unhide")
        layout.prop(context.scene, "unhide")
        


def unhide_menu(self, context):
    self.layout.operator(
        OBJECT_OT_Unhide.bl_idname,
        text="Unhiiiiide",
        icon='PLUGIN')


def register():
    bpy.types.Scene.unhide =bpy.props.EnumProperty(
            name = "Direction",
            default = 'UP',
            description = "The Direction ...",
            items = (
            ('UP', "Up", "Going UUUUUP"),
            ('DOWN', "Down", "Going downhile")),
            )
    bpy.utils.register_class(OBJECT_OT_Unhide)
    bpy.utils.register_class(UNHIDE_PT_hello)
    bpy.types.VIEW3D_MT_mesh_add.append(unhide_menu)



def unregister():
    del bpy.types.Scene.unhide
    bpy.utils.unregister_class(OBJECT_OT_Unhide)


if __name__ == "__main__":
    register()
    bpy.ops.object.unhide()
    
