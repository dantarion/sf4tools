import bac,bcm
import json
import sys
import util
import difflib
from collections import OrderedDict
HEADER = '''
    <!DOCTYPE html>
<html lang="en">
  <head>
    <meta charset="utf-8">
    <meta http-equiv="X-UA-Compatible" content="IE=edge">
    <meta name="viewport" content="width=device-width, initial-scale=1">
    <title>Dantarion's SFUltraDiff BETA</title>

    <!-- Bootstrap -->
    <link href="css/bootstrap.min.css" rel="stylesheet">

    <!-- HTML5 Shim and Respond.js IE8 support of HTML5 elements and media queries -->
    <!-- WARNING: Respond.js doesn't work if you view the page via file:// -->
    <!--[if lt IE 9]>
      <script src="https://oss.maxcdn.com/libs/html5shiv/3.7.0/html5shiv.js"></script>
      <script src="https://oss.maxcdn.com/libs/respond.js/1.4.2/respond.min.js"></script>
    <![endif]-->
        <style type="text/css">
        table.diff {{font-family:Consolas; border:medium;}}
        .diff_header {{background-color:#e0e0e0}}
        td.diff_header {{text-align:right}}
        .diff_next {{background-color:#c0c0c0}}
        .diff_add {{background-color:#aaffaa}}
        .diff_chg {{background-color:#ffff77}}
        .diff_sub {{background-color:#ffaaaa}}
        .panel {{margin:10px}}
        .panel .panel {{margin:5px}}
        .anchor {{display: block; position: relative; top: -100px; visibility: hidden;}}
    </style>
  </head>
  <body>
  <nav class="navbar navbar-default navbar-fixed-top" role="navigation">
  <div class="container-fluid">
    <!-- Brand and toggle get grouped for better mobile display -->
    <div class="navbar-header">
      <button type="button" class="navbar-toggle" data-toggle="collapse" data-target="#bs-example-navbar-collapse-1">
        <span class="sr-only">Toggle navigation</span>
        <span class="icon-bar"></span>
        <span class="icon-bar"></span>
        <span class="icon-bar"></span>
      </button>
      <a class="navbar-brand" href="#">Dantarion's SFUltraDiff BETA - {0}_{1}</a>
    </div>

    <!-- Collect the nav links, forms, and other content for toggling -->
    <div class="collapse navbar-collapse" id="bs-example-navbar-collapse-1">
        <ul class="nav navbar-nav">
            <li class="dropdown">
              <a href="#" class="dropdown-toggle" data-toggle="dropdown">{1}<b class="caret"></b></a>
              <ul class="dropdown-menu">
                <li><a href="{0}_VANILLA_TO_SUPER.html">VANILLA_TO_SUPER</a></li>
                <li><a href="{0}_SUPER_TO_AE.html">SUPER_TO_AE</a></li>
                <li><a href="{0}_AE_TO_AE2012.html">AE_TO_AE2012</a></li>
                <li><a href="{0}_AE2012_TO_ULTRA.html">AE2012_TO_ULTRA</a></li>
                <li><a href="{0}_ULTRA_TO_ULTRA104.html"></a></li>
              </ul>
            </li>
            <li class="divider"></li>
            <li><a href="#Charges">Charges</a></li>
            <li><a href="#Inputs">Inputs</a></li>
            <li><a href="#Moves">Moves</a></li>
            <li><a href="#Charges">CancelLists</a></li>
            <li class="divider"></li>
            <li><a href="#Floats">Floats</a></li>
            <li><a href="#Scripts">Scripts</a></li>
            <li><a href="#VFXScripts">VFXScripts</a></li>
            <li><a href="#HitboxTable">HitboxTable</a></li>

      </ul>
      <ul class="nav navbar-nav navbar-right">
        <li><a href="http://twitter.com/dantarion">Contact @dantarion!</a></li>
      </ul>
    </div><!-- /.navbar-collapse -->
  </div><!-- /.container-fluid -->
</nav>
<div class= "container-fluid" style="padding-top:60px">
    <div class='col-md-2'>
            <div class="list-group">
<a href="ADN_VANILLA_TO_SUPER.html" class="list-group-item">ADN</a>
<a href="AGL_VANILLA_TO_SUPER.html" class="list-group-item">AGL</a>
<a href="BLK_VANILLA_TO_SUPER.html" class="list-group-item">BLK</a>
<a href="BLR_VANILLA_TO_SUPER.html" class="list-group-item">BLR</a>
<a href="BOS_VANILLA_TO_SUPER.html" class="list-group-item">BOS</a>
<a href="BSN_VANILLA_TO_SUPER.html" class="list-group-item">BSN</a>
<a href="CDY_VANILLA_TO_SUPER.html" class="list-group-item">CDY</a>
<a href="CHB_VANILLA_TO_SUPER.html" class="list-group-item">CHB</a>
<a href="CMY_VANILLA_TO_SUPER.html" class="list-group-item">CMY</a>
<a href="CNL_VANILLA_TO_SUPER.html" class="list-group-item">CNL</a>
<a href="DAN_VANILLA_TO_SUPER.html" class="list-group-item">DAN</a>
<a href="DDL_VANILLA_TO_SUPER.html" class="list-group-item">DDL</a>
<a href="DJY_VANILLA_TO_SUPER.html" class="list-group-item">DJY</a>
<a href="DSM_VANILLA_TO_SUPER.html" class="list-group-item">DSM</a>
<a href="FLN_VANILLA_TO_SUPER.html" class="list-group-item">FLN</a>
<a href="GEN_VANILLA_TO_SUPER.html" class="list-group-item">GEN</a>
<a href="GKI_VANILLA_TO_SUPER.html" class="list-group-item">GKI</a>
<a href="GKN_VANILLA_TO_SUPER.html" class="list-group-item">GKN</a>
<a href="GUL_VANILLA_TO_SUPER.html" class="list-group-item">GUL</a>
<a href="GUY_VANILLA_TO_SUPER.html" class="list-group-item">GUY</a>
<a href="HKN_VANILLA_TO_SUPER.html" class="list-group-item">HKN</a>
<a href="HND_VANILLA_TO_SUPER.html" class="list-group-item">HND</a>
<a href="HWK_VANILLA_TO_SUPER.html" class="list-group-item">HWK</a>
<a href="IBK_VANILLA_TO_SUPER.html" class="list-group-item">IBK</a>
<a href="JHA_VANILLA_TO_SUPER.html" class="list-group-item">JHA</a>
<a href="JRI_VANILLA_TO_SUPER.html" class="list-group-item">JRI</a>
<a href="KEN_VANILLA_TO_SUPER.html" class="list-group-item">KEN</a>
<a href="MKT_VANILLA_TO_SUPER.html" class="list-group-item">MKT</a>
<a href="RIC_VANILLA_TO_SUPER.html" class="list-group-item">RIC</a>
<a href="ROS_VANILLA_TO_SUPER.html" class="list-group-item">ROS</a>
<a href="RYU_VANILLA_TO_SUPER.html" class="list-group-item">RYU</a>
<a href="SGT_VANILLA_TO_SUPER.html" class="list-group-item">SGT</a>
<a href="SKR_VANILLA_TO_SUPER.html" class="list-group-item">SKR</a>
<a href="VEG_VANILLA_TO_SUPER.html" class="list-group-item">VEG</a>
<a href="ZGF_VANILLA_TO_SUPER.html" class="list-group-item">ZGF</a>
            </div>
    </div>
    <div class='col-md-10'>
  '''
