import pygame
from pygame.locals import *
import time,random

pygame.init()

score = 0
font = pygame.font.Font(None, 24)
font1 = pygame.font.Font(None, 48)
text = font.render("Score : " + str(score),1,(255,255,255))
text2 = font.render("Vie(s) : ",1,(255,255,255))

vie_image = pygame.image.load("invader.gif")

background = pygame.image.load("fond.png")

menu1 = pygame.image.load("menu1.gif")
menu2 = pygame.image.load("menu2.gif")
menu3 = pygame.image.load("menu3.gif")

hauteur,largeur = 800,800

boucle = True
vies = 3
sens = 1
MENU = True
RECOMMENCER = True

fenetre = pygame.display.set_mode((hauteur,largeur))

class Joueur(pygame.sprite.Sprite):

    def __init__(self):
        
        pygame.sprite.Sprite.__init__(self)
        
        self.image = pygame.image.load("player.gif")
        self.rect = self.image.get_rect()
        self.rect.x = 380
        self.rect.y = 750
    
    def move(self,n):
        self.rect.x += n

    def reset(self):
        self.rect.x = 380
        self.rect.y = 750
        
class Bullet(pygame.sprite.Sprite):
    
    def __init__(self):
        
        pygame.sprite.Sprite.__init__(self)
 
        self.image = pygame.Surface([4, 10])
        self.image.fill((255,255,255))
 
        self.rect = self.image.get_rect()
 
    def update(self):
        
        self.rect.y -= 15

class Ennemi(pygame.sprite.Sprite):

    def __init__(self):
        
        pygame.sprite.Sprite.__init__(self)
        
        self.image = pygame.image.load("invader.gif")
        self.rect = self.image.get_rect()
        self.rect.x = random.randint(20,750)
        self.rect.y = random.randint(20,150)
        self.sens = 1
        self.tir = 0

class Bullet_enemy(pygame.sprite.Sprite):
    
    def __init__(self,tireur):
        
        pygame.sprite.Sprite.__init__(self)
 
        self.image = pygame.Surface([4, 10])
        self.image.fill((255,0,0))
 
        self.rect = self.image.get_rect()

        self.tireur = tireur
        
    def update(self):
        
        self.rect.y += 20

        
bullet_list = pygame.sprite.Group()
bulletE = pygame.sprite.Group()
all_sprite = pygame.sprite.Group()
ennemis = pygame.sprite.Group()

for i in range(4):
    enemy = Ennemi()
    ennemis.add(enemy)
    all_sprite.add(enemy)
    
joueur = Joueur()
all_sprite.add(joueur)

def menu(fenetre):
    global MENU
    etape = 0
    while MENU:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                
            if event.type == pygame.KEYDOWN:
                if event.key == K_SPACE:
                    if etape == 1:
                        MENU = False
                    if etape == 0:
                        etape = 1
        if etape == 0:            
            fenetre.blit(menu1,(0,0))
        if etape == 1:
            fenetre.blit(menu2,(0,0))
        pygame.display.flip()
        
def collision(vaisseau,bullet):
    
    return vaisseau.rect.colliderect(bullet.rect)

def reset(bullet,bulletE,enemis,all_sprite,joueur):
    
    bullet.empty()
    bulletE.empty()
    all_sprite.empty()
    ennemis.empty()
    for i in range(4):
        enemy = Ennemi()
        ennemis.add(enemy)
        all_sprite.add(enemy)
    joueur.reset()
    all_sprite.add(joueur)
    pygame.display.flip()

def reset_jeu(bullet,bulletE,enemis,all_sprite,joueur):
    reset(bullet,bulletE,enemis,all_sprite,joueur)
    global vies
    vies = 3

def recommencer(fenetre,bullet,bulletE,enemis,all_sprite,joueur):
   
    
    global RECOMMENCER
    global score
    text = font1.render(str(score),1,(255,255,255))
    
    while RECOMMENCER:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                
            if event.type == pygame.KEYDOWN:
                if event.key == K_SPACE:
                    reset_jeu(bullet,bulletE,enemis,all_sprite,joueur)
                    score = 0
                    RECOMMENCER =  False
                  
        fenetre.blit(menu3,(0,0))
        fenetre.blit(text,(350,290)) 
        pygame.display.flip()

while boucle:
    
    pygame.display.flip()
    fenetre.fill((0,0,0))
    fenetre.blit(background,(0,0))
    all_sprite.draw(fenetre)
    bullet_list.update()
    bulletE.update()
    for i in range(0,vies):
        fenetre.blit(vie_image,(680+40*i,10))
    text = font.render("Score : " + str(score),1,(255,255,255))
    fenetre.blit(text2,(620,15))
    fenetre.blit(text,(5,5))
    menu(fenetre)
    
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            boucle = False
        if event.type == pygame.KEYDOWN:
            if event.key == K_RIGHT:
                if joueur.rect.x < 770:
                    joueur.move(25)
            if event.key == K_LEFT:
                if joueur.rect.x > 10:
                    joueur.move(-25)
            if event.key == K_UP:
                
                bullet = Bullet()
                
                bullet.rect.x = joueur.rect.x + 12
                bullet.rect.y = joueur.rect.y

                all_sprite.add(bullet)
                bullet_list.add(bullet)
            
                
    for enemy in ennemis:
        if enemy.tir == 0:
            bullet = Bullet_enemy(enemy)
            bulletE.add(bullet)
            all_sprite.add(bullet)
            bullet.rect.x = enemy.rect.x + 12
            bullet.rect.y = enemy.rect.y + 12
            enemy.tir = 1
            
        if enemy.rect.y > 750:
            boucle =  False
        if enemy.rect.x + 5 * sens < 780 and enemy.rect.x + 5 * sens > 0:
            enemy.rect.x += 5 * sens
        else:
            for enemy in ennemis:
                enemy.rect.y += 25
            sens = sens * -1
        if collision(enemy,joueur):
            boucle = False
        for bul in bullet_list:
            if collision(enemy,bul):
                bullet_list.remove(bul)
                all_sprite.remove(bul)
                ennemis.remove(enemy)
                all_sprite.remove(enemy)
                new_enemy = Ennemi()
                ennemis.add(new_enemy)
                all_sprite.add(new_enemy)
                score += 20
                break
                
    for bul in bulletE:
        if bul.rect.y > 800:
            bul.tireur.tir = 0
            bulletE.remove(bul)
            all_sprite.remove(bul)
        if collision(joueur,bul):
            if vies > 0:
                vies -= 1
                reset(bullet_list,bulletE,enemy,all_sprite,joueur)
                break
            else:
                break
    if vies == 0:
        recommencer(fenetre,bullet_list,bulletE,enemy,all_sprite,joueur)
    
    
    time.sleep(0.1)

pygame.quit()