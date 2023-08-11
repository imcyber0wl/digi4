import pygame
import sys
import time
import threading
import os

cwd=(os.getcwd())+"/"

pygame.init()
screen_x=600
screen_y=500
screen_res=(screen_x, screen_y)
screen=pygame.display.set_mode(screen_res)
background=pygame.image.load(cwd+"background.jpg")
screen.blit(background,(0,0))
pygame.display.update()


playersize_x=100
playersize_y=40
stage_x=0 #how much the player have moved to the right
stage_limit=900 #player can only move 2000 

#ALL IMAGES
player=pygame.image.load(cwd+"player.png")
player=pygame.transform.scale(player,(playersize_x,playersize_y))

bullet1_wid=15
bullet1_hi=6
bullet1=pygame.image.load(cwd+"bullet.png")
bullet1=pygame.transform.scale(bullet1,(bullet1_wid,bullet1_hi))

damage=pygame.image.load(cwd+"damage.png")

megaman=pygame.image.load(cwd+"megaman.png")
megaman_height=100
megaman_width=55
megaman=pygame.transform.scale(megaman,(megaman_width,megaman_height))


rock=pygame.image.load(cwd+"obs2.png")
rock=pygame.transform.scale(rock,(100,70))

###Player x y vel
player_limit_x_left=10
player_limit_x_right=310

player_x=player_limit_x_left
player_y=(screen_y-2)-playersize_y
floor=player_y

vel=10
direction="n" #where the player is movings
face_direction='r' #where the player is facing

global flag
flag=0  #used to know if a collision was detected or no

##stage example
#each one is: object, x, y, x_size, y_size, 0 for wall
stage=[(rock,100,240,100,70,0),
       (rock,270,450,100,70,0),
       (rock,350,240,100,70,0),
       (rock,500,450,100,70,0),
       (rock,520,240,100,70,0),
       (rock,640,450,100,70,0),
       (rock,800,240,100,70,0),
       (rock,920,450,100,70,0),
       (rock,1120,240,100,70,0),
       (rock,2170,450,100,70,0)]

#special stage includes enemies, bullets, and items only. 
special_stage=[(0,0,0,0,0,0),(0,0,0,0,0,0),
               (0,0,0,0,0,0),(0,0,0,0,0,0),
               (megaman,270,450-megaman_height,megaman_width,megaman_height,2)
               ,(0,0,0,0,0,0),(0,0,0,0,0,0),(0,0,0,0,0,0),(0,0,0,0,0,0)]
special_stage_counter=0 #how many objects are in special stage?


########## When the player moves, this function updates each
# element in the stage list, decreasing or increasing the X of each element
def stage_loader(stage,direction):
    i=0
    while i!=len(stage)-1:
        stage_o=stage[i]
        x=stage_o[1]
        if direction=="r":
            x-=vel
        elif direction=="n" or direction=='u' or direction=='d':
            i=len(stage)-2
        else:
            x+=vel

        stage[i]=(stage_o[0],x,stage_o[2],stage_o[3],stage_o[4],stage_o[5])            
        i+=1

    return stage

####################### blitts stage. s=1 for special stage 
def stage_blitter(stage,s=0):
    global screen
    i=len(stage)-1
    n=0
    x=0
    #### Get all elements that have an x/x+size between 0  and screen width
    ### side note: some collisions where element's x is less than 0 may not be detected
    ### because code in walls() was written to pick elements where x>=0 lol, so just copy paste this loop there
    while n!=len(stage)-1 and s!=1:
        x=stage[n]
        size=x[3]
        x=x[1]
        if x+size>=0:
            x=n
            n=len(stage)-1
        else:
            n+=1

    i=len(stage)-1
    n=x
    while n!=i:
        s=stage[n]
        if s[0]!=0: #if element exists
            screen.blit(s[0],(s[1],s[2]))
            x=s[1]
            if x>screen_x: #if the x of elements in stage cant be printed, stop
                n=i-1
        else:
            pass

        n+=1


