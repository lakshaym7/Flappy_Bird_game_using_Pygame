import pygame
import sys
import random #to generate random numbers
from pygame.locals import* #basic pygame imports
pygame.init()

#=======Game Variables========
screen_width=392
screen_height=700
screen=pygame.display.set_mode([screen_width,screen_height])
clock=pygame.time.Clock()
game_font=pygame.font.Font('04B_19.ttf',30)

def welcome_screen(): #shows welcome images on the screen
    start_surface_1=game_font.render('=>Press SPACE to',True,(0,0,0))
    start_surface_2=game_font.render('    Start the Game',True,(0,0,0))
    game_function_surface_1=game_font.render("=>Press 'UP' Arrow for",True,(255,255,255))
    game_function_surface_2=game_font.render("    the Bird to Flap",True,(255,255,255))
    start_rect_1=start_surface_1.get_rect(center=(180,460))
    start_rect_2=start_surface_2.get_rect(center=(185,500))
    game_function_rect_1= game_function_surface_1.get_rect(center=(185,550))
    game_function_rect_2= game_function_surface_2.get_rect(center=(185,590))
    exit_surface_1=game_font.render('=>Press Esc to ',True,(0,0,0))
    exit_surface_2=game_font.render('    Exit the Game',True,(0,0,0))
    exit_rect_1=exit_surface_1.get_rect(center=(180,640))
    exit_rect_2=exit_surface_2.get_rect(center=(180,680))
    while True:
        for event in pygame.event.get():
            if event.type==QUIT or (event.type==KEYDOWN and event.key==K_ESCAPE):
                pygame.quit()
                sys.exit()
            elif event.type==KEYDOWN and event.key==K_SPACE:
                return #goes back to the function call statement
            else:
                screen.blit(background,(0,0))
                screen.blit(floor_surface,(0,screen_height-floor_surface.get_height()+50))
                screen.blit(message,(100,150))
                screen.blit(start_surface_1,start_rect_1)
                screen.blit(start_surface_2,start_rect_2)
                screen.blit(game_function_surface_1, game_function_rect_1)
                screen.blit(game_function_surface_2, game_function_rect_2)
                screen.blit(exit_surface_1,exit_rect_1)
                screen.blit(exit_surface_2,exit_rect_2)
            pygame.display.update()
    

