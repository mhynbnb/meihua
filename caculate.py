from datetime import datetime

from zhdate import ZhDate




def cacu(ye,mo,da,ho):
    year=ye
    month=mo
    day=da
    hour=ho
    dic={1:'乾',2:'兑',3:'离',4:'震',5:'巽',6:'坎',7:'艮',0:'坤'}
    dic2={'子':1,'丑':2,'寅':3,'卯':4,'辰':5,'巳':6,'午':7,'未':8,'申':9,'酉':10,'戌':11,'亥':12}
    dic3={1:'丑',2:'丑',3:'寅',4:'寅',5:'卯',6:'卯',7:'辰',8:'辰',9:'巳',10:'巳',11:'午',12:'午',13:'未',14:'未',15:'申',16:'申',17:'酉',18:'酉',19:'戌',20:'戌',21:'亥',22:'亥',23:'子',0:'子'}
    dic_change={
        '乾':{1:'巽',2:'离',3:'兑'},
        '兑':{1:'坎',2:'震',3:'乾'},
        '离':{1:'艮',2:'乾',3:'震'},
        '震':{1:'坤',2:'兑',3:'离'},
        '巽':{1:'乾',2:'艮',3:'坎'},
        '坎':{1:'兑',2:'坤',3:'巽'},
        '艮':{1:'离',2:'巽',3:'坤'},
        '坤':{1:'震',2:'坎',3:'艮'},
    }

    date = datetime(year, month, day)
    date_lunar = ZhDate.from_datetime(date)

    lunar_year=dic2[f"{date_lunar.chinese().split(' ')[1][1]}"]
    lunar_month=date_lunar.lunar_month
    lunar_day=date_lunar.lunar_day
    lunar_hour=dic2[dic3[hour]]

    gua_up=dic[(lunar_day+lunar_month+lunar_year)%8]
    gua_down=dic[(lunar_day+lunar_month+lunar_year+lunar_hour)%8]

    gua_change=(lunar_day+lunar_month+lunar_year+lunar_hour)%6

    if gua_change==0:
        gua_change=6

    if gua_change<=3:
        gua_change_name=dic_change[gua_down][gua_change]
        gua_use=gua_down
        gua_body=gua_up
    else:
        gua_change_name=dic_change[gua_up][gua_change-3]
        gua_use = gua_up
        gua_body = gua_down

    def gua_hu(num):
        hu_dic={
            11: ["乾", "乾", "乾为天"], 12: ["巽", "离", "天泽履"], 13: ["乾", "巽", "天火同人"], 14: ["巽", "艮", "天雷无妄"], 15: ["乾", "乾", "天风姤"], 16: ["巽", "离", "天水讼"],
            17: ["乾", "巽", "天山遯"], 18: ["巽", "艮", "天地否"],
            21: ["乾", "乾", "泽天夬"], 22: ["巽", "离", "兑为泽"], 23: ["乾", "巽", "泽火革"], 24: ["巽", "艮", "泽雷随"], 25: ["乾", "乾", "泽风大过"], 26: ["巽", "离", "泽水困"],
            27: ["乾", "巽", "泽山咸"], 28: ["巽", "艮", "泽地萃"],
            31: ["兑", "乾", "火天大有"], 32: ["坎", "离", "火泽睽"], 33: ["兑", "巽", "离为火"], 34: ["坎", "艮", "火雷噬嗑"], 35: ["兑", "乾", "火风鼎"], 36: ["坎", "离", "火水未济"],
            37: ["兑", "巽", "火山旅"], 38: ["坎", "艮", "火地晋"],
            41: ["兑", "乾", "雷天大壮"], 42: ["坎", "离", "雷泽归妹"], 43: ["兑", "巽", "雷火丰"], 44: ["坎", "艮", "震为雷"], 45: ["兑", "乾", "雷风恒"], 46: ["坎", "离", "雷水解"],
            47: ["兑", "巽", "雷山小过"], 48: ["坎", "艮", "雷地豫"],
            51: ["离", "兑", "风天小畜"], 52: ["艮", "震", "风泽中孚"], 53: ["离", "坎", "风火家人"], 54: ["艮", "坤", "风雷益"], 55: ["离", "兑", "巽为风"], 56: ["艮", "震", "风水涣"],
            57: ["离", "坎", "风山渐"], 58: ["艮", "坤", "风地观"],
            61: ["离", "兑", "水天需"], 62: ["艮", "震", "水泽节"], 63: ["离", "坎", "水火既济"], 64: ["艮", "坤", "水雷屯"], 65: ["离", "兑", "水风井"], 66: ["艮", "震", "坎为水"],
            67: ["离", "坎", "水山蹇"], 68: ["艮", "坤", "水地比"],
            71: ["震", "兑", "山天大畜"], 72: ["坤", "震", "山泽损"], 73: ["震", "坎", "山火贲"], 74: ["坤", "坤", "山雷颐"], 75: ["震", "兑", "山风蛊"], 76: ["坤", "震", "山水蒙"],
            77: ["震", "坎", "艮为山"], 78: ["坤", "坤", "山地剥"],
            81: ["震", "兑", "地天泰"], 82: ["坤", "震", "地泽临"], 83: ["震", "坎", "地火明夷"], 84: ["坤", "坤", "地雷复"], 85: ["震", "兑", "地风升"], 86: ["坤", "震", "地水师"],
            87: ["震", "坎", "地山谦"], 88: ["坤", "坤", "坤为地"]
        }
        return hu_dic[num]

    lambda_a=lambda x:x if x!=0 else 8
    up_num=lambda_a((lunar_day+lunar_month+lunar_year)%8)
    down_num=lambda_a((lunar_day+lunar_month+lunar_year+lunar_hour)%8)
    gua_huhu=gua_hu(up_num*10+down_num)
    lis=[]
    if (gua_up=='乾' and gua_down=='乾') or (gua_up=='坤' and gua_down=='坤'):
        content='上卦:'+gua_up+'  '+'下卦:'+gua_down+'  '+'\n'+gua_huhu[2]+ '\n'\
                '体卦:'+gua_body+'  '+'用卦:'+gua_use+'\n' +\
                '互卦:'+f'{gua_change_name},{gua_change_name}'+'\n'+f'变{gua_change}爻'+','+ \
                '变卦:'+gua_change_name
    else:
        content = '上卦:' + gua_up + '  ' + '下卦:' + gua_down + '  ' + '\n' + gua_huhu[2] + '\n' \
                     '体卦:' + gua_body + '  ' + '用卦:' + gua_use + '\n' + \
                  '互卦:' + f'{gua_huhu[0]},{gua_huhu[1]}' + '\n' + f'变{gua_change}爻' + ',' + \
                  '变卦:' + gua_change_name
    lis.append(content)
    lis.append(gua_up)
    lis.append(gua_down)
    lis.append(gua_huhu[2])
    return lis

# print('上卦:',gua_up,end='  ')
# print('下卦:',gua_down,end='  ')
# print(gua_huhu[2])
# print('体卦:', gua_body,end='  ')
# print('用卦:', gua_use)
# print('互卦:',f'{gua_huhu[0]},{gua_huhu[1]}')
# print(f'变{gua_change}爻',end=',')
# print('变卦:',gua_change_name)