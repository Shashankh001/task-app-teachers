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
from kivymd.uix.button import MDFlatButton
from kivy.uix.label import Label
from kivymd.uix.spinner import MDSpinner
from kivymd.uix.dialog import MDDialog
from kivy.clock import Clock
from kivy.uix.image import Image
import notif_sender
from kivy.core.window import Window
from kivy.metrics import dp, sp
from kivy.uix.boxlayout import BoxLayout
from kivymd.uix.pickers import MDDatePicker
from kivy.uix.scrollview import ScrollView
from kivy.effects.scroll import ScrollEffect
from kivy.uix.stacklayout import StackLayout
from functools import *
import sys
import time

Window.size = (1080, 720)

mega = Mega()
mega._login_user('','')

def get_ip():
    with open('ip2.txt') as f:
        return f.read()

IP = get_ip()
PORT = 2345
details = []
codes = ['LOGIN','SEND_NOTICE','SEND_HOMEWORK','SEND_ATTCH']
CLASS = None

def get_bytesize_string(string, bytelen):
    string_length = sys.getsizeof(string)

    if string_length == bytelen: return None
    
    if string_length < bytelen:
        difference = bytelen - string_length
        for i in range(0, difference):
            string += ' '

        return string

def get_bytesize_bytes(byte, bytelen):
    byte_length = sys.getsizeof(byte)

    if byte_length == bytelen: return None
    
    if byte_length < bytelen:
        difference = bytelen - byte_length
        for i in range(0, difference):
            byte += b' '

        return byte

kv = '''
#:kivy 2.1.0



WindowManager:
    Login:
        name: 'login'
        id: 'login'
    Menu:
        name: 'menu'
        id: menuu
    SelectClassNotice:
        name: 'select-class-notice'
        id: 'select-class-notice'
    SelectClassHomework:
        name: 'select-class-homework'
        id: 'select-class-homework'
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
        size: ('300dp','400dp')
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
            id: username
            text: 'Shashankh'
            hint_text: "Enter Username"
            size_hint_x: None
            width: '200dp'
            font_size: '18sp'
            multiline: False
            pos_hint: {'center_x':0.5}
            helper_text: "Invalid Details"
            helper_text_mode: "on_error"

        MDTextField:
            id: password
            text: 'HueHueHue'
            hint_text: "Enter Password"
            size_hint_x: None
            width: '200dp'
            font_size: '18sp'
            multiline: False
            pos_hint: {'center_x':0.5}
            helper_text: "Invalid Details"
            helper_text_mode: "on_error"

        Widget:
            size_hint_y: None
            height:'10dp'

        MDRaisedButton:
            id: login
            text: "Login"
            font_size: '18sp'
            pos_hint: {'center_x':0.5}
            on_release: root.login()

        Widget:
            size_hint_y: None
            height:'10dp'



<Menu>:
    MDIconButton:
        icon: 'exit-to-app'
        pos_hint: {'center_x':0.95,'center_y':0.95}
        on_release: root.log_out()

    Label: 
        text: 'Main Menu'
        font_size: '28sp'
        pos_hint: {'center_x': 0.5, 'center_y':0.83}

    MDCard:
        size_hint: None,None
        size: '265dp','150dp'
        pos_hint: {'center_x': 0.5, 'center_y':0.6}
        orientation: 'vertical'
        line_color: 150/255,150/255,150/255,1
        focus_behavior: True
        ripple_behavior: True
        on_release: root.notice()

        
        Label:
            text: 'Notices'
            font_size: '18sp'

        MDSeparator:

        Label:
            text: 'Click to sent notices'
            font_size: '14sp'
            color: 150/255,150/255,150/255,1

    MDCard:
        size_hint: None,None
        size: '265dp','150dp'
        pos_hint: {'center_x': 0.5, 'center_y':0.35}
        orientation: 'vertical'
        line_color: 150/255,150/255,150/255,1
        focus_behavior: True
        ripple_behavior: True
        on_release: root.homework()

        Label:
            text: 'Homework'
            font_size: '18sp'

        MDSeparator:

        Label:
            text: 'Click to send homework'
            font_size: '14sp'
            color: 150/255,150/255,150/255,1
    Label:
        text: 'Version 1.0.0'
        font_size: '16sp'
        pos_hint: {'center_x': 0.5, 'center_y':0.02}

<SelectClassNotice>:
    Label:
        text: 'Select a Class'
        pos_hint: {'center_x':0.5,'center_y':0.9}
        font_size: '28sp'

    MDRectangleFlatButton:
        id: back
        text: 'Back'
        pos_hint: {'center_x':0.96, 'center_y':0.96}
        on_release: root.back_to_menu()

<SelectClassHomework>:
    Label:
        text: 'Select a Class'
        pos_hint: {'center_x':0.5,'center_y':0.9}
        font_size: '28sp'

    MDRectangleFlatButton:
        id: back
        text: 'Back'
        pos_hint: {'center_x':0.96, 'center_y':0.96}
        on_release: root.back_to_menu()

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
        size_hint: ('0.9dp','0.6dp')
        pos_hint: {'center_x':0.5,'center_y':0.55}
    
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
        on_release: root.remAttch('bean')

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
        size_hint: ('0.9dp','0.6dp')
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
        on_release: root.remAttch('bean')

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
        font_size: '40sp'

    Label:
        text: 'You will be redirected to the main menu after the homework is sent!'
        font_size: '20sp'
        pos_hint: {'center_x':0.6,'center_y':0.44}
    
    MDSpinner:
        size_hint: ('0.1dp','0.1dp')
        pos_hint: {'center_x':0.2,'center_y':0.5}

<LoadHomework>:
    Label:
        text: "Sending your Homework. Hang on tight!"
        pos_hint: {'center_x':0.6,'center_y':0.5}
        bold: True
        font_size: '40sp'
    
    Label:
        text: 'You will be redirected to the main menu after the homework is sent!'
        font_size: '20sp'
        pos_hint: {'center_x':0.6,'center_y':0.44}
        
    MDSpinner:
        size_hint: ('0.1dp','0.1dp')
        pos_hint: {'center_x':0.2,'center_y':0.5}    
'''

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

                self.ids.username.text = ''
                self.ids.password.text = ''
                TaskAppApp.build.kv.current = 'menu'
                TaskAppApp.build.kv.transition.direction = 'left'

                

        if index == None:
            self.ids.username.error = True
            self.ids.password.error = True




