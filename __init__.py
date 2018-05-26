bl_info = {
	'name': 'Export JSON',
	'description': 'Export selected objects as JSONs.',
	'author': 'Jan Husák',
	'version': (0, 0, 1),
	'blender': (2, 79, 0),
	'location': 'File > Export > Export JSON',
	'support': 'COMMUNITY',
	'category': 'Import-Export',
}

from bpy_extras.io_utils import ExportHelper
from bpy.props import StringProperty, BoolProperty, IntProperty, EnumProperty
from bpy.types import Operator
import bpy
import importlib;

# reload imported modules - needed for F8 reload
if 'bpy' in locals():
 	from . import Export
 	importlib.reload(Export)
 	from . import Save
 	importlib.reload(Save)
 	from . import Base
 	importlib.reload(Base)

# ExportJSON - main class
class ExportJSON(bpy.types.Operator, ExportHelper, Base.Base):
	'''Export selected objects to JSON'''   # tooltip for menu items and buttons
	bl_idname = 'export.json'			   # unique identifier
	bl_label = 'Export JSON'				# display name in the interface
	bl_options = {'REGISTER'}

	filename_ext = '.json'
	filter_glob = StringProperty(default='*.json', options={'HIDDEN'})
	export_format = 'ASCII'

# menu registration
def menu_func(self, context):
	self.layout.operator(ExportJSON.bl_idname, text='Export JSON', icon='FILE_TEXT')

# register addon
def register():
	bpy.utils.register_module(__name__)
	bpy.types.INFO_MT_file_export.append(menu_func)

# unregister addon
def unregister():
	bpy.utils.unregister_module(__name__)
	bpy.types.INFO_MT_file_export.remove(menu_func)

# direct script run
if __name__ == '__main__':
	register()
