# NoobFramework

NoobFramework is a framework intended to teach how to manage UI from code with simple logic and basics OOP.

Each project must declare, at least, one window, one panel and one widget to have a functional layout.

It uses unheritance through Widgets to make each Panel a simple local Widget render instead of a complexe bloated renderer.


Minimal code to open an empty window:
```py
from NoobFramework import Window

title = "My beautiful noob window"
w = Window(title)
w.open()
```


## Window
## Panel
## WidgetGroup
## Widget