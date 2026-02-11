#=============================================
# author: rosa_w
#   mail: wrx1844@qq.com
#   date: Wed, 25 Jun 2014 14:43:02
#=============================================

import math
import maya.cmds as mc

#--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+


def getIntLength(intValue):
    """
    Get the how many digits in a int..
    Exp:
        8     ->  1
        86    ->  2
        835   ->  3
        ...
        96158 ->  5
    """
    i = 1
    d = 1
    while True:
        if abs(intValue) // d < 10:
            return i
        i += 1
        d *= 10


def clamp(minV, maxV, value):
    """
    0, 10,  5  ->   5
    0, 10, -1  ->   0
    0, 10, 11  ->  10
    """
    return min(max(minV, value), maxV)


def setRange(oldMin, oldMax, newMin, newMax, value):
    """
    0 - 10  --->  0 - 100
      |             |
      5      ->     50
    """
    result = ((float(value) - oldMin) / (oldMax - oldMin)
              * (newMax - newMin)) + newMin
    return result


def advanceSin(startValue, endValue, inputV):
    """
    convert a range value to sin 0 - sin 180
    """
    angleValue = setRange(startValue, endValue, 0, 180, inputV)
    sinValue = math.sin(angleValue * math.pi / 180.0)
    return sinValue


def converse(startValue, endValue, inputValue):
    """
    0.0, 0.1, 0.2 ... 0.7, 0.8, 0.9, 1.0, 0.9, 0.8, 0.7, ... 0.2, 0.1, 0.0
    """
    x = setRange(startValue, endValue, -1, 1, inputValue)
    result = 1 - abs(x)
    return result


def getPoleVectorPosition(Root, Mid, Tip):
    """
    #  * (Root)
    #   *
    #    *
    #     *
    #      *
    #       *
    #        * (Mid) -----------> * (poleVector[X, Y, Z])
    #      *
    #    *
    #  * (Tip)
    """
    #-----------------------------------------------------------
    A = mc.xform(Root, q=True, ws=True, t=True)
    B = mc.xform(Mid, q=True, ws=True, t=True)
    C = mc.xform(Tip, q=True, ws=True, t=True)

    AB = math.sqrt((A[0] - B[0]) ** 2 + (A[1] - B[1])
                   ** 2 + (A[2] - B[2]) ** 2)
    BC = math.sqrt((B[0] - C[0]) ** 2 + (B[1] - C[1])
                   ** 2 + (B[2] - C[2]) ** 2)
    AC = math.sqrt((A[0] - C[0]) ** 2 + (A[1] - C[1])
                   ** 2 + (A[2] - C[2]) ** 2)

    AD = (AB ** 2 + AC ** 2 - BC**2) / (AC * 2)
    ADpr = AD / AC

    D = ((C[0] - A[0]) * ADpr + A[0], (C[1] - A[1])
         * ADpr + A[1], (C[2] - A[2]) * ADpr + A[2])
    BD = math.sqrt((B[0] - D[0]) ** 2 + (B[1] - D[1])
                   ** 2 + (B[2] - D[2]) ** 2)
    ScaleV = (AB + BC) / BD
    VectorPosition = ((B[0] - D[0]) * ScaleV + D[0], (B[1] - D[1])
                      * ScaleV + D[1], (B[2] - D[2]) * ScaleV + D[2])

    return VectorPosition

# def remap(value, oldMin, oldMax, newMin, newMax):
#     """
#     Remap a value based on input and output minimin and maximum.

#     :param float value: Value to remap
#     :param float oldMin: Original minimum
#     :param float oldMax: Original maximum
#     :param float newMin: New minimum
#     :param float newMax: New maximum
#     :return: remapped value
#     :rtype: float
#     """
#     return (((value - oldMin) * (newMax - newMin)) / (oldMax - oldMin)) + newMin



# def remap( x, oMin, oMax, nMin, nMax ,clamp=True ):
#     #range check
#     if oMin == oMax:
#         raise Warning( "Warning: Zero input range" )
#     if nMin == nMax:
#         raise Warning( "Warning: Zero output range" )
#     #clamp value
#     if x<=oMin and oMin<oMax and clamp:
#         return nMin
#     elif x>=oMin and oMin>oMax and clamp:
#         return nMin
#     elif x<=oMax and oMin>oMax and clamp:
#         return nMax
#     elif x>=oMax and oMin<oMax and clamp:
#         return nMax
#     #check reversed input range
#     reverseInput = False
#     oldMin = min( oMin, oMax )
#     oldMax = max( oMin, oMax )
#     if not oldMin == oMin:
#         reverseInput = True
#     #check reversed output range
#     reverseOutput = False   
#     newMin = min( nMin, nMax )
#     newMax = max( nMin, nMax )
#     if not newMin == nMin :
#         reverseOutput = True
#     portion = (x-oldMin)*(newMax-newMin)/(oldMax-oldMin)
#     if reverseInput:
#         portion = (oldMax-x)*(newMax-newMin)/(oldMax-oldMin)
#     result = portion + newMin
#     if reverseOutput:
#         result = newMax - portion
#     return result



