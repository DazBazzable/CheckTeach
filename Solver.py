# Solver 2019
# Template for the algorithm to solve a sudoku. Builds a recursive backtracking solution
# that branches on possible values that could be placed in the next empty cell. 
# Initial pruning of the recursion tree - 
#       we don't continue on any branch that has already produced an inconsistent solution
#       we stop and return a complete solution once one has been found

# COMMENT FROM SUBMITTER
# I had major problems with the code and unfortunately ran out of time. Really unfair as I emailed requesting lecturer and
# tutor for help, but received no response. I guess the problem with doing this type of paper by distance.

# fundamentally I had a minor issue/bug that actually had been jeopardising my whole program. Frustratingly I only identified this
# on evening of submission. This actually screwed over the implementation of pruning

# Please note that the current pruning aspect works for easy projects. This is because of problem with a range that was coded earlier
# Please comment out the pruning section to test recursion backtracking on its own.

import pygame

import Sudoku_IO


def solve(snapshot, screen):
    # if current snapshot not complete ...
    # for each possible value for an empty cell
    #    clone current snapshot and update it,
    #    if new snapshot is consistent, perform recursive call
    # return a value

    # display current snapshot
    pygame.time.delay(20)  # originally 20
    Sudoku_IO.displayPuzzle(snapshot, screen)
    pygame.display.flip()

    # FOR DEBUGGING PURPOSES
    # print("***********")
    # print("SOLVE CYCLE")
    # print("***********")

    # PATHWAY A: BASE CASE
    ##BASE CASE IS SOLVED!?
    # if current snapshot is complete ... return a value
    if (isComplete(snapshot) == True) and (checkConsistency(snapshot) == True):
        print("Solved")
        pygame.time.delay(5000)  # allow a pause
        return snapshot


    # PATHWAY B: SOLVE IT
    else:
        # STEP 1 :: SAVE CURRENT STATE (original), ALSO MAKE COPY OF WORKING STATE
        # --- SAVE THE CURRENT STATE
        # original_snapshot = snapshot.clone()

        # --- CREATE A WORKING STATE (new_snapshot)
        new_snapshot = snapshot

        # -- METHOD 3 --#
        # --- MAIN PATHWAY -- USE THE WORKING STATE TO SOLVE --
        # This pathway uses the *Unsolved* list that has been generated as the list of items to solve

        # use dictionaries to store length for different values
        loggedUnsolvedCellsDict = {}

        ########################################################################################################################
        # -------RECURSIVE BACKTRACKING BRUTEFORCE

        def recursiveBacktrackingBruteForce():
            print("Makes it to RECURSION BACKTRACKING BRUTEFORCE")
            for i in range(0, len(new_snapshot.unsolvedCells())):
                if (len(new_snapshot.unsolvedCells()) != 0):
                    item = new_snapshot.unsolvedCells()[i]

                    # STEP 2 :: TRIPLE CHECK :: GENERATE ROW, COLUMN AND BOX VALUES FOR THE UNSOLVED CELL IN QUESTION
                    valuesTaken = ([y.getVal() for y in new_snapshot.cellsByRow(item.getRow())] +
                                   [y.getVal() for y in new_snapshot.cellsByCol(item.getCol())] +
                                   [y.getVal() for y in new_snapshot.cellsByBlock(item.getRow(), item.getCol())])
                    # STEP 3 :: USE THE ABOVE DATA TO IDENTIFY THE POSSIBLE VALUES FOR THE UNSOLVED CELL IN QUESTION
                    # eg. working out the legal values
                    possibleValues = [y for y in range(1, 10) if y not in valuesTaken]

                    # BRUTE FORCE RECURSION PART
                    for j in possibleValues:
                        if i > 0:
                            if new_snapshot.unsolvedCells()[i - 1] is not 0:
                                item.setVal(j)
                                break
                            else:
                                item.setVal(0)
                        else:
                            item.setVal(j)
                            solve(new_snapshot.clone(), screen)

                    # Backtrack
                    item.setVal(0)

        #######################################################################################################################
        # -------START WITH PRUNING
        #######################################################################################################################
        def generatePossibleValues():
            for i in range(0, len(new_snapshot.unsolvedCells())):
                if (len(new_snapshot.unsolvedCells()) != 0):
                    item = new_snapshot.unsolvedCells()[i]

                    column = item.getCol()
                    row = item.getRow()

                    # STEP 2 :: TRIPLE CHECK :: GENERATE ROW, COLUMN AND BOX VALUES FOR THE UNSOLVED CELL IN QUESTION
                    valuesTaken = ([y.getVal() for y in new_snapshot.cellsByRow(item.getRow())] +
                                   [y.getVal() for y in new_snapshot.cellsByCol(item.getCol())] +
                                   [y.getVal() for y in new_snapshot.cellsByBlock(item.getRow(), item.getCol())])
                    # STEP 3 :: USE THE ABOVE DATA TO IDENTIFY THE POSSIBLE VALUES FOR THE UNSOLVED CELL IN QUESTION
                    # eg. working out the legal values
                    possibleValues = [y for y in range(1, 10) if y not in valuesTaken]

                    # STEP 4 :: Storage of cell coordinates, with possible values
                    try:
                        loggedUnsolvedCellsDict[row].append([column, i, possibleValues])

                    except:
                        loggedUnsolvedCellsDict[row] = [[column, i, possibleValues]]

        def pruneSingletons():
            # m represents the row number
            for m in range(0, 9):
                # go through items in logged unsolved cells for purposes of storing any values (with cell as key)
                # to the dictionary logging values so can be updated by row at later point in time
                valueToDelete = 0

                # PRUNING SINGLETONS ##WORKING### NESTED FUNCTION
                print("CREATING PRUNE LIST")
                if loggedUnsolvedCellsDict[m] is not None:
                    for thingy in loggedUnsolvedCellsDict[m]:
                        if len(thingy[2]) == 1:
                            for k in thingy[2]:
                                valueToDelete = k
                                try:
                                    unsolvedCellNoToUpdate[m].append([thingy[0], k])

                                except:
                                    unsolvedCellNoToUpdate[m] = [[thingy[0], k]]
                            # break

                if loggedUnsolvedCellsDict[m] is not None:
                    for count, thingy in enumerate(loggedUnsolvedCellsDict[m]):
                        if valueToDelete in thingy[2]:
                            try:
                                thingy[2].remove(valueToDelete)
                            except:
                                pass

                # UPDATING CELL WITH PRUNED VALUES
                print("UPDATE WITH PRUNING")

                # goes through the list of the unsolved cells
                for count_it, cellToUpdate in enumerate(new_snapshot.unsolvedCells()):
                    # FIRST PART
                    # goes through the list of possible values that have been storred
                    for count, x in enumerate(loggedUnsolvedCellsDict_backup[m]):
                        if (unsolvedCellNoToUpdate.get(m) is not None):
                            for n in unsolvedCellNoToUpdate[m]:

                                if (cellToUpdate.getRow() == m) and (cellToUpdate.getCol() == n[0]):
                                    if (x[0] == n[0]):
                                        if (new_snapshot.unsolvedCells()) is not None:
                                            cellToUpdate.setVal(n[1])

                    valuesTaken = [y.getVal() for y in new_snapshot.cellsByRow(cellToUpdate.getRow())] + [y.getVal() for
                                                                                                          y in
                                                                                                          new_snapshot.cellsByCol(
                                                                                                              cellToUpdate.getCol())] + [
                                      y.getVal() for y in
                                      new_snapshot.cellsByBlock(cellToUpdate.getRow(), cellToUpdate.getCol())]

                    possValues2 = [i for i in range(1, 10) if i not in valuesTaken]

                    # if count_it is not len(new_snapshot.unsolvedCells()):
                    try:
                        if len(possValues2) == 1:
                            for k in possValues2:
                                cellToUpdate.setVal(k)

                    except:
                        break

                solve(new_snapshot.clone(), screen)

        # print("PRUNING")
        generatePossibleValues()

        # MAKE A BACKUP OF LOGGED UNSOLVED CELLS, REASON IS FOR USE IN FINAL LIST
        loggedUnsolvedCellsDict_backup = loggedUnsolvedCellsDict

        # Keep a dictionary logging values to update by row
        unsolvedCellNoToUpdate = {}

        print(loggedUnsolvedCellsDict)

        try:
            pruneSingletons()

        except:
            print("SWITCH TO BRUTEFORCE")
            recursiveBacktrackingBruteForce()
            # solve(new_snapshot.clone(),screen)


