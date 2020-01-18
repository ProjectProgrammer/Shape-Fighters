
################################

# Minimum Specification --> Windows 7 x64, 4gb ram, intel core i5 2400k @ 2.7ghz.
#Pyscripter 2.5.30
#pygame PyGame 1.9.1

#http://portablepython.com/wiki/PortablePython2.7.6.1/
################################

import pygame as enviroment
import os
import time
import math
import random


image_assets = [] #An array used to store all images
number_of_images = 36 #Number of images used in this program
Enviromental_Physics = [(500,500),0.4,0,3] #Spawn location, gravity(pixel movement/sec), and change in ground position.
End_Execution = False #To end gameplay.
Ground_Pos = [0,550,0] #variables where we store the postition of the ground.

level = 1 #We currently start at level 1
#Variables for User Game Data
player_shots = [] #Here we store all our player shots. All shots in the function will be automatically controlled by the in game shot_manger()
entities_shot = [] #Here we store all our enemy shots. All shots in the function will be automatically controlled by the in game enemy manager.
entity = [] #This is where we store all our enemys currently on the screen.

instruction_load = 0 #This variable is used to display the 2nd page of the application. The instructions pages.


#This is how our level are controlled. We use boolean values as switches to determine the next in game events.
level_switch_1 = [True,False,False,False,False,False,False,False]
level_switch_2 = [True,False,False,False,False,False,False,False]
level_switch_3 = [True,False,False,False,False,False,False,False]
level_switch_4 = [True,False,False,False,False,False,False,False]
level_switch_5 = [True,False,False,False,False,False,False,False]
prompt_level_change = [True,False,False,False,False]
move_level_switch = [True,False,False,False,False,False]

#Since its level 1 we
background = 0

#Now we initalize our enviroment
enviroment.init()
#We set the display of our enviroment 1050x700
display = enviroment.display.set_mode((1050,700))

#we use turple unpacking to get our display width and height.
display_width,display_height = display.get_size()
clock = enviroment.time.Clock()


game_over= True
final_boss_defeated = False

#This is used to control some of the ennemy/player shots which require cpu time.
Game_Internal_Clock = enviroment.time.get_ticks()

#Classes

#This is a class to produce our enemy shots. Each shot performs the same function(damage the player), but they all have diffrent images and x,y starting points.
class Entity_Bullets(object):
    def __init__(self,image,x_pos,y_pos,direction):
        self.bullet_image = image #image of bullet.
        self.bullet_image_reflected = enviroment.transform.flip(self.bullet_image, True, False) #image of bullet if enemy is flipped.
        self.x_pos = x_pos #position of bullet.
        self.y_pos = y_pos+10 #we add 10 because we want it to be at the front of the enemy/player.
        self.bullet_rect = self.bullet_image.get_rect() #rect is used for rectangular collision detection.
        self.direction = direction # Direction can be forward or backwards
        self.start_time = enviroment.time.get_ticks() #start time is used for shooting time(pLayer wise)
        self.end_time = self.start_time

    def update_bullet_pos(self): #We update the bullets position for collision checking.
        self.bullet_rect.x = self.x_pos
        self.bullet_rect.y = self.y_pos



#This is the class for producing the enemies, and the player itself.
class Entities(object):
    def __init__(self,spawn_location,entity_image,entity_image_damaged,direction,health,speed,bullet_image):

        self.new_postition = [0,0] #Changes in position will be added here.
        self.x_cord = spawn_location[0] #inital spawn location x
        self.y_cord = spawn_location[1] #inital spawn location y.
        self.kill = 0 #Amount of kills player has done.
        self.entity_image = entity_image #image of player/enemy.
        self.entity_image_flipped = enviroment.transform.flip(self.entity_image, True, False)
        self.entity_rect = self.entity_image.get_rect() #each entity has a small invisible rectangle around it. If the rectangle collides with another rectangle, a collision has occured.
        self.entity_image_damaged = entity_image_damaged #Image of player changes if its been damaged.
        self.entity_image_damaged_flipped = enviroment.transform.flip(self.entity_image_damaged, True, False)
        self.entity_image_flipped_backup = enviroment.transform.flip(self.entity_image, True, False) #This is used to change damaged image of a player back to normal.
        self.entity_image_backup = entity_image
        self.bullet_image = image_assets[bullet_image] #this is the bullet image of the player.

        self.forward_pos = direction #direction of player.
        self.shoot_bullet = True #boolean to determine if player can shoot.
        self.shoot_start_time = enviroment.time.get_ticks()
        self.shoot_end_time = self.shoot_start_time
        self.reload_time = speed

        self.restore_image_time = 0 #we use a counter by adding 1 each loop.
        self.restore_image_run = False
        self.health = health
        self.damage_image_show = False
        self.score = 0 #score of player 1.


    def entity_motion_register(self):
            self.x_cord+=self.new_postition[0] #Here we add the changes to the players x,y cordination.
            self.y_cord+=self.new_postition[1]
            self.entity_rect.x = self.x_cord #We do the samething for the players invisible rectangle.. (rectangular collision position)
            self.entity_rect.y = self.y_cord


    def entity_delay_reload_shot(self): #This is only for the player, enemies has a predermined shooting time)
        self.shoot_start_time = enviroment.time.get_ticks()
        if(self.shoot_bullet): #if the player shoots, we record the current time.
            self.shoot_start_time = enviroment.time.get_ticks()
            self.shoot_end_time = self.shoot_start_time
        else: #if the time passed is greater than reload time, then player can shoot again.
            if(abs(self.shoot_start_time-self.shoot_end_time)>=self.reload_time):
                self.shoot_bullet = True


