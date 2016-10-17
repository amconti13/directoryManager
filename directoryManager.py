#Created by Arianna Conti October 2016
#Program takes two directories and merges them together into a new one
import sys
import os
import os.path as osp
import shutil
import stat

def checkValidity() :
    #Incorrect amount of inputs
    if len(sys.argv) != 5 :
        print( "too much or too little input" )
        sys.exit()
    
    #Change input names for ease of reading program
    global command, d1, d2, d3
    command = sys.argv[1]
    d1 = sys.argv[2]
    d2 = sys.argv[3]
    d3 = sys.argv[4]

    #Command is not merge
    if command != "merge" :
        print( "Unknown Command" )
        sys.exit()

    #Directories to merge are the same
    if d1 == d2 :
        print( "Directories to merge are the same.")
        sys.exit();

    #Check if they are all valid directories
    for x in range(2,4) :
        if not osp.isdir(sys.argv[x]) :
            print( sys.argv[x], "is not a valid directory")
            sys.exit()

    #check if final directory already exists
    if not osp.isdir(sys.argv[4]) :
        os.mkdir(d3)
    else :
        print( d3, "already exists." )
        sys.exit()
#-------------------------------------------------------------------------------
def copyFirst(firstDir, finalDir) :
    itemsToCopy = os.listdir(firstDir)

    for item in itemsToCopy :
        #Item to be copied
        i = osp.join(firstDir,item)
        #print(i, osp.getmtime(i))
        #if the item is a file.
        if osp.isfile(i) :
            #copy the file into the new directory
            shutil.copy2(i, finalDir)
        #if the item is a directory
        elif osp.isdir(i) :
            cwd = os.getcwd()#base directory
            nextLvl = osp.join(cwd,finalDir)
            #Change directory to create the folder from d1
            os.chdir(nextLvl)
            os.mkdir(item)
            #Go into those folders
            cFrom = osp.join(cwd, i)
            cTo = osp.join(nextLvl, item)
            copyFirst( cFrom, cTo )
            #go back to original cwd
            os.chdir(cwd)
        elif os.path.islink(i) :
            linkto = os.readlink(i)
            os.symlink(i, finalDir)
        else :
            print("Whatever ", i, " is, isn't handled.")
#-------------------------------------------------------------------------------
def copySecond(orig1, toCopyD, finalDir) :
    itemsToMerge = os.listdir(toCopyD)
    
    for item in itemsToMerge :
        i = osp.join(toCopyD, item)
        x = osp.join(finalDir, item)
        toCompareTime = osp.join(orig1, item)
        if osp.isfile(i) : #if it is a file
            if osp.isfile(x) : #file exists already
                if os.path.getmtime(i) > os.path.getmtime(x) : #if more current
                    shutil.copy2( i, finalDir )
            else : #file doesn't exist
                shutil.copy2(i, finalDir)

        if osp.isdir(i) :
            if osp.isdir(x) :
                if os.path.getmtime(i) > os.path.getmtime(toCompareTime) : #if more current
                    shutil.rmtree(x)
                    cwd = os.getcwd()#base directory
                    nextLvl = osp.join(cwd,finalDir)
                    #Change directory to create the folder from d1
                    os.chdir(nextLvl)
                    os.mkdir(item)
                    #Go into those folders
                    cFrom = osp.join(cwd, i)
                    cTo = osp.join(nextLvl, item)
                    copyFirst( cFrom, cTo )
                    #go back to original cwd
                    os.chdir(cwd)
            else : #directory doesn't exist
                shutil.copy2(i, finalDir)
#-------------------------------------------------------------------------------
checkValidity()
copyFirst( d1, d3 )
copySecond( d1, d2, d3 )
print(d3, "was created.")