########################################################################################################################


def checkConsistency(snapshot):
    '''
    Check whether a snapshot is consistent, i.e. all cell values comply
    with the sudoku rules (each number occurs only once in each block, row and column).
    :param snapshot:
    :return: true: if the board is consistent with sudoku rules
    '''

    def checkDuplicates(some_list):
        '''
        Checks whether there are any duplicates
        :param some_list:
        :return:
        '''
        setCheck = set(some_list)
        for each in setCheck:
            count = some_list.count(each)
            if count > 1:
                return 1
            else:
                return 0

    # Var that keeps a count of any duplicate entries
    dupes_checker = 0

    for row in range(0, 9):
        checkRows = [cellRows.getVal() for cellRows in snapshot.cellsByRow(row) if cellRows.getVal() != 0]
        dupes_checker += checkDuplicates(checkRows)
    for col in range(0, 9):
        checkColls = [cellCols.getVal() for cellCols in snapshot.cellsByCol(col) if cellCols.getVal() != 0]
        dupes_checker += (checkDuplicates(checkColls))
    for row in range(0, 9, 3):
        for col in range(0, 9, 3):
            checkBlock = [cellBox.getVal() for cellBox in snapshot.cellsByBlock(row, col) if cellBox.getVal() != 0]
            dupes_checker += checkDuplicates(checkBlock)

    if dupes_checker == 0:
        return True
    else:
        return False


def isComplete(snapshot):
    '''
    Check whether a puzzle is solved.
    # return true if the sudoku is solved, false otherwise
    :param snapshot:
    :return: boolean value - is board completed or not?
    '''
    if (snapshot.unsolvedCells() == []):
        return True

    else:
        return False
