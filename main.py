from kivy.app import App
from kivy.lang import Builder
from kivy.utils import platform
from kivy.clock import Clock
from jnius import autoclass
from oscpy.client import OSCClient
from oscpy.server import OSCThreadServer
from android_permissions import AndroidPermissions
if platform == 'android':
    from android import mActivity
    from jnius import autoclass

KV = '''
BoxLayout:
    orientation: 'vertical'
    BoxLayout:
        size_hint_y: None
        height: '40sp'
        Button:
            text: 'start tests'
            on_press: app.start_services()

    ScrollView:
        Label:
            id: label
            size_hint_y: None
            height: self.texture_size[1]
            text_size: self.size[0], None
            text: 'FIRST time there is a normal 10sec delay.'

    BoxLayout:
        size_hint_y: None
        height: '40sp'
        Label:
            id: date

'''

class StickyForeground(App):
    
    def build(self):
        self.root = Builder.load_string(KV)
        return self.root

    ##################
    # Start OSC
    ##################
    def on_start(self):
        self.first = 10
        if platform == 'android':
            server = OSCThreadServer()
            server.listen(
                address=b'localhost',
                port=3002,
                default=True,
            )
            server.bind(b'/date', self.display_date)
            self.root.ids.label.text += '\n'
        else:
            self.root.ids.label.text = '\n\nAndroid ONLY'
        self.dont_gc = AndroidPermissions(self.start_app)  

    def start_app(self):
        self.dont_gc = None            
            
    ##################
    # Start a service
    ##################

    def start_service_named(self, name, small_icon, title, text):
        context =  mActivity.getApplicationContext()
        service_name = str(context.getPackageName()) + '.Service' + name
        service = autoclass(service_name)
        # extended start api for testing, specify drawable resourse name here...
        if small_icon:
            service.start(mActivity, small_icon, title, text, '')
        else:
            # The legacy behavior
            service.start(mActivity, '')
        return service

    def step1(self):
        self.start_service_named('News', 'all_inclusive', 'Important News',
                                 'Suddenly, nothing happened.')
        self.root.ids.label.text += 'Mipmap Icon started\n'

    def step2(self, dt):
        self.start_service_named('News', '','','').stop(mActivity) 
        self.root.ids.label.text += 'Mipmap Icon stopped\n'
        self.start_service_named('Oldschool', '','','')
        self.root.ids.label.text += 'Legacy Icon started\n'

    def step3(self, dt):
        self.start_service_named('Oldschool', '','','').stop(mActivity) 
        self.root.ids.label.text += 'Legacy Icon stopped\n'
        self.start_service_named('Scotty', 'align_vertical_top',
                                 'ncc1701','Look out captain, \n' +\
                                 'its argggggg..')
        self.root.ids.label.text += 'Drawable Icon started\n'

    def step4(self, dt):
        self.start_service_named('Scotty', '','','').stop(mActivity) 
        self.root.ids.label.text += 'Drawable Icon stopped\n'
        self.root.ids.label.text += 'Test finished\n'
        self.first = 0

    ##################
    # Button events
    ##################

    def start_services(self):
        if platform == 'android':
            time = 30 + self.first
            self.root.ids.label.text += f'Watch the icon for {time} seconds,\nafterwards look at notification history.\n'
            self.step1()
            Clock.schedule_once(self.step2,10 + self.first)
            Clock.schedule_once(self.step3,20 + self.first)
            Clock.schedule_once(self.step4,30 + self.first)

            
    ###############
    # OSC events
    ###############
    
    def display_date(self, message):
        if self.root:
            self.root.ids.date.text = message.decode('utf8')


StickyForeground().run()