def remapValue( inputValue, inputRange, outputRange):
    """Remap Value: that allows you to take an input value list and remap its value list with liner.
    One can remap this to a new output scalar value.
    """ 
    if type(inputValue)==list:
        res = []
        for val in inputValue:
            resVal = remap(val,inputRange[0],inputRange[1],outputRange[0],outputRange[1])
            res.append( resVal )
        return res
    else:
        resVal = remap(inputValue,inputRange[0],inputRange[1],outputRange[0],outputRange[1])
        return resVal



def __averageNumbers( evStep, counts, _range=[0.0,1.0] ):
    """__averageNumbers: funtiont in shared/mathSelf.py/
    can average value from a value to b value
    evStep: control increment or decreasing
        +float More and more dense
        -float More and more sparse
    counts: many spans
    _rang:from to
    """
    #wrong number input raise
    if evStep>1.0 or evStep<-1.0:
        raise TypeError( " evStep must in range 0.0~1.0 " )
    if len(_range)!=2:
        raise TypeError( "Range must 2 like [from,to] " )
        
    resStep = [0.0]
    #
    if evStep==1:
        for i in range(counts):
            resStep.append( 1.0 )
    elif evStep!=0:
        tempStList = []
        dev = 0.0
        flMax = 1.0
        for i in range(counts):
            flMax = flMax-flMax*evStep
            dev += flMax*evStep
            tempStList.append( dev )
        for v in tempStList:
            resStep.append( v/dev )
    else:
        v = 0.0
        devNum = 1.0/counts
        for i in range(counts):
            v += devNum
            resStep.append( v )
    #remapValue
    if _range!=[0.0,1.0]:
        resStep = remapValue(resStep,[0.0,1.0],_range)
    return resStep



def averageNumber( evStep, counts, _range=[0.0,1.0], circular=False ):
    """averageNumber: funtiont in shared/mathSelf.py/
    can average value from a value to b value
    evStep: control increment or decreasing
        +float More and more dense
        -float More and more sparse
    counts: many spans
    _rang:from to
    circular:value from min to max to min
    """
    if circular:
        res = __averageNumbers(evStep,int(counts)/2,_range)
        if counts%2==0:
            rever = res[0:-1]
            rever.reverse()
            return res + rever
        else:
            rever = res[:]
            rever.reverse()
            return res + rever
    else:
        return __averageNumbers(evStep,counts,_range)


def convertAxisToVector(axis):
    """
    Convert an axis to a normalized vector.

    :param str axis: options are x, y, z.
    :return: vector
    :rtype: list
    """
    return [1 if a == axis.lower() else 0 for a in ["x", "y", "z"]]



def remap(value, oldMin, oldMax, newMin, newMax):
    """
    Remap a value based on input and output minimin and maximum.

    :param float value: Value to remap
    :param float oldMin: Original minimum
    :param float oldMax: Original maximum
    :param float newMin: New minimum
    :param float newMax: New maximum
    :return: remapped value
    :rtype: float
    """
    return (((value - oldMin) * (newMax - newMin)) / (oldMax - oldMin)) + newMin


def remapWeighting(values1, values2=[0.0, 1.0]):
    """
    Get a weighting list how to blend values1 and values2, this math
    function is usefull to get the parenting weights, between lists with
    different parameters.

    :param list values1:
    :param list values2:
    :return: list of dictionaries with blend weighting values
    :rtype: list
    """
    tWeighting = []
    for j, tP in enumerate(values1):
        for i, mP in enumerate(values2):
            if tP == mP:
                tWeighting.append({i: 1})
                continue

            # handle lists that dont start with 0 ( closed curves )
            if mP == 0:
                mP = 1

            pP = values2[i - 1]
            if pP < tP < mP:
                weight = remap(tP, pP, mP, 0, 1)
                tWeighting.append({i - 1: 1 - weight, i: weight})
                continue

    return tWeighting


def getDistance(st, ed):
    distance = math.sqrt(pow((ed[0] - st[0]), 2) + pow((ed[1] - st[1]), 2) + pow((ed[2] - st[2]), 2))
    return distance


def normalizeVector(x=0, y=0, z=0):
    length = math.sqrt( (x*x)+(y*y)+(z*z) )
    nx = x / length
    ny = y / length
    nz = z / length
    return nx, ny, nz

def get2VectorAngle(a,b):
    aLenth = getDistance(a, (0,0,0))
    bLenth = getDistance(b, (0,0,0))
    cosValue = ( a[0]*b[0] + a[1]*b[1] + a[2]*b[2] ) / (aLenth*bLenth)
    angle = math.degrees( math.acos(cosValue) )
    return angle
