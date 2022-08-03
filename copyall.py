import os, shutil, sys

STATS = {
    'success': 0,
    'exists': 0,
    'not_found': 0
}
class OperationError(Exception):
    
    def __init__(self, message="Whoops! We're missing some arguments!"):
        self.message = message
        super().__init__(self.message)

def showHelp():
    print('Usage: [move/copy] [source] [destination] [extensions (optional)]')
    
    print('\nAvailable flags:')
    print('copy    ->   copies items from source to destination')
    print('move    ->   moves items from source to destination')
    print('ext     ->   action only items with specified extension(s)')
    print('             supply multiple extensions like: exe,png,jpg')
    
    print("\nEnclose multi-word searches with single quotes, i.e. 'foo bar'")
    
    print('\nCreated by toys0ldier, github.com/toys0ldier')
    sys.exit()
    
def progress(fileName):
    printWidth = (os.get_terminal_size().columns - 25)
    printName = fileName
    if len(printName) < printWidth:
        for _ in range(0, (printWidth - len(printName))):
            printName += ' '
    elif len(printName) > printWidth:
        printName = '...' + fileName[-(printWidth - 3):]
    else:
        pass
    sys.stdout.write("%s [ Progress: %.2f%% ]   \r" % (printName, float(sum([i for i in STATS.values()])) / float(numItems) * 100))
    if sum([i for i in STATS.values()]) % numItems == 0:
        print('')
        print('\nProcess completed successfully; summary:')
        print('[+] Items %s:\t\t%s' % ('copied' if funct == 'copy' else 'moved', '{:,}'.format(STATS['success'])))
        if STATS['exists']:
            print('[-] Items skipped (exists):\t%s' % '{:,}'.format(STATS['exists']))
        if STATS['not_found']:
            print('[!] Items not found:\t%s' % '{:,}'.format(STATS['not_found']))
    
def getJobCount(source):
    global numItems
    print('Scanning target folder for items... ', end='\r')
    numItems = 0
    for entry in os.scandir(source):
        if exts:
            if entry.name.lower().endswith(tuple(exts)):
                numItems += 1
        else:
            numItems += 1
    print('Scanning target folder for items... done! Items to %s: %s' % (funct, '{:,}'.format(numItems)), end='\r')
    print('')
    if numItems:
        singleDepth(source)
        
def singleDepth(source):
    
    def move(entry, outputFile):
        shutil.move(entry.path, outputFile)
    
    def copy(entry, outputFile):
        if entry.is_file():
            shutil.copy(entry.path, outputFile)
        else:
            shutil.copytree(entry.path, outputFile)
        
    for entry in os.scandir(source):
        outputFile = os.path.join(dest, entry.name)
        try:
            if exts:
                if entry.is_file() and entry.name.lower().endswith(tuple(exts)):
                    if funct == 'copy':
                        copy(entry, outputFile)
                    else:
                        move(entry, outputFile)
            else:
                if funct == 'copy':
                    copy(entry, outputFile)
                else:
                    move(entry, outputFile)
            STATS['success'] += 1
            progress(entry.name)
        except (FileNotFoundError, FileExistsError) as err:
            if 'exists' in str(err):
                STATS['exists'] += 1
            else:
                STATS['not_found'] += 1
    
def main():                
    global dest, funct, exts
    if len(sys.argv[1:]) <= 2 and sys.argv[1] != 'move' and sys.argv[1] != 'copy':
        if sys.argv[1] == '-h' or sys.argv[1] == '--help':
            showHelp()
        else:
            raise OperationError
    exts = None
    funct = sys.argv[1]
    source = sys.argv[2] if os.path.exists(sys.argv[2]) else None
    dest = sys.argv[3] if os.path.exists(sys.argv[3]) else os.makedirs(sys.argv[3])
    if len(sys.argv[1:]) == 4:
        exts = [e.lower() for e in sys.argv[4].split(',')]
    if not source:
        raise OperationError("No source file specified")
    getJobCount(source)

if __name__ == '__main__':

    main() 
