# +---------------------------------------------------------------------------+
# |                           NCAA XC Team Rank                               |
# |                               Nate Foss                                   |
# |                                12/3/16                                    |
# +---------------------------------------------------------------------------+

###################################START OF PROGRAM#############################
#-------------------------------------------------------------------Team Rank---
def retrieveAndInputData(regionsAndTeams, weightedVictoryGraph):
	testm = [[]]

#-------------------------------------------------------------------Team Rank---

#-------------------------------------------------------------------Team Rank---

#======================< GLOBAL STUFFS >============================Team Rank===

#===============================< MAIN >========================================
def main():
    # DO STUFF HERE
    regionsAndTeams = dict() # [name of region]:[list of top 16 teams in that region, in order]
    weightedVictoryGraph = [] # how many times team [r] beat team [c]

    retrieveAndInputData(regionsAndTeams, weightedVictoryGraph)

    



#-------------------------------------------------------------------Team Rank---
if __name__ == '__main__': from time import clock; START_TIME = clock();  main(); \
                           print('--> Run time =', round(clock() - START_TIME, 2), 'seconds <--');
#############################< END OF PROGRAM >#################################