import math
# Base62 Converter

MAP = '0123456789ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz'
decodeMap = dict()

for i in range(len(MAP)):
    decodeMap[MAP[i]] = str(i)

def to62(base10):
    ret = list()
    while(base10):
        ret.insert(0, MAP[int(base10 % 62)])
        base10 = int(base10/62)
    return "".join(ret)

def to10(base62):
    base62 = str(base62)
    ret = list()
    exp = 0
    number = 0
    for i in range(len(base62) - 1, -1, -1):
        number += int(decodeMap[base62[i]]) * math.pow(62, exp)
        exp += 1
    return int(number)

'''
print(to62(100))
print(to62(10))
print(to62(62))
print(to62(300))
print(to62(3844))
print(to62(3843))
print(to62(3845))
'''

'''
print(to10(45)) #253
print(to10(62))
print(to10(61))
print(to10(63))
print(to10(10)) # 62
'''