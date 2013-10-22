# ########################################
#
# Draws a few points in all 3d views.
# code used as reference: 'Math Vis' by Campbell Barton
#
# ########################################

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

# <pep8 compliant>

import bpy

SpaceView3D = bpy.types.SpaceView3D
callback_handle = []


def tag_redraw_all_view3d():
    context = bpy.context

    # Py cant access notifers
    for window in context.window_manager.windows:
        for area in window.screen.areas:
            if area.type == 'VIEW_3D':
                for region in area.regions:
                    if region.type == 'WINDOW':
                        region.tag_redraw()


def callback_enable():
    if callback_handle:
        return

    handle_view = SpaceView3D.draw_handler_add(draw_callback_view, (), 'WINDOW', 'POST_VIEW')
    callback_handle[:] = handle_view,

    tag_redraw_all_view3d()


def callback_disable():
    if not callback_handle:
        return

    handle_view = callback_handle[0]
    SpaceView3D.draw_handler_remove(handle_view, 'WINDOW')
    callback_handle[:] = []

    tag_redraw_all_view3d()


def draw_callback_view():
    from bgl import glColor3f, glVertex3f, glPointSize, glBegin, glEnd, GL_POINTS

    points = ((0,0,0),
            ( 1, 1, 1),
            ( 1, 1,-1),
            ( 1,-1, 1),
            ( 1,-1,-1),
            (-1, 1, 1),
            (-1, 1,-1),
            (-1,-1, 1),
            (-1,-1,-1),
            )

    glPointSize(3.0)
    glBegin(GL_POINTS)
    glColor3f(1.0, 0.0, 0.0)
    for point in points:
        glVertex3f(*point)
    glEnd()
    glPointSize(1.0)


def register():
    callback_enable()


def unregister():
    callback_disable()

