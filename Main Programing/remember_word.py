#!/usr/bin/env python3
# -*- coding: utf-8 -*-

#author Helios

import wx
import word_list_select as wls
from multiprocessing import Process

class TranslatePanel(wx.Panel):
    def __init__(self,parent,panel):
        wx.Panel.__init__(self,parent,size=(600,70),pos=(150,0))

        self.SetBackgroundColour("#ffffff")

        self.line1 = wx.StaticLine(self, pos=(0, 69), size=(600, 2))
        self.input_control = wx.TextCtrl(self,-1, pos=(20, 20), size=(440, 30),style=wx.TE_PROCESS_ENTER)
        self.translate_button=wx.Button(self,pos=(480,20),label="Translate",size=(80,30))

        font1=wx.Font(12, wx.DEFAULT, wx.NORMAL, wx.NORMAL)
        self.input_control.SetFont(font1)

class MainIterfacePanel(wx.Panel):
    def __init__(self,parent):
        wx.Panel.__init__(self,parent,size=(600,330),pos=(150,70))

        self.SetBackgroundColour("#ffffff")

        self.selection = None
        self.word_detail = None

        bitmap=wx.Image("trumpet.png",wx.BITMAP_TYPE_PNG).ConvertToBitmap()
        self.trumpetbutton=wx.BitmapButton(self,-1,bitmap,pos=(420,33))

        self.remember_button=wx.Button(self,size=(135,45),label="Remember Word",pos=(230,110))
        self.maininfo=wx.StaticText(self,label="#To Selene#",pos=(262,285))
        self.exitbutton=wx.Button(self,label="Exit",pos=(2,2),size=(60,20))
        self.kownbutton=wx.Button(self,label="Know",pos=(60,270),size=(120,30))
        self.unkownbutton=wx.Button(self,label="Unkown",pos=(430,270),size=(120,30))
        self.nextbutton = wx.Button(self, label="Next", pos=(245, 270), size=(100, 30))

        self.text1 = wx.StaticText(self, label="", pos=(180, 30), size=(240, 45), style=wx.ALIGN_CENTER)
        self.text2 = wx.StaticText(self, label="", pos=(60, 75), size=(480, 55), style=wx.ALIGN_CENTER)
        self.text3 = wx.StaticText(self, label="", pos=(60, 130), size=(480, 55), style=wx.ALIGN_CENTER)
        self.text4 = wx.StaticText(self, label="", pos=(60, 185), size=(480, 70), style=wx.ALIGN_CENTER)

        font1=wx.Font(22,wx.DEFAULT,wx.NORMAL,wx.BOLD)
        self.text1.SetFont(font1)
        font2 = wx.Font(10, wx.DEFAULT, wx.NORMAL, wx.NORMAL)
        self.text2.SetFont(font2)

        self.trumpetbutton.Bind(wx.EVT_BUTTON,self.OnTrumpetButton)
        self.remember_button.Bind(wx.EVT_BUTTON,self.OnRememberButton)
        self.kownbutton.Bind(wx.EVT_BUTTON,self.RememberNewWord)
        self.nextbutton.Bind(wx.EVT_BUTTON,self.RememberNewWord)
        self.exitbutton.Bind(wx.EVT_BUTTON,self.OnExitButton)
        self.unkownbutton.Bind(wx.EVT_BUTTON,self.OnUnkownButtonS1)

        self.OnExitButton(None)

    def OnTrumpetButton(self,event):
        word=self.word_detail[0][2]
        wls.word_audio_function(word,1)

    def change_word_data(self):
        self.current_id=self.word_detail[0][0]
        example=self.word_detail[0][3]
        example_explanation=self.word_detail[0][4]

        if max(len(x) for x in self.word_detail[0][3].split("\n"))>80:
            if len(self.word_detail[0][3].split("\n")[0])<80:
                example=self.word_detail[0][3].split("\n")[0]
                example_explanation=self.word_detail[0][4].split("\n")[0]
            else:
                half1=len(self.word_detail[0][3].split("\n")[0])//2
                half2 = len(self.word_detail[0][4].split("\n")[0]) // 2
                example = self.word_detail[0][3].split("\n")[0][:half1]+"\n"+self.word_detail[0][3].split("\n")[0][half1:]
                example_explanation = self.word_detail[0][4].split("\n")[0][:half2]+"\n"+self.word_detail[0][4].split("\n")[0][half2:]

        self.text1.SetLabel(self.word_detail[0][2])
        self.text2.SetLabel(example)
        self.text3.SetLabel(example_explanation)
        self.text4.SetLabel(self.word_detail[0][5])

    def BasicSet(self,event):
        self.remember_button.Hide()
        self.maininfo.Hide()
        self.nextbutton.Hide()
        self.text2.Hide()
        self.text3.Hide()
        self.text4.Hide()

        self.trumpetbutton.Show()
        self.exitbutton.Show()
        self.kownbutton.Show()
        self.unkownbutton.Show()
        self.text1.Show()

    def OnExitButton(self,event):
        self.trumpetbutton.Hide()
        self.exitbutton.Hide()
        self.kownbutton.Hide()
        self.unkownbutton.Hide()
        self.nextbutton.Hide()

        self.text1.Hide()
        self.text2.Hide()
        self.text3.Hide()
        self.text4.Hide()

        self.remember_button.Show()
        self.maininfo.Show()

        self.unkownbutton.Bind(wx.EVT_BUTTON, self.OnUnkownButtonS1)

    def OnRememberButton(self,event):
        self.BasicSet(event)

        self.word_detail=wls.rselect_word_content(self.selection)

        self.change_word_data()

        p=Process(target=self.OnTrumpetButton,args=(event,))
        p.start()

    def RememberNewWord(self,event):
        self.BasicSet(event)
        self.unkownbutton.Bind(wx.EVT_BUTTON, self.OnUnkownButtonS1)

        wls.update_word_status(self.selection,self.current_id)

        self.word_detail = wls.rselect_word_content(self.selection)

        self.change_word_data()

        p=Process(target=self.OnTrumpetButton,args=(event,))
        p.start()

    def OnUnkownButtonS1(self,event):
        self.BasicSet(event)
        self.text2.Show()

        self.unkownbutton.Bind(wx.EVT_BUTTON,self.OnUnkownButtonS2)

        p=Process(target=wls.sentence_audio_function,args=(self.word_detail[0][3].split("\n")[0],))
        p.start()

    def OnUnkownButtonS2(self,event):
        self.BasicSet(event)
        self.text2.Show()
        self.text3.Show()

        self.unkownbutton.Bind(wx.EVT_BUTTON,self.OnUnkownButtonS3)

    def OnUnkownButtonS3(self,event):
        self.BasicSet(event)
        self.text2.Show()
        self.text3.Show()
        self.text4.Show()
        self.nextbutton.Show()

        self.kownbutton.Hide()
        self.unkownbutton.Hide()

        self.unkownbutton.Bind(wx.EVT_BUTTON, self.OnUnkownButtonS1)

