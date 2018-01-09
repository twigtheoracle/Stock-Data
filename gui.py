import wx

APP_EXIT = 1

class InitialFrame(wx.Frame):

    def __init__(self, *args, **kwargs):

        super(InitialFrame, self).__init__(*args, **kwargs)
        self.init_UI()

    def init_UI(self):

        menu = wx.MenuBar()
        file_menu = wx.Menu()

        quit_button = wx.MenuItem(file_menu, APP_EXIT, "&Quit\tCtrl+Q") #APP_EXIT is id?
        file_menu.Append(quit_button)

        self.Bind(wx.EVT_MENU, self.OnQuit, id = APP_EXIT)

        menu.Append(file_menu, "&File")

        self.SetMenuBar(menu)

        self.SetSize((200,200))
        self.SetTitle("test")
        self.Centre()
        self.Show(True)

    def OnQuit(self, e):
        self.Close()

def main():
    app = wx.App()
    InitialFrame(None)
    app.MainLoop()

if __name__ == '__main__':
    main()
