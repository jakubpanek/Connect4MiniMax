import Board

#all needed for ai player
class AIplayer:
    #main minimmax function
    def MiniMax(maxi, board, ttl, alpha, beta):
        if(ttl == 0): return board.score(2)                                     #terminate if reached maximum depth
        bestWayScore = -9999999999 if maxi else 9999999999
        for i in range(Board.COLNUM):                                           #go through all the possible collumns
            if(board.placeStone(i)):            
                score = (9999999999 if board.victory == 2 else -9999999999) if board.victory!=0 else AIplayer.MiniMax(not maxi, board, ttl-1, alpha,beta)
                if(maxi):
                    alpha = max(alpha, score)
                else: 
                    beta = min(beta, score)
                bestWayScore = max(bestWayScore, score) if maxi else min(bestWayScore, score)
                board.removeStone(i)
                if(beta <= alpha): break                                        #terminate if value is too low
        return bestWayScore

    #starting function - use this to interface with the AI
    def play(board):
        maxscore = -9999999999
        maxindex = 0
        for i in range(Board.COLNUM):                                           #go through all the possible collumns
            if(board.placeStone(i)):
                if(board.victory == 2):
                    maxscore = 9999999999
                    maxindex = i
                else:
                    score = AIplayer.MiniMax(False, board, 3, -9999999999, 9999999999)
                    if(score > maxscore):
                        maxscore = score
                        maxindex = i
                board.removeStone(i)
        return maxindex