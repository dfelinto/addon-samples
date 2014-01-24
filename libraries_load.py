# ########################################
#
# Imports all the groups of a file
# (you can do that with any datablock)
#
# code used as reference by Andrea Weikert (elubie)
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
import os

def import_groups(filepath):
    """Import all the groups of a file"""
    for file in os.listdir(filepath):
        if file.endswith('.blend'):
            print('Importing ' + file)

            with bpy.data.libraries.load(os.path.join(filepath, file), link=True) as (data_from, data_to):
                data_to.groups = data_from.groups

            for group in data_to.groups:
                print (group.name)
