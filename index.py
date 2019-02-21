from myServer import MyServer
from myRoster import index as maccas
from mySimon.Simon import Simon
server = MyServer()

simon = Simon("", "", "intranet.stpats.vic.edu.au", False) 

#*** myRoster ***#

@server.route("/myRoster/?")
def myRosterIndex(data, urldict):
    try:
        indexFile = open('./myRoster/index.html', 'r')
        content = indexFile.read()
        indexFile.close()
    except IOError:
        content = "<h1 style='font-family:helvetica'>404: File Not Found!</h1>"
    return(content)
        
@server.route("/myRoster/api/(?P<function>[^/]*)")
def myRosterApi(data, urldict):
    if urldict['function'] == 'getRosterHTML':
        info = ""
        try:
            username = eval(data)['Username']
            password = eval(data)['Password']

            maccas.getCookies(username, password)
            for shift in maccas.getRoster():
                info += shift.html()
        except Exception as e:
            info = 'Error Occured: Believed cause incorrect data passed'
            print("Exception:", e)

        return(info)        
    else:
        return("No such function exists!")

#*** mySimon ***#

@server.route("/mySimon/?")
def mySimonIndex(data, urldict):
    try:
        indexFile = open('./mySimon/index.html', 'r')
        content = indexFile.read()
        indexFile.close()
    except IOError:
        content = "<h1 style='font-family:helvetica'>404: File Not Found!</h1>"
    return(content)
        
@server.route("/mySimon/api/(?P<function>[^/]*)")
def myRosterApi(data, urldict):
    if urldict['function'] == 'login':
        info = ""
        try:
            username = eval(data)['Username']
            password = eval(data)['Password']

            simon.login(username, password)
        except Exception as e:
            info = 'Error Occured: Believed cause incorrect data passed'
            print("Exception:", e)

        return(info) 
    elif urldict['function'] == 'getTimeTableHTML':
        if not simon.loggedIn:
            return("Please fam, log in yall!")
        return(simon.getTT('2019-01-31', 'STURT'))

    else:
        return("No such function exists!")

#*** Defaults ***#

@server.route("/(?P<path>.*)")
def defaultFile(data, urldict):
    try:
        indexFile = open('./' + urldict['path'], 'r')
        content = indexFile.read()
        indexFile.close()
    except IOError:
        content = "<h1 style='font-family:helvetica'>404: File Not Found!</h1>"
    return(content)
        
server.run()
