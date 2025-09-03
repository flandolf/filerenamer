import os
import curses

def directory_selector(stdscr, start_path="."):
    """
    A directory selector with arrow key navigation and scrolling support.
    Returns the selected directory path.
    """
    # Initialize the current path and selection index
    current_path = os.path.abspath(start_path)
    selected_index = 0
    scroll_offset = 0

    # Configure curses
    curses.curs_set(0)  # Hide the cursor
    stdscr.keypad(True)

    while True:
        # Get the list of directories
        entries = os.listdir(current_path)
        directories = [entry for entry in entries if os.path.isdir(os.path.join(current_path, entry))]

        # Add "Go up one level" and "Exit" options
        options = [".. (Go up one level)", "Exit"] + directories

        # Get terminal dimensions
        height, width = stdscr.getmaxyx()
        max_display_rows = height - 3  # Reserve lines for header and instructions

        # Adjust scroll offset based on selected index
        if selected_index - scroll_offset >= max_display_rows:
            scroll_offset = selected_index - max_display_rows + 1
        elif selected_index < scroll_offset:
            scroll_offset = selected_index

        # Clear the screen
        stdscr.clear()

        # Display the current directory at the top
        path_display = current_path
        if len(path_display) > width - 1:
            path_display = "..." + path_display[-(width - 4):]
        stdscr.addstr(0, 0, f"Current Directory: {path_display}", curses.A_BOLD)

        # Display instructions
        instructions = "↑/↓: Navigate | Enter: Select | Displaying "
        if len(options) > max_display_rows:
            instructions += f"{min(max_display_rows, len(options))} of {len(options)} items"
            if scroll_offset > 0:
                instructions += f" | Scrolled {scroll_offset} items"
        else:
            instructions += f"all {len(options)} items"

        if len(instructions) > width:
            instructions = instructions[:width-3] + "..."

        try:
            stdscr.addstr(1, 0, instructions, curses.A_DIM)
        except curses.error:
            pass  # Handle case where terminal is too small

        # Display the visible options with scrolling
        for i in range(min(max_display_rows, len(options))):
            idx = i + scroll_offset
            if idx >= len(options):
                break

            option = options[idx]
            # Truncate option text if needed
            if len(option) > width - 3:
                option = option[:width - 6] + "..."

            try:
                if idx == selected_index:
                    stdscr.addstr(i + 2, 0, f"> {option}", curses.A_REVERSE)
                else:
                    stdscr.addstr(i + 2, 0, f"  {option}")
            except curses.error:
                pass  # Handle case where terminal is too small

        # Refresh the screen
        stdscr.refresh()

        # Wait for user input
        key = stdscr.getch()

        # Handle key presses
        if key == curses.KEY_UP:
            selected_index = max(0, selected_index - 1)
        elif key == curses.KEY_DOWN:
            selected_index = min(len(options) - 1, selected_index + 1)
        elif key == curses.KEY_ENTER or key in [10, 13]:  # Enter key
            if selected_index == 0:  # Go up one level
                current_path = os.path.dirname(current_path)
                selected_index = 0
                scroll_offset = 0
            elif selected_index == 1:  # Exit
                return current_path
            else:  # Navigate into a directory
                current_path = os.path.join(current_path, directories[selected_index - 2])
                selected_index = 0
                scroll_offset = 0
        elif key == curses.KEY_RESIZE:
            # Handle terminal resize event
            stdscr.clear()
            stdscr.refresh()
