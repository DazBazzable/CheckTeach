# Solver 2019
# Template for the algorithm to solve a sudoku. Builds a recursive backtracking solution
# that branches on possible values that could be placed in the next empty cell. 
# Initial pruning of the recursion tree - 
#       we don't continue on any branch that has already produced an inconsistent solution
#       we stop and return a complete solution once one has been found

import Sudoku_IO
import pygame

def solve(snapshot, screen):
    # display current snapshot
    pygame.time.delay(2)  # originally 20
    Sudoku_IO.displayPuzzle(snapshot, screen)
    pygame.display.flip()

    # FOR DEBUGGING PURPOSES
    #print("***********")
    #print("SOLVE CYCLE")
    #print("***********")

    # PATHWAY A: BASE CASE
    ##BASE CASE IS SOLVED!?
    # if current snapshot is complete ... return a value
    if (isComplete(snapshot) == True) and (checkConsistency(snapshot) == True):
        print("Solved")
        pygame.time.delay()  # allow a pause
        return

    # if current snapshot not complete ...
    # for each possible value for an empty cell
    #    clone current snapshot and update it,
    #    if new snapshot is consistent, perform recursive call
    # return a value

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

        for i in range(0, len(new_snapshot.unsolvedCells())):  # in snapshot.unsolvedCells():
            if (len(new_snapshot.unsolvedCells()) != 0):
                #if new_snapshot.unsolvedCells()[i].getVal() == 0:
                    item = new_snapshot.unsolvedCells()[i]

                    column = item.getCol()
                    row = item.getRow()

                    # STEP 2 :: TRIPLE CHECK :: GENERATE ROW, COLUMN AND BOX VALUES FOR THE UNSOLVED CELL IN QUESTION
                    valuesTaken = ([y.getVal() for y in new_snapshot.cellsByRow(item.getRow())] +
                               [y.getVal() for y in new_snapshot.cellsByCol(item.getCol())] +
                               [y.getVal() for y in new_snapshot.cellsByBlock(item.getRow(), item.getCol())])
                    possibleValues = [y for y in range(1,10) if y not in valuesTaken]

                    # STEP 3 :: USE THE ABOVE DATA TO IDENTIFY THE POSSIBLE VALUES FOR THE UNSOLVED CELL IN QUESTION
                    #eg. working out the legal values
                    # takenValues = rowValues + columnValues + boxValues

                    # STEP 4 :: Storage of cell coordinates, with possible values
                    #loggedUnsolvedCellsList.append([i, row, column, possibleValues])
                    try:
                        loggedUnsolvedCellsDict[row].append([column, i, possibleValues])

                    except:
                        loggedUnsolvedCellsDict[row] = [[column, i, possibleValues]]




                    #BRUTE FORCE RECURSION PART
                    for j in possibleValues:
                        if i > 0:
                            if new_snapshot.unsolvedCells()[i-1] is not 0:
                                item.setVal(j)
                                break
                            else:
                                item.setVal(0)
                        else:
                            item.setVal(j)
                            solve(new_snapshot.clone(), screen)

                    #Backtrack
                    item.setVal(0)

        #MAKE A BACKUP OF LOGGED UNSOLVED CELLS, REASON IS FOR USE IN FINAL LIST
        loggedUnsolvedCellsDict_backup = loggedUnsolvedCellsDict

        #Keep a dictionary logging values to update by row
        unsolvedCellNoToUpdate = {}

        # #m represents the row number
        # for m in range (0,9):
        #     #go through items in logged unsolved cells for purposes of storing any values (with cell as key)
        #     #to the dictionary logging values so can be updated by row at later point in time
        #     valueToDelete = 0
        #
        #     #PRUNING SINGLETONS ##WORKING### NESTED FUNCTION
        #
        #     if loggedUnsolvedCellsDict[m] is not None:
        #         for thingy in loggedUnsolvedCellsDict[m]:
        #             if len(thingy[2]) == 1:
        #                 for k in thingy[2]:
        #                     valueToDelete = k
        #                     try:
        #                         unsolvedCellNoToUpdate[m].append([thingy[0], k])
        #
        #                     except:
        #                         unsolvedCellNoToUpdate[m] = [[thingy[0], k]]
        #
        #                     #unsolvedCellNoToUpdate[thingy[0]] = k
        #                 break
        #
        #     if loggedUnsolvedCellsDict[m] is not None:
        #         for count, thingy in enumerate(loggedUnsolvedCellsDict[m]):
        #             if valueToDelete in thingy[2]:
        #                 try:
        #                     thingy[2].remove(valueToDelete)
        #                 except:
        #                     pass
        #         #             if len(thingy[2]) == 1:
        #         #                 pruneSingletonValues(valueToDelete)
        #         #         return unsolvedCellNoToUpdate
        #         #
        #         # pruneSingletonValues(0)
        #
        #
        #         #UPDATING CELL WITH PRUNED VALUES
        #
        #         #goes through the list of the unsolved cells
        #         for count_it, cellToUpdate in enumerate(new_snapshot.unsolvedCells()):
        #             #FIRST PART
        #             #goes through the list of possible values that have been storred
        #                 for count, x in enumerate(loggedUnsolvedCellsDict_backup[m]):
        #
        #             # if (x[2].count(unsolvedCellNoToUpdate[x[0]])) == 1 :
        #
        #                     if(unsolvedCellNoToUpdate.get(m) is not None):
        #                         for n in unsolvedCellNoToUpdate[m]:
        #
        #                             if (cellToUpdate.getRow() == m) and (cellToUpdate.getCol() == n[0]):
        #                                 if(x[0] == n[0]):
        #                                     #print(x[0])
        #                                     if (new_snapshot.unsolvedCells()) is not None:
        #                                         cellToUpdate.setVal(n[1])
        #
        #
        #                 valuesTaken = [y.getVal() for y in new_snapshot.cellsByRow(cellToUpdate.getRow())] + [y.getVal() for y in new_snapshot.cellsByCol(cellToUpdate.getCol())] + [y.getVal() for y in new_snapshot.cellsByBlock(cellToUpdate.getRow(), cellToUpdate.getCol())]
        #
        #                 possValues2 = [i for i in range(1,10) if i not in valuesTaken]
        #
        #                 if count_it is not len(new_snapshot.unsolvedCells()):
        #                     if len(possValues2) == 1:
        #                         for k in possValues2:
        #                             print(checkConsistency(new_snapshot))
        #                             if(checkConsistency(new_snapshot) == True):
        #                                 print("THIS PATH")
        #                                 cellToUpdate.setVal(k)
        #                                 solve(new_snapshot.clone(), screen)
        #                 else:
        #                     recurseBacktrack()
        #                 #return snapshot
        #
        #
        #
        #         #call to above methods
        #
        #         #updateValues(new_snapshot)
        #         # try:
        #         #     pruneSingletonValues(0)
        #         #     updateValues(new_snapshot)
        #         # except:
        #         #     recurseBacktrack()
        #         #solve(new_snapshot.clone(), screen)
        #
        #         # for k in range(1,10):
        #         #
        #         # if (checkConsistency(new_snapshot) == True):
        #         #                     cellToUpdate.setVal(k)
        #         #         cellToUpdate.setVal(0)
        #         #
        #         #
        #         # try:
        #         #     solve(new_snapshot.clone(),screen)
        #         # except:
        #         #     pass
        #             #solve(new_snapshot, screen)
        #             #make assignment if the snapshot is consistent and unsolvedCellNo to update is not 0
        #             #if (checkConsistency(new_snapshot) is True): # and (unsolvedCellNoToUpdate[x[0]] != 0):
        #             #update the new_snapshot values that match the stored values
        #             #print("AFTER: " + unsolvedCellNoToUpdate[x])
        #
        #
        #
        #         # for leftovers in new_snapshot.unsolvedCells():
        #         #     for i in range(1,10):
        #         #         leftovers.setVal(i)
        #         #         if(checkConsistency(new_snapshot) == True):
        #         #             solve(new_snapshot.clone(), screen)
        #         #
        #         #         leftovers.setVal(0)
        #         #         #print([items.getVal() for items in new_snapshot.unsolvedCells()])
        #         # else:
        #         #     for k in possValues2:
        #         #         if(checkConsistency(new_snapshot) == True):
        #         #             cellToUpdate.setVal(k)
        #         #             try:
        #         #                 solve(new_snapshot.clone(),screen)
        #         #             except:
        #         #                 pass
        #
        #
        #
        #         # except:
        #         #     #should have been achieved by above, but just in case if failure to unmake and try again
        #         #     pass