class Menu(Screen):
    def notice(self):
        TaskAppApp.build.kv.current = 'select-class-notice'
        TaskAppApp.build.kv.transition.direction = 'left'
    
    def homework(self):
        TaskAppApp.build.kv.current = 'select-class-homework'
        TaskAppApp.build.kv.transition.direction = 'left'

    def log_out(self):
        global details
        details = []
        TaskAppApp.build.kv.current = 'login'
        TaskAppApp.build.kv.transition.direction = 'right'

class SelectClassNotice(Screen):
    layout = StackLayout(size_hint=(1, None),orientation='rl-bt', spacing=20)
    layout.bind(minimum_height=layout.setter('height'))

    root = ScrollView(size_hint=(1, 0.8), effect_cls=ScrollEffect)
    root.add_widget(layout)

    class_list = ['1-A', '1-B', '1-C', '1-D', '2-A', '2-B', '2-C', '2-D', '3-A', '3-B', '3-C', '3-D', '4-A', '4-B', '4-C', '4-D', '5-A', '5-B', '5-C', '5-D', '6-A', '6-B', '6-C', '6-D', '7-A', '7-B', '7-C', '7-D', '8-A', '8-B', '8-C', '8-D', '9-A', '9-B', '9-C', '9-D', '10-A', '10-B', '10-C', '10-D']
    
    def on_enter(self, *args):
        self.load_classes()
        return super().on_enter(*args)

    def back_to_menu(self):
        for child in [child for child in self.layout.children]:
            self.layout.remove_widget(child)

        TaskAppApp.build.kv.current = 'menu'
        TaskAppApp.build.kv.transition.direction = 'right'

    def load_classes(self):
        for i in range(0, len(self.class_list)):
            class_name = Label(text=self.class_list[i],
                        markup= True,
                        padding= [15,15],
                        size_hint=(1,None),
                        halign="left",
                        valign="middle")
            
            class_name.bind(size=class_name.setter('text_size')) 
            class_name._label.refresh()
            class_name.height= (class_name._label.texture.size[1] + 2*class_name.padding[1])

            card = MDCard(
                height=class_name.height,
                style = 'elevated',
                size_hint= (1,None),
                orientation = 'vertical',
                ripple_behavior = True
            )

            card.bind(on_release = partial(self.select_user, self.class_list[i]))

            self.layout.add_widget(card)
            card.add_widget(class_name)
            
        try:
            self.add_widget(self.root)
        except:
            print("[ERROR] Couldn't add root widget, reason: root widget already exists.")


    def select_user(self, class_name, inst):
        print(class_name)
        for child in [child for child in self.layout.children]:
            self.layout.remove_widget(child)

        global CLASS
        CLASS = class_name

        TaskAppApp.build.kv.current = 'notice'
        TaskAppApp.build.kv.transition.direction = 'left'

