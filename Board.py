ROWNUM = 6           #Number of rows the board should have(independent of the ui)
COLNUM = 7           #Number of columns
TOWIN = 4            #Number of stones on line to win the game

class Board:
    # [0] == HORIZONTAL -, [1] == VERTICAL |, [2] == DIAGONAL \, [3] == DIAGONAL /
    DIRS = [[[0,-1],[0,1]],[[-1,0],[1,0]],[[1,-1],[-1,1]],[[-1,-1],[1,1]]]                  #helping coordinates
    def __init__(self):
        self.stones = [[0 for x in range(0,ROWNUM)] for y in range(0,COLNUM)]
        self.playerturn = 1
        self.victory = 0

    #check if can play in column
    def mayPlayInCol(self, col):            
        if(col < 0 or col > COLNUM):
            return False
        if(self.stones[col][ROWNUM - 1] != 0):
            return False
        return True

    #print the board out into console
    def print(self):
        for x in range(COLNUM):
            for y in range(ROWNUM):
                print(self.stones[x][y], end = '')
            print("")

    #place stone into column
    def placeStone(self, col):
        for pos in range(0,ROWNUM):
            if(self.stones[col][pos] == 0):
                self.stones[col][pos] = self.playerturn
                self.playerturn = self.playerturn%2+1
                self.checkWin()
                return True
        return False

    #remove top stone from column
    def removeStone(self, col):
        for pos in reversed(range(0,ROWNUM)):
            if(self.stones[col][pos] != 0):
                self.stones[col][pos] = 0
                self.playerturn = self.playerturn%2+1
                self.checkWin()
                return
 
    #reset board
    def reset(self):
        self.stones = [[0 for x in range(0,ROWNUM)] for y in range(0,COLNUM)]
        self.playerturn = 1
        self.victory = 0

    #count how many stones has player on the board in specific direction from given position until some other stone
    def scanDir(self, player, row, col, dRow, dCol):
        count = 0
        while True:
            if (row < 0): return count
            if (row >= ROWNUM): return count
            if (col < 0): return count
            if (col >= COLNUM): return count
            if (self.stones[col][row] != player): return count
            count += 1
            row += dRow
            col += dCol
        return count

    #checks for win by any player
    def checkWin(self):
        for x in range(ROWNUM):
            for y in range(COLNUM):
                result = self.__checkWin(x, y)
                if(result != 0):
                    self.victory = result
                    return
        self.victory = 0
  
    #given coordinates, counts how many points max can player get from it lines runnig through it
    def __checkWin(self, row, col):
        tocheck = self.stones[col][row]
        if(tocheck == 0): return 0
        for dir in self.DIRS:
            scan1 = self.scanDir(tocheck, row, col, dir[0][0], dir[0][1])
            scan2 = self.scanDir(tocheck, row, col, dir[1][0], dir[1][1])
            count = scan1 + scan2 - 1           #remove one count bcs position [row,col] is counted twice
            if(count >= TOWIN):
                return tocheck
        return 0

    #basic heuristics - simply counts number of stones on a line and makes it to the seventh power
    def rateDir(self, player, row, col, dRow, dCol):
        result = self.scanDir(player, row, col, dRow, dCol)
        if(result == 0): return 0
        return pow(7.0, result)

    #returns rating of the board
    def score(self, forPlayer):
        if(self.victory != 0):
            if(self.victory == forPlayer): return 1000
            return -1000
        scoring = 0
        for x in range(COLNUM):
            for y in range(ROWNUM):
                scoring += self.rateDir(forPlayer, x, y, 1, -1)
                scoring += self.rateDir(forPlayer, x, y, 1, 0)
                scoring += self.rateDir(forPlayer, x, y, 1, -1)
                scoring += self.rateDir(forPlayer, x, y, 0, 1)

                scoring -= self.rateDir(not forPlayer, x, y, 1, -1)
                scoring -= self.rateDir(not forPlayer, x, y, 1, 0)
                scoring -= self.rateDir(not forPlayer, x, y, 1, -1)
                scoring -= self.rateDir(not forPlayer, x, y, 0, 1)
        return scoring