########################################################################################################################
#-------RECURSIVE BACKTRACKING
        for i in range(0, len(new_snapshot.unsolvedCells())):  # in snapshot.unsolvedCells():
            if (len(new_snapshot.unsolvedCells()) != 0):
                #if new_snapshot.unsolvedCells()[i].getVal() == 0:
                    item = new_snapshot.unsolvedCells()[i]

                    column = item.getCol()
                    row = item.getRow()

                    # STEP 2 :: TRIPLE CHECK :: GENERATE ROW, COLUMN AND BOX VALUES FOR THE UNSOLVED CELL IN QUESTION
                    valuesTaken = ([y.getVal() for y in new_snapshot.cellsByRow(item.getRow())] +
                               [y.getVal() for y in new_snapshot.cellsByCol(item.getCol())] +
                               [y.getVal() for y in new_snapshot.cellsByBlock(item.getRow(), item.getCol())])
                    # STEP 3 :: USE THE ABOVE DATA TO IDENTIFY THE POSSIBLE VALUES FOR THE UNSOLVED CELL IN QUESTION
                    #eg. working out the legal values
                    possibleValues = [y for y in range(1,10) if y not in valuesTaken]

                    #BRUTE FORCE RECURSION PART
                    for j in possibleValues:
                        if i > 0:
                            if new_snapshot.unsolvedCells()[i-1] is not 0:
                                item.setVal(j)
                                break
                            else:
                                item.setVal(0)
                        else:
                            item.setVal(j)
                            solve(new_snapshot.clone(), screen)

                    #Backtrack
                    item.setVal(0)









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

    #Var that keeps a count of any duplicate entries
    dupes_checker = 0

    for row in range(0,9):
        checkRows = [cellRows.getVal() for cellRows in snapshot.cellsByRow(row) if cellRows.getVal() != 0]
        dupes_checker += checkDuplicates(checkRows)
    for col in range(0,9):
        checkColls = [cellCols.getVal() for cellCols in snapshot.cellsByCol(col) if cellCols.getVal() != 0]
        dupes_checker += (checkDuplicates(checkColls))
    for row in range(0,9,3):
        for col in range(0,9,3):
            checkBlock = [cellBox.getVal() for cellBox in snapshot.cellsByBlock(row,col) if cellBox.getVal() != 0]
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
    if(snapshot.unsolvedCells() == []):
        return True

    else:
        return False