#File reading in python. I haven't tested this application in mac os x or linux, but it should work
#We get the absolute location of where the .py was excuted. Python has a habit of moving the .py to a seperate folder, and we cannot access our resources.
absolute_location = os.path.abspath(os.path.dirname(__file__))
def load_images(): #Each image has a number labled on it eg --> 1.png. This is used to easily load all our image assets.
    global image_assets
    for each_image in range(1,number_of_images+1,1):
        image_location = os.path.join(absolute_location, "resources/"+ str(each_image) +".png")
        image_assets.append(enviroment.image.load(image_location).convert_alpha())


load_images() #Now we load all our images.
player_1 = Entities(Enviromental_Physics[0],image_assets[4],image_assets[5],True,10,1500,6) #we create an player object, in which we can control.



def create_player_bullets(): #When called, we crate a bullet, and save it to the player_shot array.
    global player_shots,player_1
    player_shots.append((Entity_Bullets(player_1.bullet_image,player_1.x_cord,player_1.y_cord,player_1.forward_pos)))

def render_player_bullets(): #This function will automatically move all bullets 6 pixels left or right, depending on the direction of the player.
    global player_shots
    while(True): #loops until all player bullets move 2 pixels left.
        for bullets in range(len(player_shots)): #If the bullet goes of range, we erase the bullet from the array.
            if (player_shots[bullets].x_pos<=20 or player_shots[bullets].x_pos>=display_width-20):
                del player_shots[bullets] #since we erased the bullet from array, the bullet length is now incorrect/out of range, therefore we must reload this for loop with our new loop.
                break
            else: #the player can face 2 direction left or right, so we must draw the images of the bullet depending on the players direction.
                if(player_shots[bullets].direction):
                    player_shots[bullets].x_pos+=6
                    display.blit(player_shots[bullets].bullet_image, (player_shots[bullets].x_pos, player_shots[bullets].y_pos)) #we draw picture of our normal image.
                    player_shots[bullets].update_bullet_pos() #we update the positions of the players bullet.
                else:
                    player_shots[bullets].x_pos-=6
                    display.blit(player_shots[bullets].bullet_image_reflected, (player_shots[bullets].x_pos, player_shots[bullets].y_pos)) #we draw the image of our reflected bullet
                    player_shots[bullets].update_bullet_pos()

        break

#here we create a enemy bullet, and save its location in an array.
def create_enemy_bullets(bullet_image,x_cord,y_cord,direction):
    global entities_shot
    entities_shot.append((Entity_Bullets(direction,bullet_image,x_cord,y_cord)))

#,spawn_location,entity_image,entity_image_damaged
def create_enemy(x,y,image,damaged,direction,health,speed,bullet_image):
    global entity
    entity.append(Entities([x,y],image_assets[image],image_assets[damaged],direction,health,speed,bullet_image))





#Almost same thing as render_player_bullets, but we use it for rendering enemy bullets.
def render_enemy_bullets():
    global entities_shot
    while(True):
        for bullets in range(len(entities_shot)):
            if (entities_shot[bullets].x_pos<=20 or entities_shot[bullets].x_pos>=display_width-20): #out of bound
                del entities_shot[bullets]
                return render_enemy_bullets()

            if(entities_shot[bullets].direction):
                entities_shot[bullets].x_pos-=5
                display.blit(entities_shot[bullets].bullet_image, (entities_shot[bullets].x_pos, entities_shot[bullets].y_pos))
                entities_shot[bullets].update_bullet_pos()
            else:
                entities_shot[bullets].x_pos+=5
                display.blit(entities_shot[bullets].bullet_image_reflected, (entities_shot[bullets].x_pos, entities_shot[bullets].y_pos))
                entities_shot[bullets].update_bullet_pos()
        break

