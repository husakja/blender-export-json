import bpy
import json

# save meshes in JSON format
def __init__(operator, meshes, filePath):
	# set from export UI
	if(operator.separate_files):
		folderPath = filePath.rsplit('\\', 1)[0]
		for mesh in meshes:
			path = folderPath + '\\' + mesh.lower().replace(' ', '-') + '.json'
			with open(path, mode='w') as file:
				WriteJSON(operator.pretty_print, file, meshes[mesh])
	else:
		with open(filePath, mode='w') as file:
			WriteJSON(operator.pretty_print, file, meshes)

# JSON export
def WriteJSON(prettyPrint, file, data):
	# set from export UI
	if (prettyPrint):
		file.write(json.dumps(data, indent=2, separators=(',', ': '), sort_keys=True))
	else:
		file.write(json.dumps(data, separators=(',',':'), sort_keys=True))
