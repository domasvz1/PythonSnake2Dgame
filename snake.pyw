import pygame, random

# the update 0.1 is not ready te to come out, want to fix drawing with the apple and the snake itself
# -- also snake eating animation needs to fixed (done)
# -- after all that done, optimizations can be left for 0.2 and later versions
# -- also more ducumentation could be added and so on..
#-- 0.2 later update make a game over window
# Learn and chnage created gameobject and learn the right naming
# Drawing and checking might be considerede in the later patches (if needed)
# need to fix the movement


class Snake:
    def __init__( self, all_cells, cell_size, picture, display_size, surface, direction = pygame.K_DOWN ):
        # Few comments about variables here

        # related Snake's body
        self.body = all_cells
        self.original_body = all_cells[:]
        self.whichpart = [[],[],[]]     
        self.length = len( self.body )
        self.size = cell_size

        # Snake's picture and rotated forms of picture
        self.pic    = picture
        self.pic90  = pygame.transform.rotate( picture, 90 )
        self.pic180 = pygame.transform.rotate( picture, 180 )
        self.pic270 = pygame.transform.rotate( picture, 270 )
        
        # display variables
        self.display_size = display_size
        self.surface = surface
        self.direction = direction


    def _move( self, new_cell ):
        self.body = [new_cell] + self.body

    def _cut_tail( self ):
        if self.length < len(self.body):
            self.body = self.body[:self.length]

    # Task for later, change reset to 'resetDirection'
    def reset( self ):
        self.body = self.original_body[:]
        self.length = len(self.original_body)
        self.direction = pygame.K_DOWN
        

    def die( self ):
        pygame.time.wait( 2000 )
        pygame.event.clear()
        self.reset()

    # Update 0.1 No need to get surface from seperate methods, the constructor holds passed surface variable

    # So a new idea from came up with the 0.1 version
    # What if we took a variable which would decide which part should be drawn with the 'drawthepart' method
    ## -- implementing that variable, calling 'whichpart' in the constructor __init__ L35(might change +-4)
    ## idea implemented
    
    def drawthepart( self, pictureangle, thecutpart ):
        self.surface.blit( pictureangle, self.whichpart, thecutpart )

            
    def update( self, turning, apple ):
        if turning != None:
            if turning == pygame.K_UP and self.direction != pygame.K_DOWN:
                self.direction = turning
            elif turning == pygame.K_DOWN and self.direction != pygame.K_UP:
                self.direction = turning            
            elif turning == pygame.K_RIGHT and self.direction != pygame.K_LEFT:
                self.direction = turning
            elif turning == pygame.K_LEFT and self.direction != pygame.K_RIGHT:
                self.direction = turning

        if self.direction == pygame.K_UP:
            self.body[0] = self.body[0] + [pygame.K_UP]
            new_cell = [self.body[0][0],
            (self.body[0][1] - self.size)%self.display_size[1],
            pygame.K_DOWN]
        elif self.direction == pygame.K_DOWN:
            self.body[0] = self.body[0] + [pygame.K_DOWN]
            new_cell = [self.body[0][0],
            (self.body[0][1] + self.size)%self.display_size[1],
            pygame.K_UP]
        elif self.direction == pygame.K_RIGHT:
            self.body[0] = self.body[0] + [pygame.K_RIGHT]
            new_cell = [(self.body[0][0] + self.size)%self.display_size[0],
            self.body[0][1],
            pygame.K_LEFT]
        elif self.direction == pygame.K_LEFT:
            self.body[0] = self.body[0] + [pygame.K_LEFT]
            new_cell = [(self.body[0][0] - self.size)%self.display_size[0],
            self.body[0][1],
            pygame.K_RIGHT]

        collision = False
        for cell in self.body:
            if new_cell[:2] == cell[:2]:
                collision = True
                
        result = None
        if collision:
            self.die()
            return 'died'
        
        ############# naujas pridedam tasku
        elif apple.get_pos() == new_cell[:2]:
            self.length += 1
            new_cell = new_cell + [True]
            apple.new_pos( self.body )
            result = 'point'

        else:
            new_cell = new_cell + [False]

        self._move( new_cell )
        self._cut_tail()
        return result


    def draw( self ):
        # O.1 Before Drawing each part, we will let the function know where to draw by changing the variable
        self.whichpart = self.body[0][:2]

        # Starting to draw head
        if self.body[0][2] == pygame.K_UP and self.body[0][3] == False:
            self.drawthepart( self.pic270, ( 40, 0, 40, 40 ))
      
        elif self.body[0][2] == pygame.K_UP and self.body[0][3] == True:
            self.drawthepart(self.pic270, ( 0, 0, 40, 40 ) )
            
        elif self.body[0][2] == pygame.K_DOWN and self.body[0][3] == False:
            self.drawthepart( self.pic90, ( 0, 120, 40, 40 ) )

            
        elif self.body[0][2] == pygame.K_DOWN and self.body[0][3] == True:
            self.drawthepart( self.pic90, ( 40, 120, 40, 40 ) )

            
        elif self.body[0][2] == pygame.K_RIGHT and self.body[0][3] == False:
            self.drawthepart( self.pic180, ( 120, 40, 40, 40 ) )

            
        elif self.body[0][2] == pygame.K_RIGHT and self.body[0][3] == True:
            self.drawthepart( self.pic180,  ( 120, 0, 40, 40 ) )

            
        elif self.body[0][2] == pygame.K_LEFT and self.body[0][3] == False:
            self.drawthepart( self.pic, ( 0, 0, 40, 40 ) )
    
        elif self.body[0][2] == pygame.K_LEFT and self.body[0][3] == True:
            self.drawthepart( self.pic, ( 0, 40, 40, 40 ) )


        # If anyone will ever read this code, this is the part where we start drawing the body (everything without head and tale)     
        for cell in self.body[1:-1]:
            if cell[3] == False:

                # From here the second parameter is 'cell[:2]'
                self.whichpart = cell[:2]
                ####
                if (cell[2] == pygame.K_UP and cell[4] == pygame.K_DOWN) or\
                    (cell[2] == pygame.K_DOWN and cell[4] == pygame.K_UP):
                    self.drawthepart( self.pic90, ( 0, 80, 40, 40 ) )

                    
                elif (cell[2] == pygame.K_RIGHT and cell[4] == pygame.K_LEFT) or\
                    (cell[2] == pygame.K_LEFT and cell[4] == pygame.K_RIGHT):
                    self.drawthepart( self.pic, ( 40, 0, 40, 40 ) )

                    
                elif (cell[2] == pygame.K_UP and cell[4] == pygame.K_RIGHT) or\
                    (cell[2] == pygame.K_RIGHT and cell[4] == pygame.K_UP):
                    self.drawthepart( self.pic, ( 80, 0, 40, 40 ) )

                    
                elif (cell[2] == pygame.K_LEFT and cell[4] == pygame.K_UP) or\
                    (cell[2] == pygame.K_UP and cell[4] == pygame.K_LEFT):
                    self.drawthepart( self.pic90, ( 0, 40, 40, 40 ) )

                    
                elif (cell[2] == pygame.K_DOWN and cell[4] == pygame.K_LEFT) or\
                    (cell[2] == pygame.K_LEFT and cell[4] == pygame.K_DOWN):
                    self.drawthepart( self.pic180, ( 40, 40, 40, 40 ) )

                    
                elif (cell[2] == pygame.K_RIGHT and cell[4] == pygame.K_DOWN) or\
                    (cell[2] == pygame.K_DOWN and cell[4] == pygame.K_RIGHT):
                    self.drawthepart( self.pic270, ( 40, 80, 40, 40 ) )


            elif cell[3] == True:
                if (cell[2] == pygame.K_UP and cell[4] == pygame.K_DOWN) or\
                    (cell[2] == pygame.K_DOWN and cell[4] == pygame.K_UP):
                    self.drawthepart( self.pic90, ( 40, 80, 40, 40 ) )
                    
                elif (cell[2] == pygame.K_RIGHT and cell[4] == pygame.K_LEFT) or\
                    (cell[2] == pygame.K_LEFT and cell[4] == pygame.K_RIGHT):
                    self.drawthepart( self.pic, ( 40, 40, 40, 40 ) )
                    
                elif (cell[2] == pygame.K_UP and cell[4] == pygame.K_RIGHT) or\
                    (cell[2] == pygame.K_RIGHT and cell[4] == pygame.K_UP):
                    self.drawthepart( self.pic, ( 80, 40, 40, 40 ) )
                    
                elif (cell[2] == pygame.K_LEFT and cell[4] == pygame.K_UP) or\
                    (cell[2] == pygame.K_UP and cell[4] == pygame.K_LEFT):
                    self.drawthepart( self.pic90, ( 40, 40, 40, 40 ) )
                    
                elif (cell[2] == pygame.K_DOWN and cell[4] == pygame.K_LEFT) or\
                    (cell[2] == pygame.K_LEFT and cell[4] == pygame.K_DOWN):
                    self.drawthepart( self.pic180, ( 40, 0, 40, 40 ) )
                    
                elif (cell[2] == pygame.K_RIGHT and cell[4] == pygame.K_DOWN) or\
                    (cell[2] == pygame.K_DOWN and cell[4] == pygame.K_RIGHT):
                    self.drawthepart( self.pic270, ( 0, 80, 40, 40 ) )
        ###


        # Drawing tale, need to modify 'whichpart variable'
        self.whichpart = self.body[-1][:2],

        if self.body[-1][4] == pygame.K_UP and self.body[-1][3] == False:
            self.drawthepart( self.pic90, ( 0, 0, 40, 40 ) )
     
        elif self.body[-1][4] == pygame.K_UP and self.body[-1][3] == True:
            self.drawthepart( self.pic90, ( 40, 0, 40, 40 ) )
            
        elif self.body[-1][4] == pygame.K_DOWN and self.body[-1][3] == False:
            self.drawthepart( self.pic270, ( 40, 120, 40, 40 ) )
            
        elif self.body[-1][4] == pygame.K_DOWN and self.body[-1][3] == True:
            self.drawthepart( self.pic270, ( 0, 120, 40, 40 ) )
            
        elif self.body[-1][4] == pygame.K_RIGHT and self.body[-1][3] == False:
            self.drawthepart( self.pic, ( 120, 0, 40, 40 ) )
            
        elif self.body[-1][4] == pygame.K_RIGHT and self.body[-1][3] == True:
            self.drawthepart( self.pic, ( 120, 40, 40, 40 ) )
            
        elif self.body[-1][4] == pygame.K_LEFT and self.body[-1][3] == False:
            self.drawthepart( self.pic180, ( 0, 40, 40, 40 ) )
            
        elif self.body[-1][4] == pygame.K_LEFT and self.body[-1][3] == True:
            self.drawthepart( self.pic180, ( 0, 0, 40, 40 ) )