class WordListPanel(wx.Panel):
    def __init__(self,parent):
        wx.Panel.__init__(self,parent,size=(150,400))

        self.SetBackgroundColour("#ffffff")

        self.selection = None

        self.line2 = wx.StaticLine(self, pos=(149, 0), size=(2, 400))

        wordlist=["CET4 Words","CET6 Words","New Words"]
        detaillist=[]
        self.title=wx.StaticText(self,label="Word List",pos=(25,15),size=(100,20),style=wx.ALIGN_CENTER)
        self.combox=wx.ComboBox(self,choices=wordlist,pos=(25,40),size=(100,20))
        self.listbox=wx.ListBox(self,choices=detaillist,pos=(5,75),size=(140,320))

        font1 = wx.Font(14, wx.DEFAULT, wx.NORMAL, wx.NORMAL)
        self.title.SetFont(font1)
        font2=wx.Font(10, wx.DEFAULT, wx.NORMAL, wx.NORMAL)
        self.listbox.SetFont(font2)

        self.Bind(wx.EVT_LISTBOX_DCLICK,self.Wordclick)
        self.combox.Bind(wx.EVT_COMBOBOX,self.OnSelect)

    def OnSelect(self,event):
        self.detaillist_CET4=wls.get_list("CET4")
        detaillist_CET6=wls.get_list("CET6")
        detaillist_NewWords=["wait"]
        self.listbox.Clear()
        if event.GetString()=="CET4 Words":
            self.listbox.AppendItems(self.detaillist_CET4)
            self.selection="CET4"
        elif event.GetString()=="CET6 Words":
            self.listbox.AppendItems(detaillist_CET6)
            self.selection = "CET6"
        elif event.GetString()=="New Words":
            self.listbox.AppendItems(detaillist_NewWords)

    def Wordclick(self,evet):
        sel=self.listbox.GetSelection()
        word=self.listbox.GetString(sel)
        frame_word = WordFrame(None,word,self.selection)

