from kivy.uix.floatlayout import FloatLayout
from kivy.uix.image import Image
from kivymd.app import MDApp
from kivy.lang import Builder
from kivy.uix.screenmanager import ScreenManager, Screen
from kivy.properties import ObjectProperty
from kivy.core.window import Window
from kivymd.uix.button import MDFlatButton
from kivymd.uix.datatables import MDDataTable
from kivy.metrics import dp
from kivymd.uix.dialog import MDDialog
import socket, pickle

# SOCKET SETUP

# CONSTANTS
BUFFER = 1024
ADDR = '127.0.0.1'
PORT = 9090

client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
client.connect((ADDR, PORT))

screen_helper = '''
ScreenManager:
    LoginScreen:
    MenuScreen:
    RegisterScreen:
    SendScreen:
    HistoryScreen:
    
<RegisterScreen>:
    name: 'register'
    
    register: register
    firstname: firstname
    lastname: lastname
    r_username: r_username
    r_password: r_password
    email: email
    phone: phone
    
    Image:
        source: 'assets/backgroundLight.jpeg'
    
    GridLayout:
        pos_hint: {'center_x': 0.5, 'center_y': 0.5}
        size_hint: 0.4,0.9
        canvas:
            Color:
                rgba: (1,1,1,0.9)
            
            Rectangle:
                pos: self.pos
                size: self.size
        
    MDLabel:
        id: register
        text: 'Register'
        font_style: 'H2'
        halign: 'center'
        pos_hint: {'center_y': 0.82}
        color: 0,0,0,0.5
    
    MDTextField:
        id: firstname
        hint_text: 'First Name'
        pos_hint: {'center_x': 0.4, 'center_y': 0.65}
        size_hint_x: None
        width: 200
    
    MDTextField:
        id: lastname
        hint_text: 'Last Name'
        pos_hint: {'center_x': 0.6, 'center_y': 0.65}
        size_hint_x: None
        width: 200
        
    MDTextField:
        id: r_username
        hint_text: 'Username'
        pos_hint: {'center_x': 0.4, 'center_y': 0.5}
        size_hint_x: None
        width: 200
    
    MDTextField:
        id: r_password
        hint_text: 'Password'
        pos_hint: {'center_x': 0.6, 'center_y': 0.5}
        size_hint_x: None
        width: 200
        
    MDTextField:
        id: email
        hint_text: 'Email id'
        pos_hint: {'center_x': 0.4, 'center_y': 0.35}
        size_hint_x: None
        width: 200
    
    MDTextField:
        id: phone
        hint_text: 'Contact no.'
        pos_hint: {'center_x': 0.6, 'center_y': 0.35}
        size_hint_x: None
        width: 200
        
    MDRaisedButton:
        text: 'Next'
        pos_hint: {'center_x': 0.6, 'center_y': 0.2}
        on_release:
            root.manager.current = 'login'
            root.retData(None)

    MDRaisedButton:
        text: 'Back'
        pos_hint: {'center_x': 0.4, 'center_y': 0.2}
        on_release: 
            root.manager.current = 'login'


<LoginScreen>:
    name: 'login'

    username: username
    password: password

    Image:
        source: 'assets/backgroundLight.jpeg'
        
        canvas:
            Color:
                rgba:(1,1,1,0.7)
                
            Rectangle:
                pos: 500,200
                size: 275,400
    
    MDLabel:
        text: 'Login'
        font_style: 'H2'
        font_size: 50
        theme_text_color: 'Secondary'
        halign: 'center'
        pos_hint: {'center_y': 0.73}        

    MDTextField:
        id: username
        hint_text: 'Username'
        icon_right: "bitcoin"
        icon_right_color: app.theme_cls.primary_color
        pos_hint: {'center_x': 0.5, 'center_y': 0.6}
        size_hint_x: None
        width: 250
        
    MDTextField:
        id: password
        hint_text: 'Password'
        helper_text: 'forgot password?'
        helper_text_mode: 'on_focus'
        icon_right: "bitcoin"
        icon_right_color: app.theme_cls.primary_color
        pos_hint: {'center_x': 0.5, 'center_y': 0.5}
        size_hint_x: None
        width: 250
        
    MDRectangleFlatButton:
        text: 'Login'
        pos_hint: {'center_x': 0.565, 'center_y': 0.4}
        size_hint_x: None
        width: 250
        on_release:
            root.show_data(None)
            root.manager.current = 'menu'
            
    MDFlatButton:
        text: 'Register'
        theme_text_color: 'Hint'
        pos_hint: {'center_x': 0.43, 'center_y': 0.4}
        size_hint_x: None
        width: 250
        on_release:
            root.manager.current = 'register'

<MenuScreen>:
    name: 'menu'
    
    menuName: menuName
    menuBalance: menuBalance

    Image:
        source: 'assets/backgroundDark.jpeg'        
        
    GridLayout:
        canvas:
            Color:
                rgba:(0,0,0,0.4)

            Rectangle:
                pos: self.pos
                size: self.size
            
        
    GridLayout:
        size_hint: 0.4, 0.6
        pos_hint: {'center_x': 0.65, 'center_y': 0.5}
        spacing: 20
        padding_x: 0.8
        cols: 2
                
        MDRectangleFlatButton:
            text: 'Profile'
            size_hint: 0.4,0.1
            font_size: 25
        MDRectangleFlatButton:
            text: 'Transaction History'
            size_hint: 0.4,0.1
            font_size: 25
        MDRectangleFlatButton:
            text: 'Send Money'
            size_hint: 0.4,0.1
            font_size: 25
            on_release:
                root.manager.current = 'send'
                
        MDRectangleFlatButton:
            text: 'Received Money'
            size_hint: 0.4,0.1
            font_size: 25
    
    FloatLayout:
        orientation: 'tb-lr'
        size_hint: 0.3,1
        pos_hint: {'top': 1, 'left': 0}
        canvas:
            Color:
                rgba:(1,1,1,0.7)

            Rectangle:
                pos: self.pos
                size: self.size
        
        Image:
            source: 'assets/profileIcon2.png'
            pos_hint: {'center_x': 0.5, 'center_y': 0.7}
            size_hint: 0.7,0.7
            
        MDLabel:
            text: 'Welcome back,'
            font_style: 'H4'
            theme_text_color: 'Secondary'
            halign: 'center'
            pos_hint: {'center_y': 0.43}
            
        MDLabel:
            id: menuName
            text: '_'
            font_style: 'H2'
            font_size: 50
            halign: 'center'
            pos_hint: {'center_y': 0.36}
                        
    GridLayout:
        size_hint: 0.7,0.1
        pos_hint: {'right': 1, 'center_y': 1}
        canvas:
            Color:
                rgba:(1,1,1,0.7)

            Rectangle:
                pos: self.pos
                size: self.size
    
    Label:
        text: 'Balance: '
        pos_hint: {'center_y': 0.968, 'center_x': 0.04}
        color: 0,0,0,0.6
        
    Label:
        id: menuBalance
        text: '0000'
        pos_hint: {'center_y': 0.968, 'center_x': 0.1}
        color: 0,0,0,0.6

    MDIconButton:
        icon: 'cog'
        pos_hint: {'center_y': 0.975, 'right': 1}
        on_release:
            root.get_data(None)

    MDIconButton:
        icon: 'account-off'
        pos_hint: {'center_y': 0.975, 'right': 0.97}
        on_release:
            root.manager.current = 'login'

            
<SendScreen>:
    name: 'send'
    
    sendBalance: sendBalance
    sendUsername: sendUsername
    recvUsername: recvUsername
    amt: amt
    password: password
    
    Image:
        source: 'assets/backgroundDark.jpeg'

        canvas:
            Color:
                rgba:(1,1,1,0.7)

            Rectangle:
                pos: 500,200
                size: 275,400

    GridLayout:
        size_hint: 1,0.1
        pos_hint: {'left': 0, 'center_y': 1}
        canvas:
            Color:
                rgba:(1,1,1,0.7)

            Rectangle:
                pos: self.pos
                size: self.size
    
    FloatLayout:
        size: self.size        
        MDIconButton:
            icon: 'arrow-left'
            pos_hint: {'center_y': 0.975, 'left': 0}
            on_release:
                root.manager.current = 'menu'
            
        Label:
            id: sendUsername
            text: ' '
            pos_hint: {'center_y': 0.975, 'center_x': 0.75}
            color: 0,0,0,0.6
            
        Label:
            id: sendBalance
            text: '0000'
            pos_hint: {'center_y': 0.975, 'center_x': 0.94}
            color: 0,0,0,0.6
                        
        MDLabel:
            text: 'Send Money'
            font_style: 'H2'
            font_size: 45
            theme_text_color: 'Secondary'
            halign: 'center'
            pos_hint: {'center_y': 0.75}        
            
        MDTextField:
            id: recvUsername
            hint_text: "Recipient's Username"
            pos_hint: {'center_x': 0.5, 'center_y': 0.65}
            size_hint_x: None
            width: 230
    
        MDTextField:
            id: amt
            hint_text: 'Amount'
            pos_hint: {'center_x': 0.5, 'center_y': 0.55}
            size_hint_x: None
            width: 230
                
        MDTextField:
            id: password
            hint_text: 'Password'
            pos_hint: {'center_x': 0.5, 'center_y': 0.45}
            size_hint_x: None
            width: 230
            
        MDRectangleFlatButton:
            text: 'Send'
            pos_hint: {'center_x': 0.56, 'center_y': 0.35}
            size_hint_x: None
            width: 250
            on_release:
                root.sendBtn()
                
<HistoryScreen>:
    name: 'history'
'''

