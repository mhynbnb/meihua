from typing import Callable, Union

import requests
from bs4 import BeautifulSoup
import datetime
import customtkinter as ctk

def get_calenda(date):
    lis=[]
    url = f'https://www.buyiju.com/lhl/{date}.html'
    resp = requests.get(url)
    page=BeautifulSoup(resp.text)

    suit_div=page.find('div',class_='suitable_con huanglisuoyi')
    suit_li=suit_div.find('ul').find_all('li')
    suit=' '.join([li.text for li in suit_li])
    lis.append(['宜',suit])
    # print('宜：\n',suit)

    Notsuit_div=page.find('div',class_='suitable_con huanglisuoji')
    Notsuit_li=Notsuit_div.find('ul').find_all('li')
    Notsuit=' '.join([li.text for li in Notsuit_li])
    # print('忌：\n',Notsuit)
    lis.append(['忌',Notsuit])

    God=page.find_all('div',class_='solar')
    childGod=God[0].text.replace('\n','')
    fiveEle=God[1].text
    # print(childGod,fiveEle)
    lis.append(['胎神',childGod])
    lis.append(['五行',fiveEle])
    jiGodList=page.find_all('div',class_='jishen')[0].find('ul').find_all('li')
    jiGod=' '.join([i.text for i in jiGodList])
    # print('吉神宜趋：\n',jiGod)
    lis.append(['吉神宜趋',jiGod])
    XiongShaYiJiList=page.find_all('div',class_='jishen')[1].find('ul').find_all('li')
    XiongShaYiJi=' '.join([i.text.replace('\n','') for i in XiongShaYiJiList])
    # print('凶煞宜忌：\n',XiongShaYiJi)
    lis.append(['凶煞宜忌',XiongShaYiJi])
    welGodList=page.find_all('ul',class_='cs')[0].find_all('li')
    welGod=' '.join([i.text for i in welGodList])
    # print('财神位：\n',welGod)
    lis.append(['财神位',welGod])
    ChongShaList=page.find_all('ul',class_='cs')[1].find_all('li')
    ChongSha=' '.join([i.text for i in ChongShaList])
    # print('冲煞：\n',ChongSha)
    lis.append(['冲煞',ChongSha])
    date=page.find('div',class_='kalendar_foot').find_all('span')[0].text
    PengZuBaiJi=page.find('div',class_='kalendar_foot').find_all('span')[1].text
    # print(date)
    # print(PengZuBaiJi)
    lis.append(['历',date])
    lis.append(['彭祖百忌',PengZuBaiJi.split(':')[1]])
    dateClendarLunar=page.find('div',class_='kalendar_top').find('h3').text.replace('\n','')
    dateClendarGra=page.find('div',class_='kalendar_top').find('h5').text.replace('\n','')
    # print(dateClendarGra,dateClendarLunar)
    lis.append(['公历',dateClendarLunar])
    lis.append(['农历',dateClendarGra])
    '''时辰吉凶'''
    trLis=page.find('tbody',align='center').find_all('tr')
    data=[[i.text for i in trLis[n].find_all('td')] for n in range(9)]
    #时间 时间范围 时辰 星神 时宜 时忌 冲煞 煞方 时冲
    # print(data)
    return data,lis



class Calendar(ctk.CTkFrame):
    def __init__(self,master:any,command: Union[Callable[[str], None], None] = None,**kwargs,):
        super().__init__(master, **kwargs)
        self.date = datetime.date.today()
        self.current_month = self.date.month
        self.current_year = self.date.year
        self.create_widgets()
        self.command=command

    def _dropdown_callback(self, value: str):
        if self.command is not None:
            self.command(value)
    def create_widgets(self):
        # 绘制月份选择框和左右箭头按钮
        self.month_lbl = ctk.CTkLabel(self, text=self.date.strftime("%B %Y"))
        self.prev_btn = ctk.CTkButton(self, text="<", command=self.prev_month,width=10)
        self.next_btn = ctk.CTkButton(self, text=">", command=self.next_month,width=10)
        self.month_lbl.grid(row=0, column=1, columnspan=2)
        self.prev_btn.grid(row=0, column=0)
        self.next_btn.grid(row=0, column=3)

        # 绘制日历
        self.cal_frame = ctk.CTkFrame(self)
        self.cal_frame.grid(row=1, column=0, columnspan=4)
        self.create_cal()

    def create_cal(self):
        # 计算当前选定月份的第一天和最后一天
        year = self.current_year
        month = self.current_month
        first_day = datetime.date(year, month, 1)
        last_day = datetime.date(year, month + 1, 1) - datetime.timedelta(days=1)

        # 绘制日历表格
        self.days = []
        for i in range(6):
            for j in range(7):
                self.days.append(ctk.CTkLabel(self.cal_frame, text="  ", width=30, height=2,corner_radius=3))
                self.days[-1].grid(row=i + 1, column=j,padx=5,pady=5)

        # 填充日历表格
        day = datetime.timedelta(days=1)
        date = first_day
        index = first_day.weekday()
        while date <= last_day:
            self.days[index].configure(text=str(date.day))
            if date == self.date:
                self.days[index].configure(fg_color="#1F69A4")
            self.days[index].bind("<Button-1>", self.select_date)
            date += day
            index += 1

    def prev_month(self):
        # 上个月
        if self.current_month == 1:
            self.current_month = 12
            self.current_year -= 1
        else:
            self.current_month -= 1

        self.date = datetime.date(self.current_year, self.current_month, 1)
        self.month_lbl.configure(text=self.date.strftime("%B %Y"))
        self.create_cal()

    def next_month(self):
        # 下个月
        if self.current_month == 12:
            self.current_month = 1
            self.current_year += 1
        else:
            self.current_month += 1

        self.date = datetime.date(self.current_year, self.current_month, 1)
        self.month_lbl.configure(text=self.date.strftime("%B %Y"))
        self.create_cal()
    def select_date(self, event=None):
        # 选择日期
        clicked = event.widget
        day = int(clicked.configure("text")[-1])
        self.date = datetime.date(self.current_year, self.current_month, day)
        # print(self.date)
        # self.click=1
        self.command()
        self.create_cal()

    def get_date(self):
        # 获取选择的日期
        return self.date