def main_game():
    #=========Main Game Functions=========#
    def draw_floor():
        screen.blit(floor_surface,[floor_x_position,screen_height-floor_surface.get_height()+50])
        screen.blit(floor_surface,[floor_x_position+392,screen_height-floor_surface.get_height()+50])
    def draw_background():
        screen.blit(background,[background_x_position,0])
        screen.blit(background,[background_x_position+392,0])
    def create_pipes():
        random_pipe_position=random.choice(pipe_height)
        bottom_pipe=pipe_surface.get_rect(midtop=(700,random_pipe_position))
        top_pipe=pipe_surface.get_rect(midbottom=(700,random_pipe_position-200))
        return bottom_pipe,top_pipe
    def move_pipes(pipes): #take a list of pipes and move them to the left 
        for pipe in pipes:
            pipe.centerx-=5
        return pipes
    def draw_pipes(pipes): #for blitting pipes on the screen
        for pipe in pipes:
            if pipe.bottom>=700:
                screen.blit(pipe_surface,pipe)
            else:
                flip_pipe=pygame.transform.flip(pipe_surface,False,True) #x coordinate is false because we need not rotate it in that way
                screen.blit(flip_pipe,pipe)
    def check_collisions(pipes):
        for pipe in pipes:
            if bird_rect.colliderect(pipe):
                hit_sound.play()
                return False
        if bird_rect.top<=0 or bird_rect.bottom>=(screen_height-floor_surface.get_height()+50):
            die_sound.play()
            return False
        else:
            return True
    def rotate_bird(bird):
        new_bird=pygame.transform.rotozoom(bird,-bird_movement*3,1)
        return new_bird
    def bird_animation(): #used to add a rectangle around all the bird_surfaces
        new_bird=bird_frames[bird_index]
        new_bird_rect=new_bird.get_rect(center=(100,bird_rect.centery)) #we take the center y coordinate of the previous bird rectangle so that we do not change the bird's postion
        return new_bird,new_bird_rect
    def display_score(game_state):
        if game_state=='main_game':
            score_surface=game_font.render('Score: '+str(int(score)),True,(255,255,255)) #True means anti-aliased which means the text looks too sharp
            score_rect=score_surface.get_rect(center=(196,50))
            screen.blit(score_surface,score_rect)
        if game_state=='game_over':
            score_surface=game_font.render('Score: '+str(int(score)),True,(255,255,255)) #True means anti-aliased which means the text looks too sharp
            score_rect=score_surface.get_rect(center=(196,50))
            screen.blit(score_surface,score_rect)
            
            restart_surface_1=game_font.render('Press SPACE to',True,(0,0,0))
            restart_surface_2=game_font.render('Restart the Game',True,(0,0,0))
            restart_surface_3=game_font.render('Or Press ESC',True,(0,0,0))
            restart_surface_4=game_font.render('to Exit the Game',True,(0,0,0)) 
            high_score_surface=game_font.render('High Score: '+str(int(high_score)),True,(255,255,255)) #True means anti-aliased which means the text looks too sharp
            restart_rect_1=restart_surface_1.get_rect(center=(196,450))
            restart_rect_2=restart_surface_2.get_rect(center=(196,490))
            restart_rect_3=restart_surface_3.get_rect(center=(196,550))
            restart_rect_4=restart_surface_4.get_rect(center=(196,590))
            high_score_rect=high_score_surface.get_rect(center=(196,120))
            screen.blit(high_score_surface,high_score_rect)
            screen.blit(restart_surface_1,restart_rect_1)
            screen.blit(restart_surface_2,restart_rect_2)
            screen.blit(restart_surface_3,restart_rect_3)
            screen.blit(restart_surface_4,restart_rect_4)
    def update_score(score,high_score):
        if score>high_score:
            high_score=score
        return high_score
            
        

    #=======Main Game Variables (Locals Variables)=====#
    gravity=0.25
    bird_movement=0 #to move the bird_rect which in turn changes the position of the bird_surface
    floor_x_position=0
    background_x_position=0
    pipe_list=[]
    game_active=True
    score=0
    high_score=0
    score_sound_countdown=100
    bird_downflap=pygame.transform.scale2x(pygame.image.load('assets/yellowbird-downflap.png').convert_alpha())
    bird_midflap=pygame.transform.scale2x(pygame.image.load('assets/yellowbird-midflap.png').convert_alpha())
    bird_upflap=pygame.transform.scale2x(pygame.image.load('assets/yellowbird-upflap.png').convert_alpha())
    bird_frames=[bird_downflap,bird_midflap,bird_upflap]
    bird_index=0
    bird_surface=bird_frames[bird_index]
    bird_rect=bird_surface.get_rect(center=[70,350])
    spawnpipe=pygame.USEREVENT #it is an event triggered by a timer
    bird_flap=pygame.USEREVENT+1    
    pygame.time.set_timer(spawnpipe,1200) #this creates a  pipe for every 1200 milliseconds
    pygame.time.set_timer(bird_flap,200) #this changes the flapping of the bird for every 200 milliseconds
    pipe_height=[250,350,450,550]
    game_over_surface=pygame.transform.scale2x(pygame.image.load('assets/gameover.png').convert_alpha())
    game_over_rect=game_over_surface.get_rect(center=[196,300])
    
    while True:
        for event in pygame.event.get():
            if event.type==pygame.QUIT or (event.type==KEYDOWN and event.key==K_ESCAPE):
                pygame.quit()
                sys.exit()
            if event.type==pygame.KEYDOWN:
                if event.key==pygame.K_UP and game_active==True:
                    bird_movement=0
                    bird_movement-=10
                    flap_sound.play()
                if event.key==pygame.K_SPACE and game_active==False:
                    game_active=True
                    pipe_list.clear()
                    bird_rect.center=[70,350]
                    bird_movement=0
                    score=0
            if event.type==spawnpipe:
                pipe_list.extend(create_pipes())
            if event.type==bird_flap:
                if bird_index<2:
                    bird_index+=1
                else:
                    bird_index=0
                bird_surface,bird_rect=bird_animation()
        
        if game_active:
            #background   
            background_x_position-=1
            draw_background()
            if background_x_position<=-392:
                background_x_position=0
        
            #bird   
            bird_movement+=gravity
            rotated_bird=rotate_bird(bird_surface)
            bird_rect.centery+=int(bird_movement)
            screen.blit(rotated_bird,bird_rect)

            game_active=check_collisions(pipe_list)

            #pipe
            pipe_list=move_pipes(pipe_list)
            draw_pipes(pipe_list)


            #floor
            floor_x_position-=1
            draw_floor()
            if floor_x_position<=-392:
                floor_x_position=0

            score+=0.01
            display_score('main_game')
            score_sound_countdown-=1 #for each cycle, the countdown decreases and if it gets to zero, the score_sound is played
            if score_sound_countdown<=0:
                score_sound.play()
                score_sound_countdown=100

        else:
            screen.blit(background,(0,0))
            screen.blit(floor_surface,(0,screen_height-floor_surface.get_height()+50))
            screen.blit(game_over_surface,game_over_rect)
            high_score=update_score(score,high_score)
            display_score('game_over')
            
        pygame.display.update()
        clock.tick(100) #maximum speed with which the game runs
        
    
#__Main__
pygame.init() #initializes all the pygame modules   
pygame.display.set_caption('FLAPPY BIRD') #creates a caption in the window 
message=pygame.image.load('assets/message.png').convert_alpha()
floor_surface=pygame.transform.scale2x(pygame.image.load('assets/base.png').convert_alpha()) #converts the image in the form of a file that could be easily executed by pygame
background=pygame.transform.scale2x(pygame.image.load('assets/background-day.png').convert_alpha())
pipe_surface=pygame.transform.scale2x(pygame.image.load('assets/pipe-green.png').convert_alpha())
flap_sound=pygame.mixer.Sound('sound/sfx_wing.wav')
hit_sound=pygame.mixer.Sound('sound/sfx_hit.wav')
die_sound=pygame.mixer.Sound('sound/sfx_die.wav')
score_sound=pygame.mixer.Sound('sound/sfx_point.wav')
welcome_screen() #shows welcome screen to the user until the user presses any button
main_game() #this is main game function