Window.size = (1280, 720)


class LoginScreen(Screen):
    username = ObjectProperty(None)
    password = ObjectProperty(None)

    def on_leave(self, *args):
        self.username.text = ''
        self.password.text = ''

    def show_data(self, obj):
        self.user = self.username.text
        client.send(pickle.dumps(['login', self.username.text, self.password.text]))
        data = pickle.loads(client.recv(1024))
        if data == 'An Error occurred!':
            print(data)
            self.manager.current = 'login'

            self.dialog = MDDialog(text='Invalid Credentials!',
                                   buttons=[
                                       MDFlatButton(text='Okay', on_release=self.close_dialog)
                                   ])
            self.dialog.open()

        else:
            self.manager.get_screen('menu').get_data(data[0])
            self.manager.current = 'menu'

    def close_dialog(self, obj):
        self.dialog.dismiss()

    def show_password(self, obj):
        self.password.password = False

    def hide_password(self, obj):
        self.password.password = True


class MenuScreen(Screen):
    menuName = ObjectProperty(None)
    menuBalance = ObjectProperty(None)
    sendUsername = ObjectProperty(None)

    def get_data(self, data):
        self.firstname, self.balance = data
        self.menuName.text = self.firstname
        self.menuBalance.text = str(self.balance)

        self.sendUsername.text = f'User:  {self.manager.get_screen("login").user}'

    def logout(self, obj):
        self.manager.current = 'login'
        client.send(pickle.dumps(['announce', f'User: {self.manager.get_screen("login").user} is offline']))

    def change_screen_size(self):
        Window.size = (515, 720)


