"""Based on example by https://gist.github.com/claymcleod
"""

import os
import re
import sys
import time
import signal
import curses
import threading
import subprocess


PROP_REFRESH_RATE = 2

start_time = None
close = False
pipeline = None
framerate = {}

def _update_values(process, values, refresh_rate=2):
    for line in iter(process.stdout.readline, ""):
        search = re.search(
            "(.*)(framerate)(.*)(pad=\(string\))(.*)(,)(.*)(fps=\(uint\))(\d+)",
            line.decode("utf-8") 
        )

        if search is not None:
            if search.group(2) == "framerate":
                framerate[search.group(5)] = search.group(9)
    

def draw_menu(stdscr):
    global close

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
        stdscr.addstr(0, 9, " " + " ".join(pipeline))
        stdscr.attroff(curses.color_pair(4))

        # # Render title
        # stdscr.attron(curses.color_pair(4))
        # stdscr.addstr(1, 0, "Runtime:")
        # stdscr.addstr(1, 8, "{:.3f}".format(time.time() - start_time))
        # stdscr.attroff(curses.color_pair(4))

        # Render headers
        stdscr.attron(curses.color_pair(1))
        stdscr.addstr(2, 0, "Element" + (" " * (width // 2 - 7)))
        stdscr.addstr(2, width // 2, "Framerate" + (" " * (width // 2 - 9)))
        stdscr.attroff(curses.color_pair(1))

        # Render values
        stdscr.attron(curses.color_pair(2))
        for i, key in enumerate(framerate.keys()):
            stdscr.addstr(3 + i, 0, key)
            stdscr.addstr(3 + i, width // 2, str(framerate[key]))
        stdscr.attroff(curses.color_pair(2))
        
        # Render status bar
        statusbarstr = "Press 'q' to exit | runtime: {:.2f}s | Pos: {}, {}".format(
            time.time() - start_time, cursor_x, cursor_y
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

    close = True


def _initialize_update_thread(process):
    thread = threading.Thread(
        target=_update_values,
        args=(process, framerate, PROP_REFRESH_RATE)
    )
    thread.daemon = True
    thread.start()


def _run_command():
    global start_time
    global pipeline

    env = os.environ.copy()
    env["GST_DEBUG"] = "GST_TRACER:7"
    env["GST_TRACERS"] = "framerate"
    pipeline = [sys.argv[_] for _ in range(1, len(sys.argv))]
    process = subprocess.Popen(
        pipeline, stdout=subprocess.PIPE, env=env,
        stderr=subprocess.STDOUT
    )
    
    start_time = time.time()

    return process


def kill(proc_pid):
    process = psutil.Process(proc_pid)
    for proc in process.children(recursive=True):
        proc.kill()
    process.kill()


if __name__ == "__main__":
    process = _run_command()

    _initialize_update_thread(process)

    curses.wrapper(draw_menu)
    # time.sleep(10)

    process.kill()
