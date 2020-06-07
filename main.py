from kivy.app import App
from kivy.uix.gridlayout import GridLayout
from kivy.uix.floatlayout import FloatLayout
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.label import Label
from kivy.uix.textinput import TextInput
from kivy.uix.button import Button
from kivy.uix.popup import Popup
from functools import partial

def get_menu():
    import requests
    menu = "http://37.140.192.223/plesk-site-preview/vova.u0586459.plsk.regruhosting.ru/37.140.192.223/index.php"
    dishes = "http://37.140.192.223/plesk-site-preview/vova.u0586459.plsk.regruhosting.ru/37.140.192.223/Dishes.php"
    f = requests.get(menu)
    menu = eval(f.text)
    f = requests.get(dishes)
    dishes = eval(f.text)
    return menu, dishes


class MyGrid(GridLayout):
    def __init__(self, **kwargs):
        super(MyGrid, self).__init__(**kwargs)
        self.menu, self.dishes = get_menu()
        print(self.menu, self.dishes)
        self.cols = len(self.menu[0])
        self.dict_keys = list(self.menu[0].keys())
        for i in range(len(self.menu)):
            self.add_widget(Label(text=self.menu[i]["Day"]))
            for key in list(self.menu[i].keys())[1:]:
                dish = self.dishes[int(self.menu[i][key])]
                self.add_widget(Button(text=dish["Name"], on_press=partial(self.callback, dish)))

    def callback(self, info, instance):
        info = "Грамм: " + info["Gramm"] + "\nКаллории: " + info["Cal"] + "\nБелки: " + info["Protein"] + "\nЖиры: " + info["Fat"]
        content = BoxLayout(orientation='vertical')
        content.add_widget(Label(text=info, size_hint=(0.6,0.5)))
        button_exit = Button(text="Close", size_hint=(1, 0.15))
        button_exit.bind(on_press = lambda *args: popup.dismiss())
        content.add_widget(button_exit)
        popup = Popup(
            title=instance.text,
            content=content,
            size_hint=(0.3,0.3),
            pos_hint={"top":0.65, "right":0.65}
        )
        popup.open()


class MyApp(App):
    def build(self):
        return MyGrid()


if __name__ == '__main__':
    MyApp().run()
