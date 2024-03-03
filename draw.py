# -*- coding: utf-8 -*-

import math
import sqlite3

import matplotlib.pyplot as plt
import numpy as np
import wx
import wx.grid
import wx.grid as gridlib
# import wx.xrc
from matplotlib.backends.backend_wxagg import FigureCanvasWxAgg as FigureCanvas


class MyFrame1(wx.Frame):

    def __init__(self, parent, title):
        wx.Frame.__init__(self, parent, id=wx.ID_ANY, title=title, pos=wx.DefaultPosition, size=wx.Size(1025, 850),
                          style=wx.DEFAULT_FRAME_STYLE | wx.TAB_TRAVERSAL)

        self.SetSizeHints(wx.DefaultSize, wx.DefaultSize)

        self.m_toolBar1 = self.CreateToolBar(wx.TB_HORIZONTAL, wx.ID_ANY)
        self.m_toolBar1.SetToolPacking(20)
        self.m_tool1 = self.m_toolBar1.AddTool(wx.ID_ANY, u"tool",
                                               wx.Bitmap(u"girl.bmp",
                                                         wx.BITMAP_TYPE_ANY), wx.NullBitmap, wx.ITEM_NORMAL,
                                               wx.EmptyString, wx.EmptyString, None)

        self.m_toolBar1.AddSeparator()

        self.m_tool2 = self.m_toolBar1.AddTool(wx.ID_ANY, u"tool",
                                               wx.Bitmap(u"dog.bmp",
                                                         wx.BITMAP_TYPE_ANY), wx.NullBitmap, wx.ITEM_NORMAL,
                                               wx.EmptyString, wx.EmptyString, None)

        self.m_toolBar1.Realize()

        bSizer1 = wx.BoxSizer(wx.VERTICAL)

        bSizer3 = wx.BoxSizer(wx.HORIZONTAL)

        self.m_staticText2 = wx.StaticText(self, wx.ID_ANY, u"故障时间数据库：", wx.DefaultPosition, wx.DefaultSize, 0)
        self.m_staticText2.Wrap(-1)

        bSizer3.Add(self.m_staticText2, 0, wx.ALL, 5)

        self.m_filePicker1 = wx.FilePickerCtrl(self, wx.ID_ANY, wx.EmptyString, wx.EmptyString, u"*.*",
                                               wx.DefaultPosition, wx.Size(450, -1), wx.FLP_DEFAULT_STYLE)
        bSizer3.Add(self.m_filePicker1, 0, wx.ALL, 5)
        # 显示故障时间表格
        self.m_button1 = wx.Button(self, wx.ID_ANY, u"显示故障时间表格", wx.DefaultPosition, wx.DefaultSize, 0)
        bSizer3.Add(self.m_button1, 0, wx.ALL, 5)
        self.m_button1.Bind(wx.EVT_BUTTON, self.write_tables_grids)

        self.m_staticText36 = wx.StaticText(self, wx.ID_ANY, u"绘图开始时间：", wx.DefaultPosition, wx.DefaultSize, 0)
        self.m_staticText36.Wrap(-1)

        bSizer3.Add(self.m_staticText36, 0, wx.ALL, 5)

        self.m_textCtrl31 = wx.TextCtrl(self, wx.ID_ANY, wx.EmptyString, wx.DefaultPosition, wx.Size(300, -1), 0)
        bSizer3.Add(self.m_textCtrl31, 0, wx.ALL, 5)

        bSizer1.Add(bSizer3, 0, wx.EXPAND, 5)

        bSizer7 = wx.BoxSizer(wx.HORIZONTAL)

        self.m_staticText3 = wx.StaticText(self, wx.ID_ANY, u"故障数据数据库：", wx.DefaultPosition, wx.DefaultSize, 0)
        self.m_staticText3.Wrap(-1)

        bSizer7.Add(self.m_staticText3, 0, wx.ALL, 5)

        self.m_filePicker2 = wx.FilePickerCtrl(self, wx.ID_ANY, wx.EmptyString, u"Select a file", u"*.*",
                                               wx.DefaultPosition, wx.Size(450, -1), wx.FLP_DEFAULT_STYLE)
        bSizer7.Add(self.m_filePicker2, 0, wx.ALL, 5)

        self.m_button6 = wx.Button(self, wx.ID_ANY, u"绘图", wx.DefaultPosition, wx.DefaultSize, 0)
        self.m_button6.SetBackgroundColour(wx.SystemSettings.GetColour(wx.SYS_COLOUR_HIGHLIGHT))
        self.m_button6.Bind(wx.EVT_BUTTON, self.draw_plots)

        bSizer7.Add(self.m_button6, 0, wx.ALL, 5)

        self.m_staticText39 = wx.StaticText(self, wx.ID_ANY, u"结束时间:", wx.DefaultPosition, wx.DefaultSize, 0)
        self.m_staticText39.Wrap(-1)

        bSizer7.Add(self.m_staticText39, 0, wx.ALL, 5)

        self.m_textCtrl34 = wx.TextCtrl(self, wx.ID_ANY, wx.EmptyString, wx.DefaultPosition, wx.Size(200, -1), 0)
        bSizer7.Add(self.m_textCtrl34, 0, wx.ALL, 5)

        self.m_button61 = wx.Button(self, wx.ID_ANY, u"显示ID", wx.DefaultPosition, wx.DefaultSize, 0)
        bSizer7.Add(self.m_button61, 0, wx.ALL, 5)

        self.m_button61.Bind(wx.EVT_BUTTON, self.select_database_ID)

        bSizer1.Add(bSizer7, 0, wx.EXPAND, 5)

        bSizer6 = wx.BoxSizer(wx.HORIZONTAL)

        self.m_staticText4 = wx.StaticText(self, wx.ID_ANY, u"绘图通道1：", wx.DefaultPosition, wx.DefaultSize, 0)
        self.m_staticText4.Wrap(-1)

        bSizer6.Add(self.m_staticText4, 0, wx.ALL, 5)

        self.m_textCtrl1 = wx.TextCtrl(self, wx.ID_ANY, u"27", wx.DefaultPosition, wx.Size(50, -1), 0)
        bSizer6.Add(self.m_textCtrl1, 0, wx.ALL, 5)

        self.m_staticText5 = wx.StaticText(self, wx.ID_ANY, u"绘图通道2：", wx.DefaultPosition, wx.DefaultSize, 0)
        self.m_staticText5.Wrap(-1)

        bSizer6.Add(self.m_staticText5, 0, wx.ALL, 5)

        self.m_textCtrl2 = wx.TextCtrl(self, wx.ID_ANY, u"28", wx.DefaultPosition, wx.Size(50, -1), 0)
        bSizer6.Add(self.m_textCtrl2, 0, wx.ALL, 5)

        self.m_staticText6 = wx.StaticText(self, wx.ID_ANY, u"绘图通道3：", wx.DefaultPosition, wx.DefaultSize, 0)
        self.m_staticText6.Wrap(-1)

        bSizer6.Add(self.m_staticText6, 0, wx.ALL, 5)

        self.m_textCtrl3 = wx.TextCtrl(self, wx.ID_ANY, u"29", wx.DefaultPosition, wx.Size(50, -1), 0)
        bSizer6.Add(self.m_textCtrl3, 0, wx.ALL, 5)

        self.m_staticText37 = wx.StaticText(self, wx.ID_ANY, u"测量通道：", wx.DefaultPosition, wx.DefaultSize, 0)
        self.m_staticText37.Wrap(-1)

        bSizer6.Add(self.m_staticText37, 0, wx.ALL, 5)

        self.m_textCtrl32 = wx.TextCtrl(self, wx.ID_ANY, u"32", wx.DefaultPosition, wx.Size(50, -1), 0)
        bSizer6.Add(self.m_textCtrl32, 0, wx.ALL, 5)

        self.m_button4 = wx.Button(self, wx.ID_ANY, u"测量通道有效值显示", wx.DefaultPosition, wx.DefaultSize, 0)
        bSizer6.Add(self.m_button4, 0, wx.ALL, 5)
        self.m_button4.Bind(wx.EVT_BUTTON, self.cal_var)

        self.m_textCtrl36 = wx.TextCtrl(self, wx.ID_ANY, wx.EmptyString, wx.DefaultPosition, wx.DefaultSize, 0)
        bSizer6.Add(self.m_textCtrl36, 0, wx.ALL, 5)

        self.m_staticText41 = wx.StaticText(self, wx.ID_ANY, u"测量通道计算点数：", wx.DefaultPosition, wx.DefaultSize,
                                            0)
        self.m_staticText41.Wrap(-1)

        bSizer6.Add(self.m_staticText41, 0, wx.ALL, 5)

        # 从开始时间对应的ID值到增加的计算点数 开始计算
        self.m_textCtrl37 = wx.TextCtrl(self, wx.ID_ANY, u'400', wx.DefaultPosition, wx.DefaultSize, 0)
        bSizer6.Add(self.m_textCtrl37, 0, wx.ALL, 5)

        bSizer1.Add(bSizer6, 0, wx.EXPAND, 5)

        bSizer5 = wx.BoxSizer(wx.VERTICAL)

        self.m_staticText7 = wx.StaticText(self, wx.ID_ANY, u"数据可视化部分", wx.DefaultPosition, wx.DefaultSize, 0)
        self.m_staticText7.Wrap(-1)

        self.m_staticText7.SetFont(
            wx.Font(15, wx.FONTFAMILY_DEFAULT, wx.FONTSTYLE_NORMAL, wx.FONTWEIGHT_NORMAL, False, wx.EmptyString))
        self.m_staticText7.SetForegroundColour(wx.SystemSettings.GetColour(wx.SYS_COLOUR_BACKGROUND))
        self.m_staticText7.SetBackgroundColour(wx.SystemSettings.GetColour(wx.SYS_COLOUR_APPWORKSPACE))

        bSizer5.Add(self.m_staticText7, 0, wx.ALIGN_CENTER | wx.ALL, 5)

        bSizer1.Add(bSizer5, 0, wx.EXPAND, 5)

        bSizer8 = wx.BoxSizer(wx.HORIZONTAL)

        self.m_staticText8 = wx.StaticText(self, wx.ID_ANY, u"通道01：", wx.DefaultPosition, wx.DefaultSize, 0)
        self.m_staticText8.Wrap(-1)

        bSizer8.Add(self.m_staticText8, 0, wx.ALL, 5)

        self.m_textCtrl4 = wx.TextCtrl(self, wx.ID_ANY, wx.EmptyString, wx.DefaultPosition, wx.Size(70, -1), 0)
        bSizer8.Add(self.m_textCtrl4, 0, wx.ALL, 5)

        self.m_staticText9 = wx.StaticText(self, wx.ID_ANY, u"通道02：", wx.DefaultPosition, wx.DefaultSize, 0)
        self.m_staticText9.Wrap(-1)

        bSizer8.Add(self.m_staticText9, 0, wx.ALL, 5)

        self.m_textCtrl5 = wx.TextCtrl(self, wx.ID_ANY, wx.EmptyString, wx.DefaultPosition, wx.Size(70, -1), 0)
        bSizer8.Add(self.m_textCtrl5, 0, wx.ALL, 5)

        self.m_staticText10 = wx.StaticText(self, wx.ID_ANY, u"通道03：", wx.DefaultPosition, wx.DefaultSize, 0)
        self.m_staticText10.Wrap(-1)

        bSizer8.Add(self.m_staticText10, 0, wx.ALL, 5)

        self.m_textCtrl6 = wx.TextCtrl(self, wx.ID_ANY, wx.EmptyString, wx.DefaultPosition, wx.Size(70, -1), 0)
        bSizer8.Add(self.m_textCtrl6, 0, wx.ALL, 5)

        self.m_staticText11 = wx.StaticText(self, wx.ID_ANY, u"通道04：", wx.DefaultPosition, wx.DefaultSize, 0)
        self.m_staticText11.Wrap(-1)

        bSizer8.Add(self.m_staticText11, 0, wx.ALL, 5)

        self.m_textCtrl7 = wx.TextCtrl(self, wx.ID_ANY, wx.EmptyString, wx.DefaultPosition, wx.Size(70, -1), 0)
        bSizer8.Add(self.m_textCtrl7, 0, wx.ALL, 5)

        self.m_staticText12 = wx.StaticText(self, wx.ID_ANY, u"通道05：", wx.DefaultPosition, wx.DefaultSize, 0)
        self.m_staticText12.Wrap(-1)

        bSizer8.Add(self.m_staticText12, 0, wx.ALL, 5)

        self.m_textCtrl8 = wx.TextCtrl(self, wx.ID_ANY, wx.EmptyString, wx.DefaultPosition, wx.Size(70, -1), 0)
        bSizer8.Add(self.m_textCtrl8, 0, wx.ALL, 5)

        self.m_staticText13 = wx.StaticText(self, wx.ID_ANY, u"通道06：", wx.DefaultPosition, wx.DefaultSize, 0)
        self.m_staticText13.Wrap(-1)

        bSizer8.Add(self.m_staticText13, 0, wx.ALL, 5)

        self.m_textCtrl9 = wx.TextCtrl(self, wx.ID_ANY, wx.EmptyString, wx.DefaultPosition, wx.Size(70, -1), 0)
        bSizer8.Add(self.m_textCtrl9, 0, wx.ALL, 5)

        bSizer1.Add(bSizer8, 0, wx.EXPAND, 5)

        bSizer4 = wx.BoxSizer(wx.HORIZONTAL)

        self.m_staticText14 = wx.StaticText(self, wx.ID_ANY, u"通道07：", wx.DefaultPosition, wx.DefaultSize, 0)
        self.m_staticText14.Wrap(-1)

        bSizer4.Add(self.m_staticText14, 0, wx.ALL, 5)

        self.m_textCtrl10 = wx.TextCtrl(self, wx.ID_ANY, wx.EmptyString, wx.DefaultPosition, wx.Size(70, -1), 0)
        bSizer4.Add(self.m_textCtrl10, 0, wx.ALL, 5)

        self.m_staticText15 = wx.StaticText(self, wx.ID_ANY, u"通道08：", wx.DefaultPosition, wx.DefaultSize, 0)
        self.m_staticText15.Wrap(-1)

        bSizer4.Add(self.m_staticText15, 0, wx.ALL, 5)

        self.m_textCtrl11 = wx.TextCtrl(self, wx.ID_ANY, wx.EmptyString, wx.DefaultPosition, wx.Size(70, -1), 0)
        bSizer4.Add(self.m_textCtrl11, 0, wx.ALL, 5)

        self.m_staticText16 = wx.StaticText(self, wx.ID_ANY, u"通道09：", wx.DefaultPosition, wx.DefaultSize, 0)
        self.m_staticText16.Wrap(-1)

        bSizer4.Add(self.m_staticText16, 0, wx.ALL, 5)

        self.m_textCtrl12 = wx.TextCtrl(self, wx.ID_ANY, wx.EmptyString, wx.DefaultPosition, wx.Size(70, -1), 0)
        bSizer4.Add(self.m_textCtrl12, 0, wx.ALL, 5)

        self.m_staticText17 = wx.StaticText(self, wx.ID_ANY, u"通道10：", wx.DefaultPosition, wx.DefaultSize, 0)
        self.m_staticText17.Wrap(-1)

        bSizer4.Add(self.m_staticText17, 0, wx.ALL, 5)

        self.m_textCtrl13 = wx.TextCtrl(self, wx.ID_ANY, wx.EmptyString, wx.DefaultPosition, wx.Size(70, -1), 0)
        bSizer4.Add(self.m_textCtrl13, 0, wx.ALL, 5)

        self.m_staticText18 = wx.StaticText(self, wx.ID_ANY, u"通道11：", wx.DefaultPosition, wx.DefaultSize, 0)
        self.m_staticText18.Wrap(-1)

        bSizer4.Add(self.m_staticText18, 0, wx.ALL, 5)

        self.m_textCtrl14 = wx.TextCtrl(self, wx.ID_ANY, wx.EmptyString, wx.DefaultPosition, wx.Size(70, -1), 0)
        bSizer4.Add(self.m_textCtrl14, 0, wx.ALL, 5)

        self.m_staticText19 = wx.StaticText(self, wx.ID_ANY, u"通道12：", wx.DefaultPosition, wx.DefaultSize, 0)
        self.m_staticText19.Wrap(-1)

        bSizer4.Add(self.m_staticText19, 0, wx.ALL, 5)

        self.m_textCtrl15 = wx.TextCtrl(self, wx.ID_ANY, wx.EmptyString, wx.DefaultPosition, wx.Size(70, -1), 0)
        bSizer4.Add(self.m_textCtrl15, 0, wx.ALL, 5)

        bSizer1.Add(bSizer4, 0, wx.EXPAND, 5)

        bSizer9 = wx.BoxSizer(wx.HORIZONTAL)

        self.m_staticText20 = wx.StaticText(self, wx.ID_ANY, u"通道13：", wx.DefaultPosition, wx.DefaultSize, 0)
        self.m_staticText20.Wrap(-1)

        bSizer9.Add(self.m_staticText20, 0, wx.ALL, 5)

        self.m_textCtrl16 = wx.TextCtrl(self, wx.ID_ANY, wx.EmptyString, wx.DefaultPosition, wx.Size(70, -1), 0)
        bSizer9.Add(self.m_textCtrl16, 0, wx.ALL, 5)

        self.m_staticText21 = wx.StaticText(self, wx.ID_ANY, u"通道14：", wx.DefaultPosition, wx.DefaultSize, 0)
        self.m_staticText21.Wrap(-1)

        bSizer9.Add(self.m_staticText21, 0, wx.ALL, 5)

        self.m_textCtrl17 = wx.TextCtrl(self, wx.ID_ANY, wx.EmptyString, wx.DefaultPosition, wx.Size(70, -1), 0)
        bSizer9.Add(self.m_textCtrl17, 0, wx.ALL, 5)

        self.m_staticText23 = wx.StaticText(self, wx.ID_ANY, u"通道15：", wx.DefaultPosition, wx.DefaultSize, 0)
        self.m_staticText23.Wrap(-1)

        bSizer9.Add(self.m_staticText23, 0, wx.ALL, 5)

        self.m_textCtrl18 = wx.TextCtrl(self, wx.ID_ANY, wx.EmptyString, wx.DefaultPosition, wx.Size(70, -1), 0)
        bSizer9.Add(self.m_textCtrl18, 0, wx.ALL, 5)

        self.m_staticText24 = wx.StaticText(self, wx.ID_ANY, u"通道16：", wx.DefaultPosition, wx.DefaultSize, 0)
        self.m_staticText24.Wrap(-1)

        bSizer9.Add(self.m_staticText24, 0, wx.ALL, 5)

        self.m_textCtrl19 = wx.TextCtrl(self, wx.ID_ANY, wx.EmptyString, wx.DefaultPosition, wx.Size(70, -1), 0)
        bSizer9.Add(self.m_textCtrl19, 0, wx.ALL, 5)

        self.m_staticText25 = wx.StaticText(self, wx.ID_ANY, u"通道17：", wx.DefaultPosition, wx.DefaultSize, 0)
        self.m_staticText25.Wrap(-1)

        bSizer9.Add(self.m_staticText25, 0, wx.ALL, 5)

        self.m_textCtrl20 = wx.TextCtrl(self, wx.ID_ANY, wx.EmptyString, wx.DefaultPosition, wx.Size(70, -1), 0)
        bSizer9.Add(self.m_textCtrl20, 0, wx.ALL, 5)

        self.m_staticText26 = wx.StaticText(self, wx.ID_ANY, u"通道18：", wx.DefaultPosition, wx.DefaultSize, 0)
        self.m_staticText26.Wrap(-1)

        bSizer9.Add(self.m_staticText26, 0, wx.ALL, 5)

        self.m_textCtrl21 = wx.TextCtrl(self, wx.ID_ANY, wx.EmptyString, wx.DefaultPosition, wx.Size(70, -1), 0)
        bSizer9.Add(self.m_textCtrl21, 0, wx.ALL, 5)

        bSizer1.Add(bSizer9, 0, wx.EXPAND, 5)

        bSizer13 = wx.BoxSizer(wx.HORIZONTAL)

        self.m_staticText27 = wx.StaticText(self, wx.ID_ANY, u"通道19：", wx.DefaultPosition, wx.DefaultSize, 0)
        self.m_staticText27.Wrap(-1)

        bSizer13.Add(self.m_staticText27, 0, wx.ALL, 5)

        self.m_textCtrl22 = wx.TextCtrl(self, wx.ID_ANY, wx.EmptyString, wx.DefaultPosition, wx.Size(70, -1), 0)
        bSizer13.Add(self.m_textCtrl22, 0, wx.ALL, 5)

        self.m_staticText28 = wx.StaticText(self, wx.ID_ANY, u"通道20：", wx.DefaultPosition, wx.DefaultSize, 0)
        self.m_staticText28.Wrap(-1)

        bSizer13.Add(self.m_staticText28, 0, wx.ALL, 5)

        self.m_textCtrl23 = wx.TextCtrl(self, wx.ID_ANY, wx.EmptyString, wx.DefaultPosition, wx.Size(70, -1), 0)
        bSizer13.Add(self.m_textCtrl23, 0, wx.ALL, 5)

        self.m_staticText29 = wx.StaticText(self, wx.ID_ANY, u"通道21：", wx.DefaultPosition, wx.DefaultSize, 0)
        self.m_staticText29.Wrap(-1)

        bSizer13.Add(self.m_staticText29, 0, wx.ALL, 5)

        self.m_textCtrl24 = wx.TextCtrl(self, wx.ID_ANY, wx.EmptyString, wx.DefaultPosition, wx.Size(70, -1), 0)
        bSizer13.Add(self.m_textCtrl24, 0, wx.ALL, 5)

        self.m_staticText30 = wx.StaticText(self, wx.ID_ANY, u"通道22：", wx.DefaultPosition, wx.DefaultSize, 0)
        self.m_staticText30.Wrap(-1)

        bSizer13.Add(self.m_staticText30, 0, wx.ALL, 5)

        self.m_textCtrl25 = wx.TextCtrl(self, wx.ID_ANY, wx.EmptyString, wx.DefaultPosition, wx.Size(70, -1), 0)
        bSizer13.Add(self.m_textCtrl25, 0, wx.ALL, 5)

        self.m_staticText31 = wx.StaticText(self, wx.ID_ANY, u"通道23：", wx.DefaultPosition, wx.DefaultSize, 0)
        self.m_staticText31.Wrap(-1)

        bSizer13.Add(self.m_staticText31, 0, wx.ALL, 5)

        self.m_textCtrl26 = wx.TextCtrl(self, wx.ID_ANY, wx.EmptyString, wx.DefaultPosition, wx.Size(70, -1), 0)
        bSizer13.Add(self.m_textCtrl26, 0, wx.ALL, 5)

        self.m_staticText32 = wx.StaticText(self, wx.ID_ANY, u"通道24：", wx.DefaultPosition, wx.DefaultSize, 0)
        self.m_staticText32.Wrap(-1)

        bSizer13.Add(self.m_staticText32, 0, wx.ALL, 5)

        self.m_textCtrl27 = wx.TextCtrl(self, wx.ID_ANY, wx.EmptyString, wx.DefaultPosition, wx.Size(70, -1), 0)
        bSizer13.Add(self.m_textCtrl27, 0, wx.ALL, 5)

        bSizer1.Add(bSizer13, 0, wx.EXPAND, 5)

        bSizer12 = wx.BoxSizer(wx.HORIZONTAL)

        self.m_staticText34 = wx.StaticText(self, wx.ID_ANY, u"ID:", wx.DefaultPosition, wx.DefaultSize, 0)
        self.m_staticText34.Wrap(-1)

        bSizer12.Add(self.m_staticText34, 0, wx.ALL, 5)

        self.m_textCtrl30 = wx.TextCtrl(self, wx.ID_ANY, wx.EmptyString, wx.DefaultPosition, wx.DefaultSize, 0)
        bSizer12.Add(self.m_textCtrl30, 0, wx.ALL, 5)

        self.m_button7 = wx.Button(self, wx.ID_ANY, u"零序有效值计算", wx.DefaultPosition, wx.Size(90, -1), 0)
        bSizer12.Add(self.m_button7, 0, wx.ALL, 5)
        self.m_button7.Bind(wx.EVT_BUTTON, self.zero_var_cal)

        self.m_staticText35 = wx.StaticText(self, wx.ID_ANY, u"计算点个数：", wx.DefaultPosition, wx.Size(75, -1), 0)
        self.m_staticText35.Wrap(-1)

        bSizer12.Add(self.m_staticText35, 0, wx.ALL, 5)

        self.m_textCtrl29 = wx.TextCtrl(self, wx.ID_ANY, u'200', wx.DefaultPosition, wx.Size(70, -1), 0)
        bSizer12.Add(self.m_textCtrl29, 0, wx.ALL, 5)

        self.m_button8 = wx.Button(self, wx.ID_ANY, u"有功计算", wx.DefaultPosition, wx.DefaultSize, 0)
        bSizer12.Add(self.m_button8, 0, wx.ALL, 5)
        self.m_button8.Bind(wx.EVT_BUTTON, self.show_power_calculation)

        self.m_textCtrl38 = wx.TextCtrl(self, wx.ID_ANY, u"请填入ID起始值", wx.DefaultPosition, wx.DefaultSize, 0)
        self.m_textCtrl38.SetForegroundColour(wx.SystemSettings.GetColour(wx.SYS_COLOUR_HIGHLIGHT))
        bSizer12.Add(self.m_textCtrl38, 0, wx.ALL, 5)

        self.m_button11 = wx.Button(self, wx.ID_ANY, u"ID起始绘制", wx.DefaultPosition, wx.DefaultSize, 0)
        self.m_button11.SetBackgroundColour(wx.SystemSettings.GetColour(wx.SYS_COLOUR_HIGHLIGHT))
        bSizer12.Add(self.m_button11, 0, wx.ALL, 5)
        self.m_button11.Bind(wx.EVT_BUTTON, self.id_plot)

        self.m_staticText40 = wx.StaticText(self, wx.ID_ANY, u"有功最大值通道为：", wx.DefaultPosition, wx.DefaultSize,
                                            0)
        self.m_staticText40.Wrap(-1)

        bSizer12.Add(self.m_staticText40, 0, wx.ALL, 5)

        self.m_textCtrl35 = wx.TextCtrl(self, wx.ID_ANY, wx.EmptyString, wx.DefaultPosition, wx.Size(35, -1), 0)
        bSizer12.Add(self.m_textCtrl35, 0, wx.ALL, 5)

        self.m_button81 = wx.Button(self, wx.ID_ANY, u"时间轴绘制", wx.DefaultPosition, wx.DefaultSize, 0)
        self.m_button81.SetBackgroundColour(wx.SystemSettings.GetColour(wx.SYS_COLOUR_HIGHLIGHT))
        bSizer12.Add(self.m_button81, 0, wx.ALL, 5)
        self.m_button81.Bind(wx.EVT_BUTTON, self.draw_time_plots)
        bSizer1.Add(bSizer12, 1, wx.EXPAND, 5)

        bSizer14 = wx.BoxSizer(wx.VERTICAL)

        bSizer1.Add(bSizer14, 0, wx.EXPAND, 5)

        bSizer10 = wx.BoxSizer(wx.VERTICAL)

        bSizer1.Add(bSizer10, 1, wx.EXPAND, 5)

        bSizer11 = wx.BoxSizer(wx.HORIZONTAL)

        self.m_grid1 = wx.grid.Grid(self, wx.ID_ANY, wx.DefaultPosition, wx.Size(350, -1), 0)

        # Grid
        self.m_grid1.CreateGrid(22, 3)
        self.m_grid1.EnableEditing(False)
        self.m_grid1.EnableGridLines(True)
        self.m_grid1.EnableDragGridSize(False)
        self.m_grid1.SetMargins(0, 0)

        # Columns
        self.m_grid1.SetColSize(0, 70)
        self.m_grid1.SetColSize(1, 70)
        self.m_grid1.SetColSize(2, 70)
        self.m_grid1.AutoSizeColumns(True)
        self.m_grid1.EnableDragColMove(False)
        self.m_grid1.EnableDragColSize(True)
        self.m_grid1.SetColLabelAlignment(wx.ALIGN_CENTER, wx.ALIGN_CENTER)

        # Rows
        self.m_grid1.SetRowLabelSize(wx.grid.GRID_AUTOSIZE)
        self.m_grid1.AutoSizeRows()
        self.m_grid1.EnableDragRowSize(True)
        self.m_grid1.SetRowLabelAlignment(wx.ALIGN_LEFT, wx.ALIGN_CENTER)

        # Label Appearance
        # self.m_grid1.SetLabelBackgroundColour(wx.SystemSettings.GetColour(wx.SYS_COLOUR_HIGHLIGHT))

        # Cell Defaults 显示绘图开始时间
        self.m_grid1.SetDefaultCellAlignment(wx.ALIGN_LEFT, wx.ALIGN_TOP)
        self.m_grid1.SetBackgroundColour(wx.Colour(128, 128, 255))
        self.m_grid1.Bind(gridlib.EVT_GRID_CELL_LEFT_CLICK, self.cell_left_click)
        bSizer11.Add(self.m_grid1, 0, wx.ALL, 5)

        self.m_panel1 = wx.Panel(self, wx.ID_ANY, wx.DefaultPosition, wx.DefaultSize, wx.TAB_TRAVERSAL)
        self.m_panel1.SetForegroundColour(wx.SystemSettings.GetColour(wx.SYS_COLOUR_BTNFACE))
        self.m_panel1.SetBackgroundColour(wx.SystemSettings.GetColour(wx.SYS_COLOUR_INFOBK))

        bSizer11.Add(self.m_panel1, 1, wx.EXPAND | wx.ALL, 5)

        self.figure = plt.figure()
        self.canvas = FigureCanvas(self.m_panel1, -1, self.figure)

        bSizer1.Add(bSizer11, 1, wx.EXPAND, 5)

        self.SetSizer(bSizer1)
        self.Layout()

        self.Centre(wx.BOTH)

    def __del__(self):
        pass

    def select_database_ID(self, event):

        data_value = self.m_textCtrl31.GetValue()
        time_np_start = np.datetime64(data_value)
        # print(time_np_start)
        # # 纳秒的增加
        add_tim_np = 40000000
        delta_np = np.timedelta64(add_tim_np, 'ns')
        new_time_np = time_np_start + delta_np
        # print(new_time_np)
        # # 去除时间字符串中的T字母（此处为timedelta64中解决时间问题的方式）
        new_time_str = str(str(new_time_np).replace('T', ' '))

        # # print(new_time_str)
        #
        file_path = self.m_filePicker2.GetPath()
        conn = sqlite3.connect(file_path)
        cursor = conn.cursor()
        # # query = f"SELECT id, desc, time FROM check_record "
        # # sqlit3 使用sql语言进行模糊查询拼接方式不一样
        query = f"SELECT id FROM data_record  WHERE time BETWEEN '{data_value}' AND '{new_time_str}' "
        # # 执行查询
        cursor.execute(query)
        # # 获取查询结果
        result_id = cursor.fetchall()
        conn.close()
        # # 显示Id值
        self.m_textCtrl30.SetValue(str(result_id[0][0]))

    def cal_var(self, event):
        desc_value = self.m_textCtrl30.GetValue()
        desc_cal_add = self.m_textCtrl37.GetValue()
        # print(int(desc_cal_add))
        desc_value_end = str(int(desc_value) + int(desc_cal_add))
        ch_val = self.m_textCtrl32.GetValue()
        file_path = self.m_filePicker2.GetPath()
        conn = sqlite3.connect(file_path)
        cursor = conn.cursor()
        # query = f"SELECT id, desc, time FROM check_record "
        # 拼接选择框
        cha_val = 'ch' + f'{ch_val}' + '_val'

        # sqlit3 使用sql语言进行模糊查询拼接方式不一样
        query = f"SELECT {cha_val} FROM data_record  WHERE id >= '{desc_value}' AND id <= '{desc_value_end}' "
        # 执行查询
        cursor.execute(query)
        # 获取查询结果
        result_var = cursor.fetchall()
        conn.close()
        # print(result1)
        # 显示Id值
        # self.m_textCtrl10.SetValue(str(result1[0][0]))
        square_list = [(list[0] ** 2) for list in result_var]
        sum_var = math.sqrt(sum(square_list[:int(desc_cal_add)]) / int(desc_cal_add))
        sum_var_2 = round(sum_var, 2)
        self.m_textCtrl36.SetValue(str(sum_var_2))

    # 绘制可视化图例
    def draw_plots(self, event):
        data_value = self.m_textCtrl31.GetValue()
        time_np_start = np.datetime64(data_value)
        # # 纳秒的增加
        add_tim_np = 400000000
        delta_np = np.timedelta64(add_tim_np, 'ns')
        new_time_np = time_np_start + delta_np
        # # 去除时间字符串中的T字母（此处为timedelta64中解决时间问题的方式）
        new_time_str = str(str(new_time_np).replace('T', ' '))
        # # new_time_str = str(new_time_np)
        # # print(new_time_str)
        self.m_textCtrl34.SetValue(str(new_time_str))
        file_path = self.m_filePicker2.GetPath()
        conn = sqlite3.connect(file_path)
        cursor = conn.cursor()
        # # query = f"SELECT id, desc, time FROM check_record "
        # # sqlit3 使用sql语言进行模糊查询拼接方式不一样
        query = f"SELECT * FROM data_record  WHERE time BETWEEN '{data_value}' AND '{new_time_str}' "
        # # 执行查询
        cursor.execute(query)
        # # 获取查询结果
        result_id_list = cursor.fetchall()
        conn.close()

        value1 = self.m_textCtrl1.GetValue()
        value2 = self.m_textCtrl2.GetValue()
        value3 = self.m_textCtrl3.GetValue()
        value4 = self.m_textCtrl32.GetValue()
        x = [result[0] for result in result_id_list]
        y1 = [result[int(value1)] for result in result_id_list]
        y2 = [result[int(value2)] for result in result_id_list]
        y3 = [result[int(value3)] for result in result_id_list]
        y4 = [result[int(value4)] for result in result_id_list]
        # 创建画布和子图
        self.figure.clear()  # 清空之前的图形
        ax = self.figure.add_subplot(111)
        # 绘制曲线
        ax.plot(x, y1, label=value1)
        ax.plot(x, y2, label=value2)
        ax.plot(x, y3, label=value3)
        ax.plot(x, y4, label=value4)
        # 添加图例
        ax.legend()
        # 绘制
        ax.grid(True)
        self.canvas.draw()

    def zero_var_cal(self, event):
        desc_value = self.m_textCtrl30.GetValue()
        desc_cal_add = self.m_textCtrl37.GetValue()
        desc_value_end = str(int(desc_value) + int(desc_cal_add))
        # ch_val = self.m_textCtrl32.GetValue()
        file_path = self.m_filePicker2.GetPath()
        conn = sqlite3.connect(file_path)
        cursor = conn.cursor()
        # query = f"SELECT id, desc, time FROM check_record "
        # 拼接选择框
        # sqlit3 使用sql语言进行模糊查询拼接方式不一样
        query = f"SELECT * FROM data_record  WHERE id >= '{desc_value}' AND id <= '{desc_value_end}' "
        # 执行查询
        cursor.execute(query)
        # 获取查询结果
        result_zero_var = cursor.fetchall()
        conn.close()

        # zero_var_sqrt = [list[0] ** 2 for list in result_zero_var]
        # print(result_zero_var)
        #
        # 1
        zero_var_1 = [(list[1] ** 2) for list in result_zero_var]
        sum1_var = math.sqrt(sum(zero_var_1[:int(desc_cal_add)]) / int(desc_cal_add))
        sum1_var_2 = round(sum1_var, 2)
        self.m_textCtrl4.SetValue(str(sum1_var_2))

        zero_var_2 = [(list[2] ** 2) for list in result_zero_var]
        sum1_var = math.sqrt(sum(zero_var_2[:int(desc_cal_add)]) / int(desc_cal_add))
        sum1_var_2 = round(sum1_var, 2)
        self.m_textCtrl5.SetValue(str(sum1_var_2))

        zero_var_3 = [(list[3] ** 2) for list in result_zero_var]
        sum1_var = math.sqrt(sum(zero_var_3[:int(desc_cal_add)]) / int(desc_cal_add))
        sum1_var_2 = round(sum1_var, 2)
        self.m_textCtrl6.SetValue(str(sum1_var_2))

        zero_var_4 = [(list[4] ** 2) for list in result_zero_var]
        sum1_var = math.sqrt(sum(zero_var_4[:int(desc_cal_add)]) / int(desc_cal_add))
        sum1_var_2 = round(sum1_var, 2)
        self.m_textCtrl7.SetValue(str(sum1_var_2))

        zero_var_5 = [(list[5] ** 2) for list in result_zero_var]
        sum1_var = math.sqrt(sum(zero_var_5[:int(desc_cal_add)]) / int(desc_cal_add))
        sum1_var_2 = round(sum1_var, 2)
        self.m_textCtrl8.SetValue(str(sum1_var_2))

        zero_var_6 = [(list[6] ** 2) for list in result_zero_var]
        sum1_var = math.sqrt(sum(zero_var_6[:int(desc_cal_add)]) / int(desc_cal_add))
        sum1_var_2 = round(sum1_var, 2)
        self.m_textCtrl9.SetValue(str(sum1_var_2))

        zero_var_7 = [(list[7] ** 2) for list in result_zero_var]
        sum1_var = math.sqrt(sum(zero_var_7[:int(desc_cal_add)]) / int(desc_cal_add))
        sum1_var_2 = round(sum1_var, 2)
        self.m_textCtrl10.SetValue(str(sum1_var_2))

        zero_var_8 = [(list[8] ** 2) for list in result_zero_var]
        sum1_var = math.sqrt(sum(zero_var_8[:int(desc_cal_add)]) / int(desc_cal_add))
        sum1_var_2 = round(sum1_var, 2)
        self.m_textCtrl11.SetValue(str(sum1_var_2))

        zero_var_9 = [(list[9] ** 2) for list in result_zero_var]
        sum1_var = math.sqrt(sum(zero_var_9[:int(desc_cal_add)]) / int(desc_cal_add))
        sum1_var_2 = round(sum1_var, 2)
        self.m_textCtrl12.SetValue(str(sum1_var_2))

        zero_var_10 = [(list[10] ** 2) for list in result_zero_var]
        sum1_var = math.sqrt(sum(zero_var_10[:int(desc_cal_add)]) / int(desc_cal_add))
        sum1_var_2 = round(sum1_var, 2)
        self.m_textCtrl13.SetValue(str(sum1_var_2))

        zero_var_11 = [(list[11] ** 2) for list in result_zero_var]
        sum1_var = math.sqrt(sum(zero_var_11[:int(desc_cal_add)]) / int(desc_cal_add))
        sum1_var_2 = round(sum1_var, 2)
        self.m_textCtrl14.SetValue(str(sum1_var_2))

        zero_var_12 = [(list[12] ** 2) for list in result_zero_var]
        sum1_var = math.sqrt(sum(zero_var_12[:int(desc_cal_add)]) / int(desc_cal_add))
        sum1_var_2 = round(sum1_var, 2)
        self.m_textCtrl15.SetValue(str(sum1_var_2))

        zero_var_13 = [(list[13] ** 2) for list in result_zero_var]
        sum1_var = math.sqrt(sum(zero_var_13[:int(desc_cal_add)]) / int(desc_cal_add))
        sum1_var_2 = round(sum1_var, 2)
        self.m_textCtrl16.SetValue(str(sum1_var_2))

        zero_var_14 = [(list[14] ** 2) for list in result_zero_var]
        sum1_var = math.sqrt(sum(zero_var_14[:int(desc_cal_add)]) / int(desc_cal_add))
        sum1_var_2 = round(sum1_var, 2)
        self.m_textCtrl17.SetValue(str(sum1_var_2))

        zero_var_15 = [(list[15] ** 2) for list in result_zero_var]
        sum1_var = math.sqrt(sum(zero_var_15[:int(desc_cal_add)]) / int(desc_cal_add))
        sum1_var_2 = round(sum1_var, 2)
        self.m_textCtrl18.SetValue(str(sum1_var_2))

        zero_var_16 = [(list[16] ** 2) for list in result_zero_var]
        sum1_var = math.sqrt(sum(zero_var_16[:int(desc_cal_add)]) / int(desc_cal_add))
        sum1_var_2 = round(sum1_var, 2)
        self.m_textCtrl19.SetValue(str(sum1_var_2))

        zero_var_17 = [(list[17] ** 2) for list in result_zero_var]
        sum1_var = math.sqrt(sum(zero_var_17[:int(desc_cal_add)]) / int(desc_cal_add))
        sum1_var_2 = round(sum1_var, 2)
        self.m_textCtrl20.SetValue(str(sum1_var_2))

        zero_var_18 = [(list[18] ** 2) for list in result_zero_var]
        sum1_var = math.sqrt(sum(zero_var_18[:int(desc_cal_add)]) / int(desc_cal_add))
        sum1_var_2 = round(sum1_var, 2)
        self.m_textCtrl21.SetValue(str(sum1_var_2))

        zero_var_19 = [(list[19] ** 2) for list in result_zero_var]
        sum1_var = math.sqrt(sum(zero_var_19[:int(desc_cal_add)]) / int(desc_cal_add))
        sum1_var_2 = round(sum1_var, 2)
        self.m_textCtrl22.SetValue(str(sum1_var_2))

        zero_var_20 = [(list[20] ** 2) for list in result_zero_var]
        sum1_var = math.sqrt(sum(zero_var_20[:int(desc_cal_add)]) / int(desc_cal_add))
        sum1_var_2 = round(sum1_var, 2)
        self.m_textCtrl23.SetValue(str(sum1_var_2))

        zero_var_21 = [(list[21] ** 2) for list in result_zero_var]
        sum1_var = math.sqrt(sum(zero_var_21[:int(desc_cal_add)]) / int(desc_cal_add))
        sum1_var_2 = round(sum1_var, 2)
        self.m_textCtrl24.SetValue(str(sum1_var_2))

        zero_var_22 = [(list[22] ** 2) for list in result_zero_var]
        sum1_var = math.sqrt(sum(zero_var_22[:int(desc_cal_add)]) / int(desc_cal_add))
        sum1_var_2 = round(sum1_var, 2)
        self.m_textCtrl25.SetValue(str(sum1_var_2))

        zero_var_23 = [(list[23] ** 2) for list in result_zero_var]
        sum1_var = math.sqrt(sum(zero_var_23[:int(desc_cal_add)]) / int(desc_cal_add))
        sum1_var_2 = round(sum1_var, 2)
        self.m_textCtrl26.SetValue(str(sum1_var_2))

        zero_var_24 = [(list[24] ** 2) for list in result_zero_var]
        sum1_var = math.sqrt(sum(zero_var_24[:int(desc_cal_add)]) / int(desc_cal_add))
        sum1_var_2 = round(sum1_var, 2)
        self.m_textCtrl27.SetValue(str(sum1_var_2))

        # zero_var_24 = [(list[0] ** 2) for list in result_zero_var]
        # sum1_var = math.sqrt(sum(zero_var_24[:int(desc_cal_add)]) / int(desc_cal_add))
        # sum1_var_2 = round(sum1_var, 2)
        # self.m_textCtrl28.SetValue(str(sum1_var_2))

    # 将数据库app.sqlit3的数据库可视化
    def write_tables_grids(self, event):
        app_date = self.m_filePicker1.GetPath()
        # 连接到数据库
        conn = sqlite3.connect(app_date)
        cursor = conn.cursor()
        query = f"SELECT ch, desc, time FROM check_record "
        # 执行查询
        cursor.execute(query)
        # 获取查询结果
        result1 = cursor.fetchall()
        self.m_grid1.ClearGrid()
        self.m_grid1.SetColLabelValue(0, u"线路")
        self.m_grid1.SetColLabelValue(1, u"类型")
        self.m_grid1.SetColLabelValue(2, u"数据库写入时间")

        for row_num, row_data in enumerate(result1):
            self.m_grid1.AppendRows()
            for col_num, value in enumerate(row_data):
                self.m_grid1.SetCellValue(row_num, col_num, str(value))
        self.m_grid1.AutoSizeColumns()
        # 关闭数据库连接
        conn.close()

    def cell_left_click(self, event):
        global value
        # grid = event.GetEventObject()
        row = event.GetRow()
        col = event.GetCol()
        value = self.m_grid1.GetCellValue(row, col)
        self.m_textCtrl31.SetValue(value)

    # 显示有功计算值
    def show_power_calculation(self, event):
        desc_value_power = self.m_textCtrl30.GetValue()

        desc_power_add = self.m_textCtrl29.GetValue()

        desc_power_end = str(int(desc_value_power) + int(desc_power_add))

        file_path = self.m_filePicker2.GetPath()
        conn = sqlite3.connect(file_path)
        cursor = conn.cursor()
        # query = f"SELECT id, desc, time FROM check_record "
        # 拼接选择框
        # sqlit3 使用sql语言进行模糊查询拼接方式不一样
        query = f"SELECT ch1_val ,ch2_val, ch3_val, ch4_val,ch5_val,ch6_val,ch7_val,ch8_val,ch9_val,ch10_val,ch11_val,ch12_val,ch13_val,ch14_val,ch15_val,ch16_val,ch17_val,ch18_val,ch19_val,ch20_val,ch21_val,ch22_val,ch23_val,ch24_val FROM data_record  WHERE id >= '{desc_value_power}' AND id <= '{desc_power_end}' "
        # 执行查询
        row_i = cursor.execute(query)
        row_i0 = row_i.fetchall()
        # 获取查询结果

        cursor_u = cursor.execute(
            f"SELECT ch32_val FROM data_record WHERE id >= '{desc_value_power}' AND id <=  '{desc_power_end}'")
        rows_u0 = cursor_u.fetchall()

        conn.close()

        matrix_i0 = np.array(row_i0)
        # print(matrix_i0)
        matrix_u0 = np.array(rows_u0)

        # sum_all = (matrix_i0-matrix_0) * matrix_u0
        sum_all = matrix_i0 * matrix_u0
        # print(sum_all)

        # axis = 0 计算列累加
        rows_sum = sum_all.sum(axis=0)
        # print(rows_sum)
        rows_sum_list = rows_sum.tolist()
        self.m_textCtrl4.SetValue(str(round(rows_sum_list[0], 2)))
        self.m_textCtrl5.SetValue(str(round(rows_sum_list[1], 2)))
        self.m_textCtrl6.SetValue(str(round(rows_sum_list[2], 2)))
        self.m_textCtrl7.SetValue(str(round(rows_sum_list[3], 2)))
        self.m_textCtrl8.SetValue(str(round(rows_sum_list[4], 2)))
        self.m_textCtrl9.SetValue(str(round(rows_sum_list[5], 2)))
        self.m_textCtrl10.SetValue(str(round(rows_sum_list[6], 2)))
        self.m_textCtrl11.SetValue(str(round(rows_sum_list[7], 2)))
        self.m_textCtrl12.SetValue(str(round(rows_sum_list[8], 2)))
        self.m_textCtrl13.SetValue(str(round(rows_sum_list[9], 2)))
        self.m_textCtrl14.SetValue(str(round(rows_sum_list[10], 2)))
        self.m_textCtrl15.SetValue(str(round(rows_sum_list[11], 2)))
        self.m_textCtrl16.SetValue(str(round(rows_sum_list[12], 2)))
        self.m_textCtrl17.SetValue(str(round(rows_sum_list[13], 2)))
        self.m_textCtrl18.SetValue(str(round(rows_sum_list[14], 2)))
        self.m_textCtrl19.SetValue(str(round(rows_sum_list[15], 2)))
        self.m_textCtrl20.SetValue(str(round(rows_sum_list[16], 2)))
        self.m_textCtrl21.SetValue(str(round(rows_sum_list[17], 2)))
        self.m_textCtrl22.SetValue(str(round(rows_sum_list[18], 2)))
        self.m_textCtrl23.SetValue(str(round(rows_sum_list[19], 2)))
        self.m_textCtrl24.SetValue(str(round(rows_sum_list[20], 2)))
        self.m_textCtrl25.SetValue(str(round(rows_sum_list[21], 2)))
        self.m_textCtrl26.SetValue(str(round(rows_sum_list[22], 2)))
        self.m_textCtrl27.SetValue(str(round(rows_sum_list[23], 2)))

        abs_max = max(rows_sum_list, key=abs)
        index = rows_sum_list.index(abs_max)

        self.m_textCtrl35.SetValue(str(index + 1))

    def id_plot(self, event):
        start_id = self.m_textCtrl38.GetValue()

        end_id = str(int(start_id) + 800)
        file_path = self.m_filePicker2.GetPath()
        conn = sqlite3.connect(file_path)
        cursor = conn.cursor()
        query = f"SELECT * FROM data_record  WHERE id BETWEEN '{start_id}' AND '{end_id}' "
        # # 执行查询
        cursor.execute(query)
        # # 获取查询结果
        result_id_list = cursor.fetchall()
        conn.close()

        value1 = self.m_textCtrl1.GetValue()
        value2 = self.m_textCtrl2.GetValue()
        value3 = self.m_textCtrl3.GetValue()
        value4 = self.m_textCtrl32.GetValue()
        x = [result[0] for result in result_id_list]
        y1 = [result[int(value1)] for result in result_id_list]
        y2 = [result[int(value2)] for result in result_id_list]
        y3 = [result[int(value3)] for result in result_id_list]
        y4 = [result[int(value4)] for result in result_id_list]
        # 创建画布和子图
        self.figure.clear()  # 清空之前的图形
        ax = self.figure.add_subplot(111)
        # 绘制曲线
        ax.plot(x, y1, label=value1)
        ax.plot(x, y2, label=value2)
        ax.plot(x, y3, label=value3)
        ax.plot(x, y4, label=value4)
        # 添加图例
        ax.legend()
        # 绘制
        ax.grid(True)
        self.canvas.draw()

    def draw_time_plots(self, event):
        draw_start = self.m_textCtrl31.GetValue()
        draw_end = self.m_textCtrl34.GetValue()

        file_path = self.m_filePicker2.GetPath()
        conn = sqlite3.connect(file_path)
        cursor = conn.cursor()
        # # query = f"SELECT id, desc, time FROM check_record "
        # # sqlit3 使用sql语言进行模糊查询拼接方式不一样
        query = f"SELECT * FROM data_record  WHERE time BETWEEN '{draw_start}' AND '{draw_end}' "
        # # 执行查询
        cursor.execute(query)
        # # 获取查询结果
        result_id_list = cursor.fetchall()
        conn.close()

        value1 = self.m_textCtrl1.GetValue()
        value2 = self.m_textCtrl2.GetValue()
        value3 = self.m_textCtrl3.GetValue()
        value4 = self.m_textCtrl32.GetValue()
        x = [result[0] for result in result_id_list]
        y1 = [result[int(value1)] for result in result_id_list]
        y2 = [result[int(value2)] for result in result_id_list]
        y3 = [result[int(value3)] for result in result_id_list]
        y4 = [result[int(value4)] for result in result_id_list]
        # 创建画布和子图
        self.figure.clear()  # 清空之前的图形
        ax = self.figure.add_subplot(111)
        # 绘制曲线
        ax.plot(x, y1, label=value1)
        ax.plot(x, y2, label=value2)
        ax.plot(x, y3, label=value3)
        ax.plot(x, y4, label=value4)
        # 添加图例
        ax.legend()
        # 绘制
        ax.grid(True)
        self.canvas.draw()


if __name__ == '__main__':
    # 创建应用程序对象
    app = wx.App()

    # 创建主窗口对象
    frame = MyFrame1(None, '可视化绘图窗口')

    # 显示主窗口
    frame.Show(True)

    # 启动事件循环
    app.MainLoop()
