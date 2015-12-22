import os
import webbrowser

__author__ = 'Amar Kalabic - www.amarkalabic.me'

# Image meta-data scraper

import wx
import wx.grid as gridlib
from PIL import Image
from PIL.ExifTags import TAGS

TASK_RANGE = 100


class MetaDataScraper(wx.Frame):
    def __init__(self, *args, **kw):
        super(MetaDataScraper, self).__init__(*args, **kw)

        self.InitUI()

    def InitUI(self):

        self.timer = wx.Timer(self, 1)
        self.count = 0

        self.Bind(wx.EVT_TIMER, self.OnTimer, self.timer)

        pnl = wx.Panel(self)

        ico = wx.Icon('img/logo.ico', wx.BITMAP_TYPE_ICO)
        self.SetIcon(ico)

        vbox = wx.BoxSizer(wx.VERTICAL)
        hbox1 = wx.BoxSizer(wx.HORIZONTAL)
        hbox2 = wx.BoxSizer(wx.HORIZONTAL)
        hbox3 = wx.BoxSizer(wx.HORIZONTAL)
        hbox4 = wx.BoxSizer(wx.HORIZONTAL)
        hbox5 = wx.BoxSizer(wx.HORIZONTAL)
        hbox6 = wx.BoxSizer(wx.HORIZONTAL)

        self.gauge = wx.Gauge(pnl, range=TASK_RANGE, size=(250, 25))

        ######
        # GRID#
        ######

        self.myGrid = gridlib.Grid(pnl)
        self.myGrid.CreateGrid(10, 1)

        self.myGrid.SetColLabelValue(0, "Data")
        self.myGrid.SetRowLabelValue(0, "File Name")
        self.myGrid.SetRowLabelValue(1, "Device Name")
        self.myGrid.SetRowLabelValue(2, "Height")
        self.myGrid.SetRowLabelValue(3, "Width")
        self.myGrid.SetRowLabelValue(4, "Date")
        self.myGrid.SetRowLabelValue(5, "ISO Speed Ratings")
        self.myGrid.SetRowLabelValue(6, "GPS Info")
        self.myGrid.SetRowLabelValue(7, "Latitude")
        self.myGrid.SetRowLabelValue(8, "Longitude")
        self.myGrid.SetRowLabelValue(9, "Focal Length")
        # non-editable
        self.myGrid.EnableEditing(True)

        self.myGrid.SetColSize(0, 120)
        self.myGrid.SetRowLabelSize(120)

        self.sizer = wx.BoxSizer(wx.VERTICAL)
        self.sizer.Add(self.myGrid, 1, wx.EXPAND)
        pnl.SetSizer(self.sizer)

        #####
        #####

        self.btn1 = wx.Button(pnl, wx.ID_OK)
        self.btn2 = wx.Button(pnl, wx.ID_FIND, label="Google Maps GPS")
        self.btn2.Disable()
        self.btn3 = wx.Button(pnl, wx.ID_FILE, label="Browse")

        self.text = wx.HyperlinkCtrl(pnl, label='Amar Kalabic | web: amarkalabic.me')
        self.text.SetURL("http://amarkalabic.me/")
        style = wx.BORDER_SUNKEN | wx.TE_RICH2
        self.pathspot = wx.TextCtrl(pnl, style=style, size=(400, 20))

        self.Bind(wx.EVT_BUTTON, self.OnOk, self.btn1)
        self.Bind(wx.EVT_BUTTON, self.OnGPS, self.btn2)
        self.Bind(wx.EVT_BUTTON, self.OnBrowse, self.btn3)

        hbox6.Add(self.myGrid, proportion=1)
        hbox1.Add(self.gauge, proportion=1, flag=wx.ALIGN_CENTRE)
        hbox2.Add(self.btn1, proportion=1, flag=wx.RIGHT, border=10)
        hbox2.Add(self.btn2, proportion=1)
        hbox3.Add(self.text, proportion=1)
        hbox4.Add(self.pathspot, proportion=1, border=10)
        hbox5.Add(self.btn3, proportion=1)

        vbox.Add((0, 50))
        vbox.Add(hbox6, proportion=5, flag=wx.ALIGN_CENTER)
        vbox.Add((0, 20))
        vbox.Add(hbox1, flag=wx.ALIGN_CENTRE)
        vbox.Add((0, 20))
        vbox.Add(hbox2, proportion=1, flag=wx.ALIGN_CENTRE)
        vbox.Add(hbox3, proportion=1, flag=wx.ALIGN_CENTRE)
        vbox.Add(hbox4, proportion=1, flag=wx.ALIGN_CENTER)
        vbox.Add(hbox5, proportion=1, flag=wx.ALIGN_CENTER)

        pnl.SetSizer(vbox)

        self.SetSize((1200, 600))
        self.SetTitle('Image Meta Data Scraper')
        self.Centre()
        self.Show(True)

    def OnBrowse(self, e):
        wildcard = "JPG, TIF and WAV files (*.jpp;*.tif;*.wav)|*.jpg;*.tif;*wav"
        openFileDialog = wx.FileDialog(self, "Choose Image/Wav File", "", "",
                                       wildcard, wx.FD_OPEN | wx.FD_FILE_MUST_EXIST)

        if openFileDialog.ShowModal() == wx.ID_CANCEL:
            return  # the user changed idea...

        self.pathspot.SetValue(str(openFileDialog.GetPath()))

    def OnOk(self, e):

        # Scraping starts here
        path = self.pathspot.GetValue()
        metaData = {}
        if (path) or (path != ""):
            if os.path.isfile(path):
                try:

                    img = Image.open(path)
                    if img._getexif() != None:
                        metaData = {
                            TAGS[k]: v
                            for k, v in img._getexif().items()
                            if k in TAGS
                            }
                        filename = path.split(os.sep)

                        self.myGrid.SetCellValue(0, 0, str(filename[-1]))
                        if self.count >= TASK_RANGE:
                            return

                        self.timer.Start(20)
                        self.text.SetLabel('Fetching meta-data...')
                        if metaData.has_key("Model"):
                            self.myGrid.SetCellValue(1, 0, str(metaData.get("Model")))
                        else:
                            self.myGrid.SetCellValue(1, 0, "Unknown")

                        if metaData.has_key("ExifImageHeight"):
                            self.myGrid.SetCellValue(2, 0, str(metaData.get("ExifImageHeight")))
                        else:
                            self.myGrid.SetCellValue(2, 0, "Unknown")

                        if metaData.has_key("ExifImageWidth"):
                            self.myGrid.SetCellValue(3, 0, str(metaData.get("ExifImageWidth")))
                        else:
                            self.myGrid.SetCellValue(3, 0, "Unknown")

                        if metaData.has_key("DateTimeOriginal"):
                            self.myGrid.SetCellValue(4, 0, str(metaData.get("DateTimeOriginal")))
                        else:
                            self.myGrid.SetCellValue(4, 0, "Unknown")

                        if metaData.has_key("ISOSpeedRatings"):
                            self.myGrid.SetCellValue(5, 0, str(metaData.get("ISOSpeedRatings")))
                        else:
                            self.myGrid.SetCellValue(5, 0, "Unknown")

                        if metaData.has_key("GPSInfo"):
                            n = metaData.get('GPSInfo', {}).get(2)
                            n_x = n[0][0]
                            n_y = n[1][0]
                            n_z = n[2][0]

                            latitude = int(n_x) + (int(n_y) / 60.0) + (int(n_z) / 3600.0)

                            self.myGrid.SetCellValue(7, 0, str(latitude))
                        else:
                            self.myGrid.SetCellValue(7, 0, "Unknown")

                        if metaData.has_key("GPSInfo"):
                            self.btn2.Enable()
                            ee = metaData.get('GPSInfo', {}).get(4)
                            e_x = ee[0][0]
                            e_y = ee[1][0]
                            e_z = ee[2][0]

                            longitude = int(e_x) + (int(e_y) / 60.0) + (int(e_z) / 3600.0)

                            self.myGrid.SetCellValue(8, 0, str(longitude))
                        else:
                            self.myGrid.SetCellValue(8, 0, "Unknown")

                        if metaData.has_key("FocalLength"):
                            self.myGrid.SetCellValue(9, 0, str(metaData.get("FocalLength")))
                        else:
                            self.myGrid.SetCellValue(9, 0, "Unknown")
                    else:
                        wx.MessageDialog(self, style=wx.OK | wx.ICON_ERROR,
                                 message="This image doesn't contain any meta-data or it can't be seen. Sorry! ",
                                 caption="Error!").ShowModal()
                except Exception, e:
                    print e
            else:
                wx.MessageDialog(self, style=wx.OK | wx.ICON_ERROR,
                                 message="This path doesn't exist. Please choose valid path.",
                                 caption="Error!").ShowModal()
        else:
            print "error"
            wx.MessageDialog(self, style=wx.OK | wx.ICON_ERROR, message="Please choose path.",
                                        caption="Error!").ShowModal()
        return True

    def OnGPS(self, e):
        #https://www.google.ba/maps/search
        link= "https://www.google.ba/maps/search/" + str(self.myGrid.GetCellValue(7, 0)) + ",+" + str(self.myGrid.GetCellValue(8, 0))
        webbrowser.open_new_tab(url=link)




    def OnTimer(self, e):

        self.count = self.count + 1
        self.gauge.SetValue(self.count)

        if self.count == TASK_RANGE:
            self.timer.Stop()
            self.text.SetLabel('Meta-data fetched!')


def main():
    ex = wx.App()
    MetaDataScraper(None)
    ex.MainLoop()


if __name__ == '__main__':
    main()
