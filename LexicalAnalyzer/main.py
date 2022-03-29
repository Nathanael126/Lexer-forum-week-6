import re

class token:
    def __init__(self, line, column, tokenClass, tokenValue):
        self.line = line;
        self.column = column;
        self.tokenClass = tokenClass;
        self.tokenValue = tokenValue;

    def printAll(self):
        print("["+str(self.line)+", "+str(self.column)+","+self.tokenClass+","+self.tokenClass+"]")


def splitting(line, lineCount, columnCount):
    for words in line:
        columnCount += 1
        if words == '<?php':
            tokenObjects.append(token(lineCount,columnCount,"php-opening-tag",words))
            columnCount += len(words)
        elif words == '?>':
            tokenObjects.append(token(lineCount,columnCount,"php-closing-tag",words))
            columnCount += len(words)
        elif '{' in words:
            tokenObjects.append(token(lineCount,columnCount,"curly-bracket-opening",words))
            splitting(re.split("[{]",words, 1),lineCount, columnCount)
        elif '}' in words:
            tokenObjects.append(token(lineCount,columnCount,"curly-bracket-closing",words))
            splitting(re.split('[}]', words, 1),lineCount, columnCount)
        elif '(' in words:
            tokenObjects.append(token(lineCount,columnCount,"bracket-opening",words))
            splitting(re.split("[(]", words, 1),lineCount, columnCount)
        elif ')' in words:
            tokenObjects.append(token(lineCount,columnCount,"bracket-closing",words))
            splitting(re.split("[)]", words, 1),lineCount, columnCount)
        else:
            print("ERROR INVALID")

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
    print(line)
    if not line:
        break

for i in tokenObjects:
    i.printAll()