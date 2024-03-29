from re import I
import pygame
from pygame.locals import *
import classGraphOriente as graphe_oriente
import classJoueur as joueur
import random
import classpg as pg
import menu
import time 

class gameclass:
    def __init__(self,bot_or_human,level="save"):
        """
        __init__ class of the game of nim is a simple game with a AI 

        Args:
            bot_or_human (str): "bot" for play vs a bot or "human" for 1v1
        """
        pygame.init()
        
        self.bot_or_human = bot_or_human
        
        self.screen = pygame.display.set_mode((1168,826))
        
        self.background = pygame.image.load('../img/background.png').convert_alpha()
        

        pygame.display.set_caption("Jeu de Nim") 
        
        pygame.display.set_icon(pygame.image.load("../img/icon.png"))
        
        self.clock = pygame.time.Clock()
        
        self.nbr_sticks = 12
        
        self.augment_score = False
        
        self.finish = False 
        
        self.level = level

        self.timer = 0
    
        self.player1 = joueur.Joueur()
        self.player2 = joueur.Joueur()
        
        self.random_player() # we def wo start
        
        self.click_song = pg.son("../song/clic.mp3","song")
        
        if self.bot_or_human == "bot":
            
            if self.level == "save":
                self.graph = graphe_oriente.GraphOriente("save")
                self.create_graph()
                self.graph.save()
                
            elif self.level == "hard":
                self.graph = graphe_oriente.GraphOriente("hard")
                
            elif self.level == "meduim":
                self.graph = graphe_oriente.GraphOriente("meduim")
                
            elif self.level == "easy":
                self.graph = graphe_oriente.GraphOriente("easy")
                
        else: 
            self.button_r={"1" : pg.bouton("../img/b1.png",1061,260,147,147),"2" : pg.bouton("../img/b2.png",1061,445,147,147), "3" : pg.bouton("../img/b3.png",1061,630,147,147), }
            
            
        self.button_l={"1" : pg.bouton("../img/b1.png",107,260,147,147),"2" : pg.bouton("../img/b2.png",107,445,147,147),"3" : pg.bouton("../img/b3.png",107,630,147,147),}

        self.button_yes_no = { "1" : pg.bouton("../img/oui.png",435,560,147,147),"2" : pg.bouton("../img/non.png",735,560,147,147) }
        
    # i blit all images
    def grow(self,bouton):
        if bouton.rect.collidepoint(pygame.mouse.get_pos()) : 
            bouton.grow()
        if not bouton.rect.collidepoint(pygame.mouse.get_pos()) : 
            bouton.ungrow()
    
    def iblitall(self):
        """iblitall is a function for blit all the picture on the screen"""
        self.screen.blit(self.background,(0,0))
        if self.finish == True: #Si fin de partie
            
            pg.text(str(self.player1.score),130, 440,"center", color = "white", size = 100).iblit(self.screen)
            pg.text(str(self.player2.score),1035, 440,"center", color = "white", size = 100).iblit(self.screen)
            
            for i in range(1,3):
                self.button_yes_no[str(i)].iblit(self.screen)
                self.grow(self.button_yes_no[str(i)])
            
            if self.player1.gagne == True: 
                pg.img("../img/crown.png",130,160,93,77).iblit(self.screen)
            else: 
                pg.img("../img/crown.png",1035,160,93,77).iblit(self.screen)

        else:
            
            for i in range(self.nbr_sticks) :
                    pg.img('../img/sticks.png',584,i*40+228 ,460,35).iblit(self.screen)
                    
            for i in self.button_l: # on blit les bouton de gauche
                
                self.button_l[i].iblit(self.screen)
                self.grow(self.button_l[i])
                
                if self.bot_or_human == "human":
                    self.button_r[i].iblit(self.screen)
                    self.grow(self.button_r[i])
                    
            if self.player1.joue == True:
                pg.text("Joueur 1 ",590, 70,"center",size = 100, color= "white").iblit(self.screen)
            
            if self.player2.joue == True:
                pg.text("Joueur 2",590, 70,"center",size = 100, color= "white").iblit(self.screen)
    
    # some simple stuff
            
    def change_round(self):
        """change_round is a function for changing the round"""
        
        if self.player1.joue == True:
            self.player1.joue = False
            self.player2.joue = True

        else:
            self.player1.joue = True
            self.player2.joue = False   
            
    def random_player(self):
        """random_player is a function for random the player who start the game"""
        if random.randint(1,2) == 1 :
            self.player1.joue = True
        else : 
            self.player2.joue = True 
            
    def create_graph(self):
        """create_graph is a function for create a graphe used for the AI"""
        for i in range(1,13):
            self.graph.ajouter_sommet(i)
            if i>3 :
                self.graph.ajouter_arc(i,i-1)
                self.graph.ajouter_arc(i,i-2)
                self.graph.ajouter_arc(i,i-3)
        self.graph.ajouter_arc(3,2)
        self.graph.ajouter_arc(3,1)
        self.graph.ajouter_arc(2,1)
    
    # we manage the button
     
    def button(self,event):
        """
        button is a function for manage the button of the game

        Args:
            event : is the event pygame
        """
        if self.player1.joue == True:
            for boutton in self.button_l:
                if self.button_l[boutton].click(pygame.mouse.get_pos(),event):
                    self.click_song.play()
                    self.human_plays(int(boutton))
                    
        if self.bot_or_human == "human":
            if self.player2.joue == True:
                for boutton in self.button_l:
                    if self.button_r[boutton].click(pygame.mouse.get_pos(),event):
                        self.click_song.play()
                        self.human_plays(int(boutton))
        
        
        if self.button_yes_no["1"].click(pygame.mouse.get_pos(),event):
                self.click_song.play()
                self.restart_game()
                
        if self.button_yes_no["2"].click(pygame.mouse.get_pos(),event):
            self.click_song.play()
            menu.main()
            
    
    # we manage when pc play or when human play
    
    def computer_play(self):
        """
        cmpt_plays is a function 
        """
        if self.bot_or_human == "bot" and self.player2.joue == True and self.nbr_sticks >1 :
                print(self.graph)
                list_neibor = self.graph.liste_sommets_issus(self.nbr_sticks)
                
                if len(list_neibor) == 0 : # if the bot have no solutions for win
                    print("bot haven't found solution")
                    self.win(self.player1)
                    return "p2 defeat"
                
                if self.level == "save":    
                    self.graph_back = self.nbr_sticks
                
                self.nbr_sticks = random.choice(list_neibor)
                
                if self.level == "save": 
                    self.graph_after = self.nbr_sticks
                
                self.iblitall()
                   
                self.change_round()
    
    def human_plays(self,nbr):
        """
        human_plays is a function for supr a sticks when human_plays

        Args:
            nbr (int): nbr of stick for supr
        """
        if self.nbr_sticks>=int(nbr)+1 :
            self.nbr_sticks -= int(nbr)
            self.change_round() 



    #  we manage the end of the game
    
    def win(self,player_win):
        """
        win is a victory function that allows you to manage the victory

        Args:
            player_win (class): who win ?
        """
        self.finish = True
        player_win.gagne = True
        self.player1.joue = None
        self.player2.joue = None
        self.augment_score = True
        if self.bot_or_human == "bot":
            if self.player1.gagne and self.level == "save":
                self.graph.supprimer_arc(self.graph_back,self.graph_after)
                self.graph.save()
        self.end_game(player_win)
        
        
    def end_game(self,player_win):
        """
        end_game is function when the game is end

        Args:
            player_win : who player win ?
        """
        self.background = pygame.image.load('../img/background_end.png')
        if self.augment_score == True :
            player_win.score+=1
            self.augment_score = False #permet de n'augmenter le score qu'une seule fois
    
    def restart_game(self):
        """restart_game is a function for restart the game"""
        self.finish = False
        self.random_player()
        self.nbr_sticks = 12
        self.player1.gagne ,self.player2.gagne = False, False
        self.background = pygame.image.load('../img/background.png')
                                      
        
def main(bot_or_human,level):
    
    game = gameclass(bot_or_human,level)

    cmpt = 0
    
    running = True
    while running : 
        
        game.clock.tick(60)
        
        for event in pygame.event.get(): # parcours de tous les event pygame dans cette fenêtre
            if event.type == pygame.QUIT : # si l'événement est le clic sur la fermeture de la fenêtre
                running = False # running est sur False
            game.button(event)
        
        
        
        if game.nbr_sticks == 1 and game.player1.joue == True :    
            game.win(game.player2)
        if game.nbr_sticks == 1 and game.player2.joue == True :    
            game.win(game.player1)    
        
        if game.bot_or_human == "bot" and game.player2.joue == True :
            cmpt += 1

            if cmpt % 50 < 49:
                game.iblitall()
                
            else :

                game.computer_play()
                game.timer += 1
        
        
        game.iblitall()
        
        pygame.display.update()
                

    pygame.quit()


if __name__ == "__main__":
    main("bot","meduim")