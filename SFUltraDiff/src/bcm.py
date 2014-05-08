import os, struct, sys
import pprint
import difflib
import json
import fnmatch
import hashlib
from util import *
from collections import OrderedDict,defaultdict

class BCMFile(OrderedDict):
    def __init__(self,filename):
        super(BCMFile, self).__init__()
        global MODE
        f = open(filename,"rb")
        #print( "----------------------------------------- ",filename)
        TAG = f.read(4)
        if(TAG != b"#BCM"):
            raise Exception(b"Don't think this is a BCM File..."+TAG)
        EndianFlag = struct.unpack("H",f.read(2))[0]
        if(EndianFlag == 0xFFFE):
            MODE = "<"
        else:
            MODE = ">"
        struct.unpack(MODE+"HHHHH",f.read(10))

        HEADER = struct.unpack(MODE+"4H8I",f.read(40))
        #hexprint((HEADER))

        ChargeNames = readNameOffsetTable(f,HEADER[5],HEADER[0],MODE)
        InputNames = readNameOffsetTable(f,HEADER[7],HEADER[1],MODE)
        MoveNames = readNameOffsetTable(f,HEADER[9],HEADER[2],MODE)
        CancelListNames = readNameOffsetTable(f,HEADER[11],HEADER[3],MODE)

        #print( ChargeNames)
        #print( InputNames)
        #print( MoveNames)
        #print( CancelListNames)
        '''Read Charges'''
        f.seek(HEADER[4])
        self["Charges"] = {}
        for i in range(0,HEADER[0]):
            charge = {}
            #charge["Name"] = ChargeNames[i]
            charge["Input"] = struct.unpack(MODE+"H",f.read(2))[0]
            charge["Unknown1"] = struct.unpack(MODE+"H",f.read(2))[0]
            charge["MoveFlags"] = struct.unpack(MODE+"H",f.read(2))[0]
            charge["Frames"] = struct.unpack(MODE+"H",f.read(2))[0]
            charge["Frames2"] = struct.unpack(MODE+"H",f.read(2))[0]
            charge["Unknown3"] = struct.unpack(MODE+"H",f.read(2))[0]
            charge["StorageIndex"] = struct.unpack(MODE+"I",f.read(4))[0]
            self["Charges"][ChargeNames[i]] = charge
        '''Read Inputs'''

        self["Inputs"] = {}
        for i in range(0,HEADER[1]):
            f.seek(HEADER[6]+i*0xC4)
            input = {}
            input["Entries"] = []
            #input["Name"] = InputNames[i]
            count =  struct.unpack(MODE+"I",f.read(4))[0]
            for j in range(0,count):
                entry = {}
                entry["Type"] = struct.unpack(MODE+"H",f.read(2))[0]
                entry["Buffer"] = struct.unpack(MODE+"H",f.read(2))[0]
                entry["Input"] = struct.unpack(MODE+"H",f.read(2))[0]

                entry["MoveFlags"] = struct.unpack(MODE+"H",f.read(2))[0]
                entry["Flags"] = struct.unpack(MODE+"H",f.read(2))[0]
                entry["Requirement"] = struct.unpack(MODE+"H",f.read(2))[0]

                input["Entries"].append(entry)
            self["Inputs"][InputNames[i]] = input
        '''Read MOVES'''

        self["Moves"] = {}
        for i in range(0,HEADER[2]):
            f.seek(HEADER[8]+i*0x54)
            moves= OrderedDict()
            #charge["Name"] = ChargeNames[i]
            moves["Input"] = struct.unpack(MODE+"H",f.read(2))[0]
            moves["MoveFlags"] = struct.unpack(MODE+"H",f.read(2))[0]
            moves["PositionRestriction"] = struct.unpack(MODE+"H",f.read(2))[0]
            moves["Restriction"] = struct.unpack(MODE+"H",f.read(2))[0]
            moves["Unknown1"] = struct.unpack(MODE+"H",f.read(2))[0]
            moves["StateRestriction"] = struct.unpack(MODE+"H",f.read(2))[0]
            moves["Unknown2"] = struct.unpack(MODE+"H",f.read(2))[0]
            moves["MiscRestriction"] = struct.unpack(MODE+"B",f.read(1))
            moves["Unknown3"] = struct.unpack(MODE+"B",f.read(1))[0]
            moves["UltraRestriction"] = struct.unpack(MODE+"B",f.read(1))[0]
            moves["UltraRestriction?"] = struct.unpack(MODE+"3B",f.read(3))[0]
            moves["PositionRestrictionDistance"] = struct.unpack(MODE+"f",f.read(4))[0]
            moves["EXRequirement"] = struct.unpack(MODE+"H",f.read(2))[0]
            moves["EXCost"] = struct.unpack(MODE+"H",f.read(2))[0]
            moves["UltraRequirement"] = struct.unpack(MODE+"H",f.read(2))[0]
            moves["UltraCost"] = struct.unpack(MODE+"H",f.read(2))[0]
            moves["InputMotion"] = struct.unpack(MODE+"i",f.read(4))[0]
            moves["AIMoveFeatures"] = struct.unpack(MODE+"I",f.read(4))[0]
            moves["AIMinRange"] = struct.unpack(MODE+"f",f.read(4))[0]
            moves["AIMarange"] = struct.unpack(MODE+"f",f.read(4))[0]
            moves["AIUnknown1"] = struct.unpack(MODE+"I",f.read(4))[0]
            moves["CPUPassiveMove"] = struct.unpack(MODE+"I",f.read(4))[0]
            moves["CPUCounterMove"] = struct.unpack(MODE+"H",f.read(2))[0]
            moves["CPUVsStand"] = struct.unpack(MODE+"H",f.read(2))[0]
            moves["CPUVsAir"] = struct.unpack(MODE+"H",f.read(2))[0]
            moves["CPUVsDown"] = struct.unpack(MODE+"H",f.read(2))[0]
            moves["CPUVsStunned"] = struct.unpack(MODE+"H",f.read(2))[0]
            moves["CPUProbeMove"] = struct.unpack(MODE+"H",f.read(2))[0]
            moves["CPUVsVeryClose"] = struct.unpack(MODE+"H",f.read(2))[0]
            moves["CPUVsClose"] = struct.unpack(MODE+"H",f.read(2))[0]
            moves["CPUVsMidRange"] = struct.unpack(MODE+"H",f.read(2))[0]
            moves["CPUVsFar"] = struct.unpack(MODE+"H",f.read(2))[0]
            moves["CPUVsVeryFar"] = struct.unpack(MODE+"H",f.read(2))[0]

            self["Moves"][MoveNames[i]] = moves
        '''Read Cancels'''

        self["CancelLists"] = {}
        for i in range(0,HEADER[3]):
            f.seek(HEADER[10]+i*0x8)
            cancellist = []
            count = struct.unpack(MODE+"HH",f.read(4))[0]
            offset =  struct.unpack(MODE+"I",f.read(4))[0]
            f.seek(offset-8,1)
            for j in range(0,count):
                index = struct.unpack(MODE+"H",f.read(2))[0]
                #print( index)
                if index > -1 and index < len(MoveNames):
                    cancellist.append(MoveNames[index])
                else:
                    cancellist.append(index)
            self["CancelLists"][CancelListNames[i]] = cancellist

