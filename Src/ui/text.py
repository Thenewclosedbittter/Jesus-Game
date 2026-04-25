import pygame as pg 
class TextRender:
    @staticmethod
    def draw_title(surface, text, font, color, x, y):
        img = font.render(text, True, color)
        rect = img.get_rect(center=(x, y))
        surface.blit(img, rect)
        # Allows for labels to be clickable 
        return rect 
    @staticmethod
    # Draws paragraphs on menu
    def draw_p(surface, text, pos, font, color, extra_spacing=0):
        p_font = pg.font.SysFont("Arial", 30)
        
        surface_w = surface.get_width()
        
        collection = [word.split(' ') for word in text.splitlines()]
        space = p_font.size(' ')[0]
        x, y = pos
        for lines in collection:
            for words in lines:
                words_surface = p_font.render(words,  True, color)
                word_width, word_height = words_surface.get_size()
                if x + word_width >= surface_w - 50:
                    x =  pos[0]
                    y += word_height + extra_spacing
                surface.blit(words_surface, (x, y))
                x += word_width + space
            x = pos[0]
            y += word_height
