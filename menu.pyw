import pygame
import snake


# on [0.3] This needs to be updated and more documented
# Had to rename both files to .py because new python scripts cant read ".pyw"
# No need to change menu, for know if seems to be working


def menu_reset():
    pygame.display.set_mode( display_size )
    pygame.display.set_caption( 'Snake' )

def no_fun():
    pass

def quit_fun():
    global RUNNING
    RUNNING = False

def go_to_lvl():
    global active_window
    active_window = level_menu

def go_to_main():
    global active_window
    active_window = main_menu

def go_to_quit():
    global active_window
    active_window = quit_menu

def play_level_1():
    snake.snake_game( 5, 15, 'Snake: Level 1' )
    menu_reset()

def play_level_2():
    snake.snake_game( 10, 20, 'Snake: Level 2' )
    menu_reset()

def play_level_3():
    snake.snake_game( 15, 25, 'Snake: Level 3' )
    menu_reset()

#--- 3. CLASSES
class Menu:
    
    class Field:
        def __init__( self, pos, pic, pic_h = None, function = None ):
            self.pic = pic
            if pic_h == None:
                self.pic_h = pic
            else:
                self.pic_h = pic_h

            self.function = function

            self.Rect = pygame.Rect(( pos, pic.get_size() ))

    def __init__(
                  self,
                  menu_size = (800,600),
                  buttons = [],
                  bcg_color = (0,0,0),
                  picture = None,
                ):

        self.bcg_col = bcg_color
        self.picture = picture

        self.font_file_path = 'media/fonts/arial.ttf'
        self.font_size = 40

        self.Font = pygame.font.Font( self.font_file_path, self.font_size )

        self.menu_size = menu_size

        pos = [100,100]

        self.fields = []

        for button in buttons:
            pic = self.Font.render( button[0], True, (255,255,255) )
            pic_h = self.Font.render( button[0], True, (255,0,0) )

            self.fields.append( Menu.Field( pos, pic, pic_h, button[1]) )
            pos[1] += int( self.font_size * 1.5 )

    def draw( self, surface, mouse_pos ):

        if self.picture != None:
            surface.blit( self.picture, (0,0) )
        else:
            surface.fill( self.bcg_col )

        for f in self.fields:
            if f.Rect.collidepoint( mouse_pos ):
                surface.blit( f.pic_h, f.Rect )
            else:
                surface.blit( f.pic, f.Rect )

    def click( self, mouse_pos ):
        for f in self.fields:
            if f.Rect.collidepoint( mouse_pos ):
                f.function()
                break
      
pygame.init()
display_size = [ 800, 850 ]
DISPLAY = pygame.display.set_mode( display_size )
pygame.display.set_caption( "Game name..." )
game_clock = pygame.time.Clock()
FPS = 60

# creating tuples for different levels and menu choices
main_menu = Menu( 
                  buttons = [
                             ['Choose level', go_to_lvl   ],
                             ['Quit',        go_to_quit  ],
                            ],
                  picture = pygame.image.load('media/pictures/main.jpg').convert()
                 )

level_menu = Menu(
                  buttons = [
                             ['Level 1',           play_level_1 ],
                             ['Level 2',           play_level_2 ],
                             ['Level 3',           play_level_3 ],
                             ['Back to Main menu', go_to_main   ],
                             ['Quit',              go_to_quit   ],
                            ],
                  picture = pygame.image.load('media/pictures/lvl.jpg').convert()                
                  )

quit_menu = Menu(
                  buttons = [
                             ['Back to Main menu', go_to_main ],
                             ['Confirm Quit...',   quit_fun   ],
                            ],
                  picture = pygame.image.load('media/pictures/quit.jpg').convert()                
                  )

# Setting the active window
active_window = main_menu


RUNNING = True
while RUNNING:

    for event in pygame.event.get():
        if event.type == pygame.MOUSEBUTTONDOWN:
            if event.button == 1:
               active_window.click( event.pos )

        elif event.type == pygame.QUIT:
            go_to_quit()


    active_window.draw( DISPLAY, pygame.mouse.get_pos() )
    game_clock.tick( FPS )
    pygame.display.update()

#--- 7. EXITING GAME
pygame.quit()
