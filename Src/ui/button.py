import pygame as pg 

class MenuButton:
    def __init__(self, text, width=200, height=100, color = (70, 130, 180), align="center", offset=(0, 0)):
        self.width = width
        self.height = height
        self.rect = pg.Rect(0, 0, width, height)
        self.text = text
        self.color = color
        self.align = align
        self.offset = offset
        self.font = pg.font.SysFont("Arial", 20)

    def update_position(self, window):
        w, h = window.get_width(), window.get_height()
        if self.align == "center":
            self.rect.center = (w // 2, h // 2)
        elif self.align == "left":
            self.rect.midleft = (50, h // 2)
        elif self.align == "right":
            self.rect.midright = (w - 50, h // 2)
        elif self.align == "top":
            self.rect.midtop = (w // 2, 50)
        elif self.align == "bottom":
            self.rect.midbottom = (w // 2, h - 50)
        # apply offset AFTER positioning
        self.rect.move_ip(self.offset)

    def draw(self, window):
        self.update_position(window)
        pg.draw.rect(window, self.color, self.rect)
        text_surface = self.font.render(self.text, True, (255, 255, 255))
        text_rect = text_surface.get_rect(center=self.rect.center)
        window.blit(text_surface, text_rect)

    def clicked(self, pos):
        return self.rect.collidepoint(pos)
    
class SaveButtons(MenuButton):
    def __init__(self, slot_num, text, width=500, **kwargs):
        super().__init__(text, width=width, **kwargs)
        self.slot_num = slot_num
    
