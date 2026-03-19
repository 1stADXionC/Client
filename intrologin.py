import dbg
import app
import net
import ui
import ime
import snd
import wndMgr
import musicInfo
import serverInfo
import systemSetting
import ServerStateChecker
import localeInfo
import uiCommon
import time
import ServerCommandParser
import ime
import uiScriptLocale
import chat
import sys
import background
import os
import constInfo
import configparser
app.loggined = False
account_parser = configparser.ConfigParser()
STATE_DICT = {
	0:localeInfo.CHANNEL_STATUS_OFF,
	1:localeInfo.CHANNEL_STATUS_NORMAL,
	2:localeInfo.CHANNEL_STATUS_BUSY,
	3:localeInfo.CHANNEL_STATUS_FULL
}

class ConnectingDialog(ui.ScriptWindow):

	def __init__(self):
		ui.ScriptWindow.__init__(self)
		self.__LoadDialog()
		self.eventTimeOver = lambda *arg: None
		self.eventExit = lambda *arg: None

	def __del__(self):
		ui.ScriptWindow.__del__(self)

	def __LoadDialog(self):
		try:
			PythonScriptLoader = ui.PythonScriptLoader()
			PythonScriptLoader.LoadScriptFile(self, "UIScript/ConnectingDialog.py")
			self.board = self.GetChild("board")
			self.message = self.GetChild("message")
			self.countdownMessage = self.GetChild("countdown_message")
		except:
			import exception
			exception.Abort("ConnectingDialog.LoadDialog.BindObject")

	def Open(self, waitTime):
		self.Lock()
		self.SetCenterPosition()
		self.SetTop()
		self.Show()

	def Close(self):
		self.Unlock()
		self.Hide()

	def Destroy(self):
		self.Hide()
		self.ClearDictionary()

	def SetText(self, text):
		self.message.SetText(text)

	def OnPressExitKey(self):
		return True


