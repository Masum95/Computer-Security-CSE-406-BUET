import re
from collections import deque


def main():

    file = open("input2.txt", 'r')

    lineList = []
    for line in file:
        line = line.strip()
        if len(line) == 0:
            continue
        lineList.append(line)

    key = [ord(ch) for ch in list(lineList[0])]
    plainText = [ord(ch) for ch in list(lineList[1])]
    PI = readNth_FormattedArray(lineList,1)
    CP_1 = readNth_FormattedArray(lineList, 2)
    CP_2 = readNth_FormattedArray(lineList, 3)
    E = readNth_FormattedArray(lineList, 4)
    PI_2 = readNth_FormattedArray(lineList, 5)
    P = readNth_FormattedArray(lineList, 6)
    PI_1 = readNth_FormattedArray(lineList, 7)
    shiftAra = readNth_FormattedArray(lineList, 8)

    rem = len(plainText) % 8
    plainText.extend([ord('~')]*(( 8 - rem) % 8))  # filling with dummy data to make multiple of 64 bits
    # ascii to 8-bit binary string
    key = [get_bin(int(i), 8) for i in key]
    plainText = [get_bin(int(i), 8) for i in plainText]

    numOfBlocks = int(len(plainText) / 8)

    plainText = list(''.join(plainText))
    key = list(''.join(key))
    keysInRounds = []

    #  modifying key ( 64 bits key to 56 bits key
    keysIn56Bits = ['0']*56
    for i in range(0, len(CP_1)):
        keysIn56Bits[i] = key[CP_1[i] - 1]

    for blockNo in range(0, numOfBlocks):
        # initial permutation of message
        tmpList = ['0'] * 64
        for i in range(0, len(PI)):
            tmpList[i] = plainText[blockNo*64+PI[i]-1]
        plainText[blockNo*64:blockNo*64+64] = tmpList

        # 16 iterations

        L_i = plainText[blockNo*64:blockNo*64+32]
        R_i = plainText[blockNo*64+32:blockNo*64+64]

        for it in range(16):
            C_i = keysIn56Bits[0:28]
            D_i = keysIn56Bits[28:56]
            C_i = shiftByN(C_i, shiftAra[it])
            D_i = shiftByN(D_i, shiftAra[it])

            CD = C_i + D_i

            K_i = ['0'] * 48
            for i in range(0, len(CP_2)):
                K_i[i] = CD[CP_2[i] - 1]
            keysInRounds.append(K_i)
            # Li = Ri
            # Ri = Li xor f(Ri,Ki)
            tmp = R_i
            R_i = bitWiseXorAra(L_i, func(R_i, K_i, E, PI_2, P))
            L_i = tmp

        plainText[blockNo * 64:blockNo * 64 + 64] = R_i + L_i
        tmpList = ['0'] * 64
        for i in range(0, len(PI_1)):
            tmpList[i] = plainText[blockNo * 64 + PI_1[i] - 1]
        plainText[blockNo * 64:blockNo * 64 + 64] = tmpList
    plainText = ''.join(plainText)

    cipherText = ''
    for i in range(0, int(len(plainText)/8)):
        cipherText += chr(int(plainText[i * 8:i * 8 + 8], 2))

    print("Cipher Text :", cipherText)
    keysInRounds.reverse()
    cipherText = [get_bin(int(ord(i)), 8) for i in cipherText]
    cipherText = list(''.join(cipherText))

    for blockNo in range(0, numOfBlocks):
        # initial permutation of message
        tmpList = ['0'] * 64
        for i in range(0,len(PI)):
            tmpList[i] = cipherText[blockNo*64+PI[i]-1]
        cipherText[blockNo*64:blockNo*64+64] = tmpList

        # 16 iterations
        L_i = cipherText[blockNo*64:blockNo*64+32]
        R_i = cipherText[blockNo*64+32:blockNo*64+64]

        for it in range(16):

            # Li = Ri
            # Ri = Li xor f(Ri,Ki)
            tmp = R_i
            R_i = bitWiseXorAra(L_i, func(R_i, keysInRounds[it], E, PI_2, P))
            L_i = tmp

        cipherText[blockNo * 64:blockNo * 64 + 64] = R_i + L_i

        tmpList = ['0'] * 64
        for i in range(0, len(PI_1)):
            tmpList[i] = cipherText[blockNo * 64 + PI_1[i] - 1]
        cipherText[blockNo * 64:blockNo * 64 + 64] = tmpList
    cipherText = ''.join(cipherText)

    plainText = ''
    for i in range(0, int(len(cipherText) / 8)):
        ch = chr(int(cipherText[i * 8:i * 8 + 8], 2))
        if ch == '~':
            break
        plainText += ch
    print("Plain Text :",plainText)


def shiftByN(ara,n):
    items = deque(ara)
    for i in range(n):
        items.rotate(-1)
    return list(items)


def readNth_FormattedArray(lineList, n):
    cnt = 0
    ara = []
    endFlag = False
    for line in lineList:
            if bool(re.search('.*=.*\[.*',line)):
                line = line[line.rfind('[')+1:]
                cnt += 1

            if line.endswith(']') and cnt == n:
                endFlag = True
            if cnt == n:
                tmp = re.sub('[^0-9]','*',line).split('*')
                elements = []
                for i in tmp:
                    if len(i) == 0:
                        continue
                    elements.append(i)
                for x in elements:
                    ara.append(int(x))

            if endFlag:
                break
    return ara


def get_bin(x, n=0):
    """
    Get the binary representation of x.

    Parameters
    ----------
    x : int
    n : int
        Minimum number of digits. If x needs less digits in binary, the rest
        is filled with zeros.

    Returns
    -------
    str
    """
    return format(x, 'b').zfill(n)


def bitWiseXorAra(ara1, ara2):
    xorAra = ['0'] * len(ara1)
    for i, j, indx in zip(ara1,ara2,range(len(ara1))):
        xorAra[indx] = chr(((ord(i)-ord('0')) ^ (ord(j)-ord('0'))) + ord('0'))
    return xorAra


def func(R_i, K_i, E, PI_2, P):
    expandedR_i = ['0'] * 48
    for i in range(0, len(E)):
        expandedR_i[i] = R_i[E[i] - 1]
    xored = bitWiseXorAra(expandedR_i, K_i)
    sample = ['0']*32
    for i in range(0, len(PI_2)):
        sample[i] = xored[PI_2[i] - 1]

    permutated = ['0'] * 32
    for i in range(0, len(P)):
        permutated[i] = sample[P[i] - 1]

    return permutated


if __name__ == '__main__':
    main()