class RegisterScreen(Screen):
    firstname = ObjectProperty(None)
    lastname = ObjectProperty(None)
    r_username = ObjectProperty(None)
    r_password = ObjectProperty(None)
    email = ObjectProperty(None)
    phone = ObjectProperty(None)
    register = ObjectProperty(None)

    def on_leave(self, *args):
        self.firstname.text = ''
        self.lastname.text = ''
        self.r_username.text = ''
        self.r_password.text = ''
        self.email.text = ''
        self.phone.text = ''

    def retData(self, obj):
        print(self.r_username.text,
              self.r_password.text,
              self.firstname.text,
              self.lastname.text,
              self.email.text,
              self.phone.text,
              self.register.text, sep='\n')

        client.send(pickle.dumps(['register', self.r_username.text, self.r_password.text,
                                  self.firstname.text, self.lastname.text,
                                  self.email.text, int(self.phone.text)]))

        msg = client.recv(1024)
        if msg == b'v/':
            self.dialog = MDDialog(text='Thank you for registering!',
                                   buttons=[
                                       MDFlatButton(text='Okay', on_release=self.close_dialog)
                                   ])
            self.dialog.open()
            self.manager.current = 'login'

        elif msg == b'x/':
            self.dialog = MDDialog(text='Username has already been taken!',
                                   buttons=[
                                       MDFlatButton(text='Okay', on_release=self.close_dialog)
                                   ])
            self.dialog.open()

    def close_dialog(self, obj):
        self.dialog.dismiss()


