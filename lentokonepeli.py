from os import write
import pygame
import sys
import random
from pygame.locals import *
#Alustaa pygamen

pygame.init()
pygame.font.init()

koko = (400,600)
ruutu = pygame.display.set_mode(koko)
pygame.display.set_caption("Lentokonepeli")

fontti =pygame.font.SysFont("Cambria", 30)
fontti2 =pygame.font.SysFont("Cambria", 30)
fontti3 =pygame.font.SysFont("Cambria", 20)
fontti4 =pygame.font.SysFont("Cambria", 20)

tekstivari = (0, 0, 0)
loppuvari = (199, 199 , 199)

#Tausta ja Pelaaja

tausta = pygame.image.load("Kiitorata-1.png.png")
tausta = pygame.transform.scale(tausta,(400,600))
pelaaja =  pygame.image.load("lentokone-1.png.png")
pienkone = pygame.image.load("Pienlentokone-1.png.png")
pienkone = pygame.transform.scale(pienkone,(100,100))
pelaaja = pygame.transform.scale(pelaaja,(100,100))
kuva = pygame.image.load("lento.png")
kuva = pygame.transform.scale(kuva,(200,200))

pelx = 200
pely = 250
nopeus = 6
vihunopeus = 5
hp = 3
hihgscore = 0

viholliset = [[20,200],[100,100],[300,400],[200,10]]

on_kirjoitettu = False

with open("Hihgscore","r") as tiedosto:
    luettu = tiedosto.read()
    hihgscore = float(luettu)
#Ajastin

ajastin = pygame.time.Clock()
FPS = 60
alkuaika = pygame.time.get_ticks()
loppuaika = 0
def peruna():

    tapahtumat = pygame.event.get()
    for tapahtuma in tapahtumat:
        if tapahtuma.type == pygame.QUIT:
            pygame.quit()
            sys.exit()

#Pelilogiikka
def porkkana():
    global pelx
    global pely
    global hp
    global hihgscore
    global vihunopeus
#pelaajan liike

    nappaimet = pygame.key.get_pressed()
    if nappaimet[pygame.K_a]:
        pelx += -nopeus
    if nappaimet[pygame.K_d]:
        pelx += nopeus

    if pelx < 0:
        pelx = 0

    if pelx > 300:
        pelx = 300

    ruutu.blit(tausta,(0,0))

    for vihollinen in viholliset:
        ruutu.blit(pienkone,vihollinen)
    
    ruutu.blit(pelaaja,(pelx,pely))

#Kosketksen tarkistus
    for vihollinen in viholliset:
        if vihollinen[1] + 100 > pely and vihollinen[1] < pely + 100:
            if vihollinen[0] + 100 > pelx and vihollinen[0] < pelx + 100:
                #KOSKEE!
                vihollinen[1] = -300
                vihollinen[0] = random.randint(50,550)
                hp -= 1

#Tekstin piirto

    teksti = fontti.render("Healts left: " + str(hp), True, tekstivari)
    ruutu.blit(teksti, (30,30))
    aika = pygame.time.get_ticks() - alkuaika
    teksti = fontti.render("Aika: " + str(aika/1000), True, tekstivari)
    ruutu.blit(teksti, (200,30))

    if aika/1000 > hihgscore:
        hihgscore = aika/1000

    if aika//1000 % 10 == 0:
        vihunopeus += 0.01
        #Vihujen Liike

    for vihollinen in viholliset:
            vihollinen[1] += vihunopeus
            if vihollinen[1] > 600:
                vihollinen[1] = -300
                vihollinen[0] = random.randint(50,550)
    
    pygame.display.flip()
#Pelin Loppu
def lanttu():
    global on_kirjoitettu,loppuaika
    ruutu.fill(loppuvari)
    teksti = fontti2.render("LENTO-ONNETTOMUUS", True, tekstivari)
    ruutu.blit(teksti, (50,30))
    teksti = fontti2.render("TAPAHTUI, ", True, tekstivari)
    ruutu.blit(teksti, (50,80))
    teksti = fontti2.render("PERUNA-AIRIN LENTO ", True, tekstivari)
    ruutu.blit(teksti, (50,130))
    teksti = fontti2.render("PA122 RÄJÄHTI ", True, tekstivari)
    ruutu.blit(teksti, (50,180))
    teksti = fontti2.render("NOUSUKIIDOSSA", True, tekstivari)
    ruutu.blit(teksti, (50,230))
    teksti = fontti3.render("Uutiset 10.6.2021", True, tekstivari)
    ruutu.blit(teksti, (50,10))
    ruutu.blit(kuva,(150,350))
    teksti = fontti4.render("Peruna-air räjähti 9.6.2021", True, tekstivari)
    ruutu.blit(teksti, (150,320))
    teksti = fontti4.render("Hihgscore: " + str(hihgscore), True, tekstivari)
    if not on_kirjoitettu:
            on_kirjoitettu = True
            loppuaika = pygame.time.get_ticks()
            with open("Hihgscore","w") as tiedosto:
             tiedosto.write(str(hihgscore))

    if pygame.time.get_ticks() - loppuaika > 5000:
        pygame.quit()
        sys.exit()
    ruutu.blit(teksti, (200,550))

    pygame.display.flip()

#Pelin silmukka
while True:
        peruna()
        if hp > 0:
            porkkana()
        else:
            lanttu()
        ajastin.tick(FPS)