#
#
#loggedUnsolvedCellsList = []

        # values_in_block = [x.getVal() for x in new_snapshot.cellsByBlock(0, 0)]


        # if [y for y in range(1,10) if y in values_in_block] == True:
        #     pygame.time.delay(10000)
        #
        # for item in Snapshot.snapshot.cellsByBlock(snapshot, 0, 0):
        #
        #     valuesTaken = ([y.getVal() for y in new_snapshot.cellsByRow(item.getRow())] +
        #                    [y.getVal() for y in new_snapshot.cellsByCol(item.getCol())] +
        #                    [y.getVal() for y in new_snapshot.cellsByBlock(item.getRow(), item.getCol())])
        #     possValues = [y for y in range(1,10) if y not in valuesTaken]
        #
        #     if item.getVal() is 0:
        #         for value in possValues:
        #
        #             print(possValues)
        #             item.setVal(value)
        #             possValues.remove(value)
        #             print(possValues)
        #             #break
        #             solve(snapshot.clone(), screen)
        #         item.setVal(0)

        # for item in new_snapshot.cellsByRow(0):
        #
        #     if item.getVal() is 0:
        #
        #
        #         valuesTaken = ([y.getVal() for y in new_snapshot.cellsByRow(item.getRow())] +
        #                        [y.getVal() for y in new_snapshot.cellsByCol(item.getCol())] +
        #                        [y.getVal() for y in new_snapshot.cellsByBlock(item.getRow(), item.getCol())])
        #         possValues = [y for y in range(1,10) if y not in valuesTaken]
        #
        #
        #         #possValues:
        #         for value in possValues:
        #             item.setVal(value)
        #             print(possValues)
        #
        #             possValues.remove(value)
        #             print(possValues)
        #             solve(new_snapshot.clone(), screen)
        #         else:
        #             item.setVal(0)