#This function renders the enemy, and updates its positions in case there was collision between the players bullet and the enemy.

def render_enemy():
    global entity,player
    for each_enemy in range(len(entity)):
        if( not entity[each_enemy].forward_pos): #we check the direction of the enenmy. if its not forward.

            display.blit(entity[each_enemy].entity_image_flipped, (entity[each_enemy].x_cord, entity[each_enemy].y_cord)) #we use the flipped image of enemy
            entity[each_enemy].entity_motion_register() #we register/update the enemies rectangle. (collision box)
            entity[each_enemy].entity_delay_reload_shot() #We allow the enemy to shoot.

            if(entity[each_enemy].shoot_bullet): # we now have a cool down for the enemies shot.
                create_enemy_bullets(entity[each_enemy].x_cord,entity[each_enemy].y_cord,entity[each_enemy].forward_pos,entity[each_enemy].bullet_image)
                entity[each_enemy].entity_delay_reload_shot() #now we delay the reload shot.
                entity[each_enemy].shoot_bullet = False

        else:
            display.blit(entity[each_enemy].entity_image, (entity[each_enemy].x_cord, entity[each_enemy].y_cord)) #we check if the direction of enemy is forward.
            entity[each_enemy].entity_motion_register()
            entity[each_enemy].entity_delay_reload_shot()

            if(entity[each_enemy].shoot_bullet):
                create_enemy_bullets(entity[each_enemy].x_cord,entity[each_enemy].y_cord,entity[each_enemy].forward_pos,entity[each_enemy].bullet_image)
                entity[each_enemy].entity_delay_reload_shot()
                entity[each_enemy].shoot_bullet = False


def collision_check_towards_player():
    global entities_shot,player_1,End_Execution
    while(True): #go through the entire list of bullets, until there is no delection of bullets.
        for each_bullet in range(len(entities_shot)): #we go through the entire list of the enemy bullets.
            if(entities_shot[each_bullet].bullet_rect.colliderect(player_1.entity_rect)): #if the rectangles of any of the bullets collide with the player.
                player_1.health-=1 #we take away 1 hp point
                player_1.score -=10 #and we take away 10 points
                if(player_1.health == 0): #if player is 0, we end the game.
                    End_Execution = True
                else:

                    if(player_1.forward_pos): #if the player has more health, we check the direction.
                        player_1.x_cord-=20 #if he forward, he get impacted by bullet and goes back 20 pixels
                    else:
                        player_1.x_cord+=20 # if hes backwarrd, and get impacted, he goes forward 20 pixels
                    player_1.entity_image = player_1.entity_image_damaged #we display the image of the damaged player since he got impacted
                    player_1.entity_image_flipped = player_1.entity_image_damaged_flipped
                    player_1.restore_image_run = True
                    del entities_shot[each_bullet] #we delete the image of the enemy bullet.
                    break

        break


def collision_check_towards_enemy(): #same thing as collision_check_towards_player, but instead its towards enemy.
    global player_shots,player_1,entity
    for each_entity in range(len(entity)): #double for loop, to check if any of the players bullet has hit any of the enemys avaliable.
        for each_bullet in range(len(player_shots)):
            if(player_shots[each_bullet].bullet_rect.colliderect(entity[each_entity].entity_rect)):
                entity[each_entity].health-=1
                if(entity[each_entity].health<=0):
                    player_1.kill+=1 #if player has killed an enemy, he gains a kill
                    player_1.score+=100 #his score goes up by 100
                    del entity[each_entity] #we delete the enemy from array
                    del player_shots[each_bullet] #we delete the player from array.
                    return collision_check_towards_enemy() #reload this function since the length of array is now incorrect.
                if(entity[each_entity].forward_pos):
                    entity[each_entity].x_cord+=10 #if there is a collision we push the enemy by 10 pixels. depending on the directions.
                    del player_shots[each_bullet]
                    return collision_check_towards_enemy()
                else:
                    entity[each_entity].x_cord-=10
                    del player_shots[each_bullet]
                    return collision_check_towards_enemy()



