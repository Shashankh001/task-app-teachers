from kivy.app import App
from kivy.lang import Builder
from kivy.uix.screenmanager import *
from kivymd.app import MDApp
import json
import easygui
from threading import Thread
from datetime import datetime
from datetime import date
import socket
from mega import Mega
from kivymd.uix.card import MDCard
from kivy.uix.label import Label
from kivymd.uix.spinner import MDSpinner
from kivymd.uix.dialog import MDDialog
from kivy.clock import Clock
from kivy.uix.image import Image
import notif_sender

mega = Mega()
mega._login_user('shashankhgedda@gmail.com','Shashankh*12@mydad')


IP  = '192.168.0.102'
PORT = 2345
details = []
codes = ['LOGIN','SEND_NOTICE','SEND_HOMEWORK','SEND_ATTCH']

kv = """
#:kivy 2.1.0



WindowManager:
    Login:
        name: 'login'
        id: 'login'
    Menu:
        name: 'menu'
        id: menuu
    Notice:
        name: 'notice'
        id: 'notice'
    Homework:
        name: 'homework'
        id: 'homework'
    LoadNotice:
        name: 'loadnotice'
        id: 'loadnotice'
    LoadHomework:
        name: 'loadhomework'
        id: 'loadhomework'


<Login>:
    MDCard:
        size_hint: None,None
        size: 300,400
        pos_hint: {'center_x':0.5,'center_y':0.5}
        padding: 25
        spacing: 15
        orientation: 'vertical'

        MDLabel:
            text: "Login"
            font_size: '22sp'
            halign: 'center'
            size_hint_y: None
            height: self.texture_size[1]
            padding_y: 25
        
        MDTextField:
            text: 'Juliana'
            id: username
            hint_text: "Enter Username"
            size_hint_x: None
            width: 200
            font_size: '18sp'
            multiline: False
            pos_hint: {'center_x':0.5}
            helper_text: "Invalid Details"
            helper_text_mode: "on_error"

        MDTextField:
            text: 'Juliana079'
            id: password
            hint_text: "Enter Password"
            size_hint_x: None
            width: 200
            font_size: '18sp'
            multiline: False
            pos_hint: {'center_x':0.5}
            helper_text: "Invalid Details"
            helper_text_mode: "on_error"

        Widget:
            size_hint_y: None
            height:10

        MDRaisedButton:
            id: login
            text: "Login"
            font_size: '18sp'
            pos_hint: {'center_x':0.5}
            on_release: root.login()

        Widget:
            size_hint_y: None
            height:10



<Menu>:
    Label: 
        text: 'Main Menu'
        font_size: '28sp'
        pos_hint: {'center_x': 0.5, 'center_y':0.7}

    MDFillRoundFlatButton:
        text: "Send a notice"
        font_size: '18sp'
        size_hint_x: .2
        pos_hint: {'center_x': 0.5, 'center_y':0.4}
        on_release: root.notice()

    MDFillRoundFlatButton:
        text: "Send Homework"
        font_size: '18sp'
        size_hint_x: .2
        pos_hint: {'center_x': 0.5, 'center_y':0.5}
        on_release: root.homework()

    Label:
        text: 'Version 1.0.0'
        font_size: '16sp'
        pos_hint: {'center_x': 0.5, 'center_y':0.02}


<Notice>:
    Label:
        text: 'Send a Notice'
        pos_hint: {'center_x':0.5,'center_y':0.9}
        font_size: '28sp'

    MDTextField:
        id: textt
        hint_text: "Click To Enter Text"
        mode: "fill"
        multiline: True
        size_hint: 0.9,0.6
        pos_hint: {'center_x':0.5,'center_y':0.5}
    
    MDRaisedButton:
        id: files
        text: "Attach files"
        font_size: '18sp'
        pos_hint: {'center_x':0.2, 'center_y':0.14}
        on_release: root.thread_atfiles()

    MDRaisedButton:
        id: send
        text: "Send Notice"
        font_size: '18sp'
        pos_hint: {'center_x':0.5, 'center_y':0.14}
        on_release: root.thread_notice()

    MDRaisedButton:
        id: rem_attch
        text: "Remove all attachments"
        font_size: '18sp'
        pos_hint: {'center_x':0.8, 'center_y':0.14}
        on_release: root.remAttch()

    MDRectangleFlatButton:
        id: back
        text: 'Back'
        pos_hint: {'center_x':0.96, 'center_y':0.96}
        on_release: root.back_to_menu()
    
    Label:
        id: atth
        text: 'Attachments uploaded: 0'
        pos_hint: {'center_x':0.5, 'center_y':0.07}
        font_size: '16sp'


<Homework>:
    Label:
        text: 'Send Homework'
        pos_hint: {'center_x':0.5,'center_y':0.9}
        font_size: '28sp'

    MDTextField:
        id: textt
        hint_text: "Click To Enter Text"
        mode: "fill"
        multiline: True
        size_hint: 0.9,0.6
        pos_hint: {'center_x':0.5,'center_y':0.5}
    
    MDRaisedButton:
        id: files
        text: "Attach files"
        font_size: '18sp'
        pos_hint: {'center_x':0.2, 'center_y':0.14}
        on_release: root.thread_atfiles()

    MDRaisedButton:
        id: send
        text: "Send Homework"
        font_size: '18sp'
        pos_hint: {'center_x':0.5, 'center_y':0.14}
        on_release: root.thread_homework()

    MDRaisedButton:
        id: rem_attch
        text: "Remove all attachments"
        font_size: '18sp'
        pos_hint: {'center_x':0.8, 'center_y':0.14}
        on_release: root.remAttch()

    MDRectangleFlatButton:
        id: back
        text: 'Back'
        pos_hint: {'center_x':0.96, 'center_y':0.96}
        on_release: root.back_to_menu()
    
    Label:
        id: atth
        text: 'Attachments uploaded: 0'
        pos_hint: {'center_x':0.5, 'center_y':0.07}
        font_size: '16sp'

<LoadNotice>:
    Label:
        text: "Sending your Notice. Hang on tight!"
        pos_hint: {'center_x':0.6,'center_y':0.5}
        bold: True
        font_size: 40

    Label:
        text: 'You will be redirected to the main menu after the homework is sent!'
        font_size: 20
        pos_hint: {'center_x':0.6,'center_y':0.44}
    
    MDSpinner:
        size_hint: 0.1,0.1
        pos_hint: {'center_x':0.2,'center_y':0.5}

<LoadHomework>:
    Label:
        text: "Sending your Homework. Hang on tight!"
        pos_hint: {'center_x':0.6,'center_y':0.5}
        bold: True
        font_size: 40
    
    Label:
        text: 'You will be redirected to the main menu after the homework is sent!'
        font_size: 20
        pos_hint: {'center_x':0.6,'center_y':0.44}
        
    MDSpinner:
        size_hint: 0.1,0.1
        pos_hint: {'center_x':0.2,'center_y':0.5}    
"""