# #################### NEXT ATTEMPT ###############################################################################
#                     #print(possibleValues[0:2])
#
#                     for value in possibleValues:
#                         print(possibleValues[0:possibleValues.index(value)])
#                         valuesTaken = ([y.getVal() for y in new_snapshot.cellsByRow(item.getRow())] +
#                                   [y.getVal() for y in new_snapshot.cellsByCol(item.getCol())] +
#                                   [y.getVal() for y in new_snapshot.cellsByBlock(item.getRow(), item.getCol())])
#                         if (value not in valuesTaken) and (possibleValues[0:possibleValues.index(value)]):
#                             item.setVal(value)
#                             possibleValues.remove(value)
#                             solve(new_snapshot.clone(), screen)
#                     item.setVal(0)







########################################################################################################################

########################################################################################################################





                    # BACKTRACKING
                    # print(item.getVal(), possibleValues)
                    # # STEP 5: Lets try possible values
                    # for value in possibleValues:
                    #     print(value)
                    #
                    #     item.setVal(value)
                    #
                    #     #is this value valid?
                    #
                    #     solve(new_snapshot.clone(), screen)
                    #
                    # #backtrack
                    # item.setVal(0)

        # for z in new_snapshot.unsolvedCells():
        #     if z.getRow() == 0:
        #         print(z.getRow(), z.getCol(), z.getVal())


        # for col in range(0,9):
        #     print(loggedUnsolvedCellsList[0][2])
        #     filtered_list = list(filter(lambda x: x == 0, loggedUnsolvedCellsList[2]))
        #     print(filtered_list)



                # if PossibleDict.get(j) is None:
                #     print("Hey empty")
                #     PossibleDict[j] = ([possibleValues])
                # else:
                #     PossibleDict[j].append(possibleValues)


                #print(takenValues, possibleValues)
                # print(len(possibleValues)) #Debugging

                # PossDictlength.append(len(possibleValues))
                #PossDict.append(possibleValues)
                #print(len(PossibleDict))


                #PossibleDict[j].append(possibleValues)

                # print(PossDictlength)

                # print("FLIP")
                # if i == (len(PossDict)-1):
                # print(PossDict)

                # print("Possible values -- Row: " + str(row) + " Col: " + str(column) + " Item: " + str(i))

                #print("Max row: " + str(i) + " Max Col: " + str(j))

            # valueToDelete = 0
            # #print(max_List_for_Row)
            # print(PossibleDict)
            #
            # unsolvedCellNoToUpdate = {}
            #

            #
            # for i in range (0,9):
            #     if Cell.cell.getVal() is 0:
            #
            #
            #
            #
            #             # if len(PossDict[i])
            #         # for item in PossDict:
            #         #     maxValue += item
            #         # print(maxValue.count())
            #
            #         # for item in possibleValues:
            #         #    if item2 in maxValue:
            #
            #
            #     # #PRUNING
            #     # for values in possibleValues:
            #     #     print(len(values))
            #     #
            #     # #RECURSING
            #     # if ((possibleValues != [[]]) and (possibleValues != [])):
            #     #     print("BANG")
            #     #     print(possibleValues)
            #     #     for value in possibleValues:
            #     #         print(value)
            #     #         item.setVal(value)
            #     #         solve(new_snapshot.clone(), screen)
            #     #
            #     # #solve(original_snapshot, screen)
            #
            #     # count+= 1
            #
            #     #item.setVal(0)

        # print("final count: " + str(count))
        # for k in range(len(PossDict)):
        #    if len(PossDict[k]) > len(maxValue):
        #        maxValue = PossDict[k]
        # print(maxValue)

