#!/usr/bin/python

from colorama import init, Fore, Back, Style

from math import ceil

import sys, os, argparse, re



init(autoreset=True)

isVerbose = False



def lstToStr(lst, printBrackets=False, isFirst=True):

    returnStr = ""

    if isinstance(lst, list):

        if printBrackets and not isFirst:

            returnStr+="["

        for i in range(0, len(lst)):

            if isinstance(lst[i], list):

                returnStr += lstToStr(lst[i], printBrackets, False)

            elif isinstance(lst[i], str):

                if printBrackets and not isFirst:

                   returnStr += "'"+lst[i] + "'"

                else:

                   returnStr += lst[i]

	    elif isinstance( lst[i], int): 

                   returnStr += str( lst[i])

            if i!= len(lst)-1 and printBrackets and not isFirst:

                returnStr+=","

        if printBrackets and not isFirst:

            returnStr+="]"



    elif isinstance(lst, str):

        return lst

    return returnStr



def logVerbose(message):

    global isVerbose

    message = lstToStr(message, True)

    if isVerbose:

        print "\n"+ Fore.RED + Back.BLACK + message





def readFile(fileName):

    byteData = []

    with open(fileName, "rb") as f:

        byte = f.read(1)

        while byte != "":

             byteData.append( byte )

             byte = f.read(1)

    logVerbose( [ "ByteData is ", byteData])

    return byteData



def writeFile( fileName, data ):

   with open(fileName, "w") as f:

        f.seek(0)

        f.write("".join(data))

        f.truncate()

        f.close()



def toBits( byte ):

    return list('{0:08b}'.format( ord(byte)))

def toByte(bits):

    logVerbose(["Received bit array: ", bits])

    byte = str( "".join(bits))

    b = chr( int(byte, 2) ) 

    logVerbose(["Converted to bytes: ", b ])

    return b

def flipBit(byteData, start, end):

    logVerbose("In function flipBit")

    startByte = start // 8

    endByte =  end // 8

    logVerbose(["Start Byte is: ", startByte, "\nEnd Byte is: ", endByte])

    if startByte <= len(byteData) and endByte <= len(byteData) and startByte <= endByte:

        if len(byteData) == 0:

             logVerbose("byteData length is zero")

             return 

        offsetStart = start - ( startByte * 8 )

        offsetEnd = end - (endByte * 8 )

        bits = []

        print "In (bytes):   ", "".join(byteData[startByte:endByte+1])

        for byte in byteData[startByte:endByte+1]:

            bits.extend(toBits(byte))

        print "In (bits):    ", "".join(bits)

        logVerbose(["Bit array is: ", bits])

        logVerbose(["OffestStart: ", offsetStart])

        logVerbose(["OffsetEnd: ", offsetEnd])

        for i in range(offsetStart, offsetEnd + 1):

            logVerbose(["Bit was: ", bits[i]])

            bits[i] = "1" if bits[i] == "0" else "0"

            logVerbose(["Bit is: ", bits[i]])

        print "Out (bits):   ", "".join(bits)

        modifiedBytes = [ toByte(bits[i:i+8]) for i in range(0, len(bits), 8)]

        print "Out (bytes):  ", "".join(modifiedBytes)

        for i in range(0, len(modifiedBytes)):

            byteData[startByte + i] = modifiedBytes[i]

        return byteData

    else:

        logVerbose("Arguments not in range")



parser = argparse.ArgumentParser()

parser.add_argument('-bytes',  action='store_true', dest='isBytes', default=False)

parser.add_argument('-file', action='store', dest='fileName')

parser.add_argument('-start', action="store", dest='positionStart')

parser.add_argument('-end', action="store", dest='positionEnd', default=-1)

parser.add_argument('-v', action='store_true', dest='isVerbose', default=False)

parser.add_argument("-out", action='store', dest="fileOut", default="")

args = parser.parse_args()

isVerbose = args.isVerbose

fileName = args.fileName

if args.fileOut == "":

    fileOut = fileName

else:

    fileOut = args.fileOut

start = int ( args.positionStart )

end = int ( args.positionEnd )

if end < 0:

   end = start

   logVerbose( "Setting end as Start")

logVerbose([ "Start bit/byte is: ", start, " End bit/byte is: ", end])

isBytes = args.isBytes

logVerbose([ "Using ", "bytes" if isBytes else "bits"])

byteData = readFile( fileName )

result = flipBit( byteData, start, end )

logVerbose( result )

writeFile(fileOut, result)
