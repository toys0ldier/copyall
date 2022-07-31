import os, shutil, sys
from termcolor import colored

def progress(fileName, compNum):
    printWidth = (os.get_terminal_size().columns - 25)
    printName = fileName
    if len(printName) < printWidth:
        for _ in range(0, (printWidth - len(printName))):
            printName += ' '
    elif len(printName) > printWidth:
        printName = '...' + fileName[-(printWidth - 3):]
    else:
        pass
    sys.stdout.write("%s [ Progress: %.2f%% ]   \r" % (printName, float(compNum) / float(numItems) * 100))
    
def get_size(depth, startLevel):
    global numItems
    numItems = 0
    targetLevel = []
    for entry in os.scandir(startLevel):
        if depth > 1:
            for i in range(1, depth):
                for sub_entry in os.scandir(entry.path):
                    if sub_entry.is_dir():
                        targetLevel.append(sub_entry.path)
        else:
            if entry.is_dir():
                targetLevel.append(entry.path)
    for level in targetLevel:
        for _ in os.scandir(level):
            numItems += 1
    print(numItems)
        
def singleDepth(targetLevel, compNum):
    for entry in os.scandir(targetLevel):
        try:
            if entry.is_file():
                output_file = os.path.join(outputDir, entry.name)
                # shutil.copy(entry.path, output_file)
            else:
                output_file = os.path.join(outputDir, entry.name)
                # shutil.copytree(entry.path, output_file)
            if sys.argv[1] != '--progress':
                print('Moving: %s' % entry.name)
            else:
                compNum += 1
                progress(entry.name, compNum)
        except (FileNotFoundError, FileExistsError):
            pass
    return compNum

def doubleDepth(targetLevel):
    compNum = 0
    for entry in os.scandir(targetLevel):
        if entry.is_dir():
            compNum += singleDepth(entry.path, compNum)
    return compNum

def tripleDepth(targetLevel):
    compNum = 0
    for entry in os.scandir(targetLevel):
        if entry.is_dir():
            compNum += doubleDepth(entry.path, compNum)
    return compNum
    
def main():
    global outputDir
    print(colored('Folder depth = number of folders between top-level and\ntarget files/folders, including target files/folders', 'yellow'))
    depth = int(input('Input folder depth [1-3]: '))
    if sys.argv[1] == '--progress':
        get_size(depth, sys.argv[2])
        topLevel = sys.argv[2]
        outputDir = sys.argv[3]
    if depth == 1:
        singleDepth(topLevel, 0)
    elif depth == 2:
        doubleDepth(topLevel)
    elif depth == 3:
        tripleDepth(topLevel)
    else:
        print(colored('No move sequence available for depth of %s!' % depth, 'red'))

if __name__ == '__main__':

    main() 
