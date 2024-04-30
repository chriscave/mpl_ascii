import numpy as np

def overlay(background, foreground, start_row, start_col):
    min_row = min(start_row, 0)
    min_col = min(start_col, 0)
    max_row = max(start_row + foreground.shape[0], background.shape[0])
    max_col = max(start_col + foreground.shape[1], background.shape[1])

    total_rows = max_row - min_row
    total_cols = max_col - min_col

    # Create the resulting array filled with spaces (or appropriate background fill)
    result = np.full((total_rows, total_cols), ' ', dtype="object")
    bg_start_row = max(-min_row, 0)  # This will be 0 if start_row is >= 0
    bg_start_col = max(-min_col, 0)  # This will be 0 if start_col is >= 0
    result[bg_start_row:bg_start_row+background.shape[0],
           bg_start_col:bg_start_col+background.shape[1]] = background

    fg_start_row = max(start_row - min_row, 0)
    fg_start_col = max(start_col - min_col, 0)
    fg_end_row = fg_start_row + foreground.shape[0]
    fg_end_col = fg_start_col + foreground.shape[1]

    overlap_section = result[fg_start_row:fg_end_row, fg_start_col:fg_end_col]
    result[fg_start_row:fg_end_row, fg_start_col:fg_end_col] = np.where(
        foreground != ' ',  # Condition where foreground isn't just a space
        foreground,
        overlap_section  # Keep original background if foreground is a space
    )

    return result