class SelectClassHomework(Screen):
    layout = StackLayout(size_hint=(1, None),orientation='rl-bt', spacing=20)
    layout.bind(minimum_height=layout.setter('height'))

    root = ScrollView(size_hint=(1, 0.8), effect_cls=ScrollEffect)
    root.add_widget(layout)

    class_list = ['1-A', '1-B', '1-C', '1-D', '2-A', '2-B', '2-C', '2-D', '3-A', '3-B', '3-C', '3-D', '4-A', '4-B', '4-C', '4-D', '5-A', '5-B', '5-C', '5-D', '6-A', '6-B', '6-C', '6-D', '7-A', '7-B', '7-C', '7-D', '8-A', '8-B', '8-C', '8-D', '9-A', '9-B', '9-C', '9-D', '10-A', '10-B', '10-C', '10-D']
    
    def back_to_menu(self):
        for child in [child for child in self.layout.children]:
            self.layout.remove_widget(child)
            
        TaskAppApp.build.kv.current = 'menu'
        TaskAppApp.build.kv.transition.direction = 'right'

    def on_enter(self, *args):
        self.load_classes()
        return super().on_enter(*args)

    def load_classes(self):
        for i in range(0, len(self.class_list)):
            class_name = Label(text=self.class_list[i],
                        markup= True,
                        padding= [15,15],
                        size_hint=(1,None),
                        halign="left",
                        valign="middle")
            
            class_name.bind(size=class_name.setter('text_size')) 
            class_name._label.refresh()
            class_name.height= (class_name._label.texture.size[1] + 2*class_name.padding[1])

            card = MDCard(
                height=class_name.height,
                style = 'elevated',
                size_hint= (1,None),
                orientation = 'vertical',
                ripple_behavior = True
            )

            card.bind(on_release = partial(self.select_user, self.class_list[i]))

            self.layout.add_widget(card)
            card.add_widget(class_name)
            
        try:
            self.add_widget(self.root)
        except:
            print("[ERROR] Couldn't add root widget, reason: root widget already exists.")


    def select_user(self, class_name, inst):
        print(class_name)
        for child in [child for child in self.layout.children]:
            self.layout.remove_widget(child)

        global CLASS
        CLASS = class_name

        TaskAppApp.build.kv.current = 'homework'
        TaskAppApp.build.kv.transition.direction = 'left'