# I've done my best to spot what's going on and it appears you getting a little bit confused about what version of the board should be sent in a recursive call to the solve function.
#
# In line 99 you call solve on original snapshot. Why do you do this? Returning to an earlier state in the tree of recursion calls should result naturally from returning from a recursive call.
#
# In other words, each recursive call should be an attempt to add new information to the board. If the attempt fails, the solver should return the solver instance which called it and so return to the state of the board as it was in the earlier instance.
#
# ie:
#
# 1. Initial call to solver (0): Board state instance is valid afterward, but incomplete, so recurse.
# 2. Recursion 1: Board state is valid, but incomplete, so recurse.
# 3. Recursion 2: Board state in invalid, so return to recurse call 1.
# 4. Recursion 1 then leads to a new recursive call (3) with different parameters.
# 5. Recursion 3 is valid and complete, so return the completed board to 1.
# 6. Recursion 1 now has a board that is valid and complete, so return to 0.
#
# In still other words, your implementation should be making a recursive call at the point the new snapshot is created. The 'original snapshot' is kept as record of the 'state of the world' before the recursive call happened so it can be returned to if necessary.
#
# At line 188 and 210 you appear to have been closer to the mark because you snapshot.clone() as a parameter in the recursive call. My impression though is that you went a little off track at 198 and 213. I'm not quite sure what you trying to do there, but the most of the work should be done by making recursive calls on copies of the board, not sending the same board to a recursive call.
#
# Additional pruning is supposed to be done of course according to the brief, but I recommend getting your recusions working properly before attempting this.
#
# I hope this answer helps you and doesn't confuse you instead.

# PS. Something else to bear in mind is that each time solver is called, it should keep the state of board when the solver
# starts each time and start to iterate through possible values of empty cells making a recursive call to the solver
# function for each attempted change to the board state. However, the next iterative change to the board at each level
# should only be able to go ahead if the last recursive call does not end up producing a valid and complete board.


# # TIPS FROM DISCORD POST AROUND PSEUDOCODE
# '''
#     # solve method is called - done
#     # updates your screen = done
#     # solves your singletons
#     # does other pruning things
#     #
#     # recursibe work to make guesses could look like this
#     # if I have unsolved cells
#     #         if those cells have legal values
#     #         do more pruning to work out which one has least amount of legal values
#     #             pick one of those short ones for loop over legal values for that
#     #                 clone your snapshot
#     #                 set the new value for the guess cell in clone
#     #                 make recursive call using clone
#     #
#     # Once you have run out of singletons, you need another strategy.
#     # Perhaps you keep a list of the cells in the current snapshot, sorted in order of the legnths of their 'possibles' lists.
#     # There are other intelligent things that can be done.
#     #
#     # You can cross-reference betwee the missing values in a row, column or block and the possibles lists for its empty cells.
#     # If a missing value appears in only one of the possible lists, then this value must go in the cell
#
#     '''

#compare dicts
#max value amongst dictionary
#does possible values contain value
#yes it does then


#for i in range(0, len) in possibleValues:
#print(value)
#new_snapshot = snapshot.clone()
#new_snapshot = snapshot.clone()

#STEP 5 :: BACKTRACK TO PREVIOUS STATE?

#is valueValid?
#--- Yes -> then do this
#STEP 5a :: UPDATE RESULT

# if len(possibleValues)>0:
#     item.setVal(value)
#     solve(new_snapshot.clone(), screen)

#No -> then below backtracking

#STEP 5b :: BACKTRACK TO PREVIOUS STATE?

#not possible then return to previous?
#NOT WORKING AT PRESENT - not sure if I need to put this elsewhere, or use alternate instruction
#such as reference to previous cell that I have seen in other examples
# else:
#     item.setVal(0)
#     solve(original_snapshot, screen)


#STEP 4 :: Concept is to :: go through all possibilities and call the function again and again
#Read field into state (replace 0 with a set of possible values)

# for value in possibleValues:
#     print(value)
#     #new_snapshot = snapshot.clone()
#     #new_snapshot = snapshot.clone()
#
#     #STEP 5 :: BACKTRACK TO PREVIOUS STATE?
#
#     #is valueValid?
#     #--- Yes -> then do this
#     #STEP 5a :: UPDATE RESULT
#
#     if len(possibleValues)>0:
#         item.setVal(value)
#         solve(new_snapshot.clone(), screen)
#
#     #No -> then below backtracking
#
#     #STEP 5b :: BACKTRACK TO PREVIOUS STATE?
#
#     #not possible then return to previous?
#     #NOT WORKING AT PRESENT - not sure if I need to put this elsewhere, or use alternate instruction
#     #such as reference to previous cell that I have seen in other examples
#     else:
#         item.setVal(0)
#         solve(original_snapshot, screen)

