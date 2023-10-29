import tkinter
import requests
import tkinter.messagebox
from tkinter import INSERT
from tkinter.ttk import Combobox
from tkinter import ttk
import sv_ttk
from tinui import TinUI
import json
from tkcalendar import Calendar
import tkcalendar
from datetime import datetime
import datetime as dt
import threading

import date_frame
from caculate import cacu
def thread_it(func, *args):
    t = threading.Thread(target=func, args=args)
    t.setDaemon(True)
    t.start()
ye, mo, da, ho = 2022, 9, 1, 8

def main():
    top = tkinter.Tk()    # 创建顶层窗口
    top.geometry('960x600')    # 设置窗口大小
    top.title('梅花易数')    # 设置窗口标题
    top.resizable(height=False,width=False)
    # top.config(background="white")
    # 正上方“梅花易数”
    label = ttk.Label(top,text='梅花易数',font=('华文行楷',35))
    label.pack()
    #下方文字
    label_word=ttk.Label(top,text='千万不要自己感动自己。大部分人看似的努力，不过是愚蠢导致的。',font=('华文行楷',12))
    label_word.place(x=10,y=570)
    # 时间选择组件容器
    fram_time=ttk.Frame(top)
    def year_select(event):
        global ye, mo, da, ho
        ye=int(cbox_year.get())
    def mon_select(event):
        global ye, mo, da, ho
        mo=int(cbox_mon.get())
        if cbox_mon.get() in ['1', '3', '5', '7', '8', '10', '12']:
            cbox_day['value'] = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12,
                                 13, 14, 15, 16, 17, 18, 19, 20, 21, 22,
                                 23, 24, 25, 26, 27, 28, 29, 30, 31]
        elif cbox_mon.get()=='2':
            cbox_day['value'] = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12,
                                 13, 14, 15, 16, 17, 18, 19, 20, 21, 22,
                                 23, 24, 25, 26, 27, 28, 29]
        else :
            cbox_day['value'] = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12,
                                 13, 14, 15, 16, 17, 18, 19, 20, 21, 22,
                                 23, 24, 25, 26, 27, 28, 29,30]
    def day_select(event):
        global ye, mo, da, ho
        da=int(cbox_day.get())
    def hour_select(event):
        global ye, mo, da, ho
        ho=int(cbox_hour.get())
    label_time=tkinter.Label(fram_time,text='时间：',font=('黑体', 15),fg='white',anchor='w',width=8,height=1)
    label_time.grid(row=0,column=0)

    cbox_year=Combobox(fram_time,width=5)
    cbox_year['value']=[1997, 1998, 1999, 2000, 2001, 2002, 2003,
                        2004, 2005, 2006, 2007, 2008, 2009, 2010,
                        2011, 2012, 2013, 2014, 2015, 2016, 2017,
                        2018, 2019, 2020, 2021, 2022, 2023, 2024,
                        2025, 2026, 2027, 2028, 2029,2030]
    cbox_year.current(25)
    cbox_year.grid(row=1,column=0)
    cbox_year.bind("<<ComboboxSelected>>",year_select)
    label_year = tkinter.Label(fram_time,text='年',font=('黑体', 13),fg='black',width=3, height=1)
    label_year.grid(row=1, column=1)

    cbox_mon = Combobox(fram_time, width=5)
    cbox_mon['value'] = (1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12)
    cbox_mon.current(8)
    cbox_mon.grid(row=1, column=2)
    cbox_mon.bind("<<ComboboxSelected>>", mon_select)
    label_mon = tkinter.Label(fram_time,text='月',font=('黑体', 13),fg='black',width=3, height=1)
    label_mon.grid(row=1, column=3)

    cbox_day = Combobox(fram_time,width=5)
    cbox_day['value'] = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12,
                         13, 14, 15, 16, 17, 18, 19, 20, 21, 22,
                         23, 24, 25, 26, 27, 28, 29, 30,31]
    cbox_day.current(0)
    cbox_day.grid(row=1, column=4)
    cbox_day.bind("<<ComboboxSelected>>",day_select)
    label_day = tkinter.Label(fram_time,text='日',font=('黑体', 13),fg='black',width=3, height=1,)
    label_day.grid(row=1, column=5)

    cbox_hour = Combobox(fram_time, width=5)
    cbox_hour['value'] = [0,1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12,13, 14, 15, 16, 17, 18, 19, 20, 21, 22, 23,]
    cbox_hour.current(7)
    cbox_hour.grid(row=1, column=6)
    cbox_hour.bind("<<ComboboxSelected>>", hour_select)
    label_hour = tkinter.Label(fram_time,text='时',font=('黑体', 13),fg='black',width=3, height=1)
    label_hour.grid(row=1, column=7)

    fram_time.place(x=80, y=70)

    '''按钮容器start'''
    cont=''
    photo1 = tkinter.PhotoImage(file=r".\source\乾.png")
    photo2 = tkinter.PhotoImage(file=r".\source\乾.png")
    #起卦-按钮事件
    def call_run():
        global cont,photo1,photo2
        cont=cacu(ye,mo,da,ho)[0]

        i1=cacu(ye,mo,da,ho)[1]
        i2=cacu(ye,mo,da,ho)[2]
        photo1=tkinter.PhotoImage(file=fr".\source\{i1}.png")
        photo2 = tkinter.PhotoImage(file=fr".\source\{i2}.png")
        content_label.config(text=cont)
        img_label1.config(image=photo1)
        img_label2.config(image=photo2)

        value = cacu(ye,mo,da,ho)[3]
        js_go = open(r".\source\go.json", encoding='utf-8')
        js_go = json.load(js_go)
        txt.delete('1.0', 'end')
        txt.insert(INSERT, value+'\n'+js_go[value])

    #立即起卦-按钮事件
    def call_run_now():
        p = datetime.now()
        year = p.year
        month = p.month
        day = p.day
        hour = int(p.hour)
        global cont,photo1,photo2
        date=str(year)+'年'+str(month)+'月'+str(day)+'日'+str(hour)+'时'
        cont=cacu(year,month,day,hour)[0]+'\n'+date
        i1=cacu(year,month,day,hour)[1]
        i2=cacu(year,month,day,hour)[2]
        photo1=tkinter.PhotoImage(file=fr".\source\{i1}.png")
        photo2 = tkinter.PhotoImage(file=fr".\source\{i2}.png")
        content_label.config(text=cont)
        img_label1.config(image=photo1)
        img_label2.config(image=photo2)
        value = cacu(year, month, day, hour)[3]
        js_go = open(r".\source\go.json", encoding='utf-8')
        js_go = json.load(js_go)
        txt.delete('1.0', 'end')
        txt.insert(INSERT, value+'\n'+js_go[value])
    #万物类象-按钮事件
    def call_world():
        newWindow = tkinter.Toplevel(top)
        newWindow.geometry('580x500')  # 设置窗口大小
        newWindow.title('万物类象')  # 设置窗口标题
        newWindow.resizable(height=False, width=False)
        newWindow.config()
        # 万物类象-查看-按钮事件
        def call_world_btn():

            try:
                value=list_world.get(list_world.curselection())
            except:
                value='乾卦'
            js_world = open(r".\source\world.json", encoding='utf-8')
            js_world = json.load(js_world)
            txt_world.delete('1.0', 'end')
            txt_world.insert(INSERT, value+'\n'+js_world[value])
        #万物类象-查看-按钮
        btn_world_child=ttk.Button(newWindow,text='查看',width=9,command=call_world_btn,)
        btn_world_child.place(x=10,y=170)
        #万物类象-列表框
        list_world = tkinter.Listbox(newWindow,width=14,height=8,font='黑体 11',selectbackground='#2B2B2B',selectforeground='green',highlightcolor='black',activestyle='none',bd=5)
        l = ['乾卦','坤卦','坎卦','艮卦','震卦','离卦','兑卦','巽卦']
        for i, item in enumerate(l):
            list_world.insert(i, item)
        list_world.place(x=10, y=10)
        #万物类象查询结果显示框
        txt_world = tkinter.Text(newWindow, width=48,height=30,undo=True,autoseparators=False,font='黑体 11',foreground='green',wrap='word', bd=5)
        txt_world.insert(INSERT, '查询结果将显示在这里！')
        txt_world.place(x=150, y=10)
    #万年历-按钮事件
    def call_lunar():
        child = tkinter.Toplevel(top)
        child.title('万年历')
        child.resizable(height=False, width=False)
        child.geometry("1520x630")
        rst_txt = tkinter.Text(child, width=32, height=10, undo=True, autoseparators=False, font='黑体 13',
                               foreground='green', wrap='word', bd=5)
        rst_txt.place(x=10, y=130)
        # mindate = dt.date(year=1900, month=1, day=1)
        # maxdate = dt.date(year=2099, month=1, day=1)
        select=tkcalendar.DateEntry(child,width=20)
        select.place(x=10,y=10,)
        # cal = Calendar(child, font="Arial 14", bordercolor='black', selectmode='day', locale='zh_CN', mindate=mindate,
        #                maxdate=maxdate,selectbackground='#1C1C1C',selectforeground='green',
        #                foreground='white',headersbackground='#1C1C1C',headersforeground='white',
        #                normalbackground='#1C1C1C',normalforeground='white',
        #                weekendbackground='#1C1C1C',weekendforeground='white',
        #                othermonthforeground='white',othermonthbackground='#3C3F41',
        #                othermonthwebackground='#3C3F41',othermonthweforeground='white')
        # cal.place(x=10, y=10, width=300, height=200)
        lis1=str(dt.date.today()).split('-')
        lis1[-1].lstrip('0')
        lis1[-2].lstrip('0')
        date_in='-'.join(lis1)
        data,lis_out=date_frame.get_calenda(date_in)

        combo=ttk.Combobox(child,values=['黄道吉日', '嫁娶', '入宅', '出行', '宴会', '立券', '搬家', '交易', '求财', '动土', '安床', '动工', '赴任', '安葬', '纳采', '开生坟', '开基', '开市', '求嗣', '裁衣', '砌灶', '开光', '祭祀', '盖屋', '破土', '祈福', '词讼', '起工架马', '进人口', '修造', '破屋坏垣', '纳财', '经商', '造桥', '开凿池塘', '出入财物', '买田地', '开仓库', '出货财', '开渠', '上梁', '竖柱', '安门', '修井', '穿井', '筑堤防', '定磉扇架', '出财放债', '小儿剃头', '乘船渡水', '畋猎', '整手足甲', '上官', '立嗣', '求谋', '入山伐木', '宣政事', '出师', '酝酿', '补垣', '解除', '纳畜', '行船', '破券', '学技艺', '问卜', '诸事宜', '诸事忌', '黑道日'],width=100,)
        combo.place(x=10,y=300)

        table1=TinUI.BasicTinUI(child)
        table1.add_table((0,0),minwidth=80,fg='white',headbg='#1C1C1C',bg='#1C1C1C',data=data)
        table1.place(x=360,y=10,width=1300,height=640)
        def print_sel():
            date = select.get_date()
            lis = (str(date)).split('/')
            date = '-'.join(lis)
            data,lis_out=date_frame.get_calenda(date)
            table1 = TinUI.BasicTinUI(child)
            table1.add_table((0, 0), minwidth=80, fg='white', headbg='#1C1C1C', bg='#1C1C1C', data=data)
            table1.place(x=360, y=10, width=1300, height=640)
        def day_calendar():
            child2 = tkinter.Toplevel(child)
            child2.title('万年历')  # 设置窗口标题
            child2.resizable(height=False, width=False)
            child2.geometry("550x430")
            date = select.get_date()
            lis = (str(date)).split('/')
            date = '-'.join(lis)
            data, lis_out = date_frame.get_calenda(date)
            table2 = TinUI.BasicTinUI(child2)
            table2.add_table((0, 0), minwidth=250, maxwidth=250, fg='white', headbg='#1C1C1C', bg='#1C1C1C',
                             data=lis_out)
            table2.place(x=10, y=10, width=510, height=400)
        def suitAndNot():
            d=combo.get()
            f=open('./source/yiji.json',encoding='utf-8')
            f=json.load(f)
            rst_txt.delete('1.0','end')
            rst_txt.insert(INSERT,f[d])
        ttk.Button(child, text="查询", command=lambda :thread_it(print_sel)).place(x=190, y=90, width=80)
        ttk.Button(child, text="当日", command=lambda: thread_it(day_calendar)).place(x=100, y=90, width=80)
        ttk.Button(child, text="宜忌", command=lambda: thread_it(suitAndNot)).place(x=10, y=90, width=80)
        child.mainloop()
    #字典-按钮事件
    def word_search():
        word_child = tkinter.Toplevel(top)
        word_child.title('字典')  # 设置窗口标题
        word_child.resizable(height=False, width=False)
        word_child.geometry("320x500")
        word_txt1 = tkinter.Text(word_child, width=10, height=1, undo=True, autoseparators=False, font='黑体 13',
                                 foreground='green', wrap='word', bd=5)
        word_txt1.place(x=10, y=10)
        word_txt2 = tkinter.Text(word_child, width=36, height=26, undo=True, autoseparators=False, font='黑体 12',
                                 foreground='green', wrap='word', bd=5)
        word_txt2.place(x=10, y=50)
        word_txt2.insert(INSERT, '在上方输入，限制一个字')

        def search():
            try:
                word = word_txt1.get('1.0', "2.0")
                if len(word) >= 2:
                    word_txt1.delete('1.0', 'end')
                    word_txt1.insert(INSERT, word.rstrip('\n')[0])
                word = word.rstrip('\n')[0]
            except:
                word = '乾'
            url = f'https://www.mxnzp.com/api/convert/dictionary?content={word}&app_id=itmtzvhijor2gjh1&app_secret=WWtOejFLOU1YcVROOVJDeDF2UXFVZz09'
            resp = requests.get(url)
            rst = resp.json()['data']
            explain = rst[0]['explanation']
            word_txt2.delete('1.0', 'end')
            word_txt2.insert(INSERT, explain)

        ttk.Button(word_child, text="查询", command=lambda :thread_it(search)).place(x=230, y=10, width=80)
        word_child.mainloop()
    #主功能按钮容器
    fram_btn=tkinter.Frame(top)
    #起卦-按钮
    btn_run=ttk.Button(fram_btn,text='起卦',width=9,command=call_run)
    btn_run.grid(row=0,column=0,padx=2,pady=2)
    #立即起卦-按钮
    btn_run_now = ttk.Button(fram_btn,text='立即起卦',width=9,command=call_run_now)
    btn_run_now.grid(row=0, column=1,padx=2,pady=2)
    #万物类象-按钮
    btn_world = ttk.Button(fram_btn,text='万物类象',width=9,command=call_world)
    btn_world.grid(row=0, column=2,padx=2,pady=2)
    # 万年历-按钮
    btn_lunar = ttk.Button(fram_btn, text='万年历', width=9, command=call_lunar)
    btn_lunar.grid(row=1, column=0,padx=2,pady=2)
    #字典-按钮
    btn_lunar = ttk.Button(fram_btn, text='字典', width=9, command=lambda :thread_it(word_search))
    btn_lunar.grid(row=1, column=1, padx=2, pady=2)
    fram_btn.place(x=80, y=150)

    sv_ttk.set_theme("dark")
    '''按钮容器end'''


    '''查询区start'''

    #详细-按钮事件
    def call_detail():
        try:
            value=list.get(list.curselection())
        except:
            value='乾为天'
        js_detail = open(r".\source\detail.json", encoding='utf-8')
        js_detail = json.load(js_detail)
        txt.delete('1.0', 'end')
        txt.insert(INSERT, value+'\n'+js_detail[value])
    #详细-按钮
    btn_detail = ttk.Button(top,text='详细',width=7,command=call_detail)
    btn_detail.place(x=860,y=160)

    #查询-按钮事件
    def call_search():
        try:
            value=list.get(list.curselection())
        except:
            value='乾为天'
        js_go = open(r".\source\go.json", encoding='utf-8')
        js_go = json.load(js_go)
        txt.delete('1.0', 'end')
        txt.insert(INSERT, value+'\n'+js_go[value])
    btn_search=ttk.Button(top,text='查询',width=8,command=call_search,)
    btn_search.place(x=460,y=528)

    #查询框
    list=tkinter.Listbox(top,width=10,height=19,font='黑体 11',selectbackground='#2B2B2B',selectforeground='green',highlightcolor='black',activestyle='none',bd=5)
    l=['乾为天', '坤为地', '水雷屯', '山水蒙', '水天需', '天水讼', '地水师', '水地比', '风天小畜', '天泽履', '地天泰', '天地否', '天火同人', '火天大有', '地山谦', '雷地豫', '泽雷随', '山风蛊', '地泽临', '风地观', '火雷噬嗑', '山火贲', '山地剥', '地雷复', '天雷无妄', '山天大畜', '山雷颐', '泽风大过', '坎为水', '离为火', '泽山咸', '雷风恒', '天山遯', '雷天大壮', '火地晋', '地火明夷', '风火家人', '火泽睽', '水山蹇', '雷水解', '山泽损', '风雷益', '泽天夬', '天风姤', '泽地萃', '地风升', '泽水困', '水风井', '泽火革', '火风鼎', '震为雷', '艮为山', '风山渐', '雷泽归妹', '雷火丰', '火山旅', '巽为风', '兑为泽', '风水涣', '水泽节', '风泽中孚', '雷山小过', '水火既济', '火水未济']
    for i, item in enumerate(l):
        list.insert(i, item)
    list.place(x=460,y=200)
    '''查询区end'''

    '''内容显示区start'''
    #卦象显示
    content_label=tkinter.Label(top,text='卦象显示在这里',font=('黑体', 13),wraplength=190,fg='green',anchor='nw',width=20, height=7,borderwidth=5,highlightbackground='blue',justify='left',relief='ridge')
    content_label.place(x=580,y=70)
    #卦图显示
    img_label1=tkinter.Label(top,width=60,height=50,image=photo1)
    img_label1.place(x=780,y=75)
    img_label2 = tkinter.Label(top,width=60,height=50,image=photo2)
    img_label2.place(x=780, y=143)
    #详细内容
    txt=tkinter.Text(top, width=45,height=25,undo=True,autoseparators=False,font='黑体 11',foreground='green',wrap='word',bd=5)
    txt.insert(INSERT,'查询结果将显示在这里！')
    txt.place(x=580,y=210)
    '''内容显示区end'''
    tkinter.mainloop()

if __name__ == '__main__':
    main()