def body_collision_check(): #we do body collision checks.
    global entity,player_1
    for each_entity in range(len(entity)): #we check if the player has collied with any of the enemies..
        if(player_1.entity_rect.colliderect(entity[each_entity].entity_rect)):
            player_1.health-=1
            if(player_1.health <= 0): #if the players health is 0 or less than 0, the game ends.
                End_Execution = True
            else:

                if(player_1.forward_pos): #if not, then the player goes back a signficant distance to correct their behaviour
                    player_1.x_cord-=90
                else:
                    player_1.x_cord+=90
                    player_1.entity_image = player_1.entity_image_damaged
                    player_1.entity_image_flipped = player_1.entity_image_damaged_flipped
                    player_1.restore_image_run = True
                    break



#Player Declaration
load_images()




#Our level function basically spawns an enemy, and then disables parts of itself.
#These functions work in a sequential matter, and will not proceed until a condition is satisfied.
#these conditions are dependent on the amount of enemies the player has killed.
def level_1():
    global level_switch_1,create_enemy,background,move_level_switch,level,player_1
    background = 0
    level = 1
    if(level_switch_1[0]): #sub level1
        create_enemy(800,500,7,9,True,3,3200,9) #we create an enemy using the create enemy function.

        level_switch_1[0] = False #after we created enemy we disable this if statement
        level_switch_1[1] = True #and enable the next.


    if(level_switch_1[1]): #Now we keep checking if the playe has killed the spawned enemies.
        if(player_1.kill==1):
            level_switch_1[1] = False #if he did we disable this if statement and turn on the next.
            level_switch_1[2] = True


    if(level_switch_1[2]): #now we spawn more enemies.
        level_switch_1[2] = False #We now disable this if statement, and turn on the next.
        level_switch_1[3] = True
        create_enemy(900,500,7,9,True,3,3000,9) #spawn 2 enemies.
        create_enemy(60,500,7,9,False,3,3000,9)


    if(level_switch_1[3]): #we now check if the player has killed the spawned enemies.
        if(player_1.kill==3): #if the player did, we disable this if statement and enable the next.
            level_switch_1[3] = False
            level_switch_1[4] = True

    if(level_switch_1[4]): #we spawn 2 more enemies.
        level_switch_1[4] = False
        level_switch_1[5] = True
        create_enemy(240,500,7,9,False,3,3000,9)
        create_enemy(60,500,7,9,False,3,3000,9)

    if(level_switch_1[5]): #we check if enemies are killed, and load next switch.
        if(player_1.kill==5):
            level_switch_1[5] = False
            level_switch_1[6] = True

    if(level_switch_1[6]): #we spawn more enmies.
        level_switch_1[6] = False
        level_switch_1[7] = True
        create_enemy(240,480,10,12,False,10,1300,9)
        create_enemy(900,500,7,9,True,3,3000,9)

    if(level_switch_1[7]): #Once all the enemies in this level are killed, we now move to the next level. We also use boolean as switches to move between levels.
        if(player_1.kill==7): #if the player killed all enemies in this level,
            level_switch_1[7] = False #we disable this if statement
            move_level_switch[0] = False #we disable this level
            move_level_switch[1] = True #we enable the next level.
            player_1.health+=5 #To make this game way easier, we add lives to the player.

#kills ends off with 7



#each new level uses diffrent enemies, or reuses them. When creating an enemy we refer list of images we saved.

def level_2(): #this function is the exact same as level 1, but with stronger enemies (using paramenters) diffrent background and same amount of swithches.
    global level_switch_2,create_enemy,background,move_level_switch,level,player_1
    background = 1
    level = 2
#kills starts off with 7



    if(level_switch_2[0]): #sub level 1
        create_enemy(800,490,13,15,True,4,2800,15)
        create_enemy(80,490,13,15,False,4,2800,15)
        level_switch_2[0] = False
        level_switch_2[1] = True

    if(level_switch_2[1]): #switch 1
        if(player_1.kill==9):
            level_switch_2[1] = False
            level_switch_2[2] = True

    if(level_switch_2[2]): #sub level 2
        create_enemy(800,400,13,15,True,4,2800,15)
        create_enemy(80,400,13,15,False,4,2800,15)
        create_enemy(900,500,7,9,True,3,3000,9)
        create_enemy(60,500,7,9,False,3,3000,9)

        level_switch_2[2] = False
        level_switch_2[3] = True

    if(level_switch_2[3]): #switch 2
        if(player_1.kill==13):
            level_switch_2[3] = False
            level_switch_2[4] = True

    if(level_switch_2[4]): #sub level 3
        create_enemy(800,400,13,15,True,4,3000,15)
        create_enemy(80,400,13,15,False,4,3000,15)
        create_enemy(900,300,13,15,True,3,3200,15)
        create_enemy(60,300,13,15,False,3,3200,15)
        create_enemy(900,500,7,9,True,3,4000,9)
        create_enemy(60,500,7,9,False,3,4000,9)
        level_switch_2[4] = False
        level_switch_2[5] = True

    if(level_switch_2[5]): #switch 3
        if(player_1.kill==19):
            level_switch_2[5] = False
            level_switch_2[6] = True

    if(level_switch_2[6]): #sub level 4
        create_enemy(800,450,16,17,True,5,1800,15)
        create_enemy(200,450,16,17,False,5,1800,15)
        create_enemy(900,500,7,9,True,3,3000,9)
        create_enemy(60,500,7,9,False,3,3000,9)
        level_switch_2[6] = False
        level_switch_2[7] = True

    if(level_switch_2[7] == True):
        if(player_1.kill == 23):
            player_1.health+=7
            move_level_switch[1] = False
            move_level_switch[2] = True