##################### this function detects if player collided with an
## a wall and acts accordingly.
def walls(stage,direction,player_x,player_y,playersize_x,playersize_y):
    n=0
    r=0
    global flag
    flag=0
    size=playersize_x
    
    #### Get all  elements that have an x between 0  and screen width
    while n!=len(stage)-1:
        x=stage[n]
        x=x[1]
        if x>=0:
            x=n
            n=len(stage)-1
        else:
            n+=1

    # Here the code will check if there is any collision with elements on screen
    i=x
    while i<len(stage)-1:
        s=stage[i] 
        x=s[1]
        y=s[2]
        o_size_x=s[3]
        o_size_y=s[4]
        if x>310:  #310 is player limit
            i=len(stage)-1

        elif x<=310 and x>=-100 and s[5]==0:   #if object can touch player and object is wall
            ### if  pla|yer | or |player|
            rightcollied=player_x+size>=x #and player_x<=x
            ### if | pla|yer
            leftcollied=player_x<=x+o_size_x and player_x+size>x+o_size_x
            
            collision=player_x+size>x and player_x<x+o_size_x and player_y<y+o_size_y and player_y + playersize_y>y
            collision2=rightcollied and player_x<x+o_size_x and player_y<y+o_size_y and player_y + playersize_y>y
            collision3=leftcollied and player_y<y+o_size_y and player_y + playersize_y>y

            if direction=="r" and collision2==True:
                player_x=x-size
                i=len(stage)-1
                flag=1
                #print("right collision",player_x,x-o_size_x)

            elif direction=="l" and collision3==True:
                player_x=x+o_size_x
                i=len(stage)-1
                flag=1
                #print("left collision",player_x,x+o_size_x)

            elif direction=="u" and collision==True:
                player_y+=vel #return to where u were
                i=len(stage)-1
                flag=1
                #print("upper collision",player_y,y,y+o_size_y)
                
            elif direction=="d" and collision==True:
                player_y=y-playersize_y
                i=len(stage)-1
                flag=1
                #print("down collision",player_y,y-playersize_y)  

            else:
                if flag==0:
                    i+=1

        elif x<=310 and x>=-100 and s[5]==1:  #if object can touch player and it is passable
            pass

        elif x<=310 and x>=-100 and s[5]==4:  #if object can touch player and its item
            pass

        else:
            i+=1
             
    return [player_x,player_y]


### this was originally meant to be extended to be for both
### enemies and the player, but it only works for player
def bullet(bullet,x,y,wid,hi,damage,direction,speed):
    time.sleep(0.02)
    global screen
    global screen_x
    global special_stage
    global special_stage_counter
    my_counter=special_stage_counter
    special_stage_counter+=1
    
    n=0      ######## search for elements on screen
    s=0
    s2=0
    while n!=len(special_stage)-1:
        s=special_stage[n]
        s1=s[1]
        s2=s[5]
        if s1>=0 and s2==2:
            s2=n
            n=len(special_stage)-1
        else:
            n+=1

    i=s2

    if direction=="r":
        pass
    else:
        speed=speed*-1

    # in this loop, every time the bullet's x changes, it loops through all elements
    # in special stage to test if it collided with any of them
    while x+wid<screen_x+wid and x+wid>0:
        x+=speed
        special_stage[my_counter]=(bullet,x,y,wid,hi,2)
        time.sleep(0.04)
        counter=3
        while counter!=7: #3 to 6 is the place reserved for enemies in special stage is how much 
            s=special_stage[counter] 
            sx=s[1]
            sy=s[2]
            o_size_x=s[3]
            o_size_y=s[4]
            if sx<screen_x and sx>=-100 and s[5]==2:#if object can touch player and object is enemy
                if (x+wid>=sx and x<sx+o_size_x and y<y+o_size_y and y + hi>sy) or (x<=sx+o_size_x and x+wid>sx+o_size_x and y<sy+o_size_y and y + hi>sy):
                    special_stage[counter]=(0,0,0,0,0,0) #remove enemy from stage
                    x=screen_x #bullet disappears
                    damage=pygame.transform.scale(damage,(o_size_x,o_size_y)) #make damage rectangle in size of enenmy
                    screen.blit(damage,(sx,sy)) 
                    pygame.display.flip() #show damage on screen
                    counter=7 #break the loop 
                    #print(my_counter, "collision")
                else:
                    counter+=1
            else:
                counter+=1

    special_stage[my_counter]=(0,0,0,0,0,0) #remove bullet
    special_stage_counter-=1

