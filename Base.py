from bpy.props import StringProperty, BoolProperty, IntProperty, EnumProperty
from bpy.types import Operator
from .Export import Export

class Base:

	export_materials = BoolProperty(
		name = 'Export materials',
		description = '',
		default = False,
	)

	has_shells = BoolProperty(
		name = 'Split mesh by materials',
		description = 'Split mesh into shells by its materials',
		default = False,
	)

	export_normals = BoolProperty(
		name = 'Export normals',
		description = '',
		default = False,
	)

	export_uvs = BoolProperty(
		name = 'Export texture coordinates',
		description = '',
		default = False,
	)

	export_animation = BoolProperty(
		name = 'Export animation',
		description = 'Export animation for each mesh',
		default = False,
	)

	export_shape_keys = BoolProperty(
		name = 'Export shape keys',
		description = '',
		default = False,
	)

	separate_files = BoolProperty(
		name = 'Separate Files',
		description = 'Export data into separate files for selected objects',
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

	# entry point class
	def execute(self, context):
		Export(self, self.filepath, context)
		return {'FINISHED'}

	def draw(self, context):
		layout = self.layout

		col = layout.box().column()
		col.label('Mesh data', icon='MESH_DATA')
		col.prop(self, 'export_normals')
		col.prop(self, 'export_uvs')

		col = layout.box().column()
		col.label('Materials', icon='MATERIAL_DATA')
		col.prop(self, 'export_materials')
		col.prop(self, 'has_shells')

		col = layout.box().column()
		col.label('Animation', icon='ANIM')
		col.prop(self, 'export_animation')
		col.prop(self, 'export_shape_keys')

		col = layout.box().column()
		col.label('File format', icon='FILE_TEXT')
		col.prop(self, 'separate_files')
		col.prop(self, 'pretty_print')
		col.prop(self, 'exp_round')
