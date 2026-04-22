import pygame as pg
import os
from ui.button import menu_button
import ui.config  
import pythonbible as bible



pg.init()

# Gets John 3:16 
references = bible.get_references("John 3:16")

verse_ids = bible.convert_references_to_verse_ids(references)

john_316 = bible.get_verse_text(verse_ids[0])



VERSION = "0.01"

Fullscreen = False

clock = pg.time.Clock()
FPS = 60


font = pg.font.SysFont("Arial", 40)

# Default text colour is black
text_col = "BLACK"


# Default width and height (got from user display)
os.environ['SDL_VIDEO_CENTERED'] = '1'
info = pg.display.Info()
Width, Height = info.current_w, info.current_h

pg.display.set_caption("Menu")
window = pg.display.set_mode((Width, Height), pg.RESIZABLE)



og_y = -150
space = 140

def y_pos_spacer(og_y):
    og_y += space
    return og_y

start_button = menu_button("Start", offset=(0, og_y))
about_button = menu_button("About", offset=(0, y_pos_spacer(og_y)))
settings_button = menu_button("Settings", offset=(0, y_pos_spacer(y_pos_spacer(og_y))))
# If user is in fullscreen, they cannot click the ‘x’ to exit out of the game. That is why an exit button is needed. 
exit_button = menu_button("Exit", offset=(0, y_pos_spacer(y_pos_spacer(y_pos_spacer(og_y)))))
go_back_to_menu = menu_button("Back to Menu", offset=(0, y_pos_spacer(y_pos_spacer(og_y))))

right_arrow = left_arrow = is_fullscreen = go_back_to_menu_saves= None


def draw_title(text, font, color, x, y, window=window):
    img = font.render(text, True, color)
    rect = img.get_rect(center=(x, y))
    window.blit(img, rect)
    # Allows for labels to be clickable 
    return rect 

# Draws paragraphs on menu
def draw_p(surface, text, pos, font, color, extra_spacing=0):
    p_font = pg.font.SysFont("Arial", 30)
    collection = [word.split(' ') for word in text.splitlines()]
    space = p_font.size(' ')[0]
    x, y = pos
    for lines in collection:
        for words in lines:
            words_surface = p_font.render(words,  True, color)
            word_width, word_height = words_surface.get_size()
            if x + word_width >= w:
                x =  pos[0]
                y += word_height + extra_spacing
            surface.blit(words_surface, (x, y))
            x += word_width + space
        x = pos[0]
        y += word_height

def create_save():
    with open("saves.json", "w") as f:
        f.write("")    



def saves_menu(window):
    global go_back_to_menu_saves
    # Custom go back to menu button for this menu 
    pg.display.set_caption("Saves")
    draw_title("Saves", font, text_col, w//2, int(h * .1))

    spacing = 200
    # Only 3 saves available 
    num_saves = 4
    
    saves_offset = -(spacing * (num_saves - 1)) // 2
    saves_button = []
    for i in range(1, num_saves):
        y_offset = saves_offset + (i -.5)  * spacing 
        save = menu_button(f"Save {i}:", (w//2), (h//2)//2 - 100, offset=(0, y_offset))
        saves_button.append(save)
        save.draw(window)
        last_y = y_offset
    go_back_to_menu_saves = menu_button("Back to Menu", 300, 100, offset=(0, last_y + 200))
    go_back_to_menu_saves.draw(window)

    
    
    

def load(window):
    for i in range(2):
        loading = "Loading" + "." * (i * 3)
        pg.display.set_caption("Loading...")
        window.fill(("BLACK"))
        draw_title(loading, pg.font.SysFont("Arial", 70), ("WHITE"), w//2, int(h * 0.5))
        pg.display.update()
        pg.time.wait(1000)


def start(window):
    saves_menu(window)



bible_versions = ["King James Bible", "World English Bible (WEB)", "Young's Literal Translation (YLT)", "Bible in Basic English"]


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



def about(window):
    pg.display.set_caption("About")
    draw_title("About", font, text_col, w // 2, int (h * 0.1))
    draw_p(window, "This game is meant to be both educational and fun. I want to teach people about Jesus and thought a game would be a good opportunity to do that. The images and assets are AI generated. This entire project is licensed under the GPL 3.0. All code is editable, free and distributable as long as it is maintained as such. I pray to God this game is edifying.",
                       (50, 150), font, text_col,
                       extra_spacing=10)
    draw_title("John 3:16 ", font, text_col, w//2, 400)
    draw_p(window, john_316, (50, 500), pg.font.SysFont("Arial", 20), text_col)



b_version = 0

# Displays the settings window. 
def settings(window):
    global right_arrow, left_arrow
    og_space = 150
    pg.display.set_caption("Settings")
    draw_title("Settings", font, text_col, w // 2, int (h * 0.1))
    # Default Bible Version is the KJV
    curr_bible_version = draw_title( f"Bible Version: {bible_versions[b_version]}", pg.font.SysFont("Arial", 30), text_col, w // 2, og_space + 100)
    right_arrow = draw_arrow(window, text_col, (w//2) + 400, og_space + 100, 40)
    left_arrow = draw_arrow(window, text_col, (w//2) - 400, og_space + 100, 40, "left")
    # Lets the user make window full screen
    is_fullscreen = draw_title(f"Fullscreen: {str(Fullscreen).lower()}", pg.font.SysFont("Arial", 30), text_col, w//2, og_space + 200)
    return is_fullscreen

# Makes sure the background is loaded, even if not run from the directory where the image is in. 
os.chdir(os.path.dirname(__file__))
background_img = pg.image.load(os.path.join("Images", "background.png")).convert()
bg_scaled = pg.transform.scale(background_img, (Width, Height))


run = True
menu_state = "main"



if __name__=='__main__':
    while run:
        window.fill(("BLACK"))
        window.blit(bg_scaled, (0, 0))

        w, h = window.get_width(), window.get_height()

        if menu_state != "start":
            exit_button.draw(window)

        # Buttons and title disappear once user is away from main menu (except for exit button; this can be reused)
        if menu_state == "main":
            pg.display.set_caption("Menu")
            Title = draw_title("The Jesus Game", font, text_col, w // 2, int(h * 0.1))
            draw_title(f"Version: {VERSION}", pg.font.SysFont("Arial", 30), text_col, w//2, Height - 200)
            start_button.draw(window)
            about_button.draw(window)
            settings_button.draw(window)
        # if we are not in menu, draw the go_to_menu button by default. 
        else:
            # Also can't be start 
            if menu_state != "start":
                go_back_to_menu.draw(window)
            if menu_state == "about":
                    about(window)
            elif menu_state == "settings":
                is_fullscreen = settings(window)
            else:
                start(window)
                
        
        # Checks for user events
        for event in pg.event.get():
            if event.type == pg.QUIT or (event.type == pg.MOUSEBUTTONDOWN and exit_button.clicked(event.pos) and menu_state != "start"):
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
                    if go_back_to_menu.clicked(event.pos) or go_back_to_menu_saves.clicked(event.pos):
                        menu_state = "main"

        pg.display.update()
        clock.tick(FPS)

pg.quit()