### player jumps, was also meant to be used with enemies and player as well
def jump(x,y,ysize,floor):
    vel=4 #velocity of jump
    global player_y #it will be modified
    global stage
    global flag
    roof=player_y-ysize-65
    while player_y+ysize>roof:
        player_y-=vel
        player_y=walls(stage,"u",player_x,player_y,playersize_x,playersize_y)
        if flag==1:
            flag==0
            player_y=player_y[1]
            break
        player_y=player_y[1]
        time.sleep(0.01)
        
    while player_y<floor: #floor
        player_y+=vel
        player_y=walls(stage,"d",player_x,player_y,playersize_x,playersize_y)
        if flag==1:
            flag==0
            player_y=player_y[1]
            break #stop loop and dont modify player_y
        player_y=player_y[1]
        time.sleep(0.01)        
    


###### game loop 
while 1:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
            pygame.quit()
            sys.exit()
        pxb=player_x #player x backup, to know if player actually moved and didnt hit a wall

        direction="n"
        if event.type == pygame.KEYDOWN:
            
            if event.key == pygame.K_LEFT:
                direction="l"
                face_direction=direction
                player_x -= vel
                stage_x-=vel
                if player_x<player_limit_x_left:
                    player_x+=vel
                if stage_x<=player_limit_x_left:
                    stage_x+=vel
                    direction="n"

            if event.key == pygame.K_RIGHT:
                direction="r"
                face_direction=direction
                player_x += vel
                stage_x+=vel
                if stage_x>stage_limit:
                    player_x-=vel
                    stage_x=stage_limit
                    direction="n"
                elif player_x+playersize_x>player_limit_x_right:
                    player_x-=vel
            
            if event.key == pygame.K_UP:
                player_y -= vel
                direction="u"
                jump_thread=threading.Thread(target=jump,args=(player_x,player_y,playersize_y,floor))
                jump_thread.start()
            
            if event.key == pygame.K_DOWN:
                player_y += vel
                direction="d"
                if player_y+playersize_y>screen_y-2:
                    player_y=screen_y-(2+playersize_y)

            if event.key == pygame.K_l:
                thread=threading.Thread(target=bullet,args=(bullet1,player_x,player_y+10,
                    bullet1_wid,bullet1_hi,damage,face_direction,30))
                thread.start()
                time.sleep(0.001)

            #if player moved
            print(player_x,stage_x)
            if direction!='n':
                player_x=walls(stage,direction,player_x,player_y,playersize_x,playersize_y)
                player_y=player_x[1]
                player_x=player_x[0]
                if flag==0: #if player didnt collide
                    if direction=="r" or direction=="l":
                        if stage_x>=stage_limit or stage_x<=0:
                            #if player is in world limits, ignore
                            pass 
                        else:
                            #if no collision and palayer isnt at limits
                            stage=stage_loader(stage,direction) 
                            special_stage=stage_loader(special_stage,direction)
                    else:
                        #ignore this one, meant to be for direction=="u" or direction=="d"
                        stage=stage_loader(stage,direction)
                        special_stage=stage_loader(special_stage,direction)

                elif flag==1:
                    #if a collision is detected
                    #stage tracker doesnt change
                    if direction=="r":
                        stage_x-=vel 
                    elif direction=="l":
                        stage_x+=vel
                    else:
                        pass


    screen.blit(background,(0,0))
    stage_blitter(stage) #blit stage
    screen.blit(player,(player_x,player_y)) #blit player
    stage_blitter(special_stage,1) #blit special stage
    pygame.display.update()
    time.sleep(0.03)
