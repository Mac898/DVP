import tkinter as tk
from tkinter import ttk
import pystray
from pystray import MenuItem as item
from PIL import Image, ImageTk
import discordsdk
from dynaconf import settings
import winreg, os, sys, websocket, requests, asyncio
import discordsdk.enum as denum
import discordsdk.model as dmodel
from queue import Queue
from threading import Thread

#ws worker setup
def wsworker(lws, recv_queue: Queue):
    while True:
        print("Attempting Receive")
        packet = lws.recv()
        recv_queue.put(str(packet))
        print("Received: "+str(packet))

#class setup
class DVP_FrontEnd():
    def __init__(self):
        #Initalization Variables
        self.appname = "B&B MC Voice"
        self.firstTimeSetup = True
        self.discordConnectionNeeded = True

        #initalize Window
        self.w = tk.Tk()
        self.w.title(self.appname)
        self.w.geometry("840x80")
        self.autostart = tk.BooleanVar(self.w, value=settings.get('autostart'))

        #build initial UI
        self.noteApplication = ttk.Label(self.w)
        self.noteApplication.configure(font='{Arial} 16 {bold}', padding='5', text='This application allows you to use discord as a voice solution on B&B MC servers!')
        self.noteApplication.grid(column='0', row='0')
        self.noteNextSteps = ttk.Label(self.w)
        self.noteNextSteps.configure(font='{Arial} 12 {}', text='Follow the instructions in-game to continue using this software.')
        self.noteNextSteps.grid(column='0', row='1')
        self.checkboxStartOnStartup = ttk.Checkbutton(self.w)
        self.checkboxStartOnStartup.configure(text='Start Automatically on Startup', variable=self.autostart, offvalue=False, onvalue=True, command=self.handleChangedAutostart)
        self.checkboxStartOnStartup.grid(column='0', row='2')

        #setup systray
        self.icoimg = Image.open("favicon.ico")
        self.sysmenu = (item('About', self.showSysItem), item('Exit', self.quitSysItem))
        self.ico = pystray.Icon("name", self.icoimg, self.appname, self.sysmenu)

        #discord setup
        self.dsdk = discordsdk.Discord(941243759759331338, discordsdk.CreateFlags.default)
        self.dusermanager = self.dsdk.get_user_manager()
        self.duser = None
        self.dusermanager.on_current_user_update = self.onCurrentUserManager
        self.dactivmanager = self.dsdk.get_activity_manager()
        self.dlobbymanager = self.dsdk.get_lobby_manager()
        self.dvoicemanager = self.dsdk.get_voice_manager()

        #activity manager callbacks
        self.dactivmanager.on_activity_invite = self.onActivityInvite
        self.dactivmanager.on_activity_join = self.onActivityJoin
        self.dactivmanager.on_activity_join_request = self.onActivityJoinRequest
        self.dactivmanager.on_activity_spectate = self.onActivitySpectate

    def onActivityInvite(self, aattype: denum.ActivityActionType, user: dmodel.User, activity: dmodel.Activity):
        self.dLatestActivityInviteType = aattype
        self.dLatestActivityInviteUser = user
        self.dLatestActivityInviteActivity = activity

    def onActivityJoin(self, joinSecret: str):
        self.dLatestActivityJoinStr = joinSecret

    def onActivityJoinRequest(self, user: dmodel.User):
        self.dLatestActivityJoinRequestUser = user

    def onActivitySpectate(self, spectateSecret: str):
        self.dLatestActivitySpectateStr = spectateSecret

    def firstSetup(self):
        #websocket setup
        self.ws = websocket.WebSocket()
        print("Connecting to WS")
        self.ws.connect(settings.get('server'))
        print("Connected to WS")
        self.publicIP = requests.get('https://api64.ipify.org').content.decode('utf8')
        self.ws.send(f"INIT;{self.publicIP};")

        #Setup recv thread
        self.sendqueue = Queue()
        self.recvthread = Thread(target = wsworker, args=(self.ws, self.sendqueue))
        self.recvthread.start()

    def handleChangedAutostart(self):
        if self.autostart.get() == True:
            if getattr(sys, 'frozen', False) and hasattr(sys, '_MEIPASS'):
                key = winreg.OpenKey(winreg.HKEY_CURRENT_USER, r'SOFTWARE\Microsoft\Windows\CurrentVersion\Run', 0, winreg.KEY_ALL_ACCESS)
                winreg.SetValueEx(key, 'speed', 0,winreg.REG_SZ, sys.executable)
            else:
                print("Not enabling autostart in non-installer bundle")
        else:
            if getattr(sys, 'frozen', False) and hasattr(sys, '_MEIPASS'):
                key = winreg.DeleteKey(winreg.HKEY_CURRENT_USER, r'SOFTWARE\Microsoft\Windows\CurrentVersion\Run', 0, winreg.KEY_ALL_ACCESS)
            else:
                print("Not disabling autostart in non-installer bundle")

    def quitSysItem(self, icon, item):
        settings.set('autostart', self.autostart.get())
        self.ws.close()
        self.w.destroy()
        self.ico.stop()

    def showSysItem(self, icon, item):
        self.w.deiconify()
        self.w.update()

    def hideWindow(self):
        self.w.withdraw()
        self.ico.run()

    def run(self):
        self.w.protocol('WM_DELETE_WINDOW', self.hideWindow)
        self.w.after(5000, self.worker)
        self.w.mainloop()

    def onCurrentUserManager(self):
        self.duser = self.dusermanager.get_current_user()

    def fullyConnectedWS(self, user, lws):
        lws.send(f"CONNECTED;{user.username}#{user.discriminator};")

    def runActions(self):
        if self.sendqueue.empty() == False:
            self.latestactionstr = self.sendqueue.get().split(";")
            print(f"ACTIONRECV: {self.latestactionstr}")
            if self.latestactionstr[0] == "SETACTIVITY":
                self.currentactivity = discordsdk.Activity()
                #self.currentactivity.application_id -- READONLY
                self.currentactivity.assets.large_image = self.latestactionstr[0]
                self.currentactivity.assets.large_text = self.latestactionstr[1]
                self.currentactivity.assets.small_image = self.latestactionstr[2]
                self.currentactivity.assets.small_text = self.latestactionstr[3]
                self.currentactivity.details = self.latestactionstr[4]
                self.currentactivity.instance = self.latestactionstr[5]
                #self.currentactivity.name -- READONLY
                self.currentactivity.party.id = self.latestactionstr[6]
                self.currentactivity.party.size = self.latestactionstr[7]
                self.currentactivity.secrets.join = self.latestactionstr[8]
                self.currentactivity.secrets.match = self.latestactionstr[9]
                self.currentactivity.secrets.spectate = self.latestactionstr[10]
                self.currentactivity.state = self.latestactionstr[11]
                self.currentactivity.timestamps.end = self.latestactionstr[12]
                self.currentactivity.timestamps.start = self.latestactionstr[13]
            elif self.latestactionstr[0] == "GETACTIVITY":
                try:
                    ca = self.currentactivity
                    self.ws.send(f"RESPONSEACTIVITY;{self.currentactivity.assets.large_image};{self.currentactivity.assets.large_text};{self.currentactivity.assets.small_image};{self.currentactivity.assets.small_text};{self.currentactivity.details};{self.currentactivity.instance};{self.currentactivity.party.id};{self.currentactivity.party.size};{self.currentactivity.secrets.join};{self.currentactivity.secrets.match};{self.currentactivity.secrets.spectate};{self.currentactivity.state};{self.currentactivity.timestamps.end}{self.currentactivity.timestamps.start}")
                except AttributeError:
                    self.ws.send(f"RESPONSEFAIL;CURRENT_ACTIVITY_UNKNOWN")
            elif self.latestactionstr[0] == "SETLOBBY":
                if self.latestactionstr[1] == "CREATELOBBY":
                    lmt = self.dlobbymanager.get_lobby_create_transaction()
                    lmt.set_capacity(self.latestactionstr[2])
                    lmt.set_locked(self.latestactionstr[3])
                    lmt.set_type(self.latestactionstr[4])
                    self.dlobbymanager.create_lobby(lmt, self.handleFinishedLobbyTransaction)
            elif self.latestactionstr[0] == "SETVOICE":
                if self.latestactionstr[1] == "SELFMUTE":
                    self.dvoicemanager.set_self_mute(self.latestactionstr[2])
                if self.latestactionstr[1] == "SELFDEAF":
                    self.dvoicemanager.set_self_deaf(self.latestactionstr[2])
                if self.latestactionstr[1] == "LOCALMUTE":
                    self.dvoicemanager.set_local_mute(self.latestactionstr[2], self.latestactionstr[3])
                if self.latestactionstr[1] == "LOCALVOLUME":
                    self.dvoicemanager.set_local_volume(self.latestactionstr[2], self.latestactionstr[3])
            elif self.latestactionstr[0] == "GETVOICE":
                if self.latestactionstr[1] == "SELFMUTE":
                    self.ws.send(f"RESPONSEVOICE;SELFMUTE;{self.dvoicemanager.is_self_mute()};")
                if self.latestactionstr[1] == "SELFDEAF":
                    self.ws.send(f"RESPONSEVOICE;SELFDEAF;{self.dvoicemanager.is_self_deaf()()};")
                if self.latestactionstr[1] == "LOCALMUTE":
                    self.ws.send(f"RESPONSEVOICE;LOCALMUTE;{self.dvoicemanager.is_local_mute(self.latestactionstr[2])};")
                if self.latestactionstr[1] == "LOCALVOLUME":
                    self.ws.send(f"RESPONSEVOICE;LOCALVOLUME;{self.dvoicemanager.get_local_volume(self.latestactionstr[2])};")

    def handleFinishedLobbyTransaction(self, result: denum.Result, lobby: dmodel.Lobby):
        self.ws.send(f"RESPONSELOBBYTRANSACTION;{str(result)};{lobby.id};{str(lobby.type)};{lobby.owner_id};{lobby.secret};{lobby.capacity};{lobby.locked}")

    def worker(self):
        self.dsdk.run_callbacks()
        if self.firstTimeSetup == True:
            self.firstSetup()
            self.firstTimeSetup = False
        if self.discordConnectionNeeded == True:
            try:
                username = self.duser.username
                self.fullyConnectedWS(self.duser, self.ws)
                self.discordConnectionNeeded = False
            except AttributeError:
                print("Awaiting discord data...")
        self.runActions()
        #run worker again
        self.w.after(100, self.worker)

if __name__ == '__main__':
    app = DVP_FrontEnd()
    app.run()