import os
from Plugins.Plugin import PluginDescriptor
from Components.Sources.StaticText import StaticText
from Components.ActionMap import ActionMap
from Components.ChoiceList import ChoiceList, ChoiceEntryComponent
from Components.Console import Console
from Components.Label import Label
from Components.SystemInfo import SystemInfo
from Screens.Standby import TryQuitMainloop
from Screens.Screen import Screen
from Screens.MessageBox import MessageBox
from Tools.BoundFunction import boundFunction
from Tools.Directories import fileExists, fileCheck, pathExists, fileHas
from enigma import getDesktop


class FlashExpander(Screen):
	if getDesktop(0).size().width() >= 1920:
		skin = """
			<screen name="FlashExpander" position="center,center" size="1200,1035" flags="wfNoBorder" >
				<eLabel name="b" position="0,0" size="1200,1050" backgroundColor="#00ffffff" zPosition="-2" />
				<eLabel name="a" position="2,2" size="1197,1032" zPosition="-1" />
				<widget source="Title" render="Label" position="120,12" size="945,75" valign="center" halign="center" font="Regular; 42" />
				<eLabel name="line" position="2,90" size="1197,2" backgroundColor="#00ffffff" zPosition="1" />
				<eLabel name="line2" position="2,375" size="1197,6" backgroundColor="#00ffffff" zPosition="1" />
				<widget name="config" position="3,420" size="1095,570" halign="center" itemHeight="38" font="Regular; 33" />
				<widget source="labe14" render="Label" position="3,120" size="1095,45" halign="center" font="Regular; 33" />
				<widget source="labe15" render="Label" position="3,195" size="1095,90" halign="center" font="Regular; 33" />
				<widget source="key_red" render="Label" position="45,300" size="225,45" noWrap="1" zPosition="1" valign="center" font="Regular; 30" halign="left" />
				<widget source="key_green" render="Label" position="345,300" size="225,45" noWrap="1" zPosition="1" valign="center" font="Regular; 30" halign="left" />
				<widget source="key_yellow" render="Label" position="645,300" size="225,45" noWrap="1" zPosition="1" valign="center" font="Regular; 30" halign="left" />
				<widget source="key_blue" render="Label" position="945,300" size="225,45" noWrap="1" zPosition="1" valign="center" font="Regular; 30" halign="left" />
				<ePixmap pixmap="skin_default/buttons/red.png" position="45,300" size="60,60" alphatest="on" />
				<ePixmap pixmap="skin_default/buttons/green.png" position="345,300" size="60,60" alphatest="on" />
				<ePixmap pixmap="skin_default/buttons/yellow.png" position="645,300" size="60,60" alphatest="on" />
				<ePixmap pixmap="skin_default/buttons/blue.png" position="945,300" size="60,60" alphatest="on" />
			</screen>
			"""
	else:
		skin = """
			<screen name="FlashExpander" position="center,center" size="800,690" flags="wfNoBorder" >
				<eLabel name="b" position="0,0" size="800,700" backgroundColor="#00ffffff" zPosition="-2" />
				<eLabel name="a" position="1,1" size="798,688" zPosition="-1" />
				<widget source="Title" render="Label" position="80,8" size="630,50" valign="center" halign="center" font="Regular; 28" />
				<eLabel name="line" position="1,60" size="798,1" backgroundColor="#00ffffff" zPosition="1" />
				<eLabel name="line2" position="1,250" size="798,4" backgroundColor="#00ffffff" zPosition="1" />
				<widget name="config" position="2,280" size="730,380" halign="center" font="Regular; 22" />
				<widget source="labe14" render="Label" position="2,80" size="730,30" halign="center" font="Regular; 22" />
				<widget source="labe15" render="Label" position="2,130" size="730,60" halign="center" font="Regular; 22" />
				<widget source="key_red" render="Label" position="30,200" size="150,30" noWrap="1" zPosition="1" valign="center" font="Regular; 20" halign="left" />
				<widget source="key_green" render="Label" position="230,200" size="150,30" noWrap="1" zPosition="1" valign="center" font="Regular; 20" halign="left" />
				<widget source="key_yellow" render="Label" position="430,200" size="150,30" noWrap="1" zPosition="1" valign="center" font="Regular; 20" halign="left" />
				<widget source="key_blue" render="Label" position="630,200" size="150,30" noWrap="1" zPosition="1" valign="center" font="Regular; 20" halign="left" />
				<ePixmap pixmap="skin_default/buttons/red.png" position="30,200" size="40,40" alphatest="on" />
				<ePixmap pixmap="skin_default/buttons/green.png" position="230,200" size="40,40" alphatest="on" />
				<ePixmap pixmap="skin_default/buttons/yellow.png" position="430,200" size="40,40" alphatest="on" />
				<ePixmap pixmap="skin_default/buttons/blue.png" position="630,200" size="40,40" alphatest="on" />
			</screen>
			"""

	def __init__(self, session, *args):
		Screen.__init__(self, session)
		self.skinName = "FlashExpander"
		#self.skin = FlashExpander.skin
		screentitle = _("Switch Nand / SDcard / USB")
		self["key_red"] = StaticText(_("Cancel"))
		self["key_green"] = StaticText(_("SwaptoNand"))
		self["key_yellow"] = StaticText(_("SwaptoSD"))
		self["key_blue"] = StaticText(_("SwaptoUSB"))
		self.title = screentitle
		self.switchtype = " "
		self["actions"] = ActionMap(["ColorActions","OkCancelActions"],
		{
			"red": boundFunction(self.close, None),
			#"red": self.close,
			"green": self.SwaptoNand,
			"yellow": self.SwaptoSD,
			"blue": self.SwaptoUSB,
			"cancel": self.close,
		}, -1)
		self.onLayoutFinish.append(self.layoutFinished)

	def layoutFinished(self):
		self.setTitle(self.title)

	def SwaptoNand(self):
		self.switchtype = "Nand"
		f = open('/proc/cmdline', 'r').read()
		if "root=/dev/mmcblk0p1"  in f:
			self.container = Console()
			self.container.ePopen("dd if=/usr/share/bootargs-nand.bin of=/dev/mtdblock1", self.Unm)
		else:
			self.session.open(MessageBox, _("SDcard switch ERROR! - already on Nand"), MessageBox.TYPE_INFO, timeout=20)

	def SwaptoSD(self):
		self.switchtype = "mmc"
		f = open('/proc/cmdline', 'r').read()
		print "[FlashExpander] switchtype %s cmdline %s" %(self.switchtype, f) 
		if "root=/dev/mmcblk0p1" in f:
			self.session.open(MessageBox, _("SDcard switch ERROR! - already on mmc"), MessageBox.TYPE_INFO, timeout=20)
		elif os.path.isfile("/media/mmc/usr/bin/enigma2"):
			self.container = Console()
			self.container.ePopen("dd if=/usr/share/bootargs-mmc.bin of=/dev/mtdblock1", self.Unm)
		else:
			self.session.open(MessageBox, _("SDcard switch ERROR! - root files not transferred to SD card"), MessageBox.TYPE_INFO, timeout=20)

	def SwaptoUSB(self):
		self.switchtype = "usb"
		f = open('/proc/cmdline', 'r').read()
		print "[FlashExpander] switchtype %s cmdline %s" %(self.switchtype, f) 
		if "root=/dev/SDA1" in f:
			self.session.open(MessageBox, _("USB switch ERROR! - already on USB"), MessageBox.TYPE_INFO, timeout=20)
		elif os.path.isfile("/media/mmc/usr/bin/enigma2"):
			self.container = Console()
			self.container.ePopen("dd if=/usr/share/bootargs-usb.bin of=/dev/mtdblock1", self.Unm)
		else:
			self.session.open(MessageBox, _("USB switch ERROR! - root files not transferred to USB"), MessageBox.TYPE_INFO, timeout=20)


	def Unm(self, data=None, retval=None, extra_args=None):
		self.container.killAll()
		self.session.open(TryQuitMainloop, 2)

def main(session, **kwargs):
	session.open(FlashExpander)
				
def Plugins(**kwargs):
	return PluginDescriptor(
		name="Flash Expander", 
		description="Expand Flash to MMC or USB", 
		#icon="plugin.png",
		where = [ PluginDescriptor.WHERE_EXTENSIONSMENU, PluginDescriptor.WHERE_PLUGINMENU ],
		fnc=main)
