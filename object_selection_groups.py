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
# Object Selection Addon
#
# Organize Objects in Selection Groups.
#
# Dalai Felinto
#
# dalaifelinto.com
# Rio de Janeiro, October 2014
#
# ########################################

bl_info = {
    "name": "Selection Groups",
    "author": "Dalai Felinto (dfelinto), Benoit Bolsee (ben2610)",
    "version": (1,0),
    "blender": (2, 7, 2),
    "location": "Tool Panel",
    "description": "",
    "warning": "",
    "wiki_url": "https://github.com/dfelinto/addon-samples",
    "tracker_url": "",
    "category": "Object"}

import bpy

from bpy.props import (
    StringProperty,
    IntProperty,
    EnumProperty,
    PointerProperty,
    CollectionProperty,
    )

import math


# ##########################################################
# Hashes
# ##########################################################

def get_object_from_hash(scene, hash):
    """return object from hash"""
    for object in scene.objects:
        if object.hash == hash:
            return object

    return None


def hash_remap(scene):
    """update the hash for the new Blender objects - not used"""
    hashes = {'':''}
    for object in scene.objects:
        old_hash = ob.hash
        if old_hash:
            new_hash = str(hash(object))
            hashes[old_hash] = new_hash
            ob.hash = new_hash

    for selection_group in scene.selection_groups.groups:
        _to_del = []
        for i, selected in enumerate(selection_group.selecteds):
            selected.hash = hashes.get(selected.hash, "")

            if (not selected.hash) or (not get_object_from_hash(scene, selected.hash)):
                _to_del.append(i)

        _to_del.reverse()
        for i in _to_del:
            selection_group.selecteds.remove(i)


# ##########################################################
# Operators
# ##########################################################

class SCENE_OT_DeselectionGroup(bpy.types.Operator):
    ''''''
    bl_idname = "scene.deselection_group"
    bl_label = "Deselection Group"

    mode = EnumProperty(
        description="",
        items=(("ALL", "All", ""),
               ("ODD", "Odd", ""),
               ("EVEN", "Even", ""),
               ),
        default="ALL",
        options={'SKIP_SAVE'}
        )

    def execute(self, context):
        if self.mode == 'ALL':
            for object in context.selected_objects:
                object.select = False

        elif self.mode == 'ODD':
            for i, object in enumerate(context.selected_objects):
                if i % 2:
                    object.select = False

        elif self.mode == 'EVEN':
            for i, object in enumerate(context.selected_objects):
                if not i % 2:
                    object.select = False

        else:
            self.report({'ERROR'}, "Mode not yet implemented")
            return {'CANCELLED'}


        return {'FINISHED'}