#This function is the same as level 1 and level 2.
def level_3():
    global level_switch_3,create_enemy,background,move_level_switch,level
    background = 2
    level = 3

    if(level_switch_3[0]): #sub level 1
        create_enemy(800,400,20,19,True,4,2800,19)
        level_switch_3[0] = False
        level_switch_3[1] = True

    if(level_switch_3[1]):
        if(player_1.kill == 24):
            level_switch_3[1] = False
            level_switch_3[2] = True

    if(level_switch_3[2]): #sub level 1
            create_enemy(800,400,20,19,True,4,2800,19)
            create_enemy(80,400,20,19,False,4,2800,19)
            level_switch_3[2] = False
            level_switch_3[3] = True

    if(level_switch_3[3]):
        if(player_1.kill == 26):
            level_switch_3[3] = False
            level_switch_3[4] = True

    if(level_switch_3[4]): #sub level 1
            create_enemy(800,400,32,34,True,4,2800,33)
            create_enemy(80,400,32,34,False,4,2800,33)
            create_enemy(900,500,7,9,True,3,3000,9)
            create_enemy(60,500,7,9,False,3,3000,9)
            level_switch_3[4] = False
            level_switch_3[5] = True

    if(level_switch_3[5]):
        if(player_1.kill == 30):
            level_switch_3[5] = False
            level_switch_3[6] = True

    if(level_switch_3[6]):
            create_enemy(800,500,32,34,True,4,2800,33)
            create_enemy(80,500,32,34,False,4,2800,33)
            create_enemy(800,400,32,34,True,4,2800,33)
            create_enemy(80,400,32,34,False,4,2800,33)
            level_switch_3[6] = False
            level_switch_3[7] = True

    if(level_switch_3[7]):
        if(player_1.kill == 34):
            level_switch_3[7] = False
            player_1.health+=9
            move_level_switch[2] = False
            move_level_switch[3] = True




#same function as level 1, 2,3
def level_4(): #we make this level where we fight all the boss there will only be 4 sub level, each level will have 2 boss on each side.
     global level_switch_4,create_enemy,background,move_level_switch,level
     background = 3
     level = 4

     if(level_switch_4[0]): #sub level 1
        create_enemy(150,480,11,12,False,6,1000,9)
        create_enemy(800,480,11,12,True,6,1000,9)
        level_switch_4[0] = False
        level_switch_4[1] = True

     if(level_switch_4[1]):
        if(player_1.kill == 36):
            level_switch_4[1] = False
            level_switch_4[2] = True

     if(level_switch_4[2]): #sub level 1
            create_enemy(800,400,21,19,True,6,2400,19)
            create_enemy(80,400,21,19,False,6,2400,19)
            level_switch_4[2] = False
            level_switch_4[3] = True

     if(level_switch_4[3]):
        if(player_1.kill == 38):
            level_switch_4[3] = False
            level_switch_4[4] = True

     if(level_switch_4[4]): #sub level 1
            create_enemy(800,450,17,17,True,5,1500,15)
            create_enemy(200,450,17,17,False,5,1500,15)
            create_enemy(900,500,8,9,True,3,2000,9)
            create_enemy(60,500,8,9,False,3,2000,9)
            level_switch_4[4] = False
            level_switch_4[5] = True

     if(level_switch_4[5]):
        if(player_1.kill == 42):
            level_switch_4[5] = False
            level_switch_4[6] = True

     if(level_switch_4[6]):
            create_enemy(800,500,35,35,True,5,1600,33)
            create_enemy(80,500,35,35,False,5,1600,33)
            create_enemy(800,400,35,35,True,5,1600,33)
            create_enemy(80,400,35,35,False,5,1600,33)
            level_switch_4[6] = False
            level_switch_4[7] = True

     if(level_switch_4[7]):
        if(player_1.kill == 46):
            level_switch_4[7] = False
            player_1.health+=16
            move_level_switch[3] = False
            move_level_switch[4] = True


