from kivymd.app import MDApp
from kivy.lang import Builder
from kivy.properties import ObjectProperty

from kivymd.uix.textfield import MDTextField
from kivymd.uix.dialog import MDDialog
from kivy.uix.screenmanager import ScreenManager, Screen
from kivymd.uix.list import MDList, OneLineListItem, OneLineAvatarIconListItem
from kivymd.uix.button import MDFlatButton, MDIconButton




class Login_Screen(Screen):
    def verification(self):
        username = self.ids['un'].text
        password = self.ids['pw'].text

        self.manager.current = 'home'

class Home_Screen(Screen):

    def __init__(self, **kwargs):
        super(Home_Screen, self).__init__(**kwargs)
        self.amount = 0
        self.saved_names = []
        self.widgets = []
        self.textbox_code = '32-32-56-56-32-32'
        self.ch = 0
        with open('names of saved files.txt', 'r') as k:
            names = k.read().split('\n')
            names.remove('')
            self.saved_names = names

        for i in self.saved_names:
            self.amount +=1


        




            

        


    def on_pre_enter(self, *args):
        for names in self.saved_names:
            widget = OneLineListItem(text = names, on_release = lambda x, n=names:self.load_data(n))
            self.ids['nav_list'].add_widget(widget)

        for children in self.ids.HomeScreen.children:
            self.ch += 1

        self.ch = int(self.ch /2)









        

    def add_textbox(self):
        self.ch += 1

        n1 = 'tb'+str(self.ch)
        n2 = 'b'+str(self.ch)

        textbox = MDTextField(hint_text= 'Textbox',
                              mode = 'rectangle',
                              multiline = True,
                              size_hint_x= 0.89,
                              pos_hint= {'center_x': 0.5})

        
        
        deleteIcon = MDIconButton(icon = 'delete',
                                  on_release= lambda x, n=n1, v=n2: self.delete_widget(n, v) )

        self.ids[n1]= textbox
        self.ids[n2]= deleteIcon
        
        
        
        self.ids['HomeScreen'].add_widget(textbox)
        self.ids['HomeScreen'].add_widget(deleteIcon)

    def delete_widget(self, idsp, idsp2):
        
        for key, val in self.ids.items():
            if key == idsp:
                l = val
            if key == idsp2:
                l2 = val

        self.ids.HomeScreen.remove_widget(l)
        self.ids.HomeScreen.remove_widget(l2)
        















    def add_canvas(self):
        close_but = MDFlatButton(text = 'Ok',
                                 on_release = self.close_dialog )
        
        self.dialog_box = MDDialog(text = 'The Drawing Feature will come soon!!!',
                              buttons = [close_but])

        self.dialog_box.open()

    def close_dialog(self, obj):
        self.dialog_box.dismiss()















    def load_data(self, fname):

        with open(fname+'.txt', 'r') as f:
            temp = f.read()
            split = temp.split(self.textbox_code)
            self.ids['HomeScreen'].clear_widgets()
            split.pop()

        self.ch = 0
        for i in split:
            n1 = 'tb'+str(self.ch)
            n2 = 'b'+str(self.ch)

            textbox = MDTextField(hint_text = 'Textbox',
                                  text = i,
                                  mode = 'rectangle',
                                  multiline = True,
                                  size_hint_x= 0.89,
                                  pos_hint= {'center_x': 0.5})


            deleteIcon = MDIconButton(icon = 'delete',
                                      on_release= lambda x, n=n1, v=n2: self.delete_widget(n, v) )

            self.ids[n1]= textbox
            self.ids[n2]= deleteIcon



            self.ids['HomeScreen'].add_widget(textbox)
            self.ids['HomeScreen'].add_widget(deleteIcon)

            self.ch +=1

        self.ids['nav_drawer'].set_state('close')
        



    def save_notes(self):
        self.string = ''
        self.amount += 1

        for key,val in self.ids.items():
            if 'tb' in key:
                print(val.text)
                self.string += val.text + self.textbox_code

    

        with open('saved'+''+str(self.amount)+'.txt', 'w') as f:
            f.write(self.string)

            with open('names of saved files.txt', 'a') as k:
                file_name = 'saved'+ str(self.amount)
                k.write(file_name +'\n')
                widget = OneLineListItem(text = file_name, on_release = lambda x, n =file_name:self.load_data(n))
                self.ids['nav_list'].add_widget(widget)

        
        self.ids['HomeScreen'].clear_widgets()
        self.add_textbox()








    def navigation_drawer(self):
        self.ids['nav_drawer'].set_state('toggle')


        
        

class WindowManager(ScreenManager):
    pass


kv = '''
WindowManager:
    Login_Screen:
    Home_Screen:


<Login_Screen>:
    name: 'login'

    MDTextField:
        id: un
        hint_text: 'Enter Username'
        helper_text: 'or click on forgot username'
        helper_text_mode: 'on_focus'
        pos_hint: {'center_x': 0.5, 'center_y': 0.6}
        size_hint_x: 0.7


    MDTextField:
        id: pw
        hint_text: 'Enter Password'
        helper_text: 'or click on forgot password'
        helper_text_mode: 'on_focus'
        icon_right: 'android'
        icon_right_color: app.theme_cls.primary_color
        pos_hint: {'center_x': 0.5, 'center_y': 0.5}
        size_hint_x: 0.7
        password: True
        
        

    MDRectangleFlatButton:
        id: login_button
        text: 'Login'
        pos_hint: {'center_x': 0.5, 'center_y': 0.4}
        on_release: root.verification()

    

    
<Home_Screen>:
    name: 'home'

    MDNavigationLayout:
        ScreenManager:
            Screen:
            
                MDBoxLayout:
                    orientation: 'vertical'
                    padding: [0,0,0,4]

                
                    MDToolbar:
                        title: 'Notes'
                        height: '50sp'
                        elevation: 10
                        left_action_items: [['menu', lambda x: root.navigation_drawer()]]
                        right_action_items: [['form-textbox', lambda x: root.add_textbox()],  ['plus', lambda x: root.add_canvas()]]

                    AnchorLayout:
                        ScrollView:
                            size_hint_y: 0.95 # 5% spacing on each side

                            BoxLayout:
                                orientation: 'vertical'
                                size_hint_y: None
                                height: self.minimum_height
                        
                                id: HomeScreen
                            
                                MDTextField:
                                    hint_text: 'Textbox'
                                    hint_text_size: sp(15)
                                    id:tb1
                                    mode: 'rectangle'
                                    multiline: True
                                    size_hint_x: 0.89
                                    size_hint_y: None
                                    pos_hint: {'center_x': 0.5}

                                MDIconButton:
                                    id: b1
                                    icon: 'delete'
                                    on_release: root.delete_widget('tb1', 'b1')



                                
                                    

                                
                                    


                            
                    MDRectangleFlatButton:
                            
                        text: 'Save'
                        on_release: root.save_notes()
                        pos_hint: {'center_x':0.5, 'center_y': 0.9}

                    
                        

                    
    
                                
                                

                        

        MDNavigationDrawer:
            id: nav_drawer
            
            ScrollView:
                MDList:
                    id: nav_list
                    


'''


class NotesApp(MDApp):
    def build(self):
        self.theme_cls.primary_palette = 'Green'
        self.theme_cls.primary_hue = 'A700'
        self.theme_cls.accent_palette = 'Blue'
        self.theme_cls.theme_style = 'Dark'

        KV = Builder.load_string(kv)
        return KV



if __name__ == '__main__':
    NotesApp().run()
