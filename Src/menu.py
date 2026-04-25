import pygame as pg
import os
from ui.button import MenuButton, SaveButtons
from ui.config import button_position, saves_button_size, button_y, text_col, bible_versions
import pythonbible as bible
from ui.text import TextRender
from savemanager import user_new, new, display_data, data_display
import pygame_widgets
from pygame_widgets.textbox import TextBox




pg.init()

# Gets John 3:16 
references = bible.get_references("John 3:16")

verse_ids = bible.convert_references_to_verse_ids(references)

john_316 = bible.get_verse_text(verse_ids[0])

VERSION = "0.01"

Fullscreen = False

clock = pg.time.Clock()
FPS = 60


font = pg.font.SysFont("Sans Serif", 40)


# Default width and height (got from user display)
os.environ['SDL_VIDEO_CENTERED'] = '1'
info = pg.display.Info()
Width, Height = info.current_w, info.current_h

pg.display.set_caption("Menu")
window = pg.display.set_mode((Width, Height), pg.RESIZABLE)


class SaveSlot:
    def __init__(self):
        self.textbox = None
    
    def output(self):
        if self.textbox:
            text = self.textbox.getText()
            return text 
    
    def save_menu(self, window):	
        state = f"{new} Save"
        pg.display.set_caption(state)
        
        TextRender.draw_title(window, state, font, text_col, w//2, int(h * .1))
        TextRender.draw_title(window, "Enter info", font, text_col, w//2, int(h * .2))
        TextRender.draw_title(window, data_display(), pg.font.SysFont("Arial", 30), text_col, w//2, int(h * .3))
        
        if self.textbox is None:
            self.textbox = TextBox(window, w//2, int(h * .28), 300, 50, fontSize=20, borderColour="RED", textColour="BLACK",
                            onSubmit=self.output, radius=10, borderThickness=5)
        
        self.textbox.draw()
    def clear_box(self):
        if self.textbox:
            self.textbox.hide()
            self.textbox = None   

    

    


start_button = MenuButton("Start", offset=(0, button_y[0]))
about_button = MenuButton("About", offset=(0, button_y[1]))
settings_button = MenuButton("Settings", offset=(0, button_y[2]))
# If user is in fullscreen, they cannot click the ‘x’ to exit out of the game. That is why an exit button is needed. 
exit_button = MenuButton("Exit", offset=(0, button_y[3]))
go_back_to_menu = MenuButton("Back to Menu", offset=(0, button_y[2]))


go_back_to_saves = MenuButton("Back to Saves", saves_button_size["width"], saves_button_size["height"], offset=(button_position["b_saves"]))




right_arrow = left_arrow = is_fullscreen = go_back_to_menu_saves = None



def create_save():
    with open("saves.json", "w") as f:
        f.write("")    



def save_select(window):
    global go_back_to_menu_saves, save_button_list
    # Custom go back to menu button for this menu 
    pg.display.set_caption("Saves")
    TextRender.draw_title(window, "Saves", font, text_col, w//2, int(h * .1))

    spacing = 200
    num_saves = 4
    
    save_button_list = []
    selected_save = None
    
    
    saves_offset = -(spacing * (num_saves - 1)) // 2
    for i in range(1, num_saves):
        y_offset = saves_offset + (i -.5)  * spacing 
        save = SaveButtons(i, f"Save {i}", offset=(0, y_offset))
        save.draw(window)
        save_button_list.append(save)
        last_y = y_offset
    go_back_to_menu_saves = MenuButton("Back to Menu", saves_button_size["width"], saves_button_size["height"], offset=(0, last_y + 200))
    go_back_to_menu_saves.draw(window)

        

    
    
    

def load(window):
    for i in range(2):
        loading = "Loading" + "." * (i * 3)
        pg.display.set_caption("Loading...")
        window.fill(("BLACK"))
        TextRender.draw_title(window, loading, pg.font.SysFont("Arial", 70), ("WHITE"), w//2, int(h * 0.5))
        pg.display.update()
        pg.time.wait(1000)


def start(window):
    save_select(window)



def draw_arrow(surface, color, x, y, size=30, direction="right"):
    half = size//2
    quarter = size//4
    if direction == "right":
            points = [
            (x - half, y - half),
            (x - half, y + half ),
            (x + half, y),
            ]
    else:
            points = [
            (x + half, y - half),
            (x + half, y + half),
            (x - half, y),
            ]
    pg.draw.polygon(surface, color, points)
    # Makes the arrow clickable
    return pg.Rect(x - half, y - half, size, size)



def menu(window):
    pg.display.set_caption("Menu")
    Title = TextRender.draw_title(window, "The Jesus Game", font, text_col, w // 2, int(h * 0.1))
    TextRender.draw_title(window, f"Version: {VERSION}", pg.font.SysFont("Arial", 30), text_col, w//2, Height - 200)
    start_button.draw(window)
    about_button.draw(window)
    settings_button.draw(window)

    
def about(window):
    pg.display.set_caption("About")
    TextRender.draw_title(window, "About", font, text_col, w // 2, int (h * 0.1))
    TextRender.draw_p(window, "This game is meant to be both educational and fun. I want to teach people about Jesus and thought a game would be a good opportunity to do that. The images and assets are AI generated. This entire project is licensed under the GPL 3.0. All code is editable, free and distributable as long as it is maintained as such. I pray to God this game is edifying.",
                       (50, 150), font, text_col,
                       extra_spacing=10)
    TextRender.draw_title(window, "John 3:16 ", font, text_col, w//2, 400)
    TextRender.draw_p(window, john_316, (50, 500), pg.font.SysFont("Arial", 20), text_col)



b_version = 0

# Displays the settings window. 
def settings(window):
    global right_arrow, left_arrow
    og_space = 150
    pg.display.set_caption("Settings")
    TextRender.draw_title(window, "Settings", font, text_col, w // 2, int (h * 0.1))
    # Default Bible Version is the KJV
    curr_bible_version = TextRender.draw_title(window, f"Bible Version: {bible_versions[b_version]}", pg.font.SysFont("Arial", 30), text_col, w // 2, og_space + 100)
    right_arrow = draw_arrow(window, text_col, (w//2) + 400, og_space + 100, 40)
    left_arrow = draw_arrow(window, text_col, (w//2) - 400, og_space + 100, 40, "left")
    # Lets the user make window full screen
    is_fullscreen = TextRender.draw_title(window, f"Fullscreen: {str(Fullscreen).lower()}", pg.font.SysFont("Arial", 30), text_col, w//2, og_space + 200)
    
    
    
    return is_fullscreen

# Makes sure the background is loaded, even if not run from the directory where the image is in. 
os.chdir(os.path.dirname(__file__))
background_img = pg.image.load(os.path.join("Images", "background.png")).convert()
bg_scaled = pg.transform.scale(background_img, (Width, Height))


run = True
menu_state = "main"
save_slot = SaveSlot()


if __name__ == '__main__':
    while run:
        events = pg.event.get()
        window.fill(("BLACK"))
        window.blit(bg_scaled, (0, 0))

        w, h = window.get_width(), window.get_height()

        if menu_state != "start" and menu_state != "saves_menu":
            exit_button.draw(window)
            if menu_state != "main":
                go_back_to_menu.draw(window)


        # Buttons and title disappear once user is away from main menu (except for exit button; this can be reused)
        if menu_state == "main":
            menu(window)
            
        # if we are not in menu, draw the go_to_menu button by default. 
        else:
            # Also can't be start 
            if menu_state == "about":
                    about(window)
            elif menu_state == "settings":
                is_fullscreen = settings(window)
            elif menu_state == "saves_menu":
                save_slot.save_menu(window)
                go_back_to_saves.draw(window)
            else:
                start(window)
                
        # Checks for user events
        for event in events:
            if event.type == pg.QUIT or (event.type == pg.MOUSEBUTTONDOWN and exit_button.clicked(event.pos) and menu_state != "start" and menu_state != "saves_menu"):
                run = False
            if event.type == pg.RESIZABLE:
                window = pg.display.set_mode((event.w, event.h), pg.RESIZABLE)
            if event.type == pg.MOUSEBUTTONDOWN:
                # These buttons will only be heard if on main menu
                if menu_state == "main":
                    if start_button.clicked(event.pos):
                        menu_state = "start"
                    elif about_button.clicked(event.pos):
                        menu_state = "about"
                    elif settings_button.clicked(event.pos):
                        menu_state = "settings"


                # Go back to menu button fixed. It can only be heard if the current menu is NOT main. If it is main, then it will not do anything and replace the settings button. The start mennu transfers the user to the game. Buttons should be destroyed for start. 
                elif menu_state != "main":
                    # Arrows willl only work in the settings menu. The variables right_arrow and left_arrow must exist PRIOR to going to settings.
                    if menu_state == "settings" and right_arrow and left_arrow:
                    # Checks if buttons are clicked. Makes sure the arrows move the current string within the bounds of bible_versions list
                        if right_arrow.collidepoint(event.pos):
                            b_version = (b_version + 1) % len(bible_versions)
                        elif left_arrow.collidepoint(event.pos):
                            b_version = (b_version - 1) % len(bible_versions)
                        if is_fullscreen.collidepoint(event.pos):
                            Fullscreen = not Fullscreen
                            window = pg.display.set_mode((0, 0), pg.FULLSCREEN) if Fullscreen else pg.display.set_mode((Width, Height), pg.RESIZABLE)
                    
                    if menu_state == "start":
                        for save in save_button_list:
                            if save.clicked(event.pos):
                                selected_save = save.slot_num
                                menu_state = "saves_menu"
                    
                    if menu_state == "saves_menu":
                        if go_back_to_saves and go_back_to_saves.clicked(event.pos):
                            save_slot.clear_box()
                            menu_state = "start"

                        
                    if go_back_to_menu.clicked(event.pos) and menu_state != "start" and menu_state != "saves_menu" or (menu_state == "start" and go_back_to_menu_saves.clicked(event.pos) and menu_state != "saves_menu"):
                        menu_state = "main"


        pygame_widgets.update(events)
        pg.display.update()
        clock.tick(FPS)

pg.quit()