#whats diffrent about this function is that it only uses 1 type of enemy.
def level_5(): #we will make this level where we fight the super ultra boss. This boss and 3 stages, each stage becomes more deadly each time.
     global level_switch_5,create_enemy,background,move_level_switch,level,game_over,final_boss_defeated
     background = 34
     level = 5

     if(level_switch_5[0]): #sub level 1
        create_enemy(700,480,22,22,True,14,800,9)
        level_switch_5[0] = False
        level_switch_5[1] = True

     if(level_switch_5[1]):
        if(player_1.kill == 47):
            level_switch_5[1] = False
            level_switch_5[2] = True

     if(level_switch_5[2]): #sub level 1
            create_enemy(800,480,23,23,True,8,1000,24)
            level_switch_5[2] = False
            level_switch_5[3] = True

     if(level_switch_5[3]):
        if(player_1.kill == 48):
            level_switch_5[3] = False
            level_switch_5[4] = True

     if(level_switch_5[4]): #sub level 1
            create_enemy(150,480,23,23,False,8,1000,24)
            level_switch_5[4] = False
            level_switch_5[5] = True

     if(level_switch_5[5]):
        if(player_1.kill == 49):
            level_switch_5[5] = False
            level_switch_5[6] = True

     if(level_switch_5[6]):
            create_enemy(150,480,24,24,False,8,1000,5)
            create_enemy(150,300,24,24,False,8,1000,33)
            level_switch_5[6] = False
            level_switch_5[7] = True

     if(level_switch_5[7]): #once the boss is over, we create a text on the screen saying the boss has been defeated. and disable all further levels.
        if(player_1.kill == 51):
            level_switch_5[7] = False
            move_level_switch[4] = False
            final_boss_defeated = True



def won_the_game(): #If the player has won the game, we will display text on the screen saying the boss has been defeated.
    game_over_font = enviroment.font.Font(os.path.join(absolute_location, "resources/ARCADECLASSIC.ttf"),25)
    game_over = game_over_font.render(("You have defeated the ultimate boss. Your journey will continues in another time, another place."), True, (255, 255, 255))
    display.blit(game_over, [50, 200])

def stage_manager(): #all levels will be executed in a sequential manner.
    global End_Execution
    if(move_level_switch[0]):
        level_1()
    elif(move_level_switch[1]):
        level_2()
    elif(move_level_switch[2]):
        level_3()
    elif(move_level_switch[3]):
        level_4()
    elif(move_level_switch[4]):
        level_5()







def render(): #here we render the players direction,the enemies, the stage(when to spawn enemies), and the direction of the player.
    global display,player_1
    stage_manager()
    render_player_bullets()
    render_enemy_bullets()
    render_enemy()
    if(player_1.forward_pos):
        display.blit(player_1.entity_image, (player_1.x_cord, player_1.y_cord))
    else:
        display.blit(player_1.entity_image_flipped, (player_1.x_cord, player_1.y_cord))



def collision_check(): #we call all functions that are involved with the collision. IT used to check if player/enemy has collided with anything
    collision_check_towards_player()
    collision_check_towards_enemy()
    body_collision_check()


menu_screen = True #since we starting the game, we turn on menu screen.




#Clear all variables,delete player object and recreate the game enviroment, once the exit button has been pressed or the player dies.
def reset():
    global player_shots,player_1,entity,level_switch_1,level_switch_2,level_switch_3,level_switch_4,level_switch_5
    global move_level_switch,instruction_load,prompt_level_change,won_the_game
    player_1 = Entities(Enviromental_Physics[0],image_assets[4],image_assets[5],True,10,1500,6)


    #Untab the bellow statement if this game is too hard, or takes too long to complete. Will give u 999 lives and rapid shooting rate.
    #player_1 = Entities(Enviromental_Physics[0],image_assets[4],image_assets[5],True,999,3,6)

    #here we undo all the changes we did to our variables, and reload our instructions page.
    final_boss_defeated = False
    level_switch_1 = [True,False,False,False,False,False,False,False]
    level_switch_2 = [True,False,False,False,False,False,False,False]
    level_switch_3 = [True,False,False,False,False,False,False,False]
    level_switch_4 = [True,False,False,False,False,False,False,False]
    level_switch_5 = [True,False,False,False,False,False,False,False]
    move_level_switch = [True,False,False,False,False]
    prompt_level_change = [True,False,False,False,False]
    instruction_load = 0 #reloading our instructions page.
    del entity[:] #deleting all enemy currently in game
    del entities_shot[:] #deleting all shots currently in the game.




