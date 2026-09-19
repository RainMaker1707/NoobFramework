from screeninfo import get_monitors, Monitor

MONITORS: list[Monitor] = get_monitors()
PRIMARY_MONITOR : Monitor|None = None
for monitor in MONITORS:
    if monitor.is_primary:
        PRIMARY_MONITOR = monitor
        break
ACTIVE_MONITOR = PRIMARY_MONITOR or MONITORS[0]

WINDOW_HEADER_SIZE=35