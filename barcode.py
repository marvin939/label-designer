from PyQt4 import QtGui, QtCore
import math

_i2of5 = {'0':'nnwwn',
          '1':'wnnnw',
          '2':'nwnnw',
          '3':'wwnnn',
          '4':'nnwnw',
          '5':'wnwnn',
          '6':'nwwnn',
          '7':'nnnww',
          '8':'wnnwn',
          '9':'nwnwn',
          'start':'nnnn',
          'end':'Wnn'}


_3of9 = {'0':'NnNwWnWnN',
         '1':'WnNwNnNnW',
         '2':'NnWwNnNnW',
         '3':'WnWwNnNnN',
         '4':'NnNwWnNnW',
         '5':'WnNwWnNnN',
         '6':'NnWwWnNnN',
         '7':'NnNwNnWnW',
         '8':'WnNwNnWnN',
         '9':'NnWwNnWnN',
         'A':'WnNnNwNnW',
         'B':'NnWnNwNnW',
         'C':'WnWnNwNnN',
         'D':'NnNnWwNnW',
         'E':'WnNnWwNnN',
         'F':'NnWnWwNnN',
         'G':'NnNnNwWnW',
         'H':'WnNnNwWnN',
         'I':'NnWnNwWnN',
         'J':'NnNnWwWnN',
         'K':'WnNnNnNwW',
         'L':'NnWnNnNwW',
         'M':'WnWnNnNwN',
         'N':'NnNnWnNwW',
         'O':'WnNnWnNwN',
         'P':'NnWnWnNwN',
         'Q':'NnNnNnWwW',
         'R':'WnNnNnWwN',
         'S':'NnWnNnWwN',
         'T':'NnNnWnWwN',
         'U':'WwNnNnNnW',
         'V':'NwWnNnNnW',
         'W':'WwWnNnNnN',
         'X':'NwNnWnNnW',
         'Y':'WwNnWnNnN',
         'Z':'NwWnWnNnN',
         '-':'NwNnNnWnW',
         '.':'WwNnNnWnN',
         ' ':'NwWnNnWnN',
         '$':'NwNwNwNnN',
         '/':'NwNwNnNwN',
         '+':'NwNnNwNwN',
         '%':'NnNwNwNwN',
         '*':'NwNnWnWnN'}

_3of9check = {'0':0,
              '1':1,
              '2':2,
              '3':3,
              '4':4,
              '5':5,
              '6':6,
              '7':7,
              '8':8,
              '9':9,
              'A':10,
              'B':11,
              'C':12,
              'D':13,
              'E':14,
              'F':15,
              'G':16,
              'H':17,
              'I':18,
              'J':19,
              'K':20,
              'L':21,
              'M':22,
              'N':23,
              'O':24,
              'P':25,
              'Q':26,
              'R':27,
              'S':28,
              'T':29,
              'U':30,
              'V':31,
              'W':32,
              'X':33,
              'Y':34,
              'Z':35,
              '-':36,
              '.':37,
              ' ':38,
              '$':39,
              '/':40,
              '+':41,
              '%':42}


_128CharSetA =  {
                ' ':0, '!':1, '"':2, '#':3, '$':4, '%':5, '&':6, "'":7,
                '(':8, ')':9, '*':10, '+':11, ',':12, '-':13, '.':14, '/':15,
                '0':16, '1':17, '2':18, '3':19, '4':20, '5':21, '6':22, '7':23,
                '8':24, '9':25, ':':26, ';':27, '<':28, '=':29, '>':30, '?':31,
                '@':32, 'A':33, 'B':34, 'C':35, 'D':36, 'E':37, 'F':38, 'G':39,
                'H':40, 'I':41, 'J':42, 'K':43, 'L':44, 'M':45, 'N':46, 'O':47,
                'P':48, 'Q':49, 'R':50, 'S':51, 'T':52, 'U':53, 'V':54, 'W':55,
                'X':56, 'Y':57, 'Z':58, '[':59, '\\':60, ']':61, '^':62, '_':63,
                '\x00':64, '\x01':65, '\x02':66, '\x03':67, '\x04':68, '\x05':69, '\x06':70, '\x07':71,
                '\x08':72, '\x09':73, '\x0A':74, '\x0B':75, '\x0C':76, '\x0D':77, '\x0E':78, '\x0F':79,
                '\x10':80, '\x11':81, '\x12':82, '\x13':83, '\x14':84, '\x15':85, '\x16':86, '\x17':87,
                '\x18':88, '\x19':89, '\x1A':90, '\x1B':91, '\x1C':92, '\x1D':93, '\x1E':94, '\x1F':95,
                'FNC3':96, 'FNC2':97, 'SHIFT':98, 'Code C':99, 'Code B':100, 'FNC4':101, 'FNC1':102, 'START A':103,
                'START B':104, 'START C':105, 'STOP':106
           }

