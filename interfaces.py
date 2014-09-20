from tkinter import *
from database import *
import tkinter.messagebox as messagebox
import re,functools


def standardPhoneForm(input):
    result=''
    for symbol in input:
        if symbol in '0123456789':
            result+=symbol
    if result and (result[0]=='8' or result[0]=='7'): result=result[1:] 
    return result


class MainFrame(Frame):
    def __init__(self,root,DataHandler):
        Frame.__init__(self, root)
        #allTheDataList - список всех записей из базы данных
        #currentValuesList - список тех записей, что следует отобразить во фрейме
        #self.DBH есть обработчик запросов к базе данных
        self.DBH=DataHandler
        self.canvas = Canvas(root, borderwidth=0, background="#ffffff",height=570)
        self.frame = Frame(self.canvas, background="#ffffff")
        self.vsb = Scrollbar(root, orient="vertical", command=self.canvas.yview)
        self.canvas.configure(yscrollcommand=self.vsb.set)
        self.vsb.pack(side="right",fill=Y)
        self.canvas.pack(side=TOP, fill=X, expand=FALSE)
        self.canvas.create_window((4,4), window=self.frame, anchor="nw", tags="self.frame")
        self.frame.bind("<Configure>", self.OnFrameConfigure)
        #на шляпу сверху не стоит обращать внимания
        #к архитектуре программы она не имеет отношения
        self.allTheDataList=DataHandler.readData()
        self.currentValuesList=self.allTheDataList
        self.stringFrames=[]

        self.createWidgets() #создаём набор фреймов и обработчики к ним
        #теперь фреймы лежат в self.stringFrames; остаётся их только вывести
        self.packWidgets()   #выводим результат в главный фрейм

    def find(self,event,pattern):
        pattern=pattern().lower()
        self.currentValuesList=[]
        for item in self.allTheDataList:
            if pattern in item[0].lower()+item[3].lower():
                self.currentValuesList+=[item]
        pattern = standardPhoneForm(pattern)
        self.unpackWidgets()
        self.stringFrames=[]
        self.createWidgets()
        self.packWidgets()
        
   
    def createWidgets(self):
        for item in self.currentValuesList:
            def handler(event, self=self, i=self.currentValuesList.index(item)):
                return self.ChangeRowHandler(event, i)
            tempFrame=Frame(self.frame)
            t=Label(tempFrame,text=str(self.currentValuesList.index(item)),width=5,padx=1)
            t.pack(side=LEFT)
            t.bind("<Button-1>",handler)
            for i in range(len(item)):
                t=Label(tempFrame,text=str(item[i]),width=[5,38,12,8,20,12][i+1],padx=1)
                t.pack(side=LEFT)
                t.bind("<Button-1>",handler)
            self.stringFrames+=[tempFrame]
            
    def packWidgets(self):
        for frameUnit in self.stringFrames:
            frameUnit.pack(side=TOP,pady=1)
       
                
    def unpackWidgets(self):
        for frameUnit in self.stringFrames:
                frameUnit.pack_forget()

    def ChangeRowHandler(self,event,index):
        global root
        t = Toplevel(root)
        t.title('Изменить запись')
        t.geometry('300x105+110+110')
        t.resizable(FALSE,FALSE)
        
        okButton=Button(t,text="ОК",width=10)
        cancelButton=Button(t,text="Отмена",width=10)
        delButton=Button(t,text="Удалить",width=10)
        plusButton=Button(t,text="+1")
    
        nameEntry=Entry(t,width=50)
        nameEntry.insert(0,self.currentValuesList[index][0])
        oldName=self.currentValuesList[index][0]
        phoneEntry=Entry(t,width=50)
        oldPhone=self.currentValuesList[index][3]
        phoneEntry.insert(0,self.currentValuesList[index][3])
        companyEntry=Entry(t,width=50)
        companyEntry.insert(0,self.currentValuesList[index][4])
        visitsEntry=Entry(t,width=6)
        visitsEntry.insert(0,self.currentValuesList[index][1])
        
        nameEntry.place(x=0)
        phoneEntry.place(x=0,y=18)
        companyEntry.place(x=0,y=37)
        visitsEntry.place(x=235,y=37+18+1)
        plusButton.place(x=277,y=34+18)

        v = IntVar()
        
        _0=Radiobutton(t, text="0%", variable=v, value=0)
        _0.place(x=0,y=54)
        _5=Radiobutton(t, text="5%", variable=v, value=5)
        _5.place(x=40,y=54)
        _7=Radiobutton(t, text="7%", variable=v, value=7)
        _7.place(x=80,y=54)
        _15=Radiobutton(t, text="15%", variable=v, value=15)
        _15.place(x=120,y=54)
        _30=Radiobutton(t, text="30%", variable=v, value=30)
        _30.place(x=170,y=54)
        v.set(self.currentValuesList[index][2])

        okButton.place(x=5,y=78)
        cancelButton.place(x=150,y=78)
        delButton.place(x=224,y=78)


        def killThemAll(event):
            tt=messagebox.askyesno(message='Точно хотите удалить запись?',icon='question')
            if tt:
                self.DBH.deleteData(oldName,oldPhone)
                self.DBH.organizeData()
                self.unpackWidgets()
                self.allTheDataList=self.DBH.readData()
                self.currentValuesList=self.allTheDataList
                self.stringFrames=[]
                self.createWidgets()
                self.packWidgets()
                t.destroy()

        def cancelAction(event):
            t.destroy()
            

        def plusAction(event):
            p=int(visitsEntry.get(),10)
            visitsEntry.delete(0,50)
            visitsEntry.insert(0,p+1)   

        def okAction(event):
            discount=v.get()
            name=nameEntry.get()
            phone=phoneEntry.get()
            company=companyEntry.get()
            try:
                visits=int(visitsEntry.get(),10)
                if visits<0:
                    raise ValueError
                self.DBH.updateData(oldName,oldPhone,["'{}'".format(name),visits,discount,"'{}'".format(phone),"'{}'".format(company)])
                self.unpackWidgets()
                self.allTheDataList=self.DBH.readData()
                self.currentValuesList=self.allTheDataList
                self.stringFrames=[]
                self.createWidgets()
                self.packWidgets()
                t.destroy()
            except ValueError:
                messagebox.showinfo("Ошибка!", "Количество посещений должно быть натуральным числом")
                return
            
            
        delButton.bind('<ButtonRelease-1>',killThemAll)
        cancelButton.bind('<ButtonRelease-1>',cancelAction)
        plusButton.bind('<ButtonRelease-1>',plusAction)
        okButton.bind('<ButtonRelease-1>',okAction)
        t.bind('<Return>',okAction)
        t.grab_set()
        t.focus_set()
        t.wait_window()
                
    def OnFrameConfigure(self,event):
        self.canvas.configure(scrollregion=self.canvas.bbox("all"))

    
    def newClientAction(self,event):
        global root
        t = Toplevel(root)
        t.title('Добавить клиента')
        t.geometry('300x105+110+110')
        t.resizable(FALSE,FALSE)
        
        okButton=Button(t,text="ОК",width=10)
        cancelButton=Button(t,text="Отмена",width=10)
        plusButton=Button(t,text="+1")
    
        nameEntry=Entry(t,width=50)
        nameEntry.insert(0,'Ф.И.О.')
        phoneEntry=Entry(t,width=50)
        phoneEntry.insert(0,'Телефон')
        visitsEntry=Entry(t,width=6)
        visitsEntry.insert(0,'1')
        companyEntry=Entry(t,width=50)
        companyEntry.insert(0,'Телефонная компания')
        
        nameEntry.place(x=0)
        phoneEntry.place(x=0,y=18)
        companyEntry.place(x=0,y=37)
        visitsEntry.place(x=235,y=37+18+1)
        plusButton.place(x=277,y=34+18)

        v = IntVar()
        
        _0=Radiobutton(t,text="0%", variable=v, value=0)
        _0.place(x=0,y=54)
        _5=Radiobutton(t,text="5%", variable=v, value=5)
        _5.place(x=40,y=54)
        _7=Radiobutton(t,text="7%", variable=v, value=7)
        _7.place(x=80,y=54)
        _15=Radiobutton(t,text="15%", variable=v, value=15)
        _15.place(x=120,y=54)
        _30=Radiobutton(t,text="30%", variable=v, value=30)
        _30.place(x=170,y=54)
        v.set(0)

        okButton.place(x=5,y=78)
        cancelButton.place(x=224,y=78)

        def cancelAction(self):
            t.destroy()

        def plusAction(event):
            p=int(visitsEntry.get(),10)
            visitsEntry.delete(0,50)
            visitsEntry.insert(0,p+1)   

        def okAction(event):
            discount=v.get()
            name=nameEntry.get()
            phone=phoneEntry.get()
            company = companyEntry.get()
            try:
                visits=int(visitsEntry.get(),10)
                if visits<0:
                    raise ValueError
                fancyPhone=standardPhoneForm(phone)
                for item in self.allTheDataList:
                    if fancyPhone==standardPhoneForm(item[3]):
                        if phone==item[3]:
                            raise IndexError
                self.DBH.addData(["'{}'".format(s) for s in [name, phone, visits, discount,company]])
                self.unpackWidgets()
                self.allTheDataList=self.DBH.readData()
                self.currentValuesList=self.allTheDataList
                self.stringFrames=[]
                self.createWidgets()
                self.packWidgets()
                t.destroy()    
            except ValueError:
                messagebox.showinfo("Ошибка!", "Количество посещений должно быть натуральным числом")
                return
            except IndexError:
                messagebox.showinfo("Предупрежденьице в летнем платьице","Клиент с таким номером уже есть в базе")
            
        cancelButton.bind('<ButtonRelease-1>',cancelAction)
        plusButton.bind('<ButtonRelease-1>',plusAction)
        okButton.bind('<ButtonRelease-1>',okAction)
        plusButton.bind('<ButtonRelease-1>',plusAction)
        t.bind('<Return>',okAction)
        t.grab_set()
        t.focus_set()
        