FOOTER = '''</div></div><!-- jQuery (necessary for Bootstrap's JavaScript plugins) -->
    <script src="https://ajax.googleapis.com/ajax/libs/jquery/1.11.0/jquery.min.js"></script>
    <!-- Include all compiled plugins (below), or include individual files as needed -->
    <script src="js/bootstrap.min.js"></script>
  </body>
</html>'''
def diffCollectionsHeader(col1,col2,log,level=0):
    removedSet = set(col1.keys()).difference(set(col2.keys()))
    addedSet = set(col2.keys()).difference(set(col1.keys()))
    bothSet = set(col2.keys()).intersection(set(col1.keys()))
    if level == 0:
        log.write('<ul class="nav nav-pills">')
        for removed in removedSet:
            fancyName = removed
            try:
                fancyName = col1[removed]["Name"]
            except Exception:
                pass
            log.write("<li class='bg-danger'><a href='#change-{0}{1}'><span class='glyphicon glyphicon-minus'></span>Removed {1}</a></li>".format(removed,fancyName))
        for added in addedSet:
            fancyName = added
            try:
                fancyName = col2[added]["Name"]
            except Exception:
                pass
            log.write("<li class='bg-success'><a href='#change-{0}{1}'><span class='glyphicon glyphicon-plus'></span>Added {1}</a></li>".format(added,fancyName))
        for both in bothSet:
            if repr(col1[both]) == repr(col2[both]):
                continue
            fancyName = both
            try:
                fancyName = col2[both]["Name"]
            except Exception:
                pass
            log.write("<li class='bg-warning'><a href='#change-{0}{1}'><span class='glyphicon glyphicon-pencil'></span>Changed {1}</a></li>".format(both,fancyName))
        log.write("</ul>")
