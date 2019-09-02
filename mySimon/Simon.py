import requests
import os
import sys
import datetime
import getpass
import re
import time

def coloredOK(name, call, verbose=False):
    responseBool = "\033[38;5;010m{}\033[0m".format(call.status_code) if call.ok else "\033[38;5;196m{}\033[0m".format(call.status_code)
    if verbose:
        print("\033[38;5;036m{} OK:\033[0m {}".format(name, responseBool))

def printCookies(cookieList, verbose=False):
    string = ''.join(["\033[38;5;005m{}: \033[0m{}\n".format(x[0], x[1]) for x in cookieList])
    if verbose:
        print(string.rstrip('\n'))

class Simon:
    def __init__(self, username, password, url, login=True, verbose=False):
        self.url = url
        self.verbose = verbose
        self.var = "No Value!"

        self.default_headers = {
            'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64; rv:62.0) Gecko/20100101 Firefox/62.0',
            'Accept': 'text/html,application/xhtml+xml,application/xml,application/json,text/javascript;q=0.9,*/*;q=0.8',
            'Accept-Language': 'en-US,en;q=0.5',
            'Connection': 'keep-alive',
            'Upgrade-Insecure-Requests': '1',
        }

        self.session = requests.Session()

        self.today = datetime.datetime.today().strftime('%Y-%m-%d')

        self.headers = {
            'default': {
                **self.default_headers,
            },
            'adAuth': {
                **self.default_headers,
                'Referer': 'https://intranet.stpats.vic.edu.au/Login/Default.aspx?ReturnUrl=%2F',
                'Content-Type': 'application/x-www-form-urlencoded',
            },
            'timetable': {
                **self.default_headers,
                'Referer': 'https://'+self.url+'/',
                'Content-Type': 'application/json; charset=utf-8',
                'X-Requested-With': 'XMLHttpRequest',
            },
            'average': {
                'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64; rv:66.0) Gecko/20100101 Firefox/66.0',
                'Accept': 'application/json, text/javascript, */*; q=0.01',
                'Accept-Language': 'en-US,en;q=0.5',
                'Referer': 'https://intranet.stpats.vic.edu.au/WebModules/Profiles/Student/LearningResources/LearningAreaTasks.aspx',
                'Content-Type': 'application/json; charset=utf-8',
                'X-Requested-With': 'XMLHttpRequest',
                'Connection': 'keep-alive',
            },
        }

        self.params = {
            'asp': {
                'ReturnUrl': '/'
            },
            'adAuth': {
                'ReturnUrl': '/',
            }
        }
        
        if login:
            self.login(username, password)
            self.loggedIn = True
        else:
            self.loggedIn = False

    def chgVal(self, val):
        self.var = val
    def login(self, username, password):
        # logon set's cadata
        logon_data = {
            'curl': 'Z2F',
            'flags': '0',
            'forcedownlevel': '0',
            'formdir': '3',
            'trusted': '1',
            'username': username,
            'password': password,
            'SubmitCreds': 'Log On'
        }

        logon = self.session.post(
            'https://'+self.url+'/CookieAuth.dll?Logon',
            headers=self.headers['default'],
            data=logon_data
        )

        coloredOK("Logon", logon, self.verbose)

        # asp sets ASP.NET_SessionId
        asp_response = self.session.get(
            'https://intranet.stpats.vic.edu.au/Login/Default.aspx', 
            headers=self.headers['default'],
            params=self.params['asp'], 
        )

        coloredOK("ASP", asp_response, self.verbose)

        # adAuth sets adAuthCookie
        adAuth_response = self.session.post(
            'https://intranet.stpats.vic.edu.au/Login/Default.aspx', 
            headers=self.headers['adAuth'], 
            params=self.params['adAuth'], 
            data = {
                '__VIEWSTATE': '7k+wOXPRAJJ0GYcAtc5mqa80uLW4yu9jO1fhOJ+zp6kFfsjMPdjL7lsu9dQsrpuGoKr/0gSodHm4G8hDhcQ8MNuSH+3/RKFfFOCm691mtwVrmo8XIEm95oRua+4GwLs4NQizBtIOlRCPqoEcSz+pn0oPhvh3J3m9YJ5QRhYF1jnlolk9b5LvcfmGwR4scyiA8tilsmQWr0f3ZWB2o2rDqdk5C8C7KfzDETqdvQgfLAHQjnLo9mLxAbrMc4ae/lwuYYBVVJdZnU5XxuzjiqQbB+yuoZC2GaTdPVx/BuIMZkUd802DjD32TxbtKSHLewoIy+iSTHAuHYhO7pMJ57nEa50p6U+43tvaMjYhHVT0/H8FSstPW/LfcRE9eWP/rosKzfVEWtxkFcp9Ieul7URZjJFEVMO0YM6tI1MtZW/4oGVmFcnRW+9R0JtuFlxeHVAQ1tBh15UtLPeeESIq8XEiR5jB7B2VHC1cdtdY2TWlP79LTDB3ZRHwc1LNc183oqzHtxr8HRMMQ7QhMB1AE44jR6oTyL3Tjcl9JyxU1cmbwjBv/vNJpavR7vtzu2Zh7XxMI7kgactFKb+IceTLv0Bdxg==',
                '__VIEWSTATEGENERATOR': '25748CED',
                '__EVENTVALIDATION': 'N3ShdR54kE0tEdOQKZw3NpsxWi2YjGlN6AkAwlzR9zA4POU63IJWpJ2BprpAdaP+orDu4CidiRahNM977ReJguQez1CXAh6OamNuEknG8PfJIkDJY9/C4cZ7YAvs5aNgcvaDAdYv2hb55DoZAxe9q658dk+Yf1YUaU08wXq/ZbvsfvYWi6HRcRmqzQoH4lWI9/YKUVYgUOCDFx5RP3TG3g==',
                'Version': '3.13.2.5',
                'inputUsername': username, 
                'inputPassword': password,
                'buttonLogin': 'Sign+in'
            }
        )

        # self.session.cookies.set(**{"name": "YOYO", "value": "Yeah boi!!!"})
        printCookies(list(self.session.cookies.items()), self.verbose)
        coloredOK("AdAuth", adAuth_response, self.verbose)
        self.loggedIn = True

    def get_TT(self, date, group):
        timetable_data =  '{"selectedDate": "'+date+'", "selectedGroup": "'+group+'"}'
        timetable_response = self.session.post(
            'https://'+self.url+'/Default.asmx/GetTimetable', 
            headers=self.headers['timetable'],  
            data=timetable_data
        )

        try:
            timetable_response.json()
        except JSONDecodeError:
            print("RIP")

        coloredOK("Timetable", timetable_response)
        return(timetable_response)

    def print_TT(self, date, group):
        timetable = self.get_TT(date, group)
        print(timetable.json()['d']['Info'])
        periods = timetable.json()['d']['Periods']
        for period in periods:
            for schClass in period['Classes']:
                print('-------------------------')
                print(schClass['TimeTableClass'])
                print(schClass['TeacherName'])
                print(schClass['Room'])

    def get_classes(self, sem):

        guid = self.get_guid()
        data = '{"guidString":"'+guid+'","fileSeq": '+str(sem)+'}'

        response = self.session.post(
            'https://intranet.stpats.vic.edu.au/WebModules/Profiles/Student/LearningResources/LearningAreaTasks.aspx/getClasses', 
            headers=self.headers['average'], 
            # cookies=cookies, 
            data=data
        )
        return(response.json())

    def get_average(self, sem):
       
        classes_json = self.get_classes(sem)
        resultRegx = re.compile(r'(?:\d+ \/ \d+ \((\d+)%\)|(\d+)%)')
        scoreList = []    
        
        # print(response.text)
        # printCookies(list(self.session.cookies.items()))

        for subjClass in classes_json['d']['SubjectClasses']:
            for task in subjClass['Tasks']:
                finalScore = int([ x for x in resultRegx.findall(task['FinalResult'])[0] if x != ''][0]) if resultRegx.findall(task['FinalResult']) else None 
                if finalScore:
                    scoreList.append(finalScore)

        try:
            print(sum(scoreList) / len(scoreList)) 
        except ZeroDivisionError:
            print('No Tasks this semester')
 

    def get_guid(self):
        headers = {
            **self.default_headers,
            'Referer': 'https://'+self.url+'/WebModules/Profiles/Student/LearningResources/LearningAreaTasks.aspx?UserGUID=cf3e1f97-210f-4e35-a693-b4c176d9d94d',
            'Content-Type': 'application/json; charset=utf-8',
            'X-Requested-With': 'XMLHttpRequest',
            'Cache-Control': 'max-age=0',
        }
        
        params = (
            ((str(int(datetime.datetime.now().timestamp() * 1000)), ''),)
        )
        
        response = self.session.post('https://'+self.url+'/Default.asmx/GetUserInfo', headers=headers, params=params)
        coloredOK("GUID", response)
        guidRegx = re.compile(r'.*?GUID=(.*)')
        # print(response.text)
        printCookies([['GUID',guidRegx.search(response.json()['d']['UserPhotoUrl']).group(1).upper()]])
        return(guidRegx.search(response.json()['d']['UserPhotoUrl']).group(1).upper())
