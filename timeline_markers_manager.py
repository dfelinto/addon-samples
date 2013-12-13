
bl_info = {
    "name": "Markers Manager",
    "author": "Dalai Felinto (dfelinto)",
    "version": (1,0),
    "blender": (2, 6, 9),
    "location": "Scene Panel",
    "description": "",
    "warning": "Sample addon to illustrate a bug",
    "wiki_url": "https://github.com/dfelinto/addon-samples",
    "tracker_url": "",
    "category": "Scene"}

import bpy

from bpy.props import (
    StringProperty,
    IntProperty,
    PointerProperty,
    CollectionProperty,
    )

def update_marker_name(self, context):
    '''rename the marker'''
    scene = context.scene
    marker = self

    frame = marker.frame

    for timeline_marker in scene.timeline_markers:
        if timeline_marker.frame == frame:
            timeline_marker.name = marker.name
            return


class SCENE_OT_MarkerAdd(bpy.types.Operator):
    '''Add a new marker to the scene'''
    bl_idname = "scene.marker_add"
    bl_label = "Add Marker"

    name = StringProperty(name="Name")

    @classmethod
    def poll(cls, context):
        return True

    def execute(self, context):
        scene = context.scene
        mm = scene.markers_manager

        marker = mm.markers.add()
        marker.name = self.name
        marker.frame = scene.frame_current

        # Change the active preset
        mm.active_marker_index = len(mm.markers) - 1

        # Add a new marker marker
        scene.timeline_markers.new(self.name, scene.frame_current)

        return {'FINISHED'}


    def invoke(self, context, event):
        scene = context.scene
        frame = scene.frame_current

        for marker in scene.markers_manager.markers:
            if marker.frame == frame:
                self.report({'ERROR'}, "Marker \"{0}\" already set for frame {1}".format(marker.name, frame))
                return {'CANCELLED'}

        self.name = bpy.utils.smpte_from_frame(scene.frame_current)
        wm = context.window_manager
        return wm.invoke_props_dialog(self)


class SCENE_OT_MarkerDel(bpy.types.Operator):
    '''Delete selected marker'''
    bl_idname = "scene.marker_del"
    bl_label = "Delete Marker"

    @classmethod
    def poll(cls, context):
        return True

    def execute(self, context):
        scene = context.scene
        mm = scene.markers_manager

        marker = mm.markers[mm.active_marker_index]
        frame = marker.frame

        # 1) Remove real marker
        for timeline_marker in scene.timeline_markers:
            if timeline_marker.frame == frame:
                scene.timeline_markers.remove(timeline_marker)
                break


        # 2) Remove fake marker
        mm.markers.remove(mm.active_marker_index)
        mm.active_marker_index -= 1
        if mm.active_marker_index < 0:
            mm.active_marker_index = 0

        return {'FINISHED'}

    def invoke(self, context, event):
        return context.window_manager.invoke_confirm(self, event)


class SCENE_PT_markers(bpy.types.Panel):
    bl_label = "Markers"
    bl_space_type = 'PROPERTIES'
    bl_region_type = 'WINDOW'
    bl_context = "scene"

    @classmethod
    def poll(cls, context):
        return True

    def draw(self, context):
        layout = self.layout
        scene = context.scene

        mm = scene.markers_manager
        row = layout.row()
        row.template_list("UI_UL_list", "template_list_markers", mm,
                          "markers", mm, "active_marker_index", rows=3, maxrows=5)

        sub = row.column()
        subsub = sub.column(align=True)
        subsub.operator("scene.marker_add", icon='ZOOMIN', text="")
        subsub.operator("scene.marker_del", icon='ZOOMOUT', text="")

        if len(mm.markers):
            marker = mm.markers[mm.active_marker_index]
            col = layout.column()
            col.prop(marker, "name")

            frame_smpte = bpy.utils.smpte_from_frame(marker.frame)
            col.label(text="Frame: {0}".format(frame_smpte))


class MarkerInfo(bpy.types.PropertyGroup):
    name = StringProperty(default="", update=update_marker_name)
    frame = IntProperty(name="Frame", min=1, default=1, subtype='TIME')


class MarkersManagerInfo(bpy.types.PropertyGroup):
    active_marker_index = IntProperty()
    markers = CollectionProperty(type=MarkerInfo)
    template_list_markers = StringProperty(default="marker")


def register():
    bpy.utils.register_class(MarkerInfo)
    bpy.utils.register_class(MarkersManagerInfo)
    bpy.types.Scene.markers_manager = PointerProperty(name="Markers Manager", type=MarkersManagerInfo, options={'HIDDEN'})

    bpy.utils.register_class(SCENE_OT_MarkerAdd)
    bpy.utils.register_class(SCENE_OT_MarkerDel)
    bpy.utils.register_class(SCENE_PT_markers)


def unregister():
    bpy.utils.unregister_class(SCENE_PT_markers)
    bpy.utils.unregister_class(SCENE_OT_MarkerDel)
    bpy.utils.unregister_class(SCENE_OT_MarkerAdd)

    del bpy.types.Scene.markers_manager
    bpy.utils.unregister_class(MarkersManagerInfo)
    bpy.utils.unregister_class(MarkerInfo)