class SendScreen(Screen):
    sendBalance = ObjectProperty(None)
    sendUsername = ObjectProperty(None)
    recvUsername = ObjectProperty(None)
    amt = ObjectProperty(None)
    password = ObjectProperty(None)

    def on_leave(self, *args):
        self.recvUsername.text = ''
        self.amt.text = ''
        self.password.text = ''

    def on_enter(self, *args):
        self.sendBalance.text = f"Balance:  {str(self.manager.get_screen('menu').balance)}"
        self.sendUsername.text = f'User:  {self.manager.get_screen("login").user}'

    def sendBtn(self, obj=None):
        client.send(pickle.dumps(
            ['transfer', self.sendUsername.text[7:], self.recvUsername.text, self.amt.text, self.password.text]))

        recvData = pickle.loads(client.recv(1024))

        self.dialog = MDDialog(text=recvData[0],
                               buttons=[
                                   MDFlatButton(text='Okay', on_release=self.close_dialog)
                               ])
        self.dialog.open()

        data = [self.manager.get_screen('menu').firstname,
                str(float(self.manager.get_screen('menu').menuBalance.text) - int(recvData[1]))]

        self.manager.get_screen('menu').get_data(data)

    def close_dialog(self, obj):
        self.dialog.dismiss()


class HistoryScreen(Screen, MDApp):
    sendUsername = ObjectProperty(None)

    def __init__(self, **kwargs):
        super(HistoryScreen, self).__init__(**kwargs)

        layout = FloatLayout()

        layout.add_widget(Image(source='assets/backgroundLight.jpeg'))

        self.data_tables = MDDataTable(pos_hint={'center_x': 0.5, 'center_y': 0.5},
                                       size_hint=(0.75, 0.6),
                                       rows_num=50,
                                       column_data=[
                                           ('TR ID', dp(30)),
                                           ('Sender', dp(30)),
                                           ('Recepient', dp(30)),
                                           ('Bank Name', dp(30)),
                                           ('Amount', dp(30)),
                                           ('Date/Time', dp(30))
                                       ],
                                       row_data=[
                                           ('Loading...', '________', '________', '________', '________',
                                            '________')
                                       ])

        layout.add_widget(self.data_tables)

        self.add_widget(layout)

    def on_enter(self, *args):
        self.sendUsername.text = f'User:  {self.manager.get_screen("login").user}'

        client.send(pickle.dumps(['transactions', self.manager.get_screen("login").user]))

        data = pickle.loads(client.recv(1024))
        print(data)

        if data == []:
            self.data_tables.row_data.append(('_', '________', '________', '________', '________', '________'))
            return

        for row in range(len(data)):
            data[row] = list(data[row])
            data[row][-1] = str(data[row][-1])
            data[row] = tuple(data[row])
            data[row] = data[row]

        self.data_tables.row_data = data
        self.data_tables.row_data.append(('_', '________', '________', '________', '________', '________'))
        self.data_tables.rows_num = len(data)

    def on_leave(self, *args):
        self.data_tables.row_data = [('_', '________', '________', '________', '________', '________')]


class ProfileScreen(Screen):
    firstname = ObjectProperty(None)
    lastname = ObjectProperty(None)
    username = ObjectProperty(None)
    email = ObjectProperty(None)

    def change_screen_size(self):
        Window.size = (1280, 720)

    def on_enter(self, *args):
        client.send(pickle.dumps(['completeInfo', self.manager.get_screen("login").user]))
        data = pickle.loads(client.recv(1024))

        self.firstname.text, self.lastname.text, self.username.text, self.email.text = data


sm = ScreenManager()
sm.add_widget(LoginScreen(name='login'))
sm.add_widget(RegisterScreen(name='register'))
sm.add_widget(MenuScreen(name='menu'))
sm.add_widget(SendScreen(name='send'))
sm.add_widget(HistoryScreen(name='history'))
sm.add_widget(HistoryScreen(name='profile'))


class DemoApp(MDApp):
    theme = ObjectProperty(None)

    def build(self):
        self.theme_cls.primary_palette = 'Pink'
        self.theme_cls.accent_palette = 'BlueGray'
        self.theme_cls.theme_style = 'Light'
        screen = Builder.load_file('DBMS.kv')
        return screen


DemoApp().run()
