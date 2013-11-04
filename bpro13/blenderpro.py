import bpy

bl_info = {
    "name": "Renomear Objeto",
    "author": "Dalai Felinto",
    "version": (1, 0),
    "blender": (2, 69, 0),
    "location": "View3D > Add > Mesh > New Object",
    "description": "Adds a new Mesh Object",
    "warning": "",
    "wiki_url": "",
    "tracker_url": "",
    "category": "Add Mesh"}

class BlenderProOperator(bpy.types.Operator):
    """Tooltip"""
    bl_idname = "object.blenderpro"
    bl_label = "Blender Pro 2013"

    name = bpy.props.StringProperty(default="Hello World")

    def execute(self, context):
        context.object.name = self.name
        return {'FINISHED'}

    def invoke(self, context, event):
        self.name = context.object.name
        return context.window_manager.invoke_props_dialog(self)

    def draw(self, context):
        layout = self.layout
        layout.label(text="Nome do objeto:")
        layout.prop(self, "name")


class HelloWorldPanel(bpy.types.Panel):
    """Creates a Panel in the Object properties window"""
    bl_label = "Hello World Panel"
    bl_idname = "OBJECT_PT_hello"
    bl_space_type = 'PROPERTIES'
    bl_region_type = 'WINDOW'
    bl_context = "object"

    def draw(self, context):
        layout = self.layout

        col = layout.column()
        col.operator("object.blenderpro")
        col.label(text="Nova Propriedade")
        col.prop(context.object, "blenderpro")


def register():
    bpy.types.Object.blenderpro = bpy.props.StringProperty(default="Valor da Propriedade")
    bpy.utils.register_class(BlenderProOperator)
    bpy.utils.register_class(HelloWorldPanel)

def unregister():
    del bpy.types.Object.blenderpro
    bpy.utils.unregister_class(BlenderProOperator)
    bpy.utils.unregister_class(HelloWorldPanel)

if __name__ == "__main__":
    register()