class LoginWindow(ui.ScriptWindow):

	def __init__(self, stream):
		print "NEW LOGIN WINDOW  ----------------------------------------------------------------------------"
		ui.ScriptWindow.__init__(self)
		net.SetPhaseWindow(net.PHASE_WINDOW_LOGIN, self)
		net.SetAccountConnectorHandler(self)
		self.isDeletingAccount = False
		self.backgroundImage = 0
		self.inputDialog = None
		self.connectingDialog = None
		self.GuardInput = None
		self.stream = stream
		self.channelButtonList = []

	def __del__(self):
		net.ClearPhaseWindow(net.PHASE_WINDOW_LOGIN, self)
		net.SetAccountConnectorHandler(0)
		ui.ScriptWindow.__del__(self)
		print "---------------------------------------------------------------------------- DELETE LOGIN WINDOW"

	def Open(self):
		ServerStateChecker.Create(self)
		ServerStateChecker.Initialize()
		server = serverInfo.SERVER1
		ServerStateChecker.AddChannel(1, server["host"], server["ch1"])
		ServerStateChecker.AddChannel(2, server["host"], server["ch2"])
		ServerStateChecker.AddChannel(3, server["host"], server["ch3"])
		ServerStateChecker.AddChannel(4, server["host"], server["ch4"])
		ServerStateChecker.Request()
		print "LOGIN WINDOW OPEN ----------------------------------------------------------------------------"
		self.loginFailureMsgDict={
			"ALREADY"	: localeInfo.LOGIN_FAILURE_ALREAY,
			"NOID"		: localeInfo.LOGIN_FAILURE_NOT_EXIST_ID,
			"WRONGPWD"	: localeInfo.LOGIN_FAILURE_WRONG_PASSWORD,
			"FULL"		: localeInfo.LOGIN_FAILURE_TOO_MANY_USER,
			"SHUTDOWN"	: localeInfo.LOGIN_FAILURE_SHUTDOWN,
			"REPAIR"	: localeInfo.LOGIN_FAILURE_REPAIR_ID,
			"BLOCK"		: localeInfo.LOGIN_FAILURE_BLOCK_ID,
			"BESAMEKEY"	: localeInfo.LOGIN_FAILURE_BE_SAME_KEY,
			"NOTAVAIL"	: localeInfo.LOGIN_FAILURE_NOT_AVAIL,
			"NOBILL"	: localeInfo.LOGIN_FAILURE_NOBILL,
			"BLKLOGIN"	: localeInfo.LOGIN_FAILURE_BLOCK_LOGIN,
			"WEBBLK"	: localeInfo.LOGIN_FAILURE_WEB_BLOCK,
			"BADSCLID"	: localeInfo.LOGIN_FAILURE_WRONG_SOCIALID,
			"AGELIMIT"	: localeInfo.LOGIN_FAILURE_SHUTDOWN_TIME,
			"IPBAN"		: localeInfo.LOGIN_FAILURE_IP_BLOCK,
			"BAKIMVAR"	: localeInfo.LOGIN_FAILURE_DISABLE,
			"NOCLIENT"	: localeInfo.LOGIN_FAILURE_CLIENT_VERSION,
			"NOPIN"		: localeInfo.LOGIN_FAILURE_PIN,
			"NOSERVER"		: localeInfo.LOGIN_FAILURE_SERVER,
			##"BAN_IP"	: localeInfo.LOGIN_FAILURE_MACBAN,
			##"MACBAN"	: localeInfo.LOGIN_FAILURE_MACBAN,
			##"GUVENLIPC"	: localeInfo.LOGIN_FAILURE_GUVENLIPC,
			##"GUVENLIP"	: localeInfo.LOGIN_FAILURE_GUVENLIPC,
		}
	
		self.loginFailureFuncDict = {
			"QUIT"		: app.Exit,
		}
		self.SetSize(wndMgr.GetScreenWidth(), wndMgr.GetScreenHeight())
		self.SetWindowName("LoginWindow")
		if not self.__LoadScript("UIScript/LoginWindow.py"):
			dbg.TraceError("LoginWindow.Open - __LoadScript Error")
			return
		if app.loggined:
			self.loginFailureFuncDict = {
				"QUIT"		: app.Exit,
			}
		if musicInfo.loginMusic != "":
			snd.SetMusicVolume(systemSetting.GetMusicVolume())
			snd.FadeInMusic("BGM/" + musicInfo.loginMusic)
		snd.SetSoundVolume(systemSetting.GetSoundVolume())
		ime.AddExceptKey(91)
		ime.AddExceptKey(93)
		self.Show()
		connectingIP = self.stream.GetConnectAddr()
		if connectingIP:
			self.__OpenConnectBoard()
		app.ShowCursor()
		self.SetIDEditLineFocus()
		self.__SetChannel(1)
		constInfo.open_security = 0

	def Close(self):
		if self.connectingDialog:
			self.connectingDialog.Close()
		self.connectingDialog = None
		ServerStateChecker.Initialize(self)
		print "---------------------------------------------------------------------------- CLOSE LOGIN WINDOW "
		if musicInfo.loginMusic != "" and musicInfo.selectMusic != "":
			snd.FadeOutMusic("BGM/" + musicInfo.loginMusic)
		self.idEditLine.SetTabEvent(0)
		self.idEditLine.SetReturnEvent(0)
		self.pwdEditLine.SetReturnEvent(0)
		self.pwdEditLine.SetTabEvent(0)
		self.pinEditLine.SetReturnEvent(0)
		self.pinEditLine.SetTabEvent(0)
		
		self.connectBoard = None
		self.idEditLine = None
		self.pwdEditLine = None
		self.pinEditLine = None
		self.inputDialog = None
		self.connectingDialog = None
		self.GuardInput = None
		self.KillFocus()
		self.Hide()
		self.isDeletingAccount = False
		self.backgroundImage = 0
		self.stream.popupWindow.Close()
		self.loginFailureFuncDict = None
		ime.ClearExceptKey()
		app.HideCursor()

	def __ExitGame(self):
		app.Exit()

	def SetIDEditLineFocus(self):
		if self.idEditLine != None:
			self.idEditLine.SetFocus()

	def SetPasswordEditLineFocus(self):
		if self.idEditLine != None:
			self.idEditLine.SetText("")
			self.idEditLine.SetFocus()
			
		if self.pwdEditLine != None:
			self.pwdEditLine.SetText("")
			
		if self.pinEditLine != None:
			self.pinEditLine.SetText("")
			
	def SetPinEditLineFocus(self):
		if self.pinEditLine != None:
			self.pinEditLine.SetFocus()


	def OnConnectFailure(self):
		snd.PlaySound("sound/ui/loginfail.wav")
		if self.connectingDialog:
			self.connectingDialog.Close()
		self.connectingDialog = None
		if app.loggined:
			self.PopupNotifyMessage(localeInfo.LOGIN_CONNECT_FAILURE, self.__ExitGame)
		else:
			self.PopupNotifyMessage(localeInfo.LOGIN_CONNECT_FAILURE, self.SetPasswordEditLineFocus)

	def OnHandShake(self):
		snd.PlaySound("sound/ui/loginok.wav")
		self.PopupDisplayMessage(localeInfo.LOGIN_CONNECT_SUCCESS)

	def OnLoginStart(self):
		self.PopupDisplayMessage(localeInfo.LOGIN_PROCESSING)

	def OnLoginFailure(self, error):
		if self.connectingDialog:
			self.connectingDialog.Close()
		self.connectingDialog = None
		try:
			loginFailureMsg = self.loginFailureMsgDict[error]
		except KeyError:
			loginFailureMsg = localeInfo.LOGIN_FAILURE_UNKNOWN + error

		loginFailureFunc = self.loginFailureFuncDict.get(error, self.SetPasswordEditLineFocus)
		if app.loggined:
			self.PopupNotifyMessage(loginFailureMsg, self.__ExitGame)
		else:
			self.PopupNotifyMessage(loginFailureMsg, loginFailureFunc)
		snd.PlaySound("sound/ui/loginfail.wav")

	def __DisconnectAndInputID(self):
		if self.connectingDialog:
			self.connectingDialog.Close()
		self.connectingDialog = None
		self.SetIDEditLineFocus()
		net.Disconnect()

	def __DisconnectAndInputPassword(self):
		if self.connectingDialog:
			self.connectingDialog.Close()
		self.connectingDialog = None
		self.SetPasswordEditLineFocus()
		net.Disconnect()

	def SAFE_SetEvent(self, func, *args):
		self.eventFunc = __mem_func__(func)
		self.eventArgs = args

	def __LoadScript(self, fileName):
		try:
			pyScrLoader = ui.PythonScriptLoader()
			pyScrLoader.LoadScriptFile(self, fileName)
		except:
			import exception
			exception.Abort("LoginWindow.__LoadScript.LoadObject")

		try:
			GetObject = self.GetChild
			self.backgroundImage = GetObject("BackGround")
			self.connectBoard = GetObject("ConnectBoard")
			self.idEditLine = GetObject("ID_EditLine")
			self.pwdEditLine = GetObject("Password_EditLine")
			self.pinEditLine = GetObject("Pin_EditLine")

			self.channelButtonList = []
			self.channelButtonList.append(GetObject("Channel1Button"))
			self.channelButtonList.append(GetObject("Channel2Button"))
			self.channelButtonList.append(GetObject("Channel3Button"))
			self.channelButtonList.append(GetObject("Channel4Button"))

			self.loginButton = GetObject("LoginButton")
			self.loginExitButton = GetObject("LoginExitButton")
		except:
			import exception
			exception.Abort("LoginWindow.__LoadScript.BindObject")

		imgFileNameDict = {
			0: "locale/ro/ui/login/1.sub",
		}
		try:
			imgFileName = imgFileNameDict[app.GetRandom(0, len(imgFileNameDict) - 1)]
			self.backgroundImage.LoadImage(imgFileName)
		except:
			print "LoadingWindow.Open.LoadImage - %s File Load Error" % imgFileName
			self.backgroundImage.Hide()

		width = float(wndMgr.GetScreenWidth()) / float(self.backgroundImage.GetWidth())
		height = float(wndMgr.GetScreenHeight()) / float(self.backgroundImage.GetHeight())
		self.backgroundImage.SetScale(width, height)
		self.loginButton.SetEvent(ui.__mem_func__(self.__OnClickLoginButton))
		self.loginExitButton.SetEvent(ui.__mem_func__(self.__OnClickExitButton))
		self.idEditLine.SetReturnEvent(ui.__mem_func__(self.pwdEditLine.SetFocus))
		self.idEditLine.SetTabEvent(ui.__mem_func__(self.pwdEditLine.SetFocus))
		self.pwdEditLine.SetReturnEvent(ui.__mem_func__(self.__OnClickLoginButton))
		self.pwdEditLine.SetTabEvent(ui.__mem_func__(self.pinEditLine.SetFocus))
		
		self.pinEditLine.SetReturnEvent(ui.__mem_func__(self.__OnClickLoginButton))
		self.pinEditLine.SetTabEvent(ui.__mem_func__(self.idEditLine.SetFocus))

		self.channelButtonList[0].SAFE_SetEvent(self.__SetChannel, 1)
		self.channelButtonList[1].SAFE_SetEvent(self.__SetChannel, 2)
		self.channelButtonList[2].SAFE_SetEvent(self.__SetChannel, 3)
		self.channelButtonList[3].SAFE_SetEvent(self.__SetChannel, 4)

		return 1

	def __ClickRadioButton(self, buttonList, buttonIndex):
		try:
			selButton = buttonList[buttonIndex]
		except IndexError:
			return

		for eachButton in buttonList:
			eachButton.SetUp()

		selButton.Down()

	def __SetChannel(self, index):
		server = serverInfo.SERVER1

		ch_key = "ch" + str(index)
		if ch_key not in server:
			ch_key = "ch4"  

		self.stream.SetConnectInfo(server["host"], server[ch_key], server["host"], server["auth"])

		button_index = min(index - 1, len(self.channelButtonList) - 1)
		self.__ClickRadioButton(self.channelButtonList, button_index)

		self.__SetServerInfo("%s - %s " % (server.get("name", "Server"), server[ch_key]))

		net.SetMarkServer(server["host"], server.get("MARKADDR", ""))
		app.SetGuildMarkPath("10.tga")
		app.SetGuildSymbolPath("10")

	def Connect(self, id, pwd, cv, pin):
		net.ACC_ID = id
		net.ACC_PWD = pwd
		net.ACC_PIN = pin
		if constInfo.SEQUENCE_PACKET_ENABLE:
			net.SetPacketSequenceMode()
		self.stream.popupWindow.Close()
		self.stream.popupWindow.Open(localeInfo.LOGIN_CONNETING, self.OnProcessingCancel, localeInfo.UI_CANCEL)
		self.stream.SetLoginInfo(id, pwd, cv, pin)
		self.stream.Connect()

	def OnProcessingCancel(self):
		self.isLoginCanceled = True
		self.stream.popupWindow.Close()

	def RemoveAccountSlotFromSection(self, n):
		with open("accounts.ini", "r") as f:
			account_parser.read(f)
		account_parser.remove_section("ACCOUNT_" + str(n))
		with open("accounts.ini", "w") as f:
			account_parser.write(f)

	def __OnClickExitButton(self):
		self.stream.SetPhaseWindow(0)

	def PopupDisplayMessage(self, msg):
		self.stream.popupWindow.Close()
		self.stream.popupWindow.Open(msg)

	def PopupNotifyMessage(self, msg, func = 0):
		if not func:
			func = self.EmptyFunc
		self.stream.popupWindow.Close()
		self.stream.popupWindow.Open(msg, func, localeInfo.UI_OK)

	def __OnCloseInputDialog(self):
		if self.inputDialog:
			self.inputDialog.Close()
		self.inputDialog = None
		return True

	def OnPressExitKey(self):
		self.stream.popupWindow.Close()
		self.stream.SetPhaseWindow(0)
		return True

	def OnExit(self):
		self.stream.popupWindow.Close()

	def OnUpdate(self):
		ServerStateChecker.Update()

	def EmptyFunc(self):
		pass

	def __OpenConnectBoard(self):
		if app.loggined:
			self.Connect(self.id, self.pwd, serverInfo.CLIENT_VERSION, self.pin)
			self.connectBoard.Hide()
		elif not self.stream.isAutoLogin:
			self.connectBoard.Show()
		if self.idEditLine == None:
			self.idEditLine.SetText("")
		if self.pwdEditLine == None:
			self.pwdEditLine.SetText("")
		if self.pinEditLine == None:
			self.pinEditLine.SetText("")
		self.idEditLine.SetFocus()
		return

	def __OnClickLoginButton(self):
		id = self.idEditLine.GetText()
		pwd = self.pwdEditLine.GetText()
		pin = self.pinEditLine.GetText()
		if len(id) == 0:
			self.PopupNotifyMessage(localeInfo.LOGIN_INPUT_ID, self.SetIDEditLineFocus)
			return
		if len(pwd) == 0:
			self.PopupNotifyMessage(localeInfo.LOGIN_INPUT_PASSWORD, self.SetPasswordEditLineFocus)
			return
		if len(pin)==0:
			self.PopupNotifyMessage(localeInfo.LOGIN_INPUT_PIN, self.SetPinEditLineFocus)
			return

		cv = serverInfo.CLIENT_VERSION
		self.Connect(id, pwd, cv, pin)

	def NotifyChannelState(self, addrKey, state):
		try:
			addrKey = int(addrKey)
		except:
			return

		if addrKey < 1 or addrKey > len(self.channelButtonList):
			return

		status = str(STATE_DICT.get(state, STATE_DICT[0]))
		self.channelButtonList[addrKey - 1].SetText("%s %d (%s)" % (localeInfo.CHANNEL, addrKey, status))

	def __SetServerInfo(self, name):
		net.SetServerInfo(name.strip())
		


