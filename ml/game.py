import player

class Game:
    def __init__(self, player1, player2):
        self.player1 = player1
        self.player2 = player2
        
    def startPlay(self):
        while not self.player1.win(self.player2) and not self.player2.win(self.player1):
            self.player1.get_new_resource()
 
            (if_next_move_too, only_drop_next_move) = self.player1.nextMove(self.player2)
            #while if_next_move_too:
            for k in range(1):
                (if_next_move_too, only_drop_next_move) = self.player1.nextMove(self.player2, only_drop_next_move)
            
            self.player2.get_new_resource()     
        
            (if_next_move_too, only_drop_next_move) = self.player2.nextMove(self.player1)
            #while if_next_move_too:
            for k in range(1):
                (if_next_move_too, only_drop_next_move) = self.player2.nextMove(self.player1, only_drop_next_move)
                
        #json_data = self.player1.get_json()
        if self.player1.tower >= 50 or self.player2.tower <= 0:
            # for i in range(len(json_data['data']) - 1, -1, -1):
                # if 'reward' in json_data['data'][i]:
                    # break
                # else:
                    # if self.player1.name == json_data['data'][i]['name']:
                        # json_data['data'][i]['reward'] = 1
                    # else:
                        # json_data['data'][i]['reward'] = -1
            return 0
        else:
            # for i in range(len(json_data['data']) - 1, -1, -1):
                # if 'reward' in json_data['data'][i]:
                    # break
                # else:
                    # if self.player1.name == json_data['data'][i]['name']:
                        # json_data['data'][i]['reward'] = -1
                    # else:
                        # json_data['data'][i]['reward'] = 1
            return 1