_128CharSetB = {
                ' ':0, '!':1, '"':2, '#':3, '$':4, '%':5, '&':6, "'":7,
                '(':8, ')':9, '*':10, '+':11, ',':12, '-':13, '.':14, '/':15,
                '0':16, '1':17, '2':18, '3':19, '4':20, '5':21, '6':22, '7':23,
                '8':24, '9':25, ':':26, ';':27, '<':28, '=':29, '>':30, '?':31,
                '@':32, 'A':33, 'B':34, 'C':35, 'D':36, 'E':37, 'F':38, 'G':39,
                'H':40, 'I':41, 'J':42, 'K':43, 'L':44, 'M':45, 'N':46, 'O':47,
                'P':48, 'Q':49, 'R':50, 'S':51, 'T':52, 'U':53, 'V':54, 'W':55,
                'X':56, 'Y':57, 'Z':58, '[':59, '\\':60, ']':61, '^':62, '_':63,
                '' :64, 'a':65, 'b':66, 'c':67, 'd':68, 'e':69, 'f':70, 'g':71,
                'h':72, 'i':73, 'j':74, 'k':75, 'l':76, 'm':77, 'n':78, 'o':79,
                'p':80, 'q':81, 'r':82, 's':83, 't':84, 'u':85, 'v':86, 'w':87,
                'x':88, 'y':89, 'z':90, '{':91, '|':92, '}':93, '~':94, '\x7F':95,
                'FNC3':96, 'FNC2':97, 'SHIFT':98, 'Code C':99, 'FNC4':100, 'Code A':101, 'FNC1':102, 'START A':103,
                'START B':104, 'START C':105, 'STOP':106
           }

_128CharSetC = {
                '00':0, '01':1, '02':2, '03':3, '04':4, '05':5, '06':6, '07':7,
                '08':8, '09':9, '10':10, '11':11, '12':12, '13':13, '14':14, '15':15,
                '16':16, '17':17, '18':18, '19':19, '20':20, '21':21, '22':22, '23':23,
                '24':24, '25':25, '26':26, '27':27, '28':28, '29':29, '30':30, '31':31,
                '32':32, '33':33, '34':34, '35':35, '36':36, '37':37, '38':38, '39':39,
                '40':40, '41':41, '42':42, '43':43, '44':44, '45':45, '46':46, '47':47,
                '48':48, '49':49, '50':50, '51':51, '52':52, '53':53, '54':54, '55':55,
                '56':56, '57':57, '58':58, '59':59, '60':60, '61':61, '62':62, '63':63,
                '64':64, '65':65, '66':66, '67':67, '68':68, '69':69, '70':70, '71':71,
                '72':72, '73':73, '74':74, '75':75, '76':76, '77':77, '78':78, '79':79,
                '80':80, '81':81, '82':82, '83':83, '84':84, '85':85, '86':86, '87':87,
                '88':88, '89':89, '90':90, '91':91, '92':92, '93':93, '94':94, '95':95,
                '96':96, '97':97, '98':98, '99':99, 'Code B':100, 'Code A':101, 'FNC1':102, 'START A':103,
                'START B':104, 'START C':105, 'STOP':106
           }