font = enviroment.font.Font(os.path.join(absolute_location, "resources/ARCADECLASSIC.ttf"),25) #we load a cool arcade font
instructions = enviroment.font.Font(os.path.join(absolute_location, "resources/ARCADECLASSIC.ttf"),30)



def main_gameplay_stage(): #this is where we control the players movement.
    global player_1,entity,entities_shot,enviroment,Enviromental_Physics,End_Execution,Ground_Pos,Clock,menu_screen,level
    reset()
    while not End_Execution: #while the execution continues.
        for event in enviroment.event.get():
            if (event.type == enviroment.QUIT): #if the player exits the program
                End_Execution = True #he will be redirected to a gave over screen.
            if (event.type == enviroment.KEYDOWN): #if a key down was detected.
                if (event.key == enviroment.K_LEFT):
                    player_1.new_postition[0] = -4 #we keep moving 4 pixelx left if left button pressed
                    player_1.forward_pos = False
                elif (event.key == enviroment.K_RIGHT): #we keep moving 4 pixels right if the right button pressed.
                    player_1.new_postition[0] =  4
                    player_1.forward_pos = True
                elif (event.key == enviroment.K_DOWN): #we accelerate down faster if the down button is presed.
                    player_1.new_postition[1] =  5
                elif (event.key == enviroment.K_UP): #we add a counter so that the player can double jump.
                    if(Enviromental_Physics[2]!=2): #if the player has jumped 2 times, he can no longer juump.
                        player_1.new_postition[1] = -10
                        Enviromental_Physics[2] += 1
                elif (event.key == enviroment.K_SPACE): #if the spacebar is pressed, we check if the palyer can shoot, and then creates an bullet with a timer.
                    player_1.entity_delay_reload_shot()
                    if(player_1.shoot_bullet):
                        create_player_bullets()
                        player_1.entity_delay_reload_shot()
                        player_1.shoot_bullet = False
                #Trigger certain game events, For testing Only
        player_1.entity_motion_register() #we register the players x/y movements.

        if(player_1.health<=0): # if the player health is less than or equal to 0, we leave the game
            break

        player_1.new_postition[1] += Enviromental_Physics[1] # we update the postion of the enemy.


        if(player_1.y_cord>=display_height-210): #if the player goes beyond display height -210,
            player_1.y_cord= display_height-210 #we set the set the height at display -210, so that the player doesn't fall our of the map.
            player_1.new_postition[1] = 0 #we reset the changes in y position
            Enviromental_Physics[2] = 0 #we set changes in enviroment physics.
        if(player_1.x_cord>=display_width-20): # we allso do the same thing in the x axis. if the x location is beyond the screen, we prevent player from moving even further.
            player_1.x_cord=display_width-20
            player_1.new_postition[0] = 0

        if(player_1.x_cord<=20):
            player_1.x_cord=20
            player_1.new_postition[0] = 0



        #Drawing mode (Background + Road)
        display.blit(image_assets[background], [0, 0])#Background image @we always draw background first, from bottom layer to top layer.

        Ground_Pos[2]= Ground_Pos[0] % image_assets[18].get_rect().width #we get the remainder of width of rectangle
        Ground_Pos[0] -= Enviromental_Physics[3]
        display.blit(image_assets[18], (Ground_Pos[2] - image_assets[18].get_rect().width, Ground_Pos[1])) #and we draw it on to the screen.

        if(Ground_Pos[2]<display_width): #if the length is less than width of the screen, we set a new image.
            display.blit(image_assets[18],(Ground_Pos[2],Ground_Pos[1])) #this gives us an illusion that the palyer is constantly running.


        if(player_1.restore_image_run):  #we set a counter for how long the player will have an damaged image.
            if(player_1.restore_image_time>=5): # if the timer has ran out,we restore the players orginal image.
                player_1.entity_image = player_1.entity_image_backup
                player_1.entity_image_flipped = player_1.entity_image_flipped_backup
                player_1.restore_image_time = 0
                player_1.restore_image_run = False
            else:
                player_1.restore_image_time+=1



        render() # we call the render function and draws most of our stage.

        #here we draw our HUD, which includes important information.
        health = font.render("Health  "+ str(player_1.health), True, (255, 255, 255))
        stage = font.render(("Level  "+ str(level)), True, (255, 255, 255))
        score = font.render(("Score   "+ str(player_1.score)), True, (255, 255, 255))

        #we check if there is a collision between any objects.
        collision_check()

        #we draw our HUD onto the screen.
        display.blit(health, [50, 0])
        display.blit(stage, [50, 25])
        display.blit(score, [50, 50])

