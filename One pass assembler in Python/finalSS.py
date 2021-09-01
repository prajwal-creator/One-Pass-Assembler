file = open('input.txt', 'r')
outputFile = open('output.txt', 'w')
resultFile = open('result.txt', 'w')
symtab = dict()
name = ''
optab = {
    "LDA" : "00",
    "STA" : "23",
    "LDCH" : "15",
    "STCH" : "18"
}
input = list()
typeOfList = type(input)
for each in file:
    individualLine = each.split(" ")[0].split('\t')
    individualLine[-1] = (individualLine[-1])[:-1]
    input.append(individualLine)
if (input[0])[-2] == 'START':
    startingInstruction = input.pop(0)
    name = startingInstruction[0]
    sa = int(float(startingInstruction[-1]))
    locctr = sa
else:
    locctr = 0
for i in input:
    if i[1] == 'END':
        end = i
        break
    if i[0] == '-':
        opcode = optab[i[1]]
        if not i[-1] in symtab:
            symtab[i[-1]] = ['*', locctr]
            outputFile.write(opcode + '\t' + '0000' + '\n')
        else:
            if type(symtab[i[-1]]) == typeOfList:
                (symtab[i[-1]]).append(locctr)
                outputFile.write(opcode+'\t'+'0000'+ '\n')
            else:
                outputFile.write(opcode + '\t' + str(symtab[i[-1]]) + '\n')
        locctr += 3
    else:
        if not i[0] in symtab:
            symtab[i[0]] = locctr
        else:
            if type(symtab[i[0]]) == typeOfList:
                refList = symtab[i[0]]
                symtab[i[0]] = locctr
                for sym in refList[1:]:
                    outputFile.write(str(sym + 1) + '\t' + str(locctr) + '\n')
            else:
                print('error')
        if i[1] in optab:
            opcode = optab[i[1]]
            if not i[-1] in symtab:
                symtab[i[-1]] = ['*', locctr]
                outputFile.write(opcode + '\t' + '0000' + '\n')
            else:
                if type(symtab[i[-1]]) == typeOfList:
                    (symtab[i[-1]]).append(locctr)
                    outputFile.write(opcode + '\t' + '0000' + '\n')
                else:
                    outputFile.write(opcode + '\t' + str(symtab[i[-1]]) + '\n')
        if i[-2] == 'RESW':
            locctr += (3 * int(float(i[-1])))
        elif i[-2] == 'RESB':
            locctr += int(float(i[-1]))
        elif i[-2] == 'BYTE':
            locctr += len(i[-1]) - 3
        else:
            locctr += 3
lengthOfProgram = locctr - sa
outputFile = open('output.txt', 'r')
output = list()
def regToByte(str,n):
    return (n-len(str))*'0' + str
for each in outputFile:
    individualLine = each.split(" ")[0].split('\t')
    individualLine[-1] = (individualLine[-1])[:-1]
    output.append(individualLine)
headerLen = regToByte(hex((locctr - sa)).split('x')[-1],8)
headerStart = regToByte(str(sa),6)
resultFile.write("H^"+name+'^'+headerStart+'^'+headerLen+'\n')
resultFile.write("T^00"+str(sa)+'^0'+hex((locctr - sa - 2)).split('x')[-1])
for i in output:
    if len(i[0]) == 2:
        if i[1] == '0000':
            resultFile.write('^' + i[0] + i[1])
        else:
            resultFile.write('^' + i[0] + str(int(i[1])+1))
    else:
        resultFile.write('\n' + 'T^' + regToByte(i[0],6) + '^02^' + i[1])
    # if i[1] == '0000':
    #     resultFile.write('^'+i[0]+i[1])
    # else:
    #     resultFile.write('\n'+'T^'+i[0]+'^02^'+i[1])
resultFile.write('\nE^00'+str(sa))