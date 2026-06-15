extends Node

var grid_size := Vector2i(20, 20)


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
