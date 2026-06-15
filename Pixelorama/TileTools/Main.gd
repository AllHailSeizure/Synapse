extends Node

var extension_api: Node
var grid_overlay: Node2D
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


func show_grid_overlay() -> void:
	if grid_overlay != null:
		return
	grid_overlay = preload("res://GridOverlay.gd").new()
	grid_overlay.name = "TileToolsGridOverlay"
	var canvas := extension_api.general.get_canvas()
	if canvas != null:
		canvas.add_child(grid_overlay)


func hide_grid_overlay() -> void:
	if grid_overlay != null:
		grid_overlay.queue_free()
		grid_overlay = null
