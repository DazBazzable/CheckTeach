# Solver 2019
# Template for the algorithm to solve a sudoku. Builds a recursive backtracking solution
# that branches on possible values that could be placed in the next empty cell. 
# Initial pruning of the recursion tree - 
#       we don't continue on any branch that has already produced an inconsistent solution
#       we stop and return a complete solution once one has been found

import Sudoku_IO
import pygame
import Snapshot
import Cell


def solve(snapshot, screen):
    # display current snapshot
    pygame.time.delay(200) #originally 20
    Sudoku_IO.displayPuzzle(snapshot, screen)
    pygame.display.flip()

    #FOR DEBUGGING PURPOSES
    print("***********")
    print("SOLVE CYCLE")
    print("***********")

    #PATHWAY A: BASE CASE
    ##BASE CASE IS SOLVED!?
    # if current snapshot is complete ... return a value
    if (isComplete(snapshot) == True): # and (checkConsistency(snapshot) == True):
        print("Done Basecase")
        pygame.time.delay(5000) #allow a pause
        return

    # if current snapshot not complete ...
    # for each possible value for an empty cell
    #    clone current snapshot and update it,
    #    if new snapshot is consistent, perform recursive call
    # return a value

    #PATHWAY B: SOLVE IT
    else:
        #STEP 1 :: SAVE CURRENT STATE (original), ALSO MAKE COPY OF WORKING STATE
        #--- SAVE THE CURRENT STATE
        original_snapshot = snapshot.clone()

        #--- CREATE A WORKING STATE (new_snapshot)
        new_snapshot = snapshot.clone()

        #-- METHOD 3 --#
        #--- MAIN PATHWAY -- USE THE WORKING STATE TO SOLVE --
        # This pathway uses the *Unsolved* list that has been generated as the list of items to solve
        for i in range(0, len(new_snapshot.unsolvedCells())-1): #in snapshot.unsolvedCells():
            for j in range(0,9):

                item = new_snapshot.unsolvedCells()[i]
                column = item.getCol()
                row = item.getRow()

                if row == j:

                #STEP 2 :: TRIPLE CHECK :: GENERATE ROW, COLUMN AND BOX VALUES FOR THE UNSOLVED CELL IN QUESTION
                    rowValues = [cellRow.getVal() for cellRow in new_snapshot.cellsByRow(row) if cellRow.getVal() != 0]
                    columnValues = [cellCol.getVal() for cellCol in new_snapshot.cellsByCol(column) if cellCol.getVal() != 0]
                    boxValues = [cellBox.getVal() for cellBox in new_snapshot.cellsByBlock(row, column) if cellBox.getVal() != 0]

                    #STEP 3 :: USE THE ABOVE DATA TO IDENTIFY THE POSSIBLE VALUES FOR THE UNSOLVED CELL IN QUESTION
                    takenValues = rowValues + columnValues + boxValues
                    possibleValues = [possVal for possVal in range(0,9) if possVal not in takenValues]
                    possibleValues.remove(0)

                    print(takenValues, possibleValues)
                    print(len(possibleValues)) #Debugging

                    #STEP 4 :: Concept is to :: go through all possibilities and call the function again and again
                    #Read field into state (replace 0 with a set of possible values)
                    for value in possibleValues:
                        print(value)
                        #new_snapshot = snapshot.clone()
                        #new_snapshot = snapshot.clone()

                        #STEP 5 :: BACKTRACK TO PREVIOUS STATE?

                        #is valueValid?
                        #--- Yes -> then do this
                        #STEP 5a :: UPDATE RESULT

                        if len(possibleValues)>0:
                            item.setVal(value)
                            solve(new_snapshot.clone(), screen)

                        #No -> then below backtracking

                        #STEP 5b :: BACKTRACK TO PREVIOUS STATE?

                        #not possible then return to previous?
                        #NOT WORKING AT PRESENT - not sure if I need to put this elsewhere, or use alternate instruction
                        #such as reference to previous cell that I have seen in other examples
                        else:
                            item.setVal(0)
                            solve(original_snapshot, screen)


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

# Check whether a snapshot is consistent, i.e. all cell values comply 
# with the sudoku rules (each number occurs only once in each block, row and column).
# -- NOTE FROM DB - I am yet to put this method in the main solver function - Currently commented out
def checkConsistency(snapshot):
    numbers = [number for number in range(0,9)]

    for row in range(0,9):
        for col in range(0,9):
            checkColls = [cellCols.getVal() for cellCols in snapshot.cellsByCol(col) if numbers in cellCols.getVal()]
            checkRows = [cellRows.getVal() for cellRows in snapshot.cellsByRow(row) if numbers in cellRows.getVal()]
            checkBlock = [cellBox.getVal() for cellBox in snapshot.cellsByBlock(row,col) if numbers in cellBox.getVal()]
            checkTotal = checkRows + checkColls + checkBlock
            if 0 in checkTotal:
                return False
            else:
                return True

# Check whether a puzzle is solved. 
# return true if the sudoku is solved, false otherwise
# -- NOTE FROM DB will need to update this code also
def isComplete(snapshot):
    if(snapshot.unsolvedCells() == []):
        print("DONE DUMBY")
        pygame.time.delay(1000)
        return True

    else:
        print("Nope")
        return False