class SCENE_OT_SelectionGroup(bpy.types.Operator):
    ''''''
    bl_idname = "scene.selection_group"
    bl_label = "Selection Group"

    id = IntProperty(default=-1, options={'SKIP_SAVE'})
    name = StringProperty()
    onebyone_mode = EnumProperty(
        description="",
        items=(('NEXT', "Next", ""),
               ('PREV', "Prev", ""),
               ('OPEN', "Open", ""),
               ('CLOSE', "Close", ""),
               ),
        default='OPEN',
        options={'SKIP_SAVE'}
        )

    def execute(self, context):
        scene = context.scene
        sl = scene.selection_groups

        mode = sl.mode
        selection_group = sl.groups[self.id]

        if mode == 'RENAME':
            selection_group.name = self.name

        elif mode == 'RECORD':
            def add_objects(selection_group, objects):
                for ob in objects:
                    if not ob.hash:
                        ob.hash = str(hash(ob))

                    selected = selection_group.selecteds.add()
                    selected.hash = ob.hash

            selection_group.reset()

            # order them by: (1) Objects by their names (2) Lights by their names
            # (3) Camera by their lens and then their names (4) everything else
            # Object.001, Object.003, Lamp.001, Fisheye_Camera

            selected_objects = context.selected_objects

            meshes = [ob for ob in selected_objects if ob.type == 'MESH']
            meshes.sort(key=lambda ob: ob.name)

            lamps = [ob for ob in selected_objects if ob.type == 'LAMP']
            lamps.sort(key=lambda ob: ob.name)

            cameras = [ob for ob in selected_objects if ob.type == 'CAMERA']
            cameras.sort(key=lambda ob: (ob.data.lens, ob.name))

            others = [ob for ob in selected_objects if ob.type not in ('MESH', 'LAMP', 'CAMERA')]

            add_objects(selection_group, meshes)
            add_objects(selection_group, lamps)
            add_objects(selection_group, cameras)
            add_objects(selection_group, others)

        elif mode == 'PLAY' or mode == 'ADD':
            # note: we do garbage collection only
            # trying to play a selection that
            # has a spurious (deleted) object

            active_in_selection = False
            first_object_in_selection = None
            if mode == 'PLAY':
                # first deselect
                if bpy.ops.scene.deselection_group.poll():
                    bpy.ops.scene.deselection_group(mode='ALL')

            _to_del = []
            for i, selected in enumerate(selection_group.selecteds):
                object = get_object_from_hash(scene, selected.hash)
                if not object:
                    _to_del.append(i)
                else:
                    if scene.objects.active == object:
                        active_in_selection = True
                    if not first_object_in_selection:
                        first_object_in_selection = object
                    object.select = True

            _to_del.reverse()
            for i in _to_del:
                selection_group.selecteds.remove(i)
            if not active_in_selection and first_object_in_selection:
                scene.objects.active = first_object_in_selection

        elif mode == 'ONEBYONE':
            # always deselect all
            if bpy.ops.scene.deselection_group.poll():
                bpy.ops.scene.deselection_group(mode='ALL')

            if not len(selection_group.selecteds):
                sl.onebyone_active = -1
                return {'CANCELLED'}

            if self.onebyone_mode == 'OPEN':
                sl.onebyone_active = self.id
                # always start from zero
                selection_group.onebyone_index = 0

            elif self.onebyone_mode == 'CLOSE':
                sl.onebyone_active = -1

            elif self.onebyone_mode == 'PREV':
                selection_group.onebyone_index -= 1

            elif self.onebyone_mode == 'NEXT':
                selection_group.onebyone_index += 1

            if self.onebyone_mode != 'CLOSE':
                selection_group.onebyone_index %= len(selection_group.selecteds)
                current_object = get_object_from_hash(scene, selection_group.selecteds[selection_group.onebyone_index].hash)
                current_object.select = True
                scene.objects.active = current_object

        else:
            self.report({'ERROR'}, "Mode not yet implemented - {0}".format(mode))
            return {'CANCELLED'}

        return {'FINISHED'}

    def invoke(self, context, event):
        scene = context.scene
        sl = scene.selection_groups

        if self.id == -1:
            self.report({'ERROR'}, "No selection group id specified")
            return {'CANCELLED'}

        if self.id >= len(sl.groups):
            self.report({'ERROR'}, "Selection group id out of range")
            return {'CANCELLED'}

        if sl.mode == 'RENAME':
            selection_group = sl.groups[self.id]
            self.name = selection_group.name
            return context.window_manager.invoke_props_dialog(self, width=200)

        else:
            return self.execute(context)

    def draw(self,context):
        layout = self.layout
        layout.prop(self, "name", text="")


class SCENE_OT_SelectionGroupAdd(bpy.types.Operator):
    ''''''
    bl_idname = "scene.selection_group_add"
    bl_label = "Selection Group Add"

    def execute(self, context):
        scene = context.scene
        sl = scene.selection_groups

        groups = len(sl.groups)

        for i in range(groups, 20 + groups):
            selection_group = sl.groups.add()
            selection_group.name = "{0:02}".format(i)

        # the new layer is active
        layers = math.ceil(groups / 20)
        sl.layer = str(layers)

        return {'FINISHED'}


class SCENE_OT_SelectionGroupDel(bpy.types.Operator):
    ''''''
    bl_idname = "scene.selection_group_del"
    bl_label = "Selection Group Delete"

    @classmethod
    def poll(cls, context):
        return len(context.scene.selection_groups.groups) > 0

    def execute(self, context):
        scene = context.scene
        sl = scene.selection_groups

        groups = len(sl.groups)
        if groups == 0:
            return {'CANCELLED'}

        # make sure the selected layer is still valid
        layers = math.ceil(groups / 20)
        layer = int(sl.layer)

        if (layer == layers - 1) and layers > 1:
            sl.layer = str(layer - 1)

        # remove the groups
        groups_range = list(range(groups - 20, groups))
        groups_range.reverse()

        for i in groups_range:
            sl.groups.remove(i)

        return {'FINISHED'}


# ##########################################################
# User Interface
# ##########################################################

