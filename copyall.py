import os, shutil, sys

STATS = {
    'success': 0,
    'failure': 0
}

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
    sys.stdout.write("%s [ Progress: %.2f%% ]   \r" % (printName, float(STATS['success'] + STATS['failure']) / float(numItems) * 100))
    if (STATS['success'] + STATS['failure']) % numItems == 0:
        print('')
        print('\nProcess completed successfully; summary:')
        print('[+] Items copied:\t\t%s' % '{:,}'.format(STATS['success']))
        print('[-] Items skipped:\t\t%s' % '{:,}'.format(STATS['failure']))
    
def get_size(depth, startLevel):
    global numItems
    numItems = 0
    targetLevel = []
    if depth > 1:
        for entry in os.scandir(startLevel):
            for i in range(1, depth):
                for sub_entry in os.scandir(entry.path):
                    if sub_entry.is_dir():
                        targetLevel.append(sub_entry.path)
    else:
        targetLevel.append(startLevel)
    for level in targetLevel:
        for _ in os.scandir(level):
            numItems += 1
        
def singleDepth(targetLevel, compNum):
    for entry in os.scandir(targetLevel):
        try:
            if entry.is_file():
                outputFile = os.path.join(outputDir, entry.name)
                shutil.copy(entry.path, outputFile)
            else:
                outputFile = os.path.join(outputDir, entry.name)
                shutil.copytree(entry.path, outputFile)
            if sys.argv[1] != '--progress':
                print('Moving: %s' % entry.name)
            else:
                STATS['success'] += 1
                progress(entry.name, compNum)
        except (FileNotFoundError, FileExistsError):
            STATS['failure'] += 1
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
    print('Folder depth = number of folders between top-level and\ntarget files/folders, including target files/folders')
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
        print('No move sequence available for depth of %s!' % depth)

if __name__ == '__main__':

    main() 