#item.setVal(0)
#solve(snapshot, screen)

'''

##  PREVIOUS VERSION - Other methods I have coded for later reference ##
##  -- Uses a different approach to where it brute forces -> Works thru individual cells
for i in range(0,9):
#Possible and existing row values
existingRowValue = []
possibleRowValues = [1,2,3,4,5,6,7,8,9]

#TRIPLE CHECK#
##STEP 1##
#FOR ROW - Generates the possible values for ROW
#This adds valid cell values to a list
#The second part keeps removes the valid values for the row
for cell_in_row in (Snapshot.snapshot.cellsByRow(snapshot, i)):
if (cell_in_row.getVal() != 0):
    existingRowValue.append(cell_in_row.getVal())

    #The second part keeps removes the valid values for the row
    #There is probably an easier way to do this
    if cell_in_row.getVal() in possibleRowValues:
        possibleRowValues.remove(cell_in_row.getVal())


##STEP 2##
#i is the row number, j therefore can give the column number
for cell_in_row in (Snapshot.snapshot.cellsByRow(snapshot, i)):
#Possible and existing column values
possibleColValues = [1,2,3,4,5,6,7,8,9]
existingColumnValue = []

#Possible and existing block values
possibleBlockValues = [1,2,3,4,5,6,7,8,9]
existingBlockValue = []

for cell_in_coll in (Snapshot.snapshot.cellsByCol(snapshot, cell_in_row.getCol())):
    #print("Cell coll: " + str(cell_in_coll.getCol()))

    #if the value is not 0 && not the maincell
    if (cell_in_coll.getVal() != 0):
    #if((cell_in_coll.getVal() != 0) and not cell_in_coll.getVal): # and (cell_in_coll not in y)
        existingColumnValue.append(cell_in_coll.getVal())

        #The second part keeps removes the valid values for the row
        #There is probably an easier way to do this
        if (cell_in_coll.getVal() in possibleColValues):
            possibleColValues.remove(cell_in_coll.getVal())

for cell_in_block in (Snapshot.snapshot.cellsByBlock(snapshot, cell_in_row.getRow(),cell_in_row.getCol())):
    if (cell_in_block.getVal() != 0):
        existingBlockValue.append(cell_in_block.getVal())
        if (cell_in_block.getVal() in possibleBlockValues):
            possibleBlockValues.remove(cell_in_block.getVal())

#Once we arrive at a vacant cell
#Check if the x possible values are in the y possible values
if(len(existingRowValue)>3):
    print("existing Row Value: " + str(existingRowValue) + str(len(existingRowValue)))
    print("existing Column Value: " + str(existingColumnValue) + str(len(existingColumnValue)))
    print("-")
    print("possible Row Values available: " + str(possibleRowValues) + str(len(possibleRowValues)))
    print("possible Column Value available: " + str(possibleColValues)+ str(len(possibleColValues)))
    print("=========================================")

#print(possibleRowValues.symmetric possibleColValues)

#valuesToEnter = []

#setCheck = set(possibleRowValues).intersection(possibleColValues)
#print(setCheck)2e1
#for item in snapshot.unsolvedCells():
    #if item.getRow() == i:
        #cell_in_row.setValue(existingRowValue[item])
        #solve(snapshot.clone(), screen)


Method 1:


# if(cell_in_row.getVal() == 0):
#      #if len(existingRowValue) == 9:
#     for item in possibleRowValues:
#         if (item in possibleColValues):
#             if (item in possibleBlockValues):
#                 cell_in_row.setVal(item)
#                 solve(snapshot.clone(), screen)
#             else:
#                 cell_in_row.setVal(0)
#
        #else:
            #solve(snapshot.clone(), screen)
            #valuesToEnter.append(item)
            #print("Values to Enter: " + str(valuesToEnter))
                #if len(existingRowValue) == 9:

            #solve(snapshot, screen)


Method 2

#go through all possibilities and call the function again and again

# if(cell_in_row.getVal() == 0):
#     for item in possibleRowValues:
#         if(item in possibleColValues) and (item not in existingColumnValue):
#             cell_in_row.setVal(item)
# #
#             solve(snapshot.clone(), screen)
#         else:
#             cell_in_row.setVal(item)
#             solve(snapshot, screen)

#solve(snapshot, screen)
'''
