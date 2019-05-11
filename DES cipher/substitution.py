import operator
import re


def main():
    file = open("input1.txt",'r')
    lineList = []
    for line in file:
        line = line.strip()
        if len(line) == 0:
            continue
        lineList.append(line)
    cipherText = lineList[0]
    freqLetter = lineList[1].split(', ')
    freqWord = lineList[2].split(', ')
    print("Cipher Text = \n", cipherText)
    print("Frequently used words  = ", freqWord)
    print("Frequently used letters = ", freqLetter)
    countAra = {}  # this dictionary will count the occurrences of letters in cipherText

    for ch in cipherText:
        if not ch in countAra:
            countAra[ch] = 1
        else:
            countAra[ch] += 1

    countAra = sorted(countAra.items(), key=operator.itemgetter(1),reverse=True)

    plainToCipherDict = dict()
    # this dictionary will store mapping of  plain-text letter to cipher-text letter

    # direct mapping of 3 most frequent letters
    for i in range(3):
        plainToCipherDict[freqLetter[i]] = countAra[i][0]

    '''
    we look for regex match in cipher-text from the set of given words. 
    if we can unambiguously find a regex word match, we delete that word 
    from most frequent words' list and add more letter mapping to dictionary
    this process continues until the list of frequent words is empty
    
    '''

    while len(freqWord) != 0:
        regList = makeRegexList(freqWord,plainToCipherDict)
        #print(regList)

        uniqueMatchString, indx = getUniqueMatch(regList,cipherText)
        #print(uniqueMatchString)
        # index of the word which has a regex match
        for i in range(0, len(uniqueMatchString)-1):
            plainToCipherDict[freqWord[indx][i]] = uniqueMatchString[i]

        #print(plainToCipherDict)
        del freqWord[indx]

    cipherToPlainDict = reverseDict(plainToCipherDict)
    #print(cipherToPlainDict)
    plainText,conversion = getCipherToPlain(cipherText, cipherToPlainDict)
    print("Plain - Text is : ")
    print(plainText)
    cipher = getPlainToCipher(plainText, plainToCipherDict)
    print("Encoded string : ")
    print(cipher)
    accuracy = conversion*1.0/len(plainText)*100
    print("Accuracy is = %.2f %%" % accuracy)


def reverseDict(dict1):
    dict2 = {}
    for key, val in dict1.items():
        dict2[val] = key
    return dict2


def getPlainToCipher(plainText,plainToCipherDict):
    lst = list(plainText)
    i = -1
    for ch in lst:
        i += 1
        if ch in plainToCipherDict:
            lst[i] = plainToCipherDict[ch]
        else:
            lst[i] = lst[i]
            continue

    return ''.join(lst)


def getCipherToPlain(cipherText,cipherToPlainDict):
    lst = list(cipherText)
    i = -1
    cnt = 0
    for ch in lst:
        i += 1
        if ch in cipherToPlainDict:
            lst[i] = cipherToPlainDict[ch]
            cnt += 1
        else:
            lst[i] = '*'
            continue

    return ''.join(lst),cnt


def getUniqueMatch(regList,cipherText):
    indx = 0
    for reg in regList:
        match = re.findall(reg,cipherText)
        if len(match) == 1:
            return match[0],indx
        indx += 1


def makeRegexList(lst,plainToCipherDict):
    retLst = []
    for word in lst:
        regWord = ''
        for ch in word:
            if ch in plainToCipherDict:
                regWord += plainToCipherDict[ch]
            else:
                regWord += '.'
        retLst.append(regWord)
    return retLst


if __name__ == '__main__':
    main()