class Login(Screen):
    def login(self):        
        username = self.ids.username.text
        password = self.ids.password.text

        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        s.connect((IP,PORT))

        s.send(bytes(codes[0],'utf-8'))
        
        cred = s.recv(10000)
        cred = cred.decode('utf-8')

        cred = json.loads(cred)
        
        index = None
        for i in range(0,len(cred)):
            
            user = cred[i]["Name"]
            passw = cred[i]["Password"]
            subject = cred[i]["Subject"]

            if user == username and passw == password:
                self.ids.username.error = False
                self.ids.password.error = False
                s.send(bytes('SUCCESS','utf-8'))
                details.append(username)
                details.append(subject)
                index = 1
                TaskAppApp.build.kv.current = 'menu'
                

        if index == None:
            self.ids.username.error = True
            self.ids.password.error = True




class Menu(Screen):
    def notice(self):
        TaskAppApp.build.kv.current = 'notice'
        TaskAppApp.build.kv.transition.direction = 'left'
    
    def homework(self):
        TaskAppApp.build.kv.current = 'homework'



class Notice(Screen):   
    attch = []

    def back_to_menu(self):
        TaskAppApp.build.kv.current = 'menu'
        TaskAppApp.build.kv.transition.direction = 'right'

    def back_to_menu_t(self, dt):
        TaskAppApp.build.kv.current = 'menu'
        TaskAppApp.build.kv.transition.direction = 'right'

    def thread_atfiles(self):
        Notice.thread_atfiles.t1 = Thread(target=Notice.attFiles, args=(self,))
        Notice.thread_atfiles.daemon = True
        Notice.thread_atfiles.t1.start()



    def attFiles(self):
        Notice.attFiles.path = easygui.fileopenbox(title="Choose File",multiple=True)

        for i in range(0,len(Notice.attFiles.path)):
            try:    
                if Notice.attFiles.path[i] in self.attch:
                    pass

                if Notice.attFiles.path[i] not in self.attch:
                    self.attch.append(Notice.attFiles.path[i])

            except IndexError:
                self.attch.append(Notice.attFiles.path[i])

        no_of_files = len(self.attch)
        self.ids.atth.text = f"Attachments uploaded: {no_of_files}"
        Notice.thread_atfiles.t1.join

    def finishing_up(self, dt):
        self.attch = []
        self.ids.atth.text = f"Attachments uploaded: 0"
        self.ids.textt.text = ''
        self.remove_widget(Notice.thread_notice.spinner)

    def remAttch(self):
        self.attch = []
        self.ids.atth.text = f"Attachments uploaded: 0"


    def thread_notice(self):
        t1 = Thread(target= Notice.sendNotice, args =(self,))
        t1.daemon = True
        t1.start()

        TaskAppApp.build.kv.current = 'loadnotice'
        TaskAppApp.build.kv.transition.direction = 'left'

        

    def sendNotice(self):
        #gathering details
        text = self.ids.textt.text
        try:
            images = Notice.attFiles.path
        except AttributeError:
            images = 'None'
        time = datetime.today().strftime("%I:%M %p")
        datee = str(date.today())

        #connecting
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        s.connect(('192.168.0.102',2345))

        s.send(bytes(codes[1],'utf-8'))
        
        #recieving current data
        data = s.recv(10000000)
        data = data.decode('utf-8')  

        data = json.loads(data)        

        #sending attachments if any       
        attachments = len(self.attch)

        links = []
        try:
            for i in range(0, attachments):
                folder = mega.find(details[1])
                file = self.attch[i]
                
                uploaded = mega.upload(file, folder[0])
                link = mega.get_upload_link(uploaded)
                links.append(link)

        except FileNotFoundError:
            print('no file')

        notice = {"Teacher":details[0],"Subject":details[1],"Time":time,"Date":datee,"Attachments":links,"Context":text}
        data.append(notice)

        #sending the json file back
        jsonObj = json.dumps(data)
        
        s.send(bytes(jsonObj,'utf-8'))

        #finishing up
        notif_sender.send('NOT',text)
        Clock.schedule_once(self.back_to_menu_t, 1)

            