def diffCollections(col1,col2,log,level=0):
    removedSet = set(col1.keys()).difference(set(col2.keys()))
    addedSet = set(col2.keys()).difference(set(col1.keys()))
    bothSet = set(col2.keys()).intersection(set(col1.keys()))
    for removed in removedSet:
        fancyName = removed
        try:
            fancyName = col1[removed]["Name"]
        except Exception:
            pass
        log.write("<div class='panel panel-danger'>");
        log.write("<span class='anchor'  id='change-{0}{1}'></span><div class='panel-heading'>Removed {1}</div>".format(removed,fancyName))
        log.write("<div class='panel-body'><pre>")
        log.write(json.dumps(col1[removed],indent=5))
        log.write("</pre></div></div>")
    for added in addedSet:
        fancyName = added
        try:
            fancyName = col2[added]["Name"]
        except Exception:
            pass
        log.write("<div class='panel panel-success'>");
        
        log.write("<span class='anchor'  id='change-{0}{1}'></span><div class='panel-heading'>Added {1}</div>".format(added,fancyName))
        log.write("<div class='panel-body'><pre>")
        log.write(json.dumps(col2[added],indent=5))
        log.write("</pre></div></div>")

    for both in set(col2.keys()).intersection(set(col1.keys())):
        if repr(col1[both]) == repr(col2[both]):
            continue
        fancyName = both
        
        try:
            fancyName = col2[both]["Name"]
        except Exception:
            pass

        log.write("<div class='panel panel-warning'>");
        log.write("<span class='anchor'  id='change-{0}{1}'></span><div class='panel-heading'>Changed {1}</div><div class='panel-body'>".format(both,fancyName))
        if type(col1[both]) is dict or type(col1[both]) is OrderedDict:
            diffCollections(col1[both],col2[both],log,level+1)
        else:
            if type(col1[both]) is list:
                differ = difflib.HtmlDiff()
                log.write(differ.make_table(json.dumps(col1[both],indent=5).splitlines(),json.dumps(col2[both],indent=5).splitlines()))
            else:
                log.write("<div class='container-fluid'>")

                log.write("<div class='col-md-5'>Old<br />")
                log.write("<pre>")
                log.write( json.dumps(col1[both],indent=5))
                log.write("</pre></div>")
                log.write("<div class='col-md-5'>New<br />")
                log.write("<pre>")
                log.write( json.dumps(col2[both],indent=5))
                log.write("</pre></div>")
                log.write("</div>")
        log.write("</div></div>")
def dumpChar(char):
    postfix = char+"\\"+char
    SUPER = "C:\\Program Files (x86)\\Steam\\steamapps\\common\\Super Street Fighter IV - Arcade Edition\\resource\\battle\\chara\\"
    AE = "C:\\Program Files (x86)\\Steam\\steamapps\\common\\Super Street Fighter IV - Arcade Edition\\dlc\\03_character_free\\battle\\regulation\\latest\\"
    AE2012 = "C:\\Program Files (x86)\\Steam\\steamapps\\common\\Super Street Fighter IV - Arcade Edition\\patch\\battle\\regulation\\latest_ae\\"
    version_names = ["SUPER","AE","AE2012"]
    versions = [SUPER,AE,AE2012]
    
    for i,ver in enumerate(versions):

        log = open("../json/"+char+"."+version_names[i]+".bac.json","w")
        BAC= bac.BACFile(versions[i]+postfix+".bac")
        log.write(BAC.toJSON())
        log.close()
        log = open("../json/"+char+"."+version_names[i]+".bcm.json","w")
        BCM= bcm.BCMFile(versions[i]+postfix+".bcm")
        log.write(BCM.toJSON())
        log.close()
        
    
