# -*-python-*-
# GemRB - Infinity Engine Emulator
# Copyright (C) 2003-2005 The GemRB Project
#
# This program is free software; you can redistribute it and/or
# modify it under the terms of the GNU General Public License
# as published by the Free Software Foundation; either version 2
# of the License, or (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program; if not, write to the Free Software
# Foundation, Inc., 59 Temple Place - Suite 330, Boston, MA 02111-1307, USA.
#
# $Header:

import GemRB

from GUICommonWindows import *
from GUIJRNL import *
from GUIMA import *
from GUIMG import *
from GUIINV import *
from GUIOPT import *
from GUIPR import *
from GUIREC import *
from GUISTORE import *
from GUIWORLD import *
from TextScreen import *

MessageWindow = 0
PortraitWindow = 0
OptionsWindow = 0
ExpandButton = 0
ContractButton = 0

def OnLoad():
	global MessageWindow, ExpandButton, Expand
	global PortraitWindow, OptionsWindow

	GemRB.LoadWindowPack(GetWindowPack())
	ActionsWindow = GemRB.LoadWindow(3)
	OptionsWindow = GemRB.LoadWindow(0)
	MessageWindow = GemRB.LoadWindow(4)
	PortraitWindow = OpenPortraitWindow(1)

	MessageTA = GemRB.GetControl(MessageWindow, 3)
	GemRB.SetTextAreaFlags(MessageWindow, MessageTA, IE_GUI_TEXTAREA_AUTOSCROLL)
	Button=GemRB.GetControl(OptionsWindow, 10)
	GemRB.SetEvent(OptionsWindow, Button, IE_GUI_BUTTON_ON_PRESS, "MinimizeOptions")
	Button=GemRB.GetControl(PortraitWindow, 8)
	GemRB.SetEvent(PortraitWindow, Button, IE_GUI_BUTTON_ON_PRESS, "MinimizePortraits")
	Button=GemRB.GetControl(ActionsWindow, 60)
	GemRB.SetEvent(ActionsWindow, Button, IE_GUI_BUTTON_ON_PRESS, "MaximizeOptions")
	Button=GemRB.GetControl(ActionsWindow, 61)
	GemRB.SetEvent(ActionsWindow, Button, IE_GUI_BUTTON_ON_PRESS, "MaximizePortraits")

	GemRB.SetVar("PortraitWindow", PortraitWindow)
	GemRB.SetVar("ActionsWindow", ActionsWindow)
	GemRB.SetVar("OptionsWindow", OptionsWindow)
	GemRB.SetVar("MessageWindow", MessageWindow)
	GemRB.SetVar("TopWindow", -1)
	GemRB.SetVar("OtherWindow", -1)
	GemRB.SetVar("FloatWindow", -1)
	GemRB.SetVar("PortraitPosition", 2) #Right
	GemRB.SetVar("ActionsPosition", 4) #BottomAdded
	GemRB.SetVar("OptionsPosition", 0) #Left
	GemRB.SetVar("MessagePosition", 4) #BottomAdded
	GemRB.SetVar("OtherPosition", 5) #Inactivating
	GemRB.SetVar("TopPosition", 5) #Inactivating
	
	GemRB.SetVar("MessageTextArea", MessageTA)
	GemRB.SetVar("MessageWindowSize", 0)

	SetupActionsWindowControls (ActionsWindow)
	SetupMenuWindowControls (OptionsWindow)

	UpdateResizeButtons()
	
	GemRB.SetVisible(ActionsWindow, 1)
	GemRB.SetVisible(OptionsWindow, 0)
	GemRB.SetVisible(MessageWindow, 1)
	return

def MinimizeOptions():
	GemRB.HideGUI()
	GemRB.SetVisible(OptionsWindow, 0)
	GemRB.SetVar("OptionsWindow", -1)
	GemRB.UnhideGUI()
	return

def MaximizeOptions():
	GemRB.HideGUI()
	GemRB.SetVar("OptionsWindow", OptionsWindow)
	GemRB.UnhideGUI()
	return

def MinimizePortraits():
	GemRB.HideGUI()
	GemRB.SetVisible(PortraitWindow, 0)
	GemRB.SetVar("PortraitWindow", -1)
	GemRB.UnhideGUI()
	return

def MaximizePortraits():
	GemRB.HideGUI()
	GemRB.SetVar("PortraitWindow", PortraitWindow)
	GemRB.UnhideGUI()
	return

