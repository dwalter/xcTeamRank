# +---------------------------------------------------------------------------+
# |                           NCAA XC Team Rank                               |
# |                               Nate Foss                                   |
# |                                12/3/16                                    |
# +---------------------------------------------------------------------------+
from numpy import dot , transpose
###################################START OF PROGRAM#############################
#-------------------------------------------------------------------Team Rank---
def retrieveAndInputData():
    regionsAndTeams = dict()
    regionsAndTeams['r1'] = ['MIT','Tufts','Williams','TJ',]
    weightedVictoryGraph = [[0,2,2,1],
                            [1,0,2,1],
                            [1,1,0,0],
                            [1,1,2,0]]
    # weightedVictoryGraph = [[0,1,2,1],
    #                         [1,0,2,2],
    #                         [0,1,0,4],
    #                         [0,1,2,0]]
    weightedVictoryGraph = [list(elt) for elt in transpose(weightedVictoryGraph)]
    # now lowest score is best and poeple point to people they beat
    return regionsAndTeams , weightedVictoryGraph
#-------------------------------------------------------------------Team Rank---
def printMatrix(matrix):
    for r in range(len(matrix)):
        print(matrix[r])
#-------------------------------------------------------------------Team Rank---
def adjustForNumMeets(matrix):
    for r in range(len(matrix)):
        for c in range(r):
            s = 1.0*(matrix[r][c] + matrix[c][r])
            if s:
                matrix[r][c] /= s
                matrix[c][r] /= s
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
def addFudgeFactor(matrix, factor):
    for r in range(len(matrix)):
        for c in range(len(matrix)):
            matrix[r][c] = matrix[r][c]*(1-factor) + factor / len(matrix)
#-------------------------------------------------------------------Team Rank---
def adjustMatrixToUseNet(matrix):
#---******** WARNING ****** this is a mistake, don't do it
    for r in range(len(matrix)):
        for c in range(r):
            if matrix[r][c] > matrix[c][r]:
                matrix[r][c] -= matrix[c][r]
                matrix[c][r] = 0
            else:
                matrix[c][r] -= matrix[r][c]
                matrix[r][c] = 0
#-------------------------------------------------------------------Team Rank---
def PageRank(matrix, iterationStep = 15):
    # matrix should be normalized
    start = [1.0]*len(matrix)
    i = 1
    while True:
        if i % iterationStep == 0:
            #print(start)
            if input('continue? (type "n" to stop) ').strip() == 'n':
                break
        print(sum(start), start)
        start = list(dot(matrix, start))
        i += 1
    return start
#======================< GLOBAL STUFFS >============================Team Rank===

#===============================< MAIN >========================================
def main():
    # DO STUFF HERE
    regionsAndTeams = dict() # [name of region]:[list of top 16 teams in that region, in order]
    weightedVictoryGraph = [] # how many times team [r] beat team [c]

    regionsAndTeams , weightedVictoryGraph = retrieveAndInputData()

    printMatrix(weightedVictoryGraph)
    print()
    adjustForNumMeets(weightedVictoryGraph) # remove advantage for competing more (and thus giving away more of your points)
    printMatrix(weightedVictoryGraph)
    print()
    normalizeMatrix(weightedVictoryGraph) # so the total number of points is constant
    printMatrix(weightedVictoryGraph)
    print()
    addFudgeFactor(weightedVictoryGraph, .1) # fixes problem of undefeated teams and smoothes values a bit
    printMatrix(weightedVictoryGraph)
    print()

    results = PageRank(weightedVictoryGraph)

    results = zip(results, regionsAndTeams['r1'])

    results = sorted(results)
    printMatrix(results)


#-------------------------------------------------------------------Team Rank---
if __name__ == '__main__': from time import clock; START_TIME = clock();  main(); \
                           print('--> Run time =', round(clock() - START_TIME, 2), 'seconds <--');
#############################< END OF PROGRAM >#################################