def doAll():
    for char in os.listdir(PC_PATH):
        print( char)
        #print( "PC")
        versions = defaultdict(list)
        versions_data = {}
        for file in findFiles(char,'C:\\Program Files (x86)\\Steam\\steamapps\\common\\Super Street Fighter IV - Arcade Edition\\',".bcm"):
            test = BCMFile(file)
            test_text = json.dumps(test.Charges, indent=5).splitlines()+json.dumps(test.Inputs, indent=5).splitlines()+json.dumps(test.Moves, indent=5).splitlines()+json.dumps(test.CancelLists, indent=5).splitlines()
            m = hashlib.md5()
            m.update(repr(test_text))
            versions[m.hexdigest()].append(file)
            f = open("../out/"+char+"_"+m.hexdigest()+".txt","w")
            for line in test_text:
                f.write(line)
                f.write("\n")
            f.close()
        #print( "XBOX")
        for file in findFiles(char,'Z:\\SF4 Engine STuff\\XBOX AE\\',".bcm"):
            test = BCMFile(file)
            test_text = json.dumps(test.Charges, indent=5).splitlines()+json.dumps(test.Inputs, indent=5).splitlines()+json.dumps(test.Moves, indent=5).splitlines()+json.dumps(test.CancelLists, indent=5).splitlines()
            m = hashlib.md5()
            m.update(repr(test_text))
            versions[m.hexdigest()].append(file)
            f = open("../out/"+char+"_"+m.hexdigest()+".txt","w")
            for line in test_text:
                f.write(line)
                f.write("\n")
            f.close()
        print( json.dumps(versions, indent=5))

def doChar(c):
    pc = BCMFile(PC_PATH+c+"\\"+c+".bcm")
    xbox = BCMFile(XBOX_PATH+c+"\\"+c+".bcm")
    #print( json.dumps(pc.CancelLists, indent=5))
    print( "DIFF")
    htmlDiff = difflib.HtmlDiff()
    f = open("diff.html","w")
    pctxt = json.dumps(pc.Charges, indent=5).splitlines()+json.dumps(pc.Inputs, indent=5).splitlines()+json.dumps(pc.Moves, indent=5).splitlines()+json.dumps(pc.CancelLists, indent=5).splitlines()
    xboxtxt = json.dumps(xbox.Charges, indent=5).splitlines()+json.dumps(xbox.Inputs, indent=5).splitlines()+json.dumps(xbox.Moves, indent=5).splitlines()+json.dumps(xbox.CancelLists, indent=5).splitlines()
    f.write(htmlDiff.make_file(pctxt,xboxtxt))
    f.close()