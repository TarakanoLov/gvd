from . import player

class Game:
    def __init__(self, player1, player2):
        self.player1 = player1
        self.player2 = player2
        
    def startPlay(self):
        while not self.player1.win(self.player2) and not self.player2.win(self.player1):
            self.player1.get_new_resource()
 
            (if_next_move_too, only_drop_next_move) = self.player1.nextMove(self.player2)
            for k in range(0):
                (if_next_move_too, only_drop_next_move) = self.player1.nextMove(self.player2, only_drop_next_move)
            
            self.player2.get_new_resource()     
        
            (if_next_move_too, only_drop_next_move) = self.player2.nextMove(self.player1)
            for k in range(0):
                (if_next_move_too, only_drop_next_move) = self.player2.nextMove(self.player1, only_drop_next_move)
                
        if self.player1.tower >= 50 or self.player2.tower <= 0:
            return 0
        else:
            return 1