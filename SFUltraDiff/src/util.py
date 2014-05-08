import os, struct, sys
import pprint
import difflib
import json
import fnmatch
import hashlib
from collections import OrderedDict,defaultdict
XBOX_PATH = "Z:\\SF4 Engine STuff\\XBOX AE\\battle.eaf.out\\chara\\"
PC_PATH = "C:\\Program Files (x86)\\Steam\\steamapps\\common\\Super Street Fighter IV - Arcade Edition\\resource\\battle\\chara\\"
def hexprint(data):
    for thing in data:
        print( hex(thing),)
    print()
def readNameOffsetTable(f,offset,count,MODE):
    f.seek(offset)
    offsets = []
    names = []
    for i in range(0,count):
        offsets.append(struct.unpack(MODE+"I",f.read(4))[0])
    for offset in offsets:
        if offset == 0:
            names.append("")
        else:
            f.seek(offset)
            names.append(f.read(255).split(b"\x00")[0].decode(encoding='UTF-8'))
    return names
def findFiles(char,path,ext):
    matches = []
    for root, dirnames, filenames in os.walk(path):
        #print( filenames)
        for filename in fnmatch.filter(filenames, char+ext):
            matches.append(os.path.join(root, filename))
    return matches
