# +---------------------------------------------------------------------------+
# |                           NCAA XC Team Rank                               |
# |                               Nate Foss                                   |
# |                                12/3/16                                    |
# +---------------------------------------------------------------------------+
from numpy import dot
###################################START OF PROGRAM#############################
#-------------------------------------------------------------------Team Rank---
def retrieveAndInputData():
    regionsAndTeams = dict()
    regionsAndTeams['r1'] = ['MIT','Tufts','Williams','TJ',]
    weightedVictoryGraph = [[0,2,2,1],
                            [1,0,2,1],
                            [1,1,0,0],
                            [1,1,2,0]]
    return regionsAndTeams , weightedVictoryGraph
#-------------------------------------------------------------------Team Rank---
def printMatrix(matrix):
    for r in range(len(matrix)):
        print(matrix[r])
#-------------------------------------------------------------------Team Rank---
def normalizeMatrix(matrix):
    for c in range(len(matrix)):
        s = 0
        for r in range(len(matrix)):
            s += matrix[r][c]
        if s > 0:
            for r in range(len(matrix)):
                matrix[r][c] = matrix[r][c] *1.0 / s
#-------------------------------------------------------------------Team Rank---
def PageRank(matrix, iterationStep = 15):
    # matrix should be normalized
    start = [1.0]*len(matrix)
    i = 1
    while True:
        if i % iterationStep == 0:
            print(start)
            if input('continue? (type "n" to stop) ').strip() == 'n':
                break
        print(sum(start), start)
        start = list(dot(matrix, start))
        i += 1


#======================< GLOBAL STUFFS >============================Team Rank===

#===============================< MAIN >========================================
def main():
    # DO STUFF HERE
    regionsAndTeams = dict() # [name of region]:[list of top 16 teams in that region, in order]
    weightedVictoryGraph = [] # how many times team [r] beat team [c]

    regionsAndTeams , weightedVictoryGraph = retrieveAndInputData()

    printMatrix(weightedVictoryGraph)
    normalizeMatrix(weightedVictoryGraph)
    printMatrix(weightedVictoryGraph)

    PageRank(weightedVictoryGraph)

#-------------------------------------------------------------------Team Rank---
if __name__ == '__main__': from time import clock; START_TIME = clock();  main(); \
                           print('--> Run time =', round(clock() - START_TIME, 2), 'seconds <--');
#############################< END OF PROGRAM >#################################