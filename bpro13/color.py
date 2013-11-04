import bpy

def update_color(self, context):
    object = self

    cor = object.new_color

    if cor == 'RED':
        object.color = (1,0,0,1)
    elif cor == 'BLUE':
        object.color = (0,0,1,1)
    elif cor == 'YELLOW':
        object.color = (1,1,0,1)


def meu_panel(self, context):
    layout = self.layout
    object = context.object
    layout.prop(object, "new_color")


def register():
    bpy.types.OBJECT_PT_display.append(meu_panel)
    bpy.types.Object.new_color = bpy.props.EnumProperty(
        name="Nova Cor",
        description="",
        items=(("OBJECT", "Object", ""),
               ("RED", "Vermelho", ""),
               ("BLUE", "Azul", ""),
               ("YELLOW", "Amarelo", ""),
               ),
        default= "OBJECT",
        update=update_color
        )


def unregister():
    bpy.types.OBJECT_PT_display.remove(meu_painel)
    del bpy.types.Object.new_color


if __name__ == "__main__":
    register()

