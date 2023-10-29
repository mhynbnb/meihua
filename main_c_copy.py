import customtkinter as ctk
import requests
from customtkinter import INSERT
from customtkinter import CTkLabel as Label
from customtkinter import CTkComboBox as Combobox
import os
from PIL import Image
import json
from datetime import datetime
import datetime as dt
import threading

import date_frame
from caculate import cacu

ctk.set_widget_scaling(1.0)


def thread_it(func, *args):
    t = threading.Thread(target=func, args=args)
    t.setDaemon(True)
    t.start()


def is_lyear(year):
    if year % 4 == 0 and year % 100 != 0:
        return True
    elif year % 400 == 0:
        return True
    else:
        return False


class ScrollableRadiobuttonFrame(ctk.CTkScrollableFrame):
    def __init__(self, master, item_list, command=None, **kwargs):
        super().__init__(master, **kwargs)

        self.command = command
        self.radiobutton_variable = ctk.StringVar()
        self.radiobutton_list = []
        for i, item in enumerate(item_list):
            self.add_item(item)

    def add_item(self, item):
        radiobutton = ctk.CTkRadioButton(self, text=item, value=item, variable=self.radiobutton_variable)
        if self.command is not None:
            radiobutton.configure(command=self.command)
        radiobutton.grid(row=len(self.radiobutton_list), column=0, pady=(0, 10))
        self.radiobutton_list.append(radiobutton)

    def remove_item(self, item):
        for radiobutton in self.radiobutton_list:
            if item == radiobutton.cget("text"):
                radiobutton.destroy()
                self.radiobutton_list.remove(radiobutton)
                return

    def get_checked_item(self):
        return self.radiobutton_variable.get()


