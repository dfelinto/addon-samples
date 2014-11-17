import bpy
from mathutils import Vector

def add_plane(context):
    verts = [Vector((-1, 1, 0 )),
             Vector((1, 1, 0)),
             Vector((1, -1, 0)),
             Vector((-1, -1, 0)),
             ]

    edges = []
    faces = [[0, 1, 2, 3]]

    mesh = bpy.data.meshes.new(name="Plane")
    mesh.from_pydata(verts, edges, faces)

    ob = bpy.data.objects.new("Plane", mesh)

    scene = context.scene
    scene.objects.link(ob)


add_plane(bpy.context)

