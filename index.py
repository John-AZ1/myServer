from myServer import MyServer
from myRoster import index as maccas
from mySimon.Simon import Simon
server = MyServer()

simon = Simon("", "", "intranet.stpats.vic.edu.au", False, False) 

#*** myRoster ***#

@server.route("/myRoster/?")
def myRosterIndex(data, urldict):
    try:
        indexFile = open('./myRoster/index.html', 'r')
        content = indexFile.read()
        indexFile.close()
    except IOError:
        content = "<h1 style='font-family:helvetica'>404: File Not Found!</h1>"
    return(server.httpRespone(content, ["Content-Type: text/html; charset=utf-8"]))
        
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

        return(server.httpRespone(info)) 
    else:
        return(server.httpRespone("No such function exists!"))

#*** mySimon ***#

@server.route("/mySimon/?")
def mySimonIndex(data, urldict):
    try:
        indexFile = open('./mySimon/index.html', 'r')
        content = indexFile.read()
        indexFile.close()
    except IOError:
        content = "<h1 style='font-family:helvetica'>404: File Not Found!</h1>"
    return(server.httpRespone(content, ["Content-Type: text/html; charset=utf-8"]))

def test(msg, value):
    print(msg, ':', value)
    varTest = value
    return(varTest)

varTest = test("Init", 0)

@server.route("/mySimon/api/login")
def mySimonLogin(data, urldict):
    global varTest
    print("varTest:", varTest)
    varTest = test("Login", 1)
    print("varTest:", varTest)

    info = ""
    try:
        print("(\033[38;5;226mSimon\033[0m) {}".format(data))
        username = eval(data)['Username']
        password = eval(data)['Password']

        simon.login(username, password)
        simon.var = "LOGGED IN"
        print("\033[38;5;28mValue:\033[0m", simon.var)
        info = simon.var
    except Exception as e:
        print("Data:", data)
        simon.var = "LOGIN FAILED"
        info = 'Error Occured: Believed cause incorrect data passed: {}'.format(data)
        print("Exception:", e)

    return(server.httpRespone(info)) 

@server.route("/mySimon/api/getTimeTableHTML")
def mySimonTTHTML(data, urldict):
    global varTest
    print("varTest:", varTest)
    print("Is Logged In:", simon.loggedIn)
    print("\033[38;5;28mValue:\033[0m", simon.var)
    if not simon.loggedIn:
        content = "Please fam, log in yall!"
    else:
        print("Getting Timetable")
        content = simon.getTT('2019-01-31', 'STURT')
    return(server.httpRespone(content))


#*** Defaults ***#

@server.route("/")
def index(data, urldict):
    try:
        indexFile = open('./index/index.html', 'r')
        content = indexFile.read()
        indexFile.close()
    except IOError:
        content = "<h1 style='font-family:helvetica'>404: File Not Found!</h1>"
    return(server.httpRespone(content, ["Content-Type: text/html; charset=utf-8"]))

@server.route(r"/(?P<path>.*)")
def defaultFile(data, urldict):
    headers = []
    try:
        indexFile = open('./' + urldict['path'], 'r')
        content = indexFile.read()
        indexFile.close()
        fileType = urldict["path"].split(".")[-1]
        if fileType == "js":
            mimeType = "application/javascript"
        elif fileType == "css":
            mimeType = "text/css"
        headers = ["Content-Type: "+mimeType+"; charset=utf-8"]
    except IOError:
        content = "<h1 style='font-family:helvetica'>404: File Not Found!</h1>"
    return(server.httpRespone(content, headers))
        
server.run()
