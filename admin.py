import json
from urllib.request import urlopen

from kivy.app import App
from kivy.properties import ObjectProperty
from kivy.uix.gridlayout import GridLayout


def loadmemes():
    data_Memes = urlopen('http://localhost:8080/getmeme').read()
    data_Memes = json.loads(data_Memes.decode('utf-8'))
    memes_list = []
    for i in range(len(data_Memes['memes'])):
        memes_list.append('{} - {}'.format(i, data_Memes['memes'][i]['title']))
    return data_Memes['memes'], memes_list


class AdminAppForm(GridLayout):
    memes, memes_list = loadmemes()
    memes_spr = ObjectProperty()
    detail_Memes_txt = ObjectProperty()
    i = -1

    def show_detail_Memes(self, text):
        if text != '':
            self.i = int(text.split('-')[0].strip())
            Memes = self.memes[self.i]
            self.detail_Memes_txt.text = '''
            - Title: {}
            - image ref: {}
            - Description: {}'''.format(Memes['title'], Memes['img_ref'], Memes['description'])

    def delete(self):
        data = urlopen('http://localhost:8080/deletememe?i=' + str(self.i))
        data = data.read().decode('utf-8')
        if data == 'OK':
            self.detail_Memes_txt.text = ''
            self.memes_spr.text = ''
            self.memes = loadmemes()


class AdminApp(App):
    title = 'admin app'


AdminApp().run()