def compareChar(char):
    postfix = char+"\\"+char

    VANILLA = "M:\\Xbox\\Ultra Xbox\\content\\04_ae2\\battle\\regulation\\sf4\\"
    SUPER = "C:\\Program Files (x86)\\Steam\\steamapps\\common\\Super Street Fighter IV - Arcade Edition\\resource\\battle\\chara\\"
    AE = "C:\\Program Files (x86)\\Steam\\steamapps\\common\\Super Street Fighter IV - Arcade Edition\\dlc\\03_character_free\\battle\\regulation\\latest\\"
    AE2012 = "C:\\Program Files (x86)\\Steam\\steamapps\\common\\Super Street Fighter IV - Arcade Edition\\patch\\battle\\regulation\\latest_ae\\"
    ULTRA = "M:\\Xbox\\Ultra Xbox\\content\\04_ae2\\battle\\regulation\\ae2\\"
    ULTRA_TU1 = "C:\\Program Files (x86)\\Steam\\SteamApps\\common\\Super Street Fighter IV - Arcade Edition\\patch_ae2_tu1\\battle\\regulation\\ae2_109\\"
    ULTRA_TU2 = "C:\\Program Files (x86)\\Steam\\SteamApps\\common\\Super Street Fighter IV - Arcade Edition\\patch_ae2_tu1b\\battle\\regulation\\ae2_109b\\"
    ULTRA_TU3 = "C:\\Program Files (x86)\\Steam\\SteamApps\\common\\Super Street Fighter IV - Arcade Edition\\patch_ae2_tu2\\battle\\regulation\\ae2_110\\"
    #versions = [VANILLA,SUPER,AE,AE2012,ULTRA,ULTRA_TU1,ULTRA_TU2,ULTRA_TU3]
    bacs = {}
    bcms = {}
    #if char not in ["SGT","CHB"]:
    #    return
    #VANILLA,SUPER,AE,AE2012,
    #"VANILLA","SUPER","AE","AE2012"
    versions = [ULTRA_TU1,ULTRA_TU3]
    names = ["ULTRA_TU1","ULTRA_TU3"]
    
    if os.path.isfile(ULTRA_TU2+postfix+".bac"):
        return
    
    for i,version in enumerate(versions):

        if not os.path.isfile(version+postfix+".bac"):
            continue
        if os.path.isfile( "../json/"+char+"_"+names[i]+".bac.json"):
            pass
        print("\t"+names[i])
        tmp = bac.BACFile(version+postfix+".bac")
        log = open("../json/"+char+"_"+names[i]+".bac.json","w")
        log.write(tmp.toJSON())
        bacs[i] = tmp
        log.close()
        
        tmp = bcm.BCMFile(version+postfix+".bcm")
        log = open("../json/"+char+"_"+names[i]+".bcm.json","w")
        log.write(tmp.toJSON())
        #tmp.toFile("../out/"+char+"_"+names[i]+".bcm")
        bcms[i] = tmp
        log.close()
        
    
    for i in range(0,len(versions)-1):
        
        name = names[i]+"_TO_"+names[i+1]
        
        if not os.path.isfile(versions[i]+postfix+".bac"):
            continue
        if os.path.isfile( "../html/"+char+"_"+name+".html"):
            pass
        print("\tDoing ",name)
        log = open("../html/"+char+"_"+name+".html","w")
        log.write(HEADER.format(char,name))
        if len(bacs) < 2 or len(bcms) < 2:
            return;
        firstBAC= bacs[i]
        secondBAC = bacs[i+1]
        firstBCM= bcms[i]
        secondBCM = bcms[i+1]
        for k in firstBCM.keys():
            log.write("<a class='anchor' id='"+k+"'></a><h2>"+k+"</h2>")
            if type(firstBCM[k]) is list:
                pass
            else:
                diffCollectionsHeader(firstBCM[k],secondBCM[k],log)
        for k in firstBAC.keys():
            log.write("<a class='anchor' id='"+k+"'></a><h2>"+k+"</h2>")
            if type(firstBAC[k]) is list:
                pass
            else:
                diffCollectionsHeader(firstBAC[k],secondBAC[k],log)
        for k in firstBCM.keys():
            log.write("<a></a><h2>"+k+"</h2>")
            if type(firstBCM[k]) is list:
                if repr(firstBCM[k]) != repr(secondBCM[k]):
                    log.write("<div class='container-fluid'>")
                    log.write("<div class='col-md-5'>Old<br />")
                    log.write("<pre>")
                    log.write( json.dumps(firstBCM[k],indent=5))
                    log.write("</pre></div>")
                    log.write("<div class='col-md-5'>New<br />")
                    log.write("<pre>")
                    log.write( json.dumps(secondBCM[k],indent=5))
                    log.write("</pre></div>")
                    log.write("</div>")
            else:
                diffCollections(firstBCM[k],secondBCM[k],log)

        for k in firstBAC.keys():
            log.write("<a></a><h2>"+k+"</h2>")
            if type(firstBAC[k]) is list:
                if repr(firstBAC[k]) != repr(secondBAC[k]):
                    log.write("<div class='container-fluid'>")
                    log.write("<div class='col-md-6'>Old<br />")
                    log.write("<pre>")
                    log.write( json.dumps(firstBAC[k],indent=5))
                    log.write("</pre></div>")
                    log.write("<div class='col-md-6'>New<br />")
                    log.write("<pre>")
                    log.write( json.dumps(secondBAC[k],indent=5))
                    log.write("</pre></div>")
                    log.write("</div>")
            else:
                diffCollections(firstBAC[k],secondBAC[k],log)
        log.write(FOOTER)
        log.close()


import os
#compareChar("RLN")
#compareChar("SGT")
for char in os.listdir("M:\\Xbox\\Ultra Xbox\\content\\04_ae2\\battle\\regulation\\ae2\\"):
   print(char)
   compareChar(char)