class LoadNotice(Screen):
    pass
        
class LoadHomework(Screen):
    pass     

class Homework(Screen):
    attch = []

    def back_to_menu(self):
        TaskAppApp.build.kv.current = 'menu'
        TaskAppApp.build.kv.transition.direction = 'right'

    def back_to_menu_t(self, dt):
        TaskAppApp.build.kv.current = 'menu'
        TaskAppApp.build.kv.transition.direction = 'right'

    def thread_atfiles(self):
        Homework.thread_atfiles.t1 = Thread(target=Homework.attFiles, args=(self,))
        Homework.thread_atfiles.daemon = True
        Homework.thread_atfiles.t1.start()



    def attFiles(self):
        Homework.attFiles.path = easygui.fileopenbox(title="Choose File",multiple=True)

        for i in range(0,len(Homework.attFiles.path)):
            try:    
                if Homework.attFiles.path[i] in self.attch:
                    pass

                if Homework.attFiles.path[i] not in self.attch:
                    self.attch.append(Homework.attFiles.path[i])

            except IndexError:
                self.attch.append(Homework.attFiles.path[i])

        no_of_files = len(self.attch)
        self.ids.atth.text = f"Attachments uploaded: {no_of_files}"
        Homework.thread_atfiles.t1.join

    def finishing_up(self, dt):
        self.attch = []
        self.ids.atth.text = f"Attachments uploaded: 0"
        self.ids.textt.text = ''
        self.remove_widget(Homework.thread_notice.spinner)

    def remAttch(self):
        self.attch = []
        self.ids.atth.text = f"Attachments uploaded: 0"


    def thread_homework(self):
        t1 = Thread(target= Homework.sendHomework, args =(self,))
        t1.daemon = True
        t1.start()

        TaskAppApp.build.kv.current = 'loadhomework'
        TaskAppApp.build.kv.transition.direction = 'left'

        

    def sendHomework(self):
        #gathering details
        text = self.ids.textt.text
        try:
            images = Homework.attFiles.path
        except AttributeError:
            images = 'None'
        time = datetime.today().strftime("%I:%M %p")
        datee = str(date.today())

        #connecting
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        s.connect(('192.168.0.102',2345))

        s.send(bytes(codes[2],'utf-8'))
        
        #recieving current data
        data = s.recv(10000000)
        data = data.decode('utf-8')  

        data = json.loads(data)        

        #sending attachments if any       
        attachments = len(self.attch)
        print(self.attch)
        print(attachments)
        links = []
        try:
            for i in range(0, attachments):
                folder = mega.find(details[1])
                file = self.attch[i]
                
                uploaded = mega.upload(file, folder[0])
                link = mega.get_upload_link(uploaded)
                links.append(link)

        except FileNotFoundError:
            print('no file')

        notice = {"Teacher":details[0],"Subject":details[1],"Time":time,"Date":datee,"Attachments":links,"Context":text}
        data.append(notice)

        #sending the json file back
        jsonObj = json.dumps(data)
        
        s.send(bytes(jsonObj,'utf-8'))

        #finishing up
        notif_sender.send('HW',text)
        Clock.schedule_once(self.back_to_menu_t, 1)







class WindowManager(ScreenManager):
    pass



class TaskAppApp(MDApp):
    def __init__(self, **kwargs):
        self.title = "Task App"
        super().__init__(**kwargs)

    def build(self):
        TaskAppApp.build.kv = Builder.load_string(kv)
        self.theme_cls.theme_style = "Dark"
        self.theme_cls.primary_palette = "Gray"
        return TaskAppApp.build.kv


if __name__ == '__main__':
    TaskAppApp().run()