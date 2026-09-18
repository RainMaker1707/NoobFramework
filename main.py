from src import Color, Panel, Window, Button, WidgetGroup, Clickable

if __name__ == "__main__":
    w = Window(panels_dict=
            [
                Panel("test", size_x=250, size_y=1050, z_index=100, draggable=True), 
                Panel("cannot_move", color=Color.RED, position_x=1700, position_y=0, size_x=220, size_y=1050),
            ]
        )
    p1 = w.panels.get('test')
    p1.add(WidgetGroup("group_test1", w=p1.size['x']-50, h=100))
    p1.add(WidgetGroup("group_test2", w=p1.size['x']-5, h=150))
    w.panels.get('cannot_move').add(Clickable("test", lambda: print('eheheh'), 10, 0, 200, 100))
    w.open()