# Apple class
# An idea for future releases:
# Make an apple which gives you speed for some time (increases ticks FPS in game)
class Apple:

    def __init__( self, pos_range, size, picture, surface ):
        self.pos_range = pos_range
        self.size = size
        self.pic = picture
        self.pos = (-120,-120) # first position of apple
        self.surface = surface


    def new_pos( self, snake_body ):
        
        collision = True

        while collision:
            collision = False
            new_position =  [random.randrange(self.pos_range[0],self.pos_range[1]) * self.size,
                             random.randrange(self.pos_range[2],self.pos_range[3]) * self.size]
            for cell in snake_body:
                if new_position == cell[:2]:
                    collision = True

            if new_position == self.pos:
                collision = True

        self.pos = new_position
        
    def draw( self ):
        self.surface.blit( self.pic, self.pos )

    def get_pos( self ):
        return list(self.pos)


# Starting the game as a fuction, so that other files could start this
def snake_game( FPS = 5, point_limit = 30, windowCaption = 'Snake testing' ):

    pygame.init()

    #Some variables

    # An Idea for later versions:
    # -- Chnage the display size during later levels, the dsisplay size could be passed as a parameter
    display_size = [ 800, 600 ]
    initialSurface = pygame.display.set_mode( display_size )
    pygame.display.set_caption( windowCaption )
    game_clock = pygame.time.Clock()
    cell_size = 40
    score = 0
    highscore = 0
    display_size_cells = [ 0, display_size[0]//cell_size, 0, display_size[1]//cell_size]


    # Defining fonts here and preseting pictures here
    GAME_FONT = pygame.font.Font( 'media/fonts/arial.ttf', cell_size )
    score_pic = GAME_FONT.render( 'Score: '+str(score) + '/'+str(point_limit), True,(0,0,0) )
    highscore_pic = GAME_FONT.render( 'Highscore: '+str(highscore), True, (0,0,0) )


    # Changing surface options and drawing machanism when creating Snake object
    # -- Adding 'initialSurface' variable for a Class to use it
    # Creating Snake with the size of 3
    SNAKE = Snake( [[120,120,pygame.K_UP,False],
                    [120,80,pygame.K_UP,False,pygame.K_DOWN],
                    [120,40,pygame.K_UP,False,pygame.K_DOWN]],
                   cell_size, pygame.image.load('media/pictures/snake.png').convert_alpha(),
                   display_size, initialSurface )

    # Right now changing surface options with Snake, later we will move with apple

    APPLE = Apple( display_size_cells, cell_size, pygame.image.load('media/pictures/apple.png').convert_alpha(), initialSurface )

    # Maybe its possible to call a new apple method inside the apple class so that the would be no need to call it here [0.2 update?]
    APPLE.new_pos( SNAKE.body )


    gameIsRunning = True
    while gameIsRunning:

        # the game update loop and buttons
        turn = None
        for event in pygame.event.get():
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_UP or event.key == pygame.K_w:
                    turn = pygame.K_UP
                elif event.key == pygame.K_DOWN or event.key == pygame.K_s:
                    turn = pygame.K_DOWN
                elif event.key == pygame.K_RIGHT or event.key == pygame.K_d:
                    turn = pygame.K_RIGHT
                elif event.key == pygame.K_LEFT or event.key == pygame.K_a:
                    turn = pygame.K_LEFT
                elif event.key == pygame.K_SPACE:
                    SNAKE.die()

        # if you lose the game state changes                                
            elif event.type == pygame.QUIT:
                gameIsRunning = False
                result_of_game = 'quit'

        res = SNAKE.update( turn, APPLE )


        if res == 'point':
            score += 1
            score_pic = GAME_FONT.render( 'Score: '+str(score) + '/'+str(point_limit), True,(0,0,0) )

            if score > highscore:
                highscore = score
                highscore_pic = GAME_FONT.render( 'Highscore: '+str(highscore), True,(0,0,0) )
            if score >= point_limit:
                pygame.time.wait( 2000 )
                RUNNING = False
                result_of_game = 'win'
        elif res == 'died':
            score = 0
            score_pic = GAME_FONT.render( 'Score: '+str(score) + '/'+str(point_limit), True,(0,0,0) )


        # Drawing game elements on the surface
        # Snake and Apple now have draw methods, which draw the parts on surfaces
        initialSurface.fill( ( 255,255,255 ) )
        SNAKE.draw()
        APPLE.draw()


        # Drawing score and highscore, this could be added into seperate methods or class if an idea will come up regarding fancier score displays
        initialSurface.blit( score_pic, (0,0) )
        initialSurface.blit( highscore_pic, (display_size[0] - highscore_pic.get_width(), 0) )

        # All the update methods down below
        game_clock.tick( FPS )
        pygame.display.update()

    return result_of_game


# If the game is tarted from this file, launch the game with the default parameters
if __name__ == "__main__":
    snake_game()
    pygame.quit()








