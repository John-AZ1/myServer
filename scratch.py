from dec import magic
from myServer import MyServer

server = MyServer()
x = 0

@server.route("/")
def init(data, urldict):
    global x
    x = 1
    return(server.httpRespone("Init: {}".format(x)))

@server.route("/view")
def view(data, urldict):
    global x
    return(server.httpRespone("View: {}".format(x)))

server.run()
# magicObj = magic()
# x = 0
# 
# @magicObj.dec("Init")
# def funct0():
    # global x
    # x = 1
# 
# @magicObj.dec("View")
# def funct1():
    # global x
    # print(x)
# 
# magicObj.run()
