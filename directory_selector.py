import os
import curses

def get_directory_options(current_path):
    entries = os.listdir(current_path)
    # Omit if hidden directory
    entries = [entry for entry in entries if not entry.startswith(".")]
    directories = [entry for entry in entries if os.path.isdir(os.path.join(current_path, entry))]
    return [".. (Go up one level)", "Exit"] + directories

def adjust_scroll_offset(selected_index, scroll_offset, max_display_rows):
    if selected_index - scroll_offset >= max_display_rows:
        return selected_index - max_display_rows + 1
    elif selected_index < scroll_offset:
        return selected_index
    return scroll_offset

def draw_header(stdscr, current_path, width):
    path_display = current_path if len(current_path) <= width - 1 else "..." + current_path[-(width - 4):]
    stdscr.addstr(0, 0, f"Current Directory: {path_display}")

def draw_instructions(stdscr, options, scroll_offset, max_display_rows, width):
    instructions = "↑/↓: Navigate | Enter: Select | Displaying "
    if len(options) > max_display_rows:
        instructions += f"{min(max_display_rows, len(options))} of {len(options)} items"
        if scroll_offset > 0:
            instructions += f" | Scrolled {scroll_offset} items"
    else:
        instructions += f"all {len(options)} items"
    instructions = instructions[:width - 3] + "..." if len(instructions) > width else instructions
    stdscr.addstr(1, 0, instructions, curses.A_DIM)

def draw_options(stdscr, options, selected_index, scroll_offset, max_display_rows, width):
    for i in range(min(max_display_rows, len(options))):
        idx = i + scroll_offset
        if idx >= len(options):
            break

        option = options[idx]
        option = option[:width - 6] + "..." if len(option) > width - 3 else option

        try:
            if idx == selected_index:
                stdscr.addstr(i + 2, 0, f"> {option}", curses.A_REVERSE)
            else:
                stdscr.addstr(i + 2, 0, f"  {option}")
        except curses.error:
            pass

def handle_key_press(key, selected_index, options_len):
    if key == curses.KEY_UP:
        return max(0, selected_index - 1)
    elif key == curses.KEY_DOWN:
        return min(options_len - 1, selected_index + 1)
    return selected_index

def handle_selection(selected_index, current_path, directories):
    if selected_index == 0:
        return os.path.dirname(current_path), True  # Go up
    elif selected_index == 1:
        return current_path, False  # Exit
    else:
        new_path = os.path.join(current_path, directories[selected_index - 2])
        return new_path, True

def directory_selector(stdscr, start_path="."):
    current_path = os.path.expanduser(start_path)
    selected_index = 0
    scroll_offset = 0

    curses.curs_set(0)
    stdscr.keypad(True)
    curses.use_default_colors()

    while True:
        options = get_directory_options(current_path)
        directories = options[2:]

        height, width = stdscr.getmaxyx()
        max_display_rows = height - 3

        scroll_offset = adjust_scroll_offset(selected_index, scroll_offset, max_display_rows)

        stdscr.erase()
        draw_header(stdscr, current_path, width)
        try:
            draw_instructions(stdscr, options, scroll_offset, max_display_rows, width)
        except curses.error:
            pass
        draw_options(stdscr, options, selected_index, scroll_offset, max_display_rows, width)
        stdscr.refresh()

        key = stdscr.getch()
        if key in [curses.KEY_UP, curses.KEY_DOWN]:
            selected_index = handle_key_press(key, selected_index, len(options))
        elif key in [curses.KEY_ENTER, 10, 13]:
            current_path, continue_loop = handle_selection(selected_index, current_path, directories)
            if not continue_loop:
                return current_path
            selected_index = scroll_offset = 0
        elif key == curses.KEY_RESIZE:
            stdscr.erase()
            stdscr.refresh()
