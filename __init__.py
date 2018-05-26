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

# ExportJSON - main class
class ExportJSON(Operator, ExportHelper):
	'''Export selected objects to JSON'''   # tooltip for menu items and buttons
	bl_idname = 'export.json'               # unique identifier
	bl_label = 'Export JSON'                # display name in the interface
	bl_options = {'REGISTER'}

	separate_files = BoolProperty(
		name = 'Separate Files',
		description = 'Export data into separate files for selected objects',
		default = True,
	)

	# TODO - does not have a menaning till other options to export arive
	# export_meshes = BoolProperty(
	# 	name = 'Export Meshes',
	# 	description = 'Export meshes for selected objects',
	# 	default = True,
	# )

	has_shells = BoolProperty(
		name = 'Split mesh by material',
		description = 'Split mesh into shells by its materials',
		default = True,
	)

	export_normals = BoolProperty(
		name = 'Export normals',
		description = '',
		default = True,
	)

	export_uvs = BoolProperty(
		name = 'Export texture coordinates',
		description = '',
		default = True,
	)

	export_animation = BoolProperty(
		name = 'Export animation',
		description = 'Export animation for each mesh',
		default = True,
	)

	export_shape_keys = BoolProperty(
		name = 'Export shape keys',
		description = '',
		default = True,
	)

	pretty_print = BoolProperty(
		name = 'Print pretty JSON',
		description = 'Adds indentation and spaces to JSON files',
		default = True,
	)

	exp_round = IntProperty(
		name = 'Round to digits',
		description = 'Return the floating point values rounded to N digits',
		default = 3,
	)

	filename_ext = '.json'

	filter_glob = StringProperty(
		default = '.',
		options = {'HIDDEN'},
		maxlen = 255,
		subtype = 'DIR_PATH'
	)

	# entry point class
	def execute(self, context):
		from .Export import Export
		Export(self, self.filepath, context)
		return {'FINISHED'}

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