if __name__=='__main__':
  DBH = DatabaseHandler('clientsList')
  root=Tk()
  root.resizable(0,0)
  root.title("Список клиентов")
  root.geometry('620x220+100+100')
  buttomPanel = Frame()
  newClient=Button(buttomPanel,text="Добавить клиента",padx=2,pady=2)
  newClient.configure(state=ACTIVE)
  newClient.pack(side=LEFT)
  find=Button(buttomPanel,text="Найти",padx=5,pady=2)
  find.pack(side=RIGHT)
  findEntry=Entry(buttomPanel,width=20)
  findEntry.pack(side=RIGHT,padx=4)
  buttomPanel.pack(fill=X,padx=2)
  Frame(root,height=2).pack(fill=X)
  medianPanel = Frame()
  t=Label(medianPanel,text="#",relief=GROOVE,pady=5,width=5)
  t.pack(side=LEFT)
  Label(medianPanel,text="Ф.И.О.",width=38,relief=GROOVE,pady=5).pack(side=LEFT)
  Label(medianPanel,text="Посещения",relief=GROOVE,pady=5,width=12).pack(side=LEFT)
  Label(medianPanel,text="Скидка",relief=GROOVE,pady=5,width=8).pack(side=LEFT,fill=X)
  Label(medianPanel,text="Телефон",width=20,relief=GROOVE,pady=5).pack(side=LEFT)
  Label(medianPanel,text="Компания",width=12,relief=GROOVE,pady=5).pack(side=LEFT)
 
  medianPanel.pack(fill=X,padx=2,pady=5)
  mFrame=MainFrame(root,DBH)
  newClient.bind('<Button-1>',mFrame.newClientAction)
  find.bind('<ButtonRelease-1>',functools.partial(mFrame.find,pattern=findEntry.get))
  findEntry.bind('<Return>',functools.partial(mFrame.find,pattern=findEntry.get))
  root.mainloop()

            
            
