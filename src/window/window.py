import sdl2
import ctypes
from typing import Dict
from src import Config, Panel, allow_batch, Color


class DragContext:
    def __init__(self):
        self.source_panel = None      # Le panneau d'origine
        self.start_position = None   # Position d'origine (pour annuler si besoin)
        self.payload = None          # Données ou sous-élément transporté
        self.is_active = False

    def start_drag(self, panel, mx, my, payload=None):
        self.source_panel = panel
        self.start_position = dict(panel.position)
        self.payload = payload
        self.is_active = True

    def reset(self):
        self.source_panel = None
        self.start_position = None
        self.payload = None
        self.is_active = False


class Window():
    mx: int
    my: int

    def __init__(
        self,
        title: str = "Noob Engine",
        size_x: int = 1920, 
        size_y: int = 1080, 
        position_x: int = 0, 
        position_y: int = 30,
        panels_dict: dict = {},
        framerate: int = 120,
        ):
        self.title = title
        self.position = {'x': position_x, 'y': position_y}
        self.size = {'x': size_x, 'y': size_y}
        self.panels : dict(str, Panel) = {}
        if panels_dict: 
            self.add_panel(panels_dict)
        self._sdl_window = None
        self._is_running = False
        self._title_as_bytes = self.title.encode('utf-8')
        self._framerate = framerate
        self.drag_context = DragContext()
        self._drag_offset = {'x': 0, 'y': 0}

    @classmethod
    def initiate_fom_config(cls, config: Config):
        to_return = cls(
            title=config.title,
            position_x=max(0, config.window.get('position_x') or 0),
            position_y=max(30, config.window.get('position_y') or 30),
            size_x=min(1920, config.window.get('width') or 1920),
            size_y=min(1080, config.window.get('height') or 1080),
            framerate=config.window.get('framerate') or 120,
            )
        config.panels = [
            Panel(
                string=e.get('title') or "",
                position_x=max(0, e.get('position_x') or 0),
                position_y=max(0, e.get('position_y') or 0),
                size_x=min(1920, e.get('width') or 1920),
                size_y=min(1080, e.get('height') or 1080),
                z_index=e.get('z_index') or 0,
                color=Color(tuple(e.get('color') or Color.BLUE))
                ) 
            for e in config.panels
            ]
        to_return.add_panel(config.panels)
        return to_return

    @allow_batch
    def add_panel(self, o_panel: Panel, string: str = ""):
        if not string:
            string = o_panel.string
        if self.panels.get(string) is not None:
            raise KeyError(f"Panel '{string}' already exist in window '{self.title}'")
        self.panels[string] = o_panel
        return True

    def get_ordered_panels(self, order_key='z') -> list[Panel]:
        return sorted(self.panels.values(), key=lambda e: e.position['z'])

    def open(self):
        """Ouvre la fenêtre et lance la boucle de rendu 2D."""
        if self._is_running:
            return
        if sdl2.SDL_Init(sdl2.SDL_INIT_VIDEO) < 0:
            raise RuntimeError("Échec de l'initialisation de SDL2")
        # Window creation
        self._sdl_window = sdl2.SDL_CreateWindow(
            self._title_as_bytes,
            self.position['x'],
            self.position['y'],
            self.size['x'],
            self.size['y'],
            sdl2.SDL_WINDOW_SHOWN | sdl2.SDL_WINDOW_RESIZABLE
        )
        if not self._sdl_window:
            sdl2.SDL_Quit()
            raise RuntimeError("Échec de la création de la fenêtre SDL2")
        # 2. Création du moteur de rendu 2D classique
        self._sdl_renderer = sdl2.SDL_CreateRenderer(
            self._sdl_window, -1, sdl2.SDL_RENDERER_ACCELERATED
        )
        self._is_running = True
        self._run_loop()

    def _run_loop(self):
        frame_delay = 1000.0 / self._framerate
        event = sdl2.SDL_Event()
        while self._is_running:
            frame_start = sdl2.SDL_GetTicks64()
            while sdl2.SDL_PollEvent(ctypes.byref(event)) != 0:
                if event.type == sdl2.SDL_QUIT:
                    self.close()
                    return
                if event.type == sdl2.SDL_WINDOWEVENT:
                    if event.window.event == sdl2.SDL_WINDOWEVENT_RESIZED:
                        self.size['x'] = event.window.data1
                        self.size['y'] = event.window.data2

                elif event.type == sdl2.SDL_MOUSEBUTTONDOWN:
                    
                    if event.button.button == sdl2.SDL_BUTTON_LEFT:
                        self.mx, self.my = event.button.x, event.button.y
                        for panel in reversed(self.get_ordered_panels()):
                            if panel.is_header_clicked(self.mx, self.my): # ou is_draggable
                                self.drag_context.start_drag(panel, self.mx, self.my)
                                break

                elif event.type == sdl2.SDL_MOUSEMOTION:
                    if self.drag_context.is_active:
                        self.mx, self.my = event.motion.x, event.motion.y
                        self._render_panels()

                elif event.type == sdl2.SDL_MOUSEBUTTONUP:
                    if event.button.button == sdl2.SDL_BUTTON_LEFT and self.drag_context.is_active:
                        self.mx, self.my = event.button.x, event.button.y
                        target_panel = None
                        for panel in reversed(self.get_ordered_panels()):
                            if panel == self.drag_context.source_panel:
                                target_panel = panel
                                break
                        if target_panel and target_panel.draggable:
                            target_panel.position = {'x': self.mx, 'y': self.my, 'z': target_panel.z_index}
                        self.drag_context.reset()
            # Background cleanup
            sdl2.SDL_SetRenderDrawColor(self._sdl_renderer, 30, 30, 30, 255)
            sdl2.SDL_RenderClear(self._sdl_renderer)
            # Display & renderer
            self._render_panels()
            sdl2.SDL_RenderPresent(self._sdl_renderer)
            frame_time = sdl2.SDL_GetTicks64() - frame_start
            if frame_time < frame_delay:
                sdl2.SDL_Delay(int(frame_delay - frame_time))


    def _render_panels(self):
        """Dessine les panneaux sous forme de rectangles remplis."""
        for panel in self.get_ordered_panels():
            panel.render(self._sdl_renderer)
        if self.drag_context.is_active and self.drag_context.source_panel.draggable:
            mx, my = (self.mx, self.my)
            # Rectangle de prévisualisation qui suit la souris
            preview_rect = sdl2.SDL_Rect(
                int(mx - self._drag_offset['x']),
                int(my - self._drag_offset['y']),
                int(self.drag_context.source_panel.size['x']),
                int(self.drag_context.source_panel.size['y'])
            )
            # Activer le mode Blend pour la transparence SDL2
            sdl2.SDL_SetRenderDrawBlendMode(self._sdl_renderer, sdl2.SDL_BLENDMODE_BLEND)
            # Dessiner le rectangle de preview semi-transparent (ex: blanc/bleu avec alpha=100)
            sdl2.SDL_SetRenderDrawColor(self._sdl_renderer, 100, 150, 255, 100)
            sdl2.SDL_RenderFillRect(self._sdl_renderer, ctypes.byref(preview_rect))
            # Dessiner le contour de la preview
            sdl2.SDL_SetRenderDrawColor(self._sdl_renderer, 255, 255, 255, 200)
            sdl2.SDL_RenderDrawRect(self._sdl_renderer, ctypes.byref(preview_rect))

    def close(self):
        if not self._is_running:
            return
        self._is_running = False
        if self._sdl_renderer:
            sdl2.SDL_DestroyRenderer(self._sdl_renderer)
            self._sdl_renderer = None
        if self._sdl_window:
            sdl2.SDL_DestroyWindow(self._sdl_window)
            self._sdl_window = None
        sdl2.SDL_Quit()
