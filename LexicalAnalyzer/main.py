import re

class token:
    def __init__(self, line, column, tokenClass, tokenValue):
        self.line = line;
        self.column = column;
        self.tokenClass = tokenClass;
        self.tokenValue = tokenValue;

    def printAll(self):
        print("["+str(self.line)+", "+str(self.column)+","+self.tokenClass+","+self.tokenValue+"]")


def splitting(line, lineCount, columnCount):
    nextTypeID = False
    for words in line:
        columnCount += 1

        if nextTypeID == True:
            if re.match("[a-z]",words) or re.match("[A-Z]",words):
                tokenObjects.append(token(lineCount, columnCount, "type-identifier", words))
                columnCount += len(words)
            else:
                tokenObjects.append(token(lineCount, columnCount, "Expected identifier", words))
                columnCount += len(words)
            nextTypeID = False
        else:
            if words == '<?php':
                tokenObjects.append(token(lineCount,columnCount,"php-opening-tag",words))
                columnCount += len(words)

            elif words == '?>':
                tokenObjects.append(token(lineCount,columnCount,"php-closing-tag",words))
                columnCount += len(words)

            elif words == 'class':
                tokenObjects.append(token(lineCount, columnCount, "class", words))
                columnCount += len(words)
                nextTypeID = True

            elif words == 'function':
                tokenObjects.append(token(lineCount, columnCount, "function", words))
                columnCount += len(words)
                nextTypeID = True

            elif words == 'echo':
                tokenObjects.append(token(lineCount,columnCount,"print-output",words))
                columnCount += len(words)

            elif '{' in words:
                tokenObjects.append(token(lineCount,columnCount+re.search('[{]',words).start(),"curly-bracket-opening",'{'))
                splitting(re.split("[{]",words, 1),lineCount, columnCount)

            elif '}' in words:
                tokenObjects.append(token(lineCount,columnCount+re.search('[}]',words).start(),"curly-bracket-closing",'}'))
                splitting(re.split('[}]', words, 1),lineCount, columnCount)

            elif '(' in words:
                tokenObjects.append(token(lineCount,columnCount+re.search('[(]',words).start(),"bracket-opening",'('))
                splitting(re.split("[(]", words, 1),lineCount, columnCount)

            elif ')' in words:
                tokenObjects.append(token(lineCount,columnCount+re.search('[)]',words).start(),"bracket-closing",')'))
                splitting(re.split("[)]", words, 1),lineCount, columnCount)

            elif ';' in words:
                tokenObjects.append(token(lineCount,columnCount+re.search('[;]',words).start(),"semi-colon",';'))
                splitting(re.split("[;]", words, 1),lineCount, columnCount)

            elif '=' in words:
                tokenObjects.append(token(lineCount, columnCount + re.search('[=]', words).start(), "equals", '='))
                splitting(re.split("[=]", words, 1), lineCount, columnCount)

            elif re.match('[+-/*]',words):
                x = re.search('[+-/*]',words,1)
                tokenObjects.append(token(lineCount, columnCount + x.start(), "equals", x.string))
                splitting(re.split("[+-/*]", words, 1), lineCount, columnCount)

            elif '$' in words:
                x = re.sub('$','',words,1)
                tokenObjects.append(token(lineCount, columnCount, "mathematical-operator", x))
                columnCount += 1
                if re.match("^[a-z]", x) or re.match("^[A-Z]", x):
                    tokenObjects.append(token(lineCount, columnCount, "type-identifier", x))
                    columnCount += 1
                else:
                    tokenObjects.append(token(lineCount, columnCount, "Expected Variable", x))
                    columnCount += 1

            elif re.match("", words):
                continue

            else:
                tokenObjects.append(token(lineCount, columnCount, "ERROR", words))
                columnCount += len(words)

# Tokens
tokenObjects = []

# Source code input
sourceCode = open("Test.txt","r")

# Variables
lineCount = 0

# Looping
while True:
    lineCount += 1
    line = sourceCode.readline().split()
    splitting(line, lineCount, 0)
    if not line:
        break

for i in tokenObjects:
    i.printAll()