class WordFrame(wx.Frame):
    def __init__(self,parent,word,s):
        wx.Frame.__init__(self,parent,title=word,size=(500,350))

        self.SetMinSize((300, 100))
        self.WordPanel = wx.Panel(self, size=(500, 350))

        self.word=word
        self.selection=s
        self.word_list=wls.get_list(self.selection)

        if word[:4]=="[OK]":
            word=word[4:]
        word_detail=wls.get_word_detail(self.selection,word)
        ex_len = len(word_detail[0][5].split("\n")) - 3
        if len(word_detail[0][3].split("\n"))>1:
            em_len=max(len(word_detail[0][3].split("\n")[0]),len(word_detail[0][3].split("\n")[1]))-48
        else:
            em_len=len(word_detail[0][3])-48

        self.SetSize(300 + em_len * 6, 280 + ex_len * 15)

        self.text1=wx.StaticText(self.WordPanel,label=str(word_detail[0][2]),pos=(10,12),style=wx.ALIGN_LEFT)
        self.text2=wx.StaticText(self.WordPanel,label=str("[Explanation]\n"+word_detail[0][5]),pos=(10,40),style=wx.ALIGN_LEFT)
        self.text3 = wx.StaticText(self.WordPanel, label=str("[Examlpe]\n"+word_detail[0][3]), pos=(10, 110+ex_len*15), style=wx.ALIGN_LEFT)
        self.text4 = wx.StaticText(self.WordPanel, label=str(word_detail[0][4]), pos=(10, 165+ex_len*15), style=wx.ALIGN_LEFT)

        self.upbutton=wx.Button(self.WordPanel,label="UP",pos=(10,205+ex_len*15),size=(50,25))
        self.downbutton = wx.Button(self.WordPanel, label="DOWN", pos=(220, 205 + ex_len * 15), size=(50, 25))

        font1 = wx.Font(15, wx.DEFAULT, wx.NORMAL, wx.BOLD)
        self.text1.SetFont(font1)

        self.upbutton.Bind(wx.EVT_BUTTON,self.OnUpbutton)
        self.downbutton.Bind(wx.EVT_BUTTON, self.OnDowmbutton)

        self.Show()

    def OnUpbutton(self,event):
        location=self.word_list.index(self.word)
        current_word=self.word_list[location-1]
        frame_word = WordFrame(None, current_word,self.selection)
        self.Destroy()

    def OnDowmbutton(self,event):
        location=self.word_list.index(self.word)
        current_word=self.word_list[location+1]
        frame_word = WordFrame(None, current_word,self.selection)
        self.Destroy()