#if the final boss has been defeated, we will also show a text saying they have defeated the final boss.
        if(final_boss_defeated):
            won_the_game()

        #we update our display
        enviroment.display.update()
        #we set our clock speed to 62. clock speed is important since it decides how fast our game should be fps wise.
        clock.tick(62)
    menu_screen = True
    #we the game ends/ we sho the menu screen.


menu_screen = True

#we draw our welcome screen. with inputs.
def welcome_screen():
    global menu_screen,enviroment,End_Execution,instruction_load
    while(menu_screen):
        for event in enviroment.event.get(): #we get our key presses from a que.
                    if (event.type == enviroment.QUIT):
                        menu_screen = False
                        End_Execution = True

                    if (event.type == enviroment.KEYDOWN): #if a key was pressed down. event
                        if (event.key == enviroment.K_RETURN):  #if they key was enter.
                            instruction_load+=1 #we load the instructions page
                            if(instruction_load == 2): #if the user press enter again
                                menu_screen = False #we load the game
                                End_Execution = False   #we load the game
                                break

        if(instruction_load==0): #this is the beginning page.

                                #I used images as text, to make it harder to tamper with game files(change 1 file name, and the entire program stops working or behaves inccorectly.

            display.blit(image_assets[28], [0, 0])#Background image
            display.blit(image_assets[30], [250, 600])#Background image
            display.blit(image_assets[25], [200, 200])#Background image
            display.blit(image_assets[4], [500, 300])#Background image
            display.blit(image_assets[27], [100, 500])#Background image
        else:
            #here we render our pygame surface to show te following text.
            display.blit(image_assets[28], [0, 0])#Background image
            Instruction = instructions.render(("Instructions"), True, (255, 255, 255))
            Instruction_1 = instructions.render(("UP  key  to  jump   You  are  allowed  to  double  jump"), True, (255, 255, 255))
            Instruction_2 = instructions.render(("LEFT  key  to  move  left"), True, (255, 255, 255))
            Instruction_3 = instructions.render(("Right  key  to  right  left"), True, (255, 255, 255))
            Instruction_4 = instructions.render(("Spacebar  to  shoot  You  only  have  1.5  second  reload  time"), True, (255, 255, 255))
            Instruction_5 = instructions.render(("Objective  is  to  destroy  all enemies  and  beat  the  final  boss"), True, (255, 255, 255))
            Instruction_6 = instructions.render(("Press  enter  to  begin"), True, (255, 255, 255))

            #using the pygame surfaces, we draw the text onto the screen at their specified x,y location.
            display.blit(Instruction, [450, 100])
            display.blit(Instruction_1, [50, 200])
            display.blit(Instruction_2, [50, 250])
            display.blit(Instruction_3, [50, 300])
            display.blit(Instruction_4, [50, 350])
            display.blit(Instruction_5, [50, 450])
            display.blit(image_assets[26], [100, 600])#Background image

        enviroment.display.update() #finally we update the screen.






def game_over_screen():
    global menu_screen,enviroment,End_Execution,game_over
    while(game_over): #if the game is over because of player death, or user pressed exit.
        for event in enviroment.event.get():
                    if (event.type == enviroment.QUIT):
                        menu_screen = False #we exit the menu screen
                        End_Execution = True #we turn off game player
                        game_over = False #and we turn off this function. This causes the application to exit.

                    if (event.type == enviroment.KEYDOWN): #if the enter key is entered, we will reset all our variables and restart the game.
                        if (event.key == enviroment.K_RETURN):
                            menu_screen = True
                            End_Execution = True
                            return game_UI()
                            break

        display.blit(image_assets[28], [0, 0])#Background image
        display.blit(image_assets[29], [350, 300])#Background image
        display.blit(image_assets[27], [100, 500])#Background image




        enviroment.display.update()


#we load our game UI, in sequential order.
def game_UI():
    welcome_screen()
    main_gameplay_stage()
    game_over_screen()

game_UI() #we load game UI
enviroment.quit() #when all functions are returned, and game_ui is exited, we close the application safly