class SCENE_PT_SelectionGroups(bpy.types.Panel):
    bl_category = "Tools"
    bl_context = "objectmode"
    bl_label = "Selection Groups"
    bl_space_type = 'VIEW_3D'
    bl_region_type = 'TOOLS'

    @classmethod
    def poll(cls, context):
        return True

    def draw(self, context):
        layout = self.layout
        scene = context.scene
        sl = scene.selection_groups

        if len(sl.groups) == 0:
            layout.operator("scene.selection_group_add", "Add Selection Groups")
            return

        col = layout.column()

        row = col.row(align=True)
        row.operator("scene.deselection_group", text="Deselect Odd").mode='ODD'
        row.operator("scene.deselection_group", text="Deselect Even").mode='EVEN'

        col.separator()
        col.label(text="Selection Mode")
        col.row().prop(sl, "mode", expand=True)

        if sl.mode == 'RENAME':
            icon = 'GREASEPENCIL'
            #icon = 'OUTLINER_DATA_FONT'
        elif sl.mode == 'RECORD':
            icon = 'FILE_REFRESH'
        elif sl.mode == 'PLAY':
            icon = 'NONE'
        else: #'ONEBYONE' or 'ADD'
            icon = 'NONE'

        col.separator()
        row = col.row(align=True)
        row.prop(sl, "layer", expand=True)
        row.operator("scene.selection_group_add", text="", icon='ZOOMIN')
        row.operator("scene.selection_group_del", text="", icon='ZOOMOUT')

        selection_start = int(sl.layer) * 20
        selection_end = selection_start + 20

        if sl.mode == 'ONEBYONE' and \
                sl.onebyone_active != -1:

            for i in range(selection_start, selection_end):
                selection_group = sl.groups[i]

                if not i % 2:
                    row = col.row()
                    split = row.split()

                if i == sl.onebyone_active:
                    sub = split.row(align=True)
                    props = sub.operator("scene.selection_group", text=" ", icon='X')
                    props.id=i
                    props.onebyone_mode='CLOSE'

                    props = sub.operator("scene.selection_group", text=" ", icon='TRIA_LEFT')
                    props.id=i
                    props.onebyone_mode='PREV'

                    props = sub.operator("scene.selection_group", text=" ", icon='TRIA_RIGHT')
                    props.id=i
                    props.onebyone_mode='NEXT'
                else:
                    sub = split.row()
                    sub.operator("scene.selection_group", text=selection_group.name, icon=icon).id=i


        else:
            for i in range(selection_start, selection_end):
                selection_group = sl.groups[i]

                if not i % 2:
                    row = col.row()

                row.operator("scene.selection_group", text=selection_group.name, icon=icon).id=i


# ##########################################################
# Callbacks
# ##########################################################

def update_selection_mode(self, context):
    """Callback function for selection mode"""
    scene = context.scene
    sl = scene.selection_groups

    if sl.mode == 'ONEBYONE':
        sl.onebyone_active = -1

        if bpy.ops.scene.deselection_group.poll():
            bpy.ops.scene.deselection_group(mode='ALL')


# ##########################################################
# Properties
# ##########################################################

class SelectedInfo(bpy.types.PropertyGroup):
    """"""
    hash = StringProperty(name="Hash", description="")


class SelectionGroupInfo(bpy.types.PropertyGroup):
    """"""
    name = StringProperty(name="Name", default="")
    selecteds = CollectionProperty(type=SelectedInfo)
    onebyone_index = IntProperty()

    def reset(self):
        # purge objects
        while self.selecteds:
            self.selecteds.remove(0)

    @staticmethod
    def layers(self, context):
        groups = len(self.groups)
        layers = math.ceil(groups / 20)
        return [(str(id), str(id), "") for id in range(layers)]


class SelectionGroupsInfo(bpy.types.PropertyGroup):
    # selection functionality
    mode = EnumProperty(
        description="Selection Mode",
        items=(("PLAY", "Play", "Change current selection to use the stored selection"),
               ("ADD", "Add", "Select the objects in the selection group on top of current selection"),
               ("ONEBYONE", "1 by 1", "Go over a selection group one object at a time"),
               ("RECORD", "Record", "Save a new selection"),
               ("RENAME", "Rename", "Rename a selection button"),
               ),
        default="PLAY",
        update=update_selection_mode,
        )

    onebyone_active = IntProperty(default=-1)
    groups = CollectionProperty(type=SelectionGroupInfo)
    layer = EnumProperty(items=SelectionGroupInfo.layers)


# ##########################################################
# Un/Register
# ##########################################################

def register():
    bpy.utils.register_class(SelectedInfo)
    bpy.utils.register_class(SelectionGroupInfo)
    bpy.utils.register_class(SelectionGroupsInfo)
    bpy.types.Scene.selection_groups = PointerProperty(name="selection_groups", type=SelectionGroupsInfo, options={'HIDDEN'})
    bpy.types.Object.hash = StringProperty(name="Hash", description="Hashcode of the object")
    bpy.utils.register_class(SCENE_OT_DeselectionGroup)
    bpy.utils.register_class(SCENE_OT_SelectionGroup)
    bpy.utils.register_class(SCENE_OT_SelectionGroupAdd)
    bpy.utils.register_class(SCENE_OT_SelectionGroupDel)
    bpy.utils.register_class(SCENE_PT_SelectionGroups)


def unregister():
    bpy.utils.unregister_class(SCENE_OT_SelectionGroupDel)
    bpy.utils.unregister_class(SCENE_OT_SelectionGroupAdd)
    bpy.utils.unregister_class(SCENE_PT_SelectionGroups)
    bpy.utils.unregister_class(SCENE_OT_DeselectionGroup)
    bpy.utils.unregister_class(SCENE_OT_SelectionGroup)
    del bpy.types.Object.hash
    del bpy.types.Scene.selection_groups
    bpy.utils.unregister_class(SelectionGroupsInfo)
    bpy.utils.unregister_class(SelectionGroupInfo)
    bpy.utils.unregister_class(SelectedInfo)


if __name__ == "__main__":
    register()