_128ValueEncodings = {  0:'11011001100',  1:'11001101100',  2:'11001100110', 
                        3:'10010011000',  4:'10010001100',  5:'10001001100',
                        6:'10011001000',  7:'10011000100',  8:'10001100100',
                        9:'11001001000',  10:'11001000100', 11:'11000100100',
                        12:'10110011100', 13:'10011011100', 14:'10011001110',
                        15:'10111001100', 16:'10011101100', 17:'10011100110',
                        18:'11001110010', 19:'11001011100', 20:'11001001110',
                        21:'11011100100', 22:'11001110100', 23:'11101101110',
                        24:'11101001100', 25:'11100101100', 26:'11100100110',
                        27:'11101100100', 28:'11100110100', 29:'11100110010',
                        30:'11011011000', 31:'11011000110', 32:'11000110110',
                        33:'10100011000', 34:'10001011000', 35:'10001000110',
                        36:'10110001000', 37:'10001101000', 38:'10001100010',
                        39:'11010001000', 40:'11000101000', 41:'11000100010',
                        42:'10110111000', 43:'10110001110', 44:'10001101110',
                        45:'10111011000', 46:'10111000110', 47:'10001110110',
                        48:'11101110110', 49:'11010001110', 50:'11000101110',
                        51:'11011101000', 52:'11011100010', 53:'11011101110',
                        54:'11101011000', 55:'11101000110', 56:'11100010110',
                        57:'11101101000', 58:'11101100010', 59:'11100011010',
                        60:'11101111010', 61:'11001000010', 62:'11110001010',
                        63:'10100110000', 64:'10100001100', 65:'10010110000',
                        66:'10010000110', 67:'10000101100', 68:'10000100110',
                        69:'10110010000', 70:'10110000100', 71:'10011010000',
                        72:'10011000010', 73:'10000110100', 74:'10000110010',
                        75:'11000010010', 76:'11001010000', 77:'11110111010',
                        78:'11000010100', 79:'10001111010', 80:'10100111100',
                        81:'10010111100', 82:'10010011110', 83:'10111100100',
                        84:'10011110100', 85:'10011110010', 86:'11110100100',
                        87:'11110010100', 88:'11110010010', 89:'11011011110',
                        90:'11011110110', 91:'11110110110', 92:'10101111000',
                        93:'10100011110', 94:'10001011110', 95:'10111101000',
                        96:'10111100010', 97:'11110101000', 98:'11110100010',
                        99:'10111011110', 100:'10111101110',101:'11101011110',
                        102:'11110101110',103:'11010000100',104:'11010010000',
                        105:'11010011100',106:'11000111010'
                        }


def bar_Code128(data, checksum=False):
    """ Returns a QPixmap containing the barcode
        charSet can be 'A', 'B', or 'C' to denote a preference"""
    _dpi = (QtCore.QCoreApplication.instance().desktop().physicalDpiX(), QtCore.QCoreApplication.instance().desktop().physicalDpiY())
    _dpmm = (_dpi[0] / 25.4, _dpi[1] / 25.4)
    datatext = str(data) 
    
    #n = 2.4 # narrow to wide ratio
    c = len(datatext) # number of characters
    x = 2.0 # bar size
  
    
    
    currentSet = ""
    # Look ahead 2 and check to see if they're digits, if so, use set C
    if datatext[:2].isdigit() and len(datatext[:2]) == 2:
        code = "11010011100" # start with set C
        currentSet = "C"
    else:
        if datatext[0] in _128CharSetB:
            code = "11010010000" # start with set B
            currentSet = "B"
        else:
            code = "11010000100" # start with set A
            currentSet = "A"
            
    completed = False
    index = 0
    checksumTotal = 0
    weight = 1
    while not completed:
        if currentSet == "C":
            val = _128CharSetC[datatext[index:index+2]]
            index += 2
            
            if index == len(datatext):
                completed = True
            
            elif datatext[index:index+2].isdigit() and len(datatext[index:index+2]) == 2:
                currentSet = "C"
            else:
                if datatext[index] in _128CharSetB:
                    currentSet = "B"
                else:
                    currentSet = "A"
        elif currentSet == "B":
            val = _128CharSetB[datatext[index]]
            index += 1
            if index == len(datatext):
                completed = True
            
            elif datatext[index:index+2].isdigit() and len(datatext[index:index+2]) == 2:
                currentSet = "C"
            else:
                if datatext[index] in _128CharSetB:
                    currentSet = "B"
                else:
                    currentSet = "A"
        elif currentSet == "A":
            val = _128CharSetA[datatext[index]]
            index += 1
            
            if index == len(datatext):
                completed = True
            
            elif datatext[index:index+2].isdigit() and len(datatext[index:index+2]) == 2:
                currentSet = "C"
            else:
                if datatext[index] in _128CharSetA:
                    currentSet = "A"
                else:
                    currentSet = "B"
        code += _128ValueEncodings[val]
            
        checksumTotal += weight*val
        weight += 1
            
    
    code += "1100011101011"
    
    
    codeGroups = []
    
    last = None
    for i in code:
        if i == last:
            codeGroups[-1].append(i)
        else:
            codeGroups.append([i])
            last = i
            
    width = x * len(code)
    
    height = 10.0
    
    bitmap = QtGui.QPixmap(width, height)
    
    bitmap.fill()
    
    painter = QtGui.QPainter(bitmap)
    painter.setBrush(QtCore.Qt.black)
    currentPos = 0.0
    
    pen = painter.pen()
    pen.setWidthF(x)
    painter.setPen(pen)
    
    for group in codeGroups:
        if group[0] == "1": # bar
            for i in group:
                currentPos += x/2.0
                start = QtCore.QPointF(currentPos, 0.0)
                end = QtCore.QPointF(currentPos, height)
                painter.drawLine(start, end)
                currentPos += x/2.0
        else:
            currentPos += len(group) * x
            
    return bitmap
    
            
    


