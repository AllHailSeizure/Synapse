extends Node

var extension_api: Node
const TOOL_NAME := "TileSelect"


func _enter_tree() -> void:
	extension_api = get_node_or_null("/root/ExtensionsApi")
	if extension_api == null:
		push_error("TileTools: ExtensionsApi not found")
		return
	var tool_scene := preload("res://TileSelectTool.tscn")
	extension_api.add_tool(
		TOOL_NAME,
		"Tile Select",
		tool_scene,
		[],
		"Grid-based tile selection",
		"",
		[],
		-1
	)


func _exit_tree() -> void:
	if extension_api == null:
		return
	extension_api.remove_tool(TOOL_NAME)