class MainFrame(wx.Frame):
    def __init__(self,parent,title):
        wx.Frame.__init__(self,parent,title=title,size=(750,460))
        self.SetMaxSize((750,460))

        self.icon = wx.Icon('duck.ico',wx.BITMAP_TYPE_ICO)
        self.SetIcon(self.icon)

        self.statusbar = self.CreateStatusBar()

        self.MainIterfacePanel = MainIterfacePanel(self)
        self.TranslatePanel=TranslatePanel(self,self.MainIterfacePanel)
        self.WordListPanel=WordListPanel(self)

        self.RightIterSizer=wx.BoxSizer(wx.VERTICAL)
        self.RightIterSizer.Add(self.TranslatePanel,7,wx.EXPAND)
        self.RightIterSizer.Add(self.MainIterfacePanel,33,wx.EXPAND)

        self.MainIterSizer=wx.BoxSizer(wx.HORIZONTAL)
        self.MainIterSizer.Add(self.WordListPanel,1,wx.EXPAND)
        self.MainIterSizer.Add(self.RightIterSizer,4,wx.EXPAND)

        self.SetSizer(self.MainIterSizer)
        self.SetAutoLayout(1)
        self.MainIterSizer.Fit(self)

        self.MainIterfacePanel.nextbutton.Bind(wx.EVT_BUTTON,self.OnChangeStatusbar)
        self.MainIterfacePanel.kownbutton.Bind(wx.EVT_BUTTON, self.OnChangeStatusbar)
        self.MainIterfacePanel.remember_button.Bind(wx.EVT_BUTTON, self.OnCheckRemember)
        self.TranslatePanel.translate_button.Bind(wx.EVT_BUTTON, self.OnTranslate)
        self.TranslatePanel.input_control.Bind(wx.EVT_COMMAND_ENTER, self.OnTranslate)
        self.TranslatePanel.Bind(wx.EVT_TEXT_ENTER, self.OnTranslate)

        self.RightMenu()

        self.Show()

    def OnCheckRemember(self,event):
        if self.WordListPanel.selection is None:
            wx.MessageBox('Please select a word list', 'Tips')
        else:
            self.MainIterfacePanel.selection=self.WordListPanel.selection
            self.MainIterfacePanel.OnRememberButton(event)

    def OnTranslate(self,event):
        getvalue=self.TranslatePanel.input_control.GetValue()
        text=wls.translate_function(getvalue)
        if getvalue.strip() >= '\u4e00' and getvalue.strip() <= '\u9fa5':
            self.statusbar.SetStatusText(" " + text)
        elif getvalue.strip().isalpha():
            self.statusbar.SetStatusText(" " + "[" + getvalue + "]" + " " + text)
        else:
            self.statusbar.SetStatusText(" " + text)

    def OnChangeStatusbar(self,event):
        text=self.MainIterfacePanel.word_detail[0][2]+"  "+self.MainIterfacePanel.word_detail[0][5]
        self.statusbar.SetStatusText(" "+text)
        self.MainIterfacePanel.RememberNewWord(event)

    def RightMenu(self):
        self.popupmenu=wx.Menu()

        self.CheckItem=self.popupmenu.AppendCheckItem(-1,"Word List")
        self.CheckItem.Check(True)
        self.Bind(wx.EVT_MENU,self.Open0Close,self.CheckItem)

        self.Bind(wx.EVT_CONTEXT_MENU, self.OnShowPopup)

    def OnShowPopup(self,event):
        pos = event.GetPosition()
        pos = self.ScreenToClient(pos)
        self.PopupMenu(self.popupmenu, pos)

    def Open0Close(self,event):
        if self.CheckItem.IsChecked():
            self.OnOpenWordList(event)
        else:
            self.OnCloseWordList(event)

    def OnOpenWordList(self,event):
        self.SetSize((750, 460))

        self.TranslatePanel.SetPosition((150, 0))
        self.MainIterfacePanel.SetPosition((150, 70))

        self.WordListPanel.Show()

    def OnCloseWordList(self,event):
        self.WordListPanel.Hide()

        self.TranslatePanel.SetPosition((0, 0))
        self.MainIterfacePanel.SetPosition((0, 70))

        self.SetSize((600, 460))

if __name__ == "__main__":
    app=wx.App(False)
    frame=MainFrame(None,"Duck Remember Words 1.3")
    app.MainLoop()