def bar_I2of5(data, checksum=False):
    """ Returns a QPixmap containing the barcode """
    _dpi = (QtCore.QCoreApplication.instance().desktop().physicalDpiX(), QtCore.QCoreApplication.instance().desktop().physicalDpiY())
    _dpmm = (_dpi[0] / 25.4, _dpi[1] / 25.4)
    datatext = str(data) 
    if not datatext.isdigit():
        raise TypeError("i2of5 can only contain digits 0-9")
    
    if checksum:
        if len(datatext) % 2 == 0:
            datatext = '0'+datatext
        odd = True
        total = 0
        for i in datatext:
            if odd:
                total += int(i)*3
            else:
                total += int(i)
            odd = not odd
        datatext += str(10 - (total % 10))
                   
    
    elif len(datatext) % 2 == 1:
        datatext = '0' + datatext
    
    n = 2.7 # narrow to wide ratio
    c = len(datatext) # number of characters
    x = 5.0 # small bar size
    
    width = math.ceil(((c * ((2*n) + 3)) + 6 + n ) * x)
    
    height = 20.0
    
    bitmap = QtGui.QPixmap(width, height)
    
    bitmap.fill()
    
    
    painter = QtGui.QPainter(bitmap)
    painter.setBrush(QtCore.Qt.black)
    currentPos = 0.0
    
    currentPos = _draw_i2of5_line(painter, _i2of5['start'], currentPos)
    
    for i in range(c/2):
        first = _i2of5[datatext[(i*2)]]
        second = _i2of5[datatext[(i*2)+1]]
        
        code = ''
        for h in range(5):
            code += first[h] + second[h]
            
        currentPos = _draw_i2of5_line(painter, code, currentPos)
        
    _draw_i2of5_line(painter, _i2of5['end'], currentPos)
        
    return bitmap
            
    
        
def _draw_i2of5_line(painter, digitcode, currentPos):
    """ Digitcode is the interlaced code (nnwnw...) """
    #_dpi = (QtCore.QCoreApplication.instance().desktop().physicalDpiX(), QtCore.QCoreApplication.instance().desktop().physicalDpiY())
    #_dpmm = (_dpi[0] / 25.4, _dpi[1] / 25.4)
    n = 2.7
    x = 5.0 #0.508 * _dpmm[0]
    #x = 2.0
    height = 20.0
    newPos = currentPos
    space = False
    for i in digitcode:
        if i == 'n':
            size = x
        else:
            size = x*n
        newPos += size/2.0
        if not space:
            start = QtCore.QPointF(newPos, 0.0)
            end = QtCore.QPointF(newPos, height)
            
            pen = painter.pen()
            pen.setWidthF(size)
            painter.setPen(pen)
            
            painter.drawLine(start, end)
        newPos += size/2.0
        space = not space
    return newPos

def bar_3of9(data, checksum=False):
    datatext = str(data)
    n = 2.8
    x = 5.0
    c = len(datatext) + 2
    if checksum:
        c += 1
    
    if "*" in datatext:
        raise ValueError("data cannot contain the * character")
    
    
    codeList = []
    
    checksumValue = 0
    datatext = "*%s*" % datatext
    for char in datatext:
        codeList.append(_3of9[char])
        if char <> "*":
            checksumValue += _3of9check[char]
            
    if checksum:
        checksumValue = checksumValue % 43
        for i, v in _3of9check.items():
            if v == checksumValue:
                checksumChar = i
                break
        codeList.insert(-1, _3of9[checksumChar])
    
    
    
    
    height = 20.0
    
    width = c * ((n*3.0) + 6) * x + ((c - 1) * x)
    
    bitmap = QtGui.QPixmap(width, height)
    
    bitmap.fill()
    
    painter = QtGui.QPainter(bitmap)
    painter.setBrush(QtCore.Qt.black)
    currentPos = 0.0
    for block in codeList:
        for pos in range(len(block)):

            if block[pos].lower() == 'w':
                size = n * x
            else:
                size = x
            if pos % 2 == 0:
                currentPos += size/2.0
                
                start = QtCore.QPointF(currentPos, 0.0)
                end = QtCore.QPointF(currentPos, height)
                
                pen = painter.pen()
                pen.setWidthF(size)
                painter.setPen(pen)
                     
                painter.drawLine(start, end)
                     
                currentPos += size/2.0
            else:
                currentPos += size
        
        currentPos += x
    print currentPos-x, width
            
    return bitmap
    
    
    
    
    
    