extends Node

var extension_api: Node


func _enter_tree() -> void:
	extension_api = get_node_or_null("/root/ExtensionsApi")
	if extension_api == null:
		push_error("TileTools: ExtensionsApi not found")
		return


func _exit_tree() -> void:
	if extension_api == null:
		return
