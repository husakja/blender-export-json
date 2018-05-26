import bpy
from .Save import Save

class Export:

	def __init__(self, operator, filePath, context):
		# save operator
		self.operator = operator

		# active object
		activeObject = bpy.context.scene.objects.active

		try:
			# do export
			meshes = self.MeshesFromSelected()
			Save(operator, meshes, filePath)
		finally:
			# reset active object
			bpy.context.scene.objects.active = activeObject

		# finished successfully
		operator.report({'INFO'}, "%d objects exported" % (len(bpy.context.selected_objects)))

	def GetShells(self, mesh, geometry):
		for polygon in mesh.polygons:
			materialName = mesh.materials[polygon.material_index].name
			if(materialName not in geometry['shells']):
				geometry['shells'][materialName] = []

			geometry['shells'][materialName].extend(polygon.vertices)

	# make attributes arrays from mesh geometry
	def MakeAttributes(self, mesh):
		expRound = self.operator.exp_round

		# set from export UI
		# has shells -> split mesh by materials
		if(self.operator.has_shells):
			geometry = { 'vertices':[], 'shells':{} }

			if(self.operator.export_normals):
				geometry['normals'] = []

			self.GetShells(mesh, geometry)

		# else export just one array with polygons
		else:
			geometry = { 'vertices':[], 'polygons':[] }

			if(self.operator.export_normals):
				geometry['normals'] = []

			geometry['polygons'].extend([index for polygon in mesh.polygons for index in polygon.vertices])

		for vertex in mesh.vertices:
			geometry['vertices'].extend([round(i, expRound) for i in tuple(vertex.co.xyz)])

			if(self.operator.export_normals):
				geometry['normals'].extend([round(i, expRound) for i in tuple(vertex.normal.xyz)])

		# texture coordinates
		if(self.operator.export_uvs):
			uvs = mesh.uv_layers[0].data
			geometry['uvs'] = [0] * (len(mesh.vertices) * 2)
			for polygonId, polygon in enumerate(mesh.polygons):
				for i, vertexId in enumerate(polygon.vertices):
					geometry['uvs'][vertexId * 2] = round(uvs[polygonId * 3 + i].uv.x, expRound)
					geometry['uvs'][vertexId * 2 + 1] = round(uvs[polygonId * 3 + i].uv.y, expRound)

		return geometry

	# return object parameter from armature modifier of current object
	def GetArmature(self, object):
		for modifier in object.modifiers:
			if (modifier.type == "ARMATURE"):
				if (modifier.object):
					return modifier.object.data

		# no armature modifier found
		return False

	# return matrix as list
	def MatrixAsList(self, matrix):
		return [round(cell, self.operator.exp_round) for row in matrix for cell in row]

	# export animation for mesh - animation is selected form modifiers
	def ExportAnimation(self, object, armature):
		animation = { 'bones':[], 'keyframes':[] }
		bones = armature.bones

		for bone in bones:
			animation['bones'].append({
				'length': round(bone.length, self.operator.exp_round), # length of the bone - Y local distance to child bone
				'matrix': self.MatrixAsList(bone.matrix.to_4x4()), # trasnformation of bone itself
				'inverted': self.MatrixAsList(bone.matrix_local.inverted()) # transform to zero point
			})

		return animation

	# export armatures vertex groups from mesh
	def ExportVertexGroups(self, mesh, armature):
		vertexGroups = []

		for vertex in mesh.vertices:
			vertexGroups.append(vertex.groups[0].group)

		return vertexGroups

	# export shape keys
	def ExportShapeKeys(self, object, mesh, key):
		shape = { 'vertices':[] }
		expRound = self.operator.exp_round
		shapeKeys = bpy.data.shape_keys[object.data.shape_keys.name].key_blocks[key]

		# vertices
		vertices = shapeKeys.data
		shape['vertices'] = [round(i, expRound) for vertex in vertices for i in tuple(vertex.co.xyz)]

		# normals
		if (self.operator.export_normals):
			normals = shapeKeys.normals_vertex_get()
			shape['normals'] = [round(normal, expRound) for normal in normals]

		return shape


	# parse single mesh
	def ParseMesh(self, object):
		print('Object: ', object.name)

		try:
			bpy.context.scene.objects.active = object # set object i to active
			bpy.ops.object.modifier_add(type = 'TRIANGULATE') # add triangulate modifier
			meshAtt = object.to_mesh(bpy.context.scene, apply_modifiers = True, settings = 'PREVIEW') # create mesh

			# attributes
			print('Mesh: ', object.data.name)
			expMesh = self.MakeAttributes(meshAtt)

			# export animation
			if (self.operator.export_animation):
				armature = self.GetArmature(object)
				if (armature):
					expMesh['animation'] = self.ExportAnimation(object, armature)
					expMesh['groups'] = self.ExportVertexGroups(meshAtt, armature)

			# export shape keys
			if (self.operator.export_shape_keys and object.data.shape_keys):
				expMesh['shapes'] = []
				expMesh['shapes'].append(self.ExportShapeKeys(object, meshAtt, 'idle_30F'))
				expMesh['shapes'].append(self.ExportShapeKeys(object, meshAtt, 'idle_60F'))

		finally:
			bpy.ops.object.modifier_remove(modifier = object.modifiers[-1].name) # remove last modifier (trinagulate)

		bpy.data.meshes.remove(meshAtt) # clear

		return expMesh # add mesh to the scene

	# parse selected objects and create scene structure form them
	def MeshesFromSelected(self):
		# meshes
		meshes = {}

		# export meshes of selected objects
		for object in bpy.context.selected_objects:
			# export meshe objects
			if object.type == 'MESH':
				objName = object.data.name;
				# parse mesh assigned to material
				if objName not in meshes:
					meshes[objName] = self.ParseMesh(object)

		return meshes