def OnIncreaseSize():
	global MessageWindow, ExpandButton
	
	TMessageWindow = 0
	TMessageTA = 0
	
	GemRB.HideGUI()
	MessageTA = GemRB.GetVar("MessageTextArea")
	Expand = GemRB.GetVar("MessageWindowSize")
	
	if Expand == 0:
		GemRB.LoadWindowPack(GetWindowPack())
		TMessageWindow = GemRB.LoadWindow(12)
		TMessageTA = GemRB.GetControl(TMessageWindow, 1)
		GemRB.SetVar("MessageWindow", TMessageWindow)
		GemRB.SetVar("MessageTextArea", TMessageTA)
		GemRB.SetTextAreaFlags(TMessageWindow, TMessageTA, IE_GUI_TEXTAREA_AUTOSCROLL)
	else :
		if Expand == 1:
			GemRB.LoadWindowPack(GetWindowPack())
			TMessageWindow = GemRB.LoadWindow(7)
			TMessageTA = GemRB.GetControl(TMessageWindow, 1)
			GemRB.SetVar("MessageWindow", TMessageWindow)
			GemRB.SetVar("MessageTextArea", TMessageTA)
			GemRB.SetTextAreaFlags(TMessageWindow, TMessageTA, IE_GUI_TEXTAREA_AUTOSCROLL)

	if Expand!=2:
		GemRB.MoveTAText(MessageWindow, MessageTA, TMessageWindow, TMessageTA)
		GemRB.UnloadWindow(MessageWindow)
		Expand = Expand+1
		MessageWindow = TMessageWindow
		GemRB.SetVar("MessageWindowSize", Expand)
		UpdateResizeButtons()

	GemRB.UnhideGUI()
	GemRB.SetControlStatus(TMessageWindow,TMessageTA,IE_GUI_CONTROL_FOCUSED)
	return
	
def OnDecreaseSize():
	global MessageWindow, ContractButton
	
	TMessageWindow = 0
	TMessageTA = 0
	
	GemRB.HideGUI()
	MessageTA = GemRB.GetVar("MessageTextArea")
	Expand = GemRB.GetVar("MessageWindowSize")
	
	if Expand == 2:
		GemRB.LoadWindowPack(GetWindowPack())
		TMessageWindow = GemRB.LoadWindow(12)
		TMessageTA = GemRB.GetControl(TMessageWindow, 1)
		GemRB.SetVar("MessageWindow", TMessageWindow)
		GemRB.SetVar("MessageTextArea", TMessageTA)
		GemRB.SetTextAreaFlags(TMessageWindow, TMessageTA, IE_GUI_TEXTAREA_AUTOSCROLL)
	else:
		if Expand == 1:
			GemRB.LoadWindowPack(GetWindowPack())
			TMessageWindow = GemRB.LoadWindow(4)
			TMessageTA = GemRB.GetControl(TMessageWindow, 3)
			GemRB.SetVar("MessageWindow", TMessageWindow)
			GemRB.SetVar("MessageTextArea", TMessageTA)
			GemRB.SetTextAreaFlags(TMessageWindow, TMessageTA, IE_GUI_TEXTAREA_AUTOSCROLL)
	if Expand:
		GemRB.MoveTAText(MessageWindow, MessageTA, TMessageWindow, TMessageTA)
		GemRB.UnloadWindow(MessageWindow)
		Expand = Expand-1
		MessageWindow = TMessageWindow
		GemRB.SetVar("MessageWindowSize", Expand)
		UpdateResizeButtons()

	GemRB.UnhideGUI()
	if Expand:
		GemRB.SetControlStatus(TMessageWindow,TMessageTA,IE_GUI_CONTROL_FOCUSED)
	else:
		GemRB.SetControlStatus(0,0,IE_GUI_CONTROL_FOCUSED)
	return
	
def UpdateResizeButtons():
	global MessageWindow, ExpandButton, ContractButton
	Expand = GemRB.GetVar("MessageWindowSize")
	
	if Expand == 0:
		ExpandButton = GemRB.GetControl(MessageWindow, 2)
		GemRB.SetEvent(MessageWindow, ExpandButton, IE_GUI_BUTTON_ON_PRESS, "OnIncreaseSize")
	else:
		if Expand == 1:
			ExpandButton = GemRB.GetControl(MessageWindow, 0)
			GemRB.SetEvent(MessageWindow, ExpandButton, IE_GUI_BUTTON_ON_PRESS, "OnIncreaseSize")
			ContractButton = GemRB.GetControl(MessageWindow, 3)
			GemRB.SetEvent(MessageWindow, ContractButton, IE_GUI_BUTTON_ON_PRESS, "OnDecreaseSize")
		else:
			ContractButton = GemRB.GetControl(MessageWindow, 0)
			GemRB.SetEvent(MessageWindow, ContractButton, IE_GUI_BUTTON_ON_PRESS, "OnDecreaseSize")
	return

