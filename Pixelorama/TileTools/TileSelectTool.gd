extends Node

var grid_size := Vector2i(20, 20)

var _selected_cells: Array[Vector2i] = []
var _is_drawing := false
var _is_shift_held := false
var _shift_drag_start: Vector2i
var _shift_drag_cells: Array[Vector2i] = []
var _pre_shift_cells: Array[Vector2i] = []


func pos_to_cell(pos: Vector2i) -> Vector2i:
	var cell_x := pos.x / grid_size.x
	var cell_y := pos.y / grid_size.y
	if pos.x < 0:
		cell_x -= 1
	if pos.y < 0:
		cell_y -= 1
	return Vector2i(cell_x, cell_y)


func cell_to_rect(cell: Vector2i) -> Rect2i:
	return Rect2i(cell * grid_size, grid_size)


func cells_bounding_box(cells: Array[Vector2i]) -> Rect2i:
	if cells.is_empty():
		return Rect2i()
	var min_cell := cells[0]
	var max_cell := cells[0]
	for cell in cells:
		min_cell.x = mini(min_cell.x, cell.x)
		min_cell.y = mini(min_cell.y, cell.y)
		max_cell.x = maxi(max_cell.x, cell.x)
		max_cell.y = maxi(max_cell.y, cell.y)
	return Rect2i(min_cell * grid_size, (max_cell - min_cell + Vector2i.ONE) * grid_size)


func snap_to_grid(pos: Vector2i) -> Vector2i:
	var cell := pos_to_cell(pos)
	return cell * grid_size


func draw_start(pos: Vector2i) -> void:
	_is_drawing = true
	_is_shift_held = Input.is_key_pressed(KEY_SHIFT)
	_shift_drag_cells.clear()
	var cell := pos_to_cell(pos)
	if _is_shift_held:
		_pre_shift_cells = _selected_cells.duplicate()
		_shift_drag_start = cell
	else:
		_selected_cells.clear()
		_pre_shift_cells.clear()
	if cell not in _selected_cells:
		_selected_cells.append(cell)
	_apply_selection()


func draw_move(pos: Vector2i) -> void:
	if not _is_drawing:
		return
	var cell := pos_to_cell(pos)
	var shift_now := Input.is_key_pressed(KEY_SHIFT)

	if shift_now and not _is_shift_held:
		_is_shift_held = true
		_pre_shift_cells = _selected_cells.duplicate()
		_shift_drag_start = cell

	if _is_shift_held and shift_now:
		_shift_drag_cells.clear()
		var min_x := mini(_shift_drag_start.x, cell.x)
		var max_x := maxi(_shift_drag_start.x, cell.x)
		var min_y := mini(_shift_drag_start.y, cell.y)
		var max_y := maxi(_shift_drag_start.y, cell.y)
		for x in range(min_x, max_x + 1):
			for y in range(min_y, max_y + 1):
				_shift_drag_cells.append(Vector2i(x, y))
		_selected_cells = _pre_shift_cells.duplicate()
		for c in _shift_drag_cells:
			if c not in _selected_cells:
				_selected_cells.append(c)
		_apply_selection()
	elif not shift_now:
		_is_shift_held = false
		if cell not in _selected_cells:
			_selected_cells.append(cell)
			_apply_selection()


func draw_end(pos: Vector2i) -> void:
	_is_drawing = false
	if _is_shift_held:
		_pre_shift_cells.clear()
		_shift_drag_cells.clear()
	_is_shift_held = false


func cursor_move(pos: Vector2i) -> void:
	pass


func draw_indicator(left: bool) -> void:
	pass


func draw_preview() -> void:
	pass


func _apply_selection() -> void:
	var ext_api := get_node_or_null("/root/ExtensionsApi")
	if ext_api == null:
		return
	ext_api.selection.clear_selection()
	for cell in _selected_cells:
		var rect := cell_to_rect(cell)
		ext_api.selection.select_rect(rect, 0)  # 0 = add


func _clear_selection() -> void:
	var ext_api := get_node_or_null("/root/ExtensionsApi")
	if ext_api == null:
		return
	ext_api.selection.clear_selection()
