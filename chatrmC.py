import socket
from tkinter import *
from tkinter import simpledialog
import threading
class Display (Tk):
    def __init__(self,b):
        Tk.__init__(self)
        self.b=b
        #Name Setting
        self.oname=simpledialog.askstring("Name Input","Enter Username: ")
        tempS="".join([self.oname,"`s Chat Terminal"])
        self.title(tempS)
        tempS="".join(["✲ ",self.oname," ⁛ "" has joined the session"])
        self.b.senddata(tempS)
        #Setting up Tkinter
        self.rtextbox=Text(self,width=100,height=20,bg="black",fg="green") 
        self.rtextbox.grid(column=0,row=0,columnspan=3)
        #Label(self,text="Your Message:").grid(column=0,row=1)
        self.mainentry=Entry(self,width=120)
        self.mainentry.grid(column=0,row=1,columnspan=2)
        self.rtextbox.config(state='disabled')
        self.submitb=Button(self,text="     Submit     ",bg="green",fg="white",command= lambda: self.dataprocessing(self.mainentry.get(),0))
        self.submitb.grid(column=2,row=1)
        self.commLis=[]
    def dataprocessing(self,strent,tb):
        self.tempstr=strent
        if tb==0:
            self.b.senddata(self.tempstr)
        else:
            self.tempstr=self.tempstr +"\n"
            self.textedit(self.tempstr)
        self.mainentry.delete(0,'end')
    def textedit(self,value):
        self.rtextbox.config(state='normal')
        self.rtextbox.insert('end',value)
        self.rtextbox.config(state='disabled')

    def gethelper(self):
        while True:
            data=self.b.constantconn()
            self.commLis=[data,1]

    def mainloop(self):
        try:
            threading.Thread(target=self.gethelper,daemon=True).start()
        except Exception as e:
            print("Thread Exception:", e)
        while True:
            if self.commLis:
                self.dataprocessing(self.commLis[0],self.commLis[1])
                self.commLis=[]
            self.update_idletasks()
            self.update()
        
class Backend ():
    def __init__(self):
        host='localhost'
        port=12345
        self.s=socket.socket(socket.AF_INET,socket.SOCK_STREAM)
        self.s.connect((host,port))
        self.s.send("ping".encode())
    def constantconn(self):
        self.data=self.s.recv(1024)
        self.data=self.data.decode()
        return self.data
    def senddata(self,data):
        self.s.send(data.encode())
            
if __name__ == "__main__":
    b=Backend()
    app = Display(b)
    app.mainloop()