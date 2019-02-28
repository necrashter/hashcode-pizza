import sys
from math import ceil
import numpy as np
from time import time
from pizzaMath import *

def pizzaToNP(pizza,rows,cols):
    out = np.zeros([rows,cols], dtype=np.int8)
    for r in range(rows):
        for c in range(cols):
            if pizza[r][c] == 'T': out[r,c] = 1
    return out

def getConnections(pizza,rows,cols,minEach,maxCell,rRow,rCol):
    output = []
    taken = np.zeros([rows,cols],dtype=np.int8)
    sys.stdout.write("Progress: ")
    for r in range(rows) if rRow else range(rows-1,-1,-1):
        sys.stdout.write('%4d / %4d'%((r+1) if rRow else (rows-r),rows));
        sys.stdout.flush();
        sys.stdout.write('\b'*11)
        for c in range(cols) if rCol else range(cols-1,-1,-1):
            if taken[r,c]: continue
            #import pdb; pdb.set_trace()
            currentReversed = 0 if pizza[r,c] else 1
            if r != 0:
                if pizza[r-1,c] == currentReversed and not taken[r-1,c]:
                    #add this couple to the output
                    toAdd = [r-1,c,r,c]
                    rect,area,diff = getBiggestExtension(pizza,toAdd,taken,rows,cols,minEach,maxCell)
                    if rect:
                        fillTaken(taken,rect)
                        output.append(rect)
                        continue
            if r != rows-1:
                if pizza[r+1,c] == currentReversed and not taken[r+1,c]:
                    #add this couple to the output
                    toAdd = [r,c,r+1,c]
                    rect,area,diff = getBiggestExtension(pizza,toAdd,taken,rows,cols,minEach,maxCell)
                    if rect:
                        fillTaken(taken,rect)
                        output.append(rect)
                        continue
            if c != 0:
                if pizza[r,c-1] == currentReversed and not taken[r,c-1]:
                    toAdd = [r,c-1,r,c]
                    rect,area,diff = getBiggestExtension(pizza,toAdd,taken,rows,cols,minEach,maxCell)
                    if rect:
                        fillTaken(taken,rect)
                        output.append(rect)
                        continue
            if c != cols-1:
                if pizza[r,c+1] == currentReversed and not taken[r,c+1]:
                    toAdd = [r,c,r,c+1]
                    rect,area,diff = getBiggestExtension(pizza,toAdd,taken,rows,cols,minEach,maxCell)
                    if rect:
                        fillTaken(taken,rect)
                        output.append(rect)
                        continue
    print()
    return output,taken

def improvePart(pizza,rows,cols,minEach,maxCell,rectangles,taken,r,c,toAdd):
    #import pdb; pdb.set_trace();
    deleteRects = [i for i in rectangles if isInside(r,c,i)]
    lostScore,oldDiff = 0,0
    for i in deleteRects:
        lostScore += getArea(i)
        emptyTaken(taken,i)
        rectangles.remove(i)
        oldDiff += countMinEach(pizza,i,minEach)
    rect,area,diff = getBiggestExtension(pizza,toAdd,taken,rows,cols,minEach,maxCell)
    if rect and (area>lostScore or (area==lostScore and diff>oldDiff)):
        fillTaken(taken,rect)
        rectangles.append(rect)
        return True
    else:
        for i in deleteRects:
            fillTaken(taken,i)
            rectangles.append(i)
        return False


def improve(pizza,rows,cols,minEach,maxCell,rectangles,taken):
    #taken = np.copy(take)
    sys.stdout.write("Progress: ")
    for r in range(rows):# if False else range(rows-1,-1,-1):
        sys.stdout.write('%4d / %4d'%((r+1),rows));
        sys.stdout.flush();
        sys.stdout.write('\b'*11)
        for c in range(cols):
            if taken[r,c]: continue
            currentReversed = 0 if pizza[r,c] else 1
            if r != 0:
                if pizza[r-1,c] == currentReversed:
                    toAdd = [r-1,c,r,c]
                    if improvePart(pizza,rows,cols,minEach,maxCell,rectangles,taken,r-1,c,toAdd): continue
            if r != rows-1:
                if pizza[r+1,c] == currentReversed:
                    toAdd = [r,c,r+1,c]
                    if improvePart(pizza,rows,cols,minEach,maxCell,rectangles,taken,r+1,c,toAdd): continue
            if c != 0:
                if pizza[r,c-1] == currentReversed:
                    toAdd = [r,c-1,r,c]
                    if improvePart(pizza,rows,cols,minEach,maxCell,rectangles,taken,r,c-1,toAdd): continue
            if c != cols-1:
                if pizza[r,c+1] == currentReversed:
                    toAdd = [r,c,r,c+1]
                    if improvePart(pizza,rows,cols,minEach,maxCell,rectangles,taken,r,c+1,toAdd): continue
    print()
    return rectangles,taken


def cutPizza(filename):
    start = time()
    with open(filename) as f:
        data = f.read().split('\n')
    pizzadata = data[1:]
    data = data[0].split(' ')

    minEach = int(data[2]) 
    maxCell = int(data[3])

    rows = int(data[0])
    cols = int(data[1])
    
    pizza = pizzaToNP(pizzadata,rows,cols)
    
    bestRects = None
    bestScore = 0

    for it,combs in enumerate([[True,True],[False,False],[True,False],[False,True]]):
        print("\033[91m\n===ITERATION",it+1,"OF 4===\n\033[0m");
        rectangles,taken = getConnections(pizza,rows,cols,minEach,maxCell,combs[0],combs[1]);
        oldScore = sum(getArea(r) for r in rectangles)
        print()
        print("\033[92mInitial pass has been completed.\033[0m")
        print("Score:\033[1m",oldScore,"\033[0m")
        print("Time elapsed:",time()-start);
        print("Attemping to improve the score...\n")
        improve(pizza,rows,cols,minEach,maxCell,rectangles,taken)
        newScore = sum(getArea(r) for r in rectangles)
        print()
        print("\033[92mCorrection pass has been completed.\033[0m")
        print("Score:\033[1m",newScore,"\033[0m")
        print("Improvement:",newScore-oldScore)
        print("Total Time elapsed:",time()-start);
        if newScore>bestScore:
            bestScore =newScore
            bestRects = rectangles
    return bestRects,bestScore


def main():
    if len(sys.argv)<3:
        print("npPizza.py <input file> <output file>");
        exit()
    solution,score = cutPizza(sys.argv[1])
    print("\nFINISHED")
    print("Final score:",score);
    output = str(len(solution))+'\n'
    output += '\n'.join([ ' '.join(str(j) for j in i) for i in solution])
    with open(sys.argv[2],'w') as f:
        f.write(output)
    print("Output has been saved to %s"%sys.argv[2])

if __name__=='__main__':
    main()
