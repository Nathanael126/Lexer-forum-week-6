import re

def splitString(str):
    return [char for char in str]

class Tokens:
    def __init__(self,Line,Column,TokenClass,TokenValue):
        self.Line = Line
        self.Column = Column
        self.TokenClass = TokenClass
        self.TokenValue = TokenValue

    def printAttributes(self):
        print(str(self.Line) + ', ' + str(self.Column) + ', ' + self.TokenClass + ', ' + self.TokenValue)

tokenArray = []

lineCount = 0
columnCount = 0
typeIDCheck = False
variableCheck = False
stringLiteralCheck = False
stringLiteralArray = []
codeInput = open('Test.txt', 'r').readlines()

for lines in codeInput:
    columnCount = 1
    lineCount += 1
    for check in splitString(lines):
        if check == ' ':
            columnCount += 1
        else:
            break
    for word in lines.split():
        extraColCount = 0
        strArray = splitString(word)
        if typeIDCheck == True:
            typeIDCheck = False
            typeID = []
            for i in strArray:
                j = re.match("[a-z]|[A-Z]", i)
                if j:
                    typeID.append(i)
                    extraColCount += 1
                else:
                    break
            for i in typeID:
                strArray.remove(i)

            tokenArray.append(Tokens(lineCount, columnCount, "type-identifier", "".join(str(x) for x in typeID)))
            columnCount += extraColCount

        if strArray == ['<', '?', 'p', 'h', 'p']:
            tokenArray.append(Tokens(lineCount,columnCount,"php-open-tag", word))
            columnCount += len(strArray)
        elif strArray == ['?', '>']:
            tokenArray.append(Tokens(lineCount, columnCount, "php-close-tag", word))
            columnCount += len(strArray)
        elif strArray == ['c', 'l', 'a', 's', 's']:
            tokenArray.append(Tokens(lineCount, columnCount, "class-declaration", word))
            typeIDCheck = True
            columnCount += len(strArray)
        elif strArray == ['f', 'u', 'n', 'c', 't', 'i', 'o', 'n']:
            tokenArray.append(Tokens(lineCount, columnCount, "function-declaration", word))
            typeIDCheck = True
            columnCount += len(strArray)
        elif strArray == ['e', 'c', 'h', 'o']:
            tokenArray.append(Tokens(lineCount, columnCount, "print", word))
            columnCount += len(strArray)
        else:
            for i in strArray:
                if stringLiteralCheck == True:
                    if not i == '"':
                        stringLiteralArray.append(i)
                        extraColCount += 1
                        continue
                    else:
                        tokenArray.append(Tokens(lineCount, columnCount, "string-literal", "".join(str(x) for x in stringLiteralArray)))
                        columnCount += extraColCount
                        tokenArray.append(Tokens(lineCount, columnCount, "close-string-literal", i))
                        stringLiteralCheck == False
                        continue
                    extraColCount += 1

                if variableCheck == True:
                    variableCheck = False
                    j = re.match("[a-z]|[A-Z]", i)
                    if j:
                        tokenArray.append(Tokens(lineCount, columnCount, "type-identifier",i))
                    else:
                        tokenArray.append(Tokens(lineCount, columnCount, "error, expected variable", i))
                    continue

                if i == '{':
                    tokenArray.append(Tokens(lineCount, columnCount, "open-curly-brackets", i))
                    columnCount += 1
                elif i == '}':
                    tokenArray.append(Tokens(lineCount, columnCount, "closed-curly-brackets", i))
                    columnCount += 1
                elif i == '(':
                    tokenArray.append(Tokens(lineCount, columnCount, "open-brackets", i))
                    columnCount += 1
                elif i == ')':
                    tokenArray.append(Tokens(lineCount, columnCount, "closed-brackets", i))
                    columnCount += 1
                elif i == '=':
                    tokenArray.append(Tokens(lineCount, columnCount, "equals", i))
                    columnCount += 1
                elif i == ';':
                    tokenArray.append(Tokens(lineCount, columnCount, "semicolon", i))
                    columnCount += 1
                elif re.match("[-]|[+*/]", i):
                    tokenArray.append(Tokens(lineCount, columnCount, "math-operator", i))
                    columnCount += 1
                elif re.match("[0-9]", i):
                    tokenArray.append(Tokens(lineCount, columnCount, "number", i))
                    columnCount += 1
                elif i == '$':
                    tokenArray.append(Tokens(lineCount, columnCount, "variable", i))
                    columnCount += 1
                    variableCheck = True
                elif i == '"':
                    tokenArray.append(Tokens(lineCount, columnCount, "open-string-literal", i))
                    columnCount += 1
                    stringLiteralCheck = True
        columnCount += 1

for i in tokenArray:
    i.printAttributes()