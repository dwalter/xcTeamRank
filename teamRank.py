# +---------------------------------------------------------------------------+
# |                           NCAA XC Team Rank                               |
# |                               Nate Foss                                   |
# |                                12/3/16                                    |
# +---------------------------------------------------------------------------+

###################################START OF PROGRAM#############################
#-------------------------------------------------------------------Team Rank---
def retrieveAndInputData():
    regionsAndTeams = dict()
    regionsAndTeams['r1'] = ['MIT','Tufts','Williams','TJ',]
    weightedVictoryGraph = [[0,2,1,0],
                            [0,0,1,0],
                            [1,1,0,0],
                            [1,1,1,0]]
    return regionsAndTeams , weightedVictoryGraph
#-------------------------------------------------------------------Team Rank---
def printMatrix(matrix):
    for r in range(len(matrix)):
        print(matrix[r])
#-------------------------------------------------------------------Team Rank---
def PageRank(matrix):
    

#======================< GLOBAL STUFFS >============================Team Rank===

#===============================< MAIN >========================================
def main():
    # DO STUFF HERE
    regionsAndTeams = dict() # [name of region]:[list of top 16 teams in that region, in order]
    weightedVictoryGraph = [] # how many times team [r] beat team [c]

    regionsAndTeams , weightedVictoryGraph = retrieveAndInputData()

    printMatrix(weightedVictoryGraph)




#-------------------------------------------------------------------Team Rank---
if __name__ == '__main__': from time import clock; START_TIME = clock();  main(); \
                           print('--> Run time =', round(clock() - START_TIME, 2), 'seconds <--');
#############################< END OF PROGRAM >#################################