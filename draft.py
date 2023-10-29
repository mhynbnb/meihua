import requests
from bs4 import BeautifulSoup
import json
import datetime

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


if __name__ == '__main__':
    with open('calen.json', 'w',encoding='utf-8') as f:
        f1=open('calenDay.json','w',encoding='utf-8')
        d={}
        d2={}
        for i in range(1,3000):
            try:
                date=datetime.date.fromordinal(i)
                data, lis = get_calenda(str(date))
                data[0][13]=data[0][13]+'0'
                print(date)
                date=str(date)
                d[date]={}
                d2[date]={}
                for m in range(1,14):
                    d[date][data[0][m]]={}
                    d[date][data[0][m]]['时刻'] =data[1][m]
                    d[date][data[0][m]]['时辰'] = data[2][m]
                    d[date][data[0][m]]['星神'] = data[3][m]
                    d[date][data[0][m]]['时宜'] = data[4][m]
                    d[date][data[0][m]]['时忌'] = data[5][m]
                    d[date][data[0][m]]['冲煞'] = data[6][m]
                    d[date][data[0][m]]['煞方'] = data[7][m]
                    d[date][data[0][m]]['时冲'] = data[8][m]
                for t in lis:
                    d2[date][t[0]]=t[1]
            except:
                pass
        # print(d)

        json.dump(d, f)
        json.dump(d2,f1)
        # print(d2)
    # print(str(datetime.date.fromordinal(10)))


