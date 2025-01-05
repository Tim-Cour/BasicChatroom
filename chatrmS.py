import socket
import threading
import sqlite3
import time
from pytz import timezone
from datetime import datetime
format = "%m-%d-%Y %H:%M %Z"
class Mainframe ():
    def __init__(self):
        self.s=socket.socket(socket.AF_INET,socket.SOCK_STREAM)
        host='localhost'
        port=12345
        self.s.bind((host,port))
        self.connlis=[]
        threading.Thread(target=self.commcheck,daemon=True).start()
    def distcomm(self,msg):
        for i, sc in enumerate(self.connlis):
            try:
                sc.getconn().send(msg.encode())
            except:
                #tempmsg=sc.getname()+" has left the call"
                #self.distcomm(tempmsg)
                print("Removed Connection: ",self.connlis.pop(i))
    def commcheck(self):
        self.hist=SQLIntegrate("C:\\Users\\timco\\OneDrive\\Documents\\YoungWonks\\Level 3\\3. SQL\\timc.db")
        self.hist.createtable()
        while True:
            for sc in self.connlis:
                if sc.getCM():
                    print("MESSAGE!!!")
                    tempmsg=sc.getCM()
                    if tempmsg[0]=="✲":
                        print("INTROMSG")
                        tempNE=tempmsg.index("⁛")
                        tempN=tempmsg[2:tempNE-1]
                        print(tempN)
                        #try:
                            #print("Sent Message History")
                        #except:
                            #print("No Message History")
                        sc.setname(tempN)
                        self.distcomm(tempmsg)
                        self.submithist(tempmsg)
                        sc.getconn().send(self.gethist().encode())
                        sc.clearHist()
                    else:
                        self.cstnow=datetime.now(timezone("CST6CDT"))
                        tempmsg=sc.getname()+" at "+self.cstnow.strftime(format)+": "+tempmsg
                        print(tempmsg)
                        self.distcomm(tempmsg)
                        self.submithist(tempmsg)
                        sc.clearHist()
    def roomentry(self):
        while True:
            self.s.listen(5)
            self.conn,self.addr=self.s.accept()
            self.dataINIT=self.conn.recv(1024)
            self.dataINIT=self.dataINIT.decode()
            self.connlis.append(SubComm(self.conn,self.addr))
    def gethist(self):
        self.histIND=self.hist.getlogs()
        print(self.histIND)
        return self.histIND
    def submithist(self,msg):
        self.hist.executequery("INSERT INTO chatRmDB (msg) VALUES (?);",((msg,)))
            
class SubComm():
    def __init__(self,conn,addr):
        self.conn=conn
        self.addr=addr
        self.currentmsg=[]
        self.commhist=[]
        self.name=""
        threading.Thread(target=self.constantconn,daemon=True).start()
    def constantconn (self):
        while True:
            self.data=self.conn.recv(1024)
            self.data=self.data.decode()
            self.commhist.append(self.data)
            self.currentmsg=[self.data]
    def getCM(self):
        try:
            tmp=self.currentmsg[0]
            return tmp
        except IndexError:
            return False
    def clearHist(self):
        self.currentmsg=[]
    def getconn(self):
        return self.conn
    def setname(self,nn):
        self.name=nn
    def getname(self):
        return self.name
class Database():
    def __init__(self,name):
        self.name=name
        self.conn=sqlite3.connect(self.name)
        self.cursor=self.conn.cursor()
        print(name,self.conn,self.cursor)
    def executequery(self,query,params=None):
        if params:
            self.cursor.execute(query,params)
        else:
            self.cursor.execute(query)
        self.conn.commit()
    def fetchdata(self,query,params=None):
        if params:
            self.cursor.execute(query,params)
        else:
            self.cursor.execute(query)
        return self.cursor.fetchall()
    def closeconnection(self):
        self.cursor.close()
        self.conn.close()
class SQLIntegrate(Database):
    def __init__(self,name):
        super().__init__(name)
    def createtable(self):
        createquery='''
        CREATE TABLE IF NOT EXISTS chatRmDB (msg STRING)
        '''
        self.executequery(createquery)
    def getlogs(self):
        selectquery='SELECT * FROM chatRmDB'
        print(self.fetchdata(selectquery))
        templis=[]
        for msg in self.fetchdata(selectquery):
            templis.append("".join(msg))
        templis.append("\n")
        return "\n".join(templis)

if __name__ == "__main__":
    m=Mainframe()
    m.roomentry()