def main():
    top = ctk.CTk()  # 创建顶层窗口
    top.geometry('960x630')  # 设置窗口大小
    top.title('梅花易数')  # 设置窗口标题
    top.resizable(height=True, width=True)
    top.columnconfigure(1, weight=1)
    # 正上方“梅花易数”
    label = ctk.CTkLabel(top, text='梅花易数', font=('华文行楷', 35), width=300)
    label.grid(row=0, column=1, sticky='w')
    # 分辨率选择
    # def change_scaling_event(event):
    #     scal=scaling_optionemenu.get()
    #     print(scal)
    #     new_scaling_float = int(scal.replace("%", "")) / 100
    #     ctk.set_widget_scaling(new_scaling_float)
    # scaling_optionemenu = ctk.CTkOptionMenu(top, values=["70%","75%","80%","85%", "90%", "95%","100%", "110%", "120%"],
    #                             command=change_scaling_event)
    # scaling_optionemenu.grid(row=0,column=2,padx=30,pady=10,sticky='e')

    # 时间选择组件容器
    fram_time = ctk.CTkFrame(top, width=400)
    fram_time.grid(row=1, column=0, padx=30)

    def change_day(chioces):
        y = int(cbox_year.get())
        m = int(cbox_mon.get())
        monl1 = [1, 3, 5, 7, 8, 10, 12]
        monl2 = [4, 6, 9, 11]
        if m in monl1:
            d_li = [str(i) for i in range(1, 32)]
        elif m in monl2:
            d_li = [str(i) for i in range(1, 31)]
        else:
            if is_lyear(y):
                d_li = [str(i) for i in range(1, 30)]
            else:
                d_li = [str(i) for i in range(1, 29)]
        cbox_day.configure(values=d_li)

    yyyy = [str(i) for i in range(2000, 2050)]
    cbox_year = ctk.CTkComboBox(fram_time, width=80, values=yyyy, command=change_day)
    cbox_year.grid(row=1, column=0)
    label_year = ctk.CTkLabel(fram_time, text='年', font=('黑体', 13), width=20, height=1)
    label_year.grid(row=1, column=1)

    mm = [str(i) for i in range(1, 13)]
    cbox_mon = ctk.CTkComboBox(fram_time, width=50, values=mm, command=change_day)
    cbox_mon.grid(row=1, column=2)

    label_mon = Label(fram_time, text='月', font=('黑体', 13), width=20, height=1)
    label_mon.grid(row=1, column=3)

    dd = [str(i) for i in range(1, 32)]
    cbox_day = Combobox(fram_time, width=70, values=dd)
    cbox_day.grid(row=1, column=4)

    label_day = Label(fram_time, text='日', font=('黑体', 13), width=20, height=1, )
    label_day.grid(row=1, column=5)

    hh = [str(i) for i in range(0, 24)]
    cbox_hour = Combobox(fram_time, width=70, values=hh)
    cbox_hour.grid(row=1, column=6)

    label_hour = Label(fram_time, text='时', font=('黑体', 13), width=3, height=1)
    label_hour.grid(row=1, column=7)

    '''按钮容器start'''
    cont = ''
    p1_path = './source/'
    p2_path = r"./source/"
    photo1 = ctk.CTkImage(dark_image=Image.open(os.path.join(p1_path, "乾.png")), size=(70, 55))
    photo2 = ctk.CTkImage(dark_image=Image.open(os.path.join(p2_path, "乾.png")), size=(70, 55))

    # 起卦-按钮事件
    def call_run():
        global cont, photo1, photo2
        ye, mo, da, ho = int(cbox_year.get()), int(cbox_mon.get()), int(cbox_day.get()), int(cbox_hour.get())
        if mo in [4, 6, 9, 11] and da > 30:
            da = 30
        if mo == 2 and is_lyear(ye) and da > 29:
            da = 29
        if mo == 2 and (not is_lyear(ye)) and da > 28:
            da = 28
        rr = cacu(ye, mo, da, ho)
        cont = rr[0]
        i1 = rr[1]
        i2 = rr[2]
        cont = cont + '\n' + str(ye) + '年' + str(mo) + '月' + str(da) + '日' + str(ho) + '时'
        p1_path = r"./source/"
        p2_path = r"./source/"
        photo1 = ctk.CTkImage(dark_image=Image.open(os.path.join(p1_path, f"{i1}.png")), size=(70, 55))
        photo2 = ctk.CTkImage(dark_image=Image.open(os.path.join(p2_path, f"{i2}.png")), size=(70, 55))
        content_label.configure(text=cont)
        img_label1.configure(image=photo1)
        img_label2.configure(image=photo2)

        value = rr[3]
        js_go = open(r".\source\go.json", encoding='utf-8')
        js_go = json.load(js_go)
        txt.delete('1.0', 'end')
        txt.insert(INSERT, value + '\n' + js_go[value])

    # 立即起卦-按钮事件
    def call_run_now():
        p = datetime.now()
        year = p.year
        month = p.month
        day = p.day
        hour = int(p.hour)
        global cont, photo1, photo2
        date = str(year) + '年' + str(month) + '月' + str(day) + '日' + str(hour) + '时'
        cont = cacu(year, month, day, hour)[0] + '\n' + date
        i1 = cacu(year, month, day, hour)[1]
        i2 = cacu(year, month, day, hour)[2]
        p1_path = "./source/"
        p2_path = "./source/"
        photo1 = ctk.CTkImage(dark_image=Image.open(os.path.join(p1_path, f"{i1}.png")), size=(70, 55))
        photo2 = ctk.CTkImage(dark_image=Image.open(os.path.join(p2_path, f"{i2}.png")), size=(70, 55))
        content_label.configure(text=cont)

        img_label1.configure(image=photo1)
        img_label2.configure(image=photo2)
        value = cacu(year, month, day, hour)[3]
        js_go = open(r".\source\go.json", encoding='utf-8')
        js_go = json.load(js_go)
        txt.delete('1.0', 'end')
        txt.insert(INSERT, value + '\n' + js_go[value])

    # 万物类象-按钮事件
    def call_world():
        newWindow = ctk.CTkToplevel(top)
        newWindow.geometry('500x500')  # 设置窗口大小
        newWindow.title('万物类象')  # 设置窗口标题
        newWindow.resizable(height=False, width=False)
        newWindow.attributes('-topmost', 'true')
        # 万物类象-点击
        def wanwu_click():
            t = str(wanwu_lis.get_checked_item())
            js_world = open(r".\source\world.json", encoding='utf-8')
            js_world = json.load(js_world)
            txt_world.delete('1.0', 'end')
            txt_world.insert(INSERT, t + '\n\n' + js_world[t])

        # 万物类象-列表框
        l_w = ['乾卦', '坤卦', '坎卦', '艮卦', '震卦', '离卦', '兑卦', '巽卦']
        wanwu_lis = ScrollableRadiobuttonFrame(master=newWindow, width=60, height=250,
                                               command=wanwu_click,
                                               item_list=[f"{i}" for i in l_w],
                                               label_text="")
        wanwu_lis.grid(row=0, column=0, padx=0, pady=10, sticky='en')
        # 万物类象查询结果显示框
        txt_world = ctk.CTkTextbox(newWindow, width=380, height=450, undo=True, autoseparators=False, wrap='word')
        txt_world.insert(INSERT, '查询结果将显示在这里！')
        txt_world.grid(row=0, column=1, padx=0, pady=10, sticky='en')

    # 万年历-按钮事件
    def call_lunar():
        child = ctk.CTkToplevel(top)
        child.title('万年历')
        child.geometry("1250x630")
        child.rowconfigure(3, weight=2)
        child.attributes('-topmost', 'true')

        def calenClick():
            lis1 = str(calen.get_date()).split('-')
            lis1[-1]=lis1[-1].lstrip('0')
            lis1[-2]=lis1[-2].lstrip('0')
            print(lis1)
            date = '-'.join(lis1)
            print(date)
            data, lis_out = date_frame.get_calenda(date)
            try:
                for ii in range(9):
                    for iii in range(14):
                        tex = data[ii][iii]
                        lab1_lis[ii][iii].configure(text=tex)
                for ii in range(12):
                    for iii in range(2):
                        tex = lis_out[ii][iii]
                        lab2_lis[ii][iii].configure(text=tex)
            except:
                pass

        def choose(event):
            lis1 = str(entry.get())
            date =lis1[0:4]+'-'+lis1[4:6].lstrip('0')+'-'+lis1[6:8].lstrip('0')
            data, lis_out = date_frame.get_calenda(date)
            try:
                for ii in range(9):
                    for iii in range(14):
                        tex = data[ii][iii]
                        lab1_lis[ii][iii].configure(text=tex)
                for ii in range(12):
                    for iii in range(2):
                        tex = lis_out[ii][iii]
                        lab2_lis[ii][iii].configure(text=tex)
            except:
                pass

        def suitAndNot(event):
            d = combo.get()
            f = open('./source/yiji.json', encoding='utf-8')
            f = json.load(f)
            rst_txt.delete('1.0', 'end')
            rst_txt.insert(INSERT, f[d])

        def start():
            lis1 = str(dt.date.today()).split('-')
            lis1[-1].lstrip('0')
            lis1[-2].lstrip('0')
            date_in = '-'.join(lis1)
            data, lis_out = date_frame.get_calenda(date_in)
            for ii in range(9):
                for iii in range(14):
                    tex = data[ii][iii]
                    lab1_lis[ii][iii].configure(text=tex)
            for ii in range(12):
                for iii in range(2):
                    tex = lis_out[ii][iii]
                    lab2_lis[ii][iii].configure(text=tex)

        calen = date_frame.Calendar(child, command=lambda: thread_it(calenClick))
        calen.grid(row=0, column=0, pady=10, padx=10)

        fram_btn2 = ctk.CTkFrame(child)
        fram_btn2.grid(row=1, column=0, pady=10, padx=10, sticky='w')
        entry = ctk.CTkEntry(fram_btn2, placeholder_text='例如：20220105',width=120)
        entry.grid(row=0, column=1,padx=2)
        entry.bind('<Return>', choose)

        bt2 = ctk.CTkButton(fram_btn2, text="跳转", command=lambda: thread_it(choose), width=60)
        bt2.grid(row=0, column=2)

        rst_txt = ctk.CTkTextbox(child, width=300, height=280, undo=True, autoseparators=False, wrap='word')
        rst_txt.grid(row=2, column=0, sticky='nw', pady=10, padx=10)

        combo = Combobox(fram_btn2,
                         values=['黄道吉日', '嫁娶', '入宅', '出行', '宴会', '立券', '搬家', '交易', '求财', '动土', '安床', '动工', '赴任', '安葬',
                                 '纳采', '开生坟', '开基', '开市', '求嗣', '裁衣', '砌灶', '开光', '祭祀', '盖屋', '破土', '祈福', '词讼', '起工架马',
                                 '进人口', '修造', '破屋坏垣', '纳财', '经商', '造桥', '开凿池塘', '出入财物', '买田地', '开仓库', '出货财', '开渠', '上梁',
                                 '竖柱', '安门', '修井', '穿井', '筑堤防', '定磉扇架', '出财放债', '小儿剃头', '乘船渡水', '畋猎', '整手足甲', '上官',
                                 '立嗣', '求谋', '入山伐木', '宣政事', '出师', '酝酿', '补垣', '解除', '纳畜', '行船', '破券', '学技艺', '问卜',
                                 '诸事宜', '诸事忌', '黑道日'], width=80, command=suitAndNot)
        combo.grid(row=0, column=0, sticky='w', pady=10, padx=10)
        combo.bind('<Return>',suitAndNot)

        tab_view = ctk.CTkTabview(child, width=900, height=600)
        tab_view.grid(row=0, column=1, rowspan=4, pady=10, padx=10)
        tab_view.add('时辰')
        tab_view.add('当日')
        tab_view.tab('时辰').grid_columnconfigure(0, weight=2)
        tab_view.tab('当日').grid_columnconfigure(0, weight=2)

        lab1_lis = []
        for ii in range(9):
            l_temp = []
            for iii in range(14):
                l_temp.append(ctk.CTkLabel(tab_view.tab('时辰'), width=6, height=1, text='', compound='left', anchor='nw',
                                           font=('黑体', 12), wraplength=60))
                l_temp[-1].grid(row=ii, column=iii, sticky='n', pady=10, padx=2)
            lab1_lis.append(l_temp)
        tab_view.tab('时辰').grid_columnconfigure(0, weight=0)
        lab2_lis = []
        for ii in range(12):
            l_temp = []
            for iii in range(2):
                if iii == 0:
                    flag = 'ne'
                else:
                    flag = 'nw'
                l_temp.append(ctk.CTkLabel(tab_view.tab('当日'), width=6, height=1, text='', anchor='w',
                                           font=('黑体', 15), wraplength=300))
                l_temp[-1].grid(row=ii, column=iii, sticky=flag, pady=10, padx=10)
            lab2_lis.append(l_temp)
        tab_view.tab('当日').grid_columnconfigure(0, weight=2)
        tab_view.tab('当日').grid_columnconfigure(1, weight=1)

        start()
        child.mainloop()

    # 字典-按钮事件
    def word_search():
        word_child = ctk.CTkToplevel(top)
        word_child.title('字典')  # 设置窗口标题
        word_child.resizable(height=False, width=False)
        word_child.geometry("320x500")
        word_child.attributes('-topmost', 'true')

        def test_length(text):
            if len(text) > 10:
                word_child.bell()  # 声音提示
                return False
            return True

        word_entry = ctk.CTkEntry(word_child, width=100, height=10)
        word_entry.place(x=10, y=10)

        word_txt2 = ctk.CTkTextbox(word_child, width=300, height=400, undo=True, autoseparators=False, wrap='word', )
        word_txt2.place(x=10, y=50)
        word_txt2.insert(INSERT, '在上方输入，限制一个字')

        def search(event):
            try:
                word = word_entry.get()
                print(word)
                if len(word) >= 2:
                    word_entry.delete(1, 'end')
                word = word.rstrip('\n')[0]
            except:
                word = '乾'
            url = f'https://www.mxnzp.com/api/convert/dictionary?content={word}&app_id=itmtzvhijor2gjh1&app_secret=WWtOejFLOU1YcVROOVJDeDF2UXFVZz09'
            resp = requests.get(url)
            rst = resp.json()['data']
            explain = rst[0]['explanation']
            word_txt2.delete('1.0', 'end')
            word_txt2.insert(INSERT, explain)

        word_entry.bind('<Return>', search)
        ctk.CTkButton(word_child, text="查询", command=lambda: thread_it(search), width=80).place(x=120, y=10)
        word_child.mainloop()

    # coffee
    def coffee():
        coffe = ctk.CTkToplevel(top, )
        coffe.geometry('300x500')
        coffe.title('感谢作者分享')
        coffe.resizable(height=False, width=False)
        coffe.attributes('-topmost', 'true')
        image = ctk.CTkImage(dark_image=Image.open("./source/code.jpg"), size=(300, 500))
        lab = ctk.CTkLabel(coffe, image=image, text='')
        lab.grid(row=0, column=0)

    # 主功能按钮容器：起卦，立即起卦，字典，万年历，万物类象
    def main_button():
        fram_btn = ctk.CTkFrame(top)
        fram_btn.grid(row=3, column=0, sticky='n')
        # 起卦-按钮
        btn_run = ctk.CTkButton(fram_btn, text='起        卦', font=('华文行楷', 20), width=20, height=40, command=call_run)
        btn_run.grid(row=0, column=0, padx=5, pady=5)
        # 立即起卦-按钮
        btn_run_now = ctk.CTkButton(fram_btn, text='立即起卦', font=('华文行楷', 20), width=20, height=40, command=call_run_now)
        btn_run_now.grid(row=0, column=1, padx=5, pady=5)
        # 万物类象-按钮
        btn_world = ctk.CTkButton(fram_btn, text='万物类象', font=('华文行楷', 20), width=20, height=40, command=call_world)
        btn_world.grid(row=0, column=2, padx=5, pady=5)
        # 万年历-按钮
        btn_lunar = ctk.CTkButton(fram_btn, text='万  年  历', font=('华文行楷', 20), width=20, height=40, command=call_lunar)
        btn_lunar.grid(row=1, column=0, padx=5, pady=5)
        # 字典-按钮
        btn_lunar = ctk.CTkButton(fram_btn, text='字        典', font=('华文行楷', 20), width=20, height=40,
                                  command=lambda: thread_it(word_search))
        btn_lunar.grid(row=1, column=1, padx=5, pady=5)
        # 待续-按钮
        image = ctk.CTkImage(dark_image=Image.open("./source/coffe.jpeg"), size=(80, 35))
        btn_lunar = ctk.CTkButton(fram_btn, text='', font=('华文行楷', 16), width=20, height=40, image=image,
                                  command=coffee)
        btn_lunar.grid(row=1, column=2, padx=5, pady=5)

    # 底部
    # 下方文字
    label_word = ctk.CTkLabel(top, text='千万不要自己感动自己。大部分人看似的努力，不过是愚蠢导致的。', font=('华文行楷', 17))
    label_word.grid(row=4, column=0, padx=30, pady=5, columnspan=3, sticky='w')
    main_button()
    '''END'''

    # 显示区：卦象，卦图，详细内容
    # 卦象显示
    fram_show = ctk.CTkFrame(top)
    fram_show.grid(row=2, column=2, padx=20)
    content_label = Label(fram_show, text='卦象显示在这里', font=('黑体', 13), wraplength=190, anchor='n', width=10, height=8,
                          justify='left')
    content_label.grid(row=0, column=0, rowspan=2, padx=20)
    # 卦图显示
    img_label1 = Label(fram_show, width=60, height=50, image=photo1, text='')
    img_label1.grid(row=0, column=1, padx=10, pady=7)
    img_label2 = Label(fram_show, width=60, height=50, image=photo2, text='')
    img_label2.grid(row=1, column=1, padx=10, pady=7)
    # 详细内容

    txt = ctk.CTkTextbox(top, width=340, height=365, undo=True, autoseparators=False, wrap='word')
    txt.insert(INSERT, '查询结果将显示在这里！')
    txt.grid(row=3, column=2, padx=0, pady=10, rowspan=2, sticky='n')
    '''END'''

    # 详细-按钮事件
    def call_detail():
        t = f"{top.scrollable_radiobutton_frame.get_checked_item()}"
        if t == '':
            t = '乾为天'
        js_detail = open(r".\source\detail.json", encoding='utf-8')
        js_detail = json.load(js_detail)
        txt.delete('1.0', 'end')
        txt.insert(INSERT, t + '\n' + js_detail[t])

    # 详细-按钮
    btn_detail = ctk.CTkButton(fram_show, text='详  细', font=('华文行楷', 20), width=20, height=30, command=call_detail)
    btn_detail.grid(row=1, column=2, padx=10, sticky='s')
    # 查询框
    l2 = ['乾为天', '坤为地', '水雷屯', '山水蒙', '水天需', '天水讼', '地水师', '水地比', '风天小畜', '天泽履', '地天泰', '天地否', '天火同人', '火天大有', '地山谦',
          '雷地豫', '泽雷随', '山风蛊', '地泽临', '风地观', '火雷噬嗑', '山火贲', '山地剥', '地雷复', '天雷无妄', '山天大畜', '山雷颐', '泽风大过', '坎为水', '离为火',
          '泽山咸', '雷风恒', '天山遯', '雷天大壮', '火地晋', '地火明夷', '风火家人', '火泽睽', '水山蹇', '雷水解', '山泽损', '风雷益', '泽天夬', '天风姤', '泽地萃',
          '地风升', '泽水困', '水风井', '泽火革', '火风鼎', '震为雷', '艮为山', '风山渐', '雷泽归妹', '雷火丰', '火山旅', '巽为风', '兑为泽', '风水涣', '水泽节',
          '风泽中孚', '雷山小过', '水火既济', '火水未济']

    def radiobutton_frame_event():
        t = f"{top.scrollable_radiobutton_frame.get_checked_item()}"
        print(t)
        js_go = open(r".\source\go.json", encoding='utf-8')
        js_go = json.load(js_go)
        txt.delete('1.0', 'end')
        txt.insert(INSERT, t + '\n' + js_go[t])

    top.scrollable_radiobutton_frame = ScrollableRadiobuttonFrame(master=top, width=90, height=350,
                                                                  command=radiobutton_frame_event,
                                                                  item_list=[f"{i}" for i in l2],
                                                                  label_text="")
    top.scrollable_radiobutton_frame.grid(row=3, column=1, padx=0, pady=10, sticky='en')
    '''END'''
    top.mainloop()


if __name__ == '__main__':
    ctk.set_appearance_mode("dark")
    main()
