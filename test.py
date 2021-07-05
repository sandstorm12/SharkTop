"""Based on example by https://gist.github.com/claymcleod
"""

import os
import sys
import time
import curses
import threading


PROP_REFRESH_RATE = 2

start_time = None
values = {
    'videotestsrc': 0,
    'fakesink': 0
}

def _update_values(values, refresh_rate=2):
    while True:
        for key in values:
            values[key] += 1

        time.sleep(1 / refresh_rate)

def draw_menu(stdscr):
    k = 0
    cursor_x = 0
    cursor_y = 0

    # Clear and refresh the screen for a blank canvas
    stdscr.clear()
    stdscr.refresh()

    # Start colors in curses
    curses.start_color()
    curses.init_pair(1, curses.COLOR_CYAN, curses.COLOR_WHITE)
    curses.init_pair(2, curses.COLOR_BLUE, curses.COLOR_BLACK)
    curses.init_pair(3, curses.COLOR_BLACK, curses.COLOR_WHITE)
    curses.init_pair(4, curses.COLOR_RED, curses.COLOR_YELLOW)

    # Loop where k is the last character pressed
    while (k != ord('q')):
        # Initialization
        stdscr.clear()
        height, width = stdscr.getmaxyx()

        if k == curses.KEY_DOWN:
            cursor_y = min(height - 1, max(0, cursor_y + 1))
            print("down")
        elif k == curses.KEY_UP:
            cursor_y = min(height - 1, max(0, cursor_y - 1))
        elif k == curses.KEY_RIGHT:
            cursor_x = min(width - 1, max(0, cursor_x + 1))
        elif k == curses.KEY_LEFT:
            cursor_x = min(width - 1, max(0, cursor_x - 1))

        # Render title
        stdscr.attron(curses.color_pair(4))
        stdscr.addstr(0, 0, "Pipeline:")
        stdscr.addstr(0, 9, " gst-launch-1.0 videotestsrc ! fakesink")
        stdscr.attroff(curses.color_pair(4))

        # Render title
        stdscr.attron(curses.color_pair(4))
        stdscr.addstr(1, 0, "Runtime:")
        stdscr.addstr(1, 8, "{:.3f}".format(time.time() - start_time))
        stdscr.attroff(curses.color_pair(4))

        # Render headers
        stdscr.attron(curses.color_pair(1))
        stdscr.addstr(2, 0, "Names" + (" " * (width // 2 - 5)))
        stdscr.addstr(2, width // 2, "Values" + (" " * (width // 2 - 6)))
        stdscr.attroff(curses.color_pair(1))

        # Render values
        stdscr.attron(curses.color_pair(2))
        for i, key in enumerate(values.keys()):
            stdscr.addstr(3 + i, 0, key)
            stdscr.addstr(3 + i, width // 2, str(values[key]))
        stdscr.attroff(curses.color_pair(2))
        
        # Render status bar
        statusbarstr = "Press 'q' to exit | STATUS BAR | Pos: {}, {}".format(
            cursor_x, cursor_y
        )
        stdscr.attron(curses.color_pair(3))
        stdscr.addstr(height-1, 0, statusbarstr)
        stdscr.addstr(height-1, len(statusbarstr), " " * (width - len(statusbarstr) - 1))
        stdscr.attroff(curses.color_pair(3))

        # Move curser
        stdscr.move(cursor_y, cursor_x)

        # Refresh the screen
        stdscr.refresh()

        # Wait for next input
        stdscr.nodelay(True)
        k = stdscr.getch()
        time.sleep(min(1 / PROP_REFRESH_RATE, .1))


def _initialize_update_thread():
    thread = threading.Thread(
        target=_update_values, args=(values, PROP_REFRESH_RATE)
    )
    thread.daemon = True
    thread.start()

if __name__ == "__main__":
    _initialize_update_thread()

    start_time = time.time()

    curses.wrapper(draw_menu)
