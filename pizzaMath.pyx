import numpy as np
cimport numpy as np

DTYPE = np.int8

def getExtensions(list rectang,np.ndarray taken,int rows,int cols, int maxCell):
    extensions = [rectang]
    for rectangle in extensions:
        if getArea(rectangle)==maxCell: continue 
        #import pdb; pdb.set_trace()
        if getArea2(rectangle[0]-1,rectangle[1],rectangle[2],rectangle[3])<=maxCell:
            if rectangle[0] != 0:
                for c in range(rectangle[1],rectangle[3]+1):
                    if taken[rectangle[0]-1,c]: break
                else:
                    extensions.append([rectangle[0]-1,rectangle[1],rectangle[2],rectangle[3]])
            if rectangle[2] != rows-1:
                for c in range(rectangle[1],rectangle[3]+1):
                    if taken[rectangle[2]+1,c]: break
                else:
                    extensions.append([rectangle[0],rectangle[1],rectangle[2]+1,rectangle[3]])
        if getArea2(rectangle[0],rectangle[1]-1,rectangle[2],rectangle[3])<=maxCell:
            if rectangle[1] != 0:
                for r in range(rectangle[0],rectangle[2]+1):
                    if taken[r,rectangle[1]-1]: break
                else:
                    extensions.append([rectangle[0],rectangle[1]-1,rectangle[2],rectangle[3]])
            if rectangle[3] != cols-1:
                for r in range(rectangle[0],rectangle[2]+1):
                    if taken[r,rectangle[3]+1]: break
                else:
                    extensions.append([rectangle[0],rectangle[1],rectangle[2],rectangle[3]+1])
    return extensions

def countMinEach(np.ndarray pizza,list ext,int minEach):
    t,m=0,0
    for row in range(ext[0],ext[2]+1):
        for col in range(ext[1],ext[3]+1):
            if pizza[row,col]:
                t+=1
            else:
                m+=1
    return abs(t-m)+1 if t>=minEach and m>=minEach else 0

def getBiggestExtension(np.ndarray pizza, list rectangle,np.ndarray taken,int rows,int cols, int minEach,int maxCell):
    exts = getExtensions(rectangle,taken,rows,cols,maxCell);
    #import pdb; pdb.set_trace()
    if not exts:
        return (rectangle,2,1) if minEach ==1 else ([],0,0)
    exts = sorted([[getArea(e)]+e for e in exts],reverse=True)
    maxArea = int(exts[0][0])
    exts = [e[1:] for e in exts if e[0]==maxArea]
    bestDiff = -1
    best = []
    for e in exts:
        diff = countMinEach(pizza,e,minEach)
        if diff and diff>bestDiff:
            best= e
            bestDiff=diff
    return (best,maxArea,bestDiff)

def fillTaken(np.ndarray taken,list rect):
    for row in range(rect[0],rect[2]+1):
        for col in range(rect[1],rect[3]+1):
            taken[row,col] =1 

def emptyTaken(np.ndarray taken,list rect):
    for row in range(rect[0],rect[2]+1):
        for col in range(rect[1],rect[3]+1):
            taken[row,col]=0

def getArea(list rectangle):
    return (rectangle[2]-rectangle[0]+1)*(rectangle[3]-rectangle[1]+1)

def getArea2(int a0,int a1,int a2,int a3):
    return (a2-a0+1)*(a3-a1+1)

def isInside(int x,int y,list rect):
    return x>=rect[0] and x<= rect[2] and y>=rect[1] and y<=rect[3]
