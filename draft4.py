import datetime
import customtkinter as ctk


class Calendar(ctk.CTkFrame):
    def __init__(self, master=None, **kwargs):
        super().__init__(master, **kwargs)
        self.date = datetime.date.today()
        self.current_month = self.date.month
        self.current_year = self.date.year
        self.create_widgets()

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
        self.create_cal()

    def get_date(self):
        # 获取选择的日期
        return self.date


# 导入所需的库
from calendar import monthrange

# 创建主窗口和日历组件
root = ctk.CTk()
root.title("Calendar Select")

cal = Calendar(root)
cal.grid()

# 运行主循环
root.mainloop()