class Notice(Screen):
    attch = []

    def back_to_menu(self):
        global CLASS
        CLASS = None

        self.ids.textt.text = ''
        TaskAppApp.build.kv.current = 'menu'
        TaskAppApp.build.kv.transition.direction = 'right'

    def back_to_menu_t(self, dt):
        global CLASS
        CLASS = None

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

    def remAttch(self, dt):
        self.attch = []
        self.ids.atth.text = f"Attachments uploaded: 0"


    def thread_notice(self):
        datepicker = MDDatePicker()
        datepicker.open()

        datepicker.bind(on_save=self.send_notice, on_cancel=self.send_notice_no_due)

    
    def send_notice(self, instance, value, date_range):
        t1 = Thread(target= Notice.sendNotice, args =(self,str(value)))
        t1.daemon = True
        t1.start()

        TaskAppApp.build.kv.current = 'loadnotice'
        TaskAppApp.build.kv.transition.direction = 'left'

    def send_notice_no_due(self, *args):
        t1 = Thread(target= Notice.sendNotice, args =(self,'No Due Date Specified'))
        t1.daemon = True
        t1.start()

        TaskAppApp.build.kv.current = 'loadnotice'
        TaskAppApp.build.kv.transition.direction = 'left'

    def sendNotice(self, duedate):
        #gathering details
        text = self.ids.textt.text
        try:
            images = Notice.attFiles.path
        except AttributeError:
            images = 'None'
        timee = datetime.today().strftime("%I:%M %p")
        datee = str(date.today())

        #connecting
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        s.connect((IP,2345))

        CODE = get_bytesize_string(codes[1],1024)
        s.send(bytes(CODE,'utf-8'))
        time.sleep(0.03)
        
        global CLASS

        CLASSS = get_bytesize_string(CLASS,1024)
        s.send(bytes(CLASSS,'utf-8'))
        
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

        if len(data) == 50:
            del data[0]

        notice = {"Teacher":details[0],"Subject":details[1],"Time":timee,"Date":datee,"DueDate":duedate,"Attachments":links,"Context":text}
        data.append(notice)

        #sending the json file back
        jsonObj = json.dumps(data)
        
        s.send(bytes(jsonObj,'utf-8'))

        #finishing up
        #notif_sender.send('NOT',text)
        Clock.schedule_once(self.remAttch, 1)
        Clock.schedule_once(self.back_to_menu_t, 1)

        CLASS = None
        

            

class LoadNotice(Screen):
    pass
        
class LoadHomework(Screen):
    pass     

class Homework(Screen):
    attch = []

    def back_to_menu(self):
        global CLASS
        CLASS = None

        TaskAppApp.build.kv.current = 'menu'
        TaskAppApp.build.kv.transition.direction = 'right'

    def back_to_menu_t(self, dt):
        global CLASS
        CLASS = None

        self.ids.textt.text = ''
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

    def remAttch(self, dt):
        self.attch = []
        self.ids.atth.text = f"Attachments uploaded: 0"


    def thread_homework(self):
        datepicker = MDDatePicker()
        datepicker.open()

        datepicker.bind(on_save=self.send_homework, on_cancel=self.send_homework_no_due)

    
    def send_homework(self, instance, value, date_range):
        t1 = Thread(target= Homework.sendHomework, args =(self,str(value)))
        t1.daemon = True
        t1.start()

        TaskAppApp.build.kv.current = 'loadhomework'
        TaskAppApp.build.kv.transition.direction = 'left'

    def send_homework_no_due(self, *args):
        t1 = Thread(target= Homework.sendHomework, args =(self,'No Due Date Specified'))
        t1.daemon = True
        t1.start()

        TaskAppApp.build.kv.current = 'loadhomework'
        TaskAppApp.build.kv.transition.direction = 'left'

    def sendHomework(self, duedate):
        #gathering details
        text = self.ids.textt.text
        try:
            images = Homework.attFiles.path
        except AttributeError:
            images = 'None'
        timee = datetime.today().strftime("%I:%M %p")
        datee = str(date.today())

        #connecting
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        s.connect((IP,2345))

        CODE = get_bytesize_string(codes[2],1024)
        s.send(bytes(CODE,'utf-8'))
        time.sleep(0.03)
        
        global CLASS

        CLASSS = get_bytesize_string(CLASS,1024)
        s.send(bytes(CLASSS,'utf-8'))
        
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

        if len(data) == 50:
            del data[0]

        homework = {"Teacher":details[0],"Subject":details[1],"Time":timee,"Date":datee,"DueDate":duedate,"Attachments":links,"Context":text}
        data.append(homework)

        #sending the json file back
        jsonObj = json.dumps(data)
        
        s.send(bytes(jsonObj,'utf-8'))

        #finishing up
        #notif_sender.send('HW',text)
        Clock.schedule_once(self.remAttch, 1)
        Clock.schedule_once(self.back_to_menu_t, 1)
        CLASS = None






class WindowManager(ScreenManager):
    pass



class TaskAppApp(MDApp):
    def __init__(self, **kwargs):
        self.title = "Task App - Teachers"
        super().__init__(**kwargs)

    def build(self):
        TaskAppApp.build.kv = Builder.load_string(kv)
        self.theme_cls.theme_style = "Dark"
        self.theme_cls.primary_palette = "Gray"
        return TaskAppApp.build.kv


if __name__ == '__main__':
    TaskAppApp().run()