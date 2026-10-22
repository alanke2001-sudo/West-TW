def T(x,y,s,c='d-t',a='start',extra=''): return '<text class="%s" x="%s" y="%s" text-anchor="%s"%s>%s</text>'%(c,x,y,a,extra,s)
def R(x,y,w,h,c='d-box',rx=6): return '<rect class="%s" x="%s" y="%s" width="%s" height="%s" rx="%s"/>'%(c,x,y,w,h,rx)
def L(x1,y1,x2,y2,c='d-line',m=''): return '<line class="%s" x1="%s" y1="%s" x2="%s" y2="%s"%s/>'%(c,x1,y1,x2,y2,(' marker-end="url(#%s)"'%m) if m else '')
def svg(w,h,label,body,defs=''):
    return '<svg viewBox="0 0 %d %d" role="img" aria-label="%s">%s%s</svg>'%(w,h,label,defs,''.join(body))
ARROW=lambda i:'<defs><marker id="%s" viewBox="0 0 10 10" refX="9" refY="5" markerWidth="6" markerHeight="6" orient="auto-start-reverse"><path d="M0 0L10 5L0 10z" class="ahead"/></marker></defs>'%i

def fig1():
    steps=[('灰色地帶襲擾','機艦擾台','海警巡查金門'),('戰備警巡・軍演','聯合利劍、海峽','雷霆、正義使命'),('海警隔離','識別查證、登檢','扣押、宣示管轄'),('聯合封鎖','封港、斷航','斷纜、斷網'),('聯合火力打擊','飛彈與空中打擊','癱瘓指管、斬首'),('聯合登島','奪外島、搶灘','攻占要港要點')]
    b=[T(24,26,'行動強度與風險','d-th'),T(24,44,'由左至右升高；各選項可單獨使用或快速轉換','d-ts')]
    for i,(n,a,c) in enumerate(steps):
        x=24+i*122; top=250-i*34; b.append('<rect class="st%d" x="%d" y="%d" width="114" height="%d" rx="4" stroke-width="1.3"/>'%(i,x,top,330-top))
        b.append(T(x+10,top+24,n,'d-th')); b.append(T(x+10,top+44,a,'d-ts')); b.append(T(x+10,top+60,c,'d-ts'))
    b.append(L(385,72,385,340,'d-dash')); b.append(T(392,84,'封鎖門檻：國際法上之戰爭行為','d-ac'))
    b.append(T(24,352,'低於戰爭門檻（灰色地帶、法律戰、認知戰）','d-ts')); b.append(T(738,352,'武裝衝突','d-ts','end'))
    return svg(760,362,'解放軍對台軍事選項升級階梯',b)

def fig2():
    cols=[('政治法律',['反分裂國家法(2005)','國防動員法(2010)','懲治台獨22條(2024)','國際輿論「法理戰」']),
          ('指揮編制',['東部戰區(2016)','信息支援部隊(2024)','聯合作戰指揮體系','高層整肅影響待觀察']),
          ('裝備投送',['075型×4、071型×8','076四川艦海試','水橋駁船(2025)','民用滾裝船動員']),
          ('演訓轉戰',['由訓轉戰、由演轉戰','抵近24浬演習','封港・斷航想定','戰備警巡常態化']),
          ('動員後勤',['民船徵用演練','油料・彈藥儲備','野戰醫療・捐血','港口裝載能力'])]
    b=[]
    for i,(h,items) in enumerate(cols):
        x=19+i*146; b.append(R(x,20,138,170)); b.append('<rect class="d-tw" x="%d" y="20" width="138" height="40" rx="6"/>'%x); b.append(T(x+69,46,h,'d-th','middle'))
        for j,it in enumerate(items): b.append(T(x+12,88+j*26,it,'d-t'))
    b.append(R(19,206,722,40,'d-hi')); b.append(T(380,231,'美方評估目標：2027 年建軍百年前，具備對台取得「戰略決勝」的可信軍事選項','d-th','middle'))
    return svg(760,256,'解放軍對台軍事準備五個面向',b)

def fig3():
    pts=[('D－12 個月以上',['關鍵彈藥增產','飛彈陣地擴建']),('D－3～4 個月',['正式動員令','徵用船舶車輛']),('D－1～2 個月',['沿海野戰醫院','捐血、部隊集結']),('D－數週',['油料推進港口','遠距部隊戰備']),('D 日',['封鎖或火力打擊','演習轉為行動'])]
    b=[ARROW('a3'),L(40,70,736,70,'d-axis','a3')]
    for i,(t,ls) in enumerate(pts):
        cx=92+i*144; b.append('<circle class="%s" cx="%d" cy="70" r="7"/>'%('d-dot' if i==4 else 'd-dot2',cx)); b.append(T(cx,48,t,'d-th','middle'))
        b.append(R(cx-66,96,132,70,'d-hi' if i==4 else 'd-box')); b.append(L(cx,77,cx,96))
        for j,l in enumerate(ls): b.append(T(cx,124+j*22,l,'d-t','middle'))
    b.append(T(24,196,'「演轉戰」或封鎖情境：上述步驟可能在演習名義下並行，預警時間縮短為數日至數週。','d-ts'))
    return svg(760,210,'全面登陸作戰預警指標時序',b)

def fig4():
    ev=[('2022-08','台灣周邊重要軍事演訓','裴洛西訪台後；彈道飛彈飛越台灣上空',0),
        ('2023-04','聯合利劍','總統過境美國後；演練封控與聯合打擊',0),
        ('2024-05','聯合利劍-2024A','總統就職後；本島 5 區塊、外島 4 區塊',0),
        ('2024-10','聯合利劍-2024B','6 區塊與鄰接區重疊；海警 4 編隊環台',0),
        ('2025-03','水橋駁船湛江試驗','可延伸棧橋碼頭，直通岸際卸載',1),
        ('2025-04','海峽雷霆-2025A','攔截扣押課目；模擬打擊港口與能源設施',0),
        ('2025-08','我國防部 114 年中共軍力報告','評估 2035 年前完備對台封鎖戰力',2),
        ('2025-11','福建艦成軍、076 型四川艦海試','航艦與兩棲攻擊艦能力擴充',1),
        ('2025-12','正義使命-2025；美 2025 年中共軍力報告','封控要港要域；火箭彈落入 24 浬鄰接區',0),
        ('2026-08','漢光 42 號；115 年中共軍力報告','首度演練西太平洋反封鎖；確認登島想定',2),
        ('2026-10','截至 10 月中旬','今年尚無具名大型環台演習，日常擾台持續',3),
        ('2027','建軍百年目標','美方評估：具備「戰略決勝」選項',4),
        ('2030–35','聯合登島作戰轉型完成（我方評估）','台灣國防部 2026 年報告',4),
        ('2035','國防和軍隊現代化','我方評估之最高風險時點',4),
        ('2049','建政百年','「世界一流軍隊」目標',4)]
    b=[T(24,24,'圖例：','d-ts'),'<circle class="d-dot" cx="72" cy="20" r="5"/>',T(82,24,'演習','d-ts'),'<circle class="d-dot3" cx="130" cy="20" r="5"/>',T(140,24,'裝備','d-ts'),'<rect class="d-tw" x="182" y="15" width="10" height="10"/>',T(198,24,'報告與我方演習','d-ts'),'<circle class="d-dot2" cx="306" cy="20" r="5"/>',T(316,24,'未來目標（評估）','d-ts')]
    y0=62; dy=48; yN=y0+dy*(len(ev)-1)
    b.append(L(150,y0-14,150,y0+dy*10,'d-axis')); b.append('<line class="d-dash" x1="150" y1="%d" x2="150" y2="%d"/>'%(y0+dy*10,yN+10))
    for i,(d,t,s,k) in enumerate(ev):
        y=y0+i*dy; b.append(T(132,y+5,d,'d-th','end'))
        if k==0: b.append('<circle class="d-dot" cx="150" cy="%d" r="6"/>'%y)
        elif k==1: b.append('<circle class="d-dot3" cx="150" cy="%d" r="6"/>'%y)
        elif k==2: b.append('<rect class="d-tw" x="144" y="%d" width="12" height="12"/>'%(y-6))
        else: b.append('<circle class="d-dot2" cx="150" cy="%d" r="6"/>'%y)
        b.append(T(172,y,t,'d-th')); b.append(T(172,y+18,s,'d-ts'))
    return svg(760,yN+40,'重大時間節點時間軸',b)

def fig5():
    r='ppfgfpppfgpp'; b=[]
    for i,c in enumerate(r):
        x=40+i*58; b.append('<rect class="wx-%s" x="%d" y="40" width="54" height="54" rx="3"/>'%(c,x)); b.append(T(x+27,72,'%d月'%(i+1),'d-th','middle'))
    def span(m1,m2,t,y):
        x1=40+(m1-1)*58; x2=40+m2*58-4; return L(x1,y,x2,y,'d-axis')+T((x1+x2)/2,y+18,t,'d-ts','middle')
    b+= [span(1,2,'東北季風',114),span(11,12,'東北季風',114),span(5,6,'梅雨',114),span(7,9,'颱風季',114)]
    b.append(T(40,26,'適合度：','d-ts')); 
    for j,(c,t) in enumerate([('g','良好'),('f','尚可'),('p','不佳')]):
        b.append('<rect class="wx-%s" x="%d" y="16" width="12" height="12" rx="2"/>'%(c,100+j*70)); b.append(T(118+j*70,26,t,'d-ts'))
    return svg(760,150,'各月份渡海作戰天候適合度',b)

def fig6():
    b=['<ellipse class="ring1" cx="380" cy="200" rx="356" ry="186"/>','<ellipse class="ring2" cx="380" cy="214" rx="262" ry="140"/>','<ellipse class="ring3" cx="380" cy="230" rx="172" ry="94"/>','<ellipse class="ring4" cx="380" cy="246" rx="86" ry="44"/>']
    b+=[T(380,40,'外線懾阻・反介入','d-ac','middle'),T(380,58,'航艦編隊於台灣以東、遠海長航、第一島鏈以外兵力','d-ts','middle'),
        T(380,98,'海空封控','d-ac','middle'),T(380,116,'封控要港要域、管制航道、截擊驅離、布雷','d-ts','middle'),
        T(380,160,'海警執法隔離','d-ac','middle'),T(380,178,'識別查證、登臨檢查、扣押、宣示管轄','d-ts','middle'),
        T(380,242,'台灣本島','d-th','middle'),T(380,262,'能源・資訊斷鏈','d-ts','middle')]
    b+=[T(24,372,'貫穿各層：網攻、電戰、海底電纜破壞、認知作戰','d-ts')]
    return svg(760,392,'聯合封控層次概念圖',b)

def fig9():
    st=[('1 集結裝載',['福建沿海港口','民船徵用、裝載']),('2 出港編隊',['夜間出港','電戰掩護、掃雷']),('3 航渡',['130～200 公里','約 7～11 小時*']),('4 換乘泛水',['兩棲車泛水','舟波編組']),
        ('8 後續梯隊',['民船循環運補','跨海後勤線']),('7 奪港接收',['台中港、台北港','滾裝船卸載']),('6 建立灘頭',['浮動碼頭','水橋駁船棧橋']),('5 搶灘突擊',['直升機垂直登陸','灘岸破障'])]
    b=[ARROW('a9')]
    for i,(h,ls) in enumerate(st):
        row=i//4; col=i%4; x=24+col*182; y=30+row*150
        cls='d-hi' if h[0] in '57' else 'd-box'
        b.append(R(x,y,164,92,cls)); b.append(T(x+12,y+26,h,'d-th'))
        for j,l in enumerate(ls): b.append(T(x+12,y+50+j*20,l,'d-t'))
        if col<3: b.append(L(x+164,y+46,x+182,y+46,'d-line','a9') if row==0 else L(x+182,y+46,x+164,y+46,'d-line','a9'))
    b.append('<path class="d-line" d="M652 122 V180" marker-end="url(#a9)"/>')
    b.append(T(24,296,'* 本報告推算：以編隊航速 10～12 節計。紅框為決定成敗的關鍵步驟。','d-ts'))
    return svg(760,306,'渡海登陸作戰流程',b)

def fig10():
    b=[R(250,16,260,52,'d-hi'),T(380,40,'東部戰區聯合指揮部','d-th','middle'),T(380,58,'南京；對台作戰主責','d-ts','middle')]
    cols=[('陸軍',['第71集團軍','第72集團軍','第73集團軍','兩棲合成旅×4','南部戰區74軍','另2旅可支援']),
          ('海軍',['東部戰區海軍','海軍陸戰隊','兩棲艦隊','驅護艦、潛艦','航艦編隊','（山東、福建）']),
          ('空軍',['東部戰區空軍','空降兵軍','運輸機、直升機','轟炸機、預警機','',''] ),
          ('火箭軍',['常規導彈旅','短中程彈道','巡弋飛彈','陸軍遠程火箭','（PCH191）','']),
          ('支援部隊',['信息支援部隊','網絡空間部隊','軍事航天部隊','聯勤保障部隊','','']),
          ('海警・民兵',['中國海警','海上民兵','徵用民船','滾裝船船隊','',''])]
    b.append(L(380,68,380,92)); b.append(L(80,92,685,92))
    for i,(h,ls) in enumerate(cols):
        x=24+i*121; cx=x+56; b.append(L(cx,92,cx,110))
        cls='d-tw' if i==5 else 'd-box'
        b.append(R(x,110,112,168,cls)); b.append(T(cx,134,h,'d-th','middle'))
        for j,l in enumerate([l for l in ls if l]): b.append(T(cx,160+j*20,l,'d-t','middle'))
    b.append(T(24,300,'兩棲合成旅：第72、73集團軍各2旅（東部戰區），第74集團軍2旅（南部戰區）。藍框為非軍隊但可能參與封鎖的力量。','d-ts'))
    return svg(760,312,'可能投入對台作戰兵力架構',b)

def fig11():
    rows=[('軍用兩棲艦首波',21000,'約 2.1 萬（2～2.5 萬）','bar'),('軍民船合計首波',60000,'約 6 萬','bar2'),('約 10 天累計（含民船）',300000,'約 30 萬','bar3')]
    X=lambda v:220+v/300000*480
    b=[]
    for t in [0,100000,200000,300000]:
        b.append(L(X(t),20,X(t),168,'grid')); b.append(T(X(t),186,'%d 萬'%(t//10000) if t else '0','d-ts','middle'))
    for i,(n,v,lab,c) in enumerate(rows):
        y=34+i*46; b.append(T(206,y+20,n,'d-t','end')); b.append('<rect class="%s" x="220" y="%d" width="%.1f" height="28" rx="2"/>'%(c,y,X(v)-220))
        tx=X(v)+8; anchor='start'
        if X(v)>620: tx=X(v)-8; anchor='end'
        b.append(T(tx,y+19,lab,'d-th',anchor))
    b.append(T(24,210,'來源：Tom Shugart、Dupuy Institute 估計（見參考資料 17、18）；人數，非裝備噸位。','d-ts'))
    return svg(760,220,'兩棲投送人數公開估計',b)

def fig12():
    st=[('鞏固灘頭','擴大登陸場、防反擊','d-box'),('奪港奪機場','空降、空突配合','d-hi'),('行政下卸','民船、重裝上岸','d-box'),('突破推進','沿西部走廊、阻斷南北','d-box'),('包圍首都','城鎮戰、斬首、癱瘓指揮','d-hi'),('綏靖控制','要點、媒體、基礎設施','d-box')]
    b=[ARROW('a12')]
    for i,(h,s,c) in enumerate(st):
        x=24+i*122; b.append(R(x,40,112,112,c)); b.append(T(x+56,30,'階段 %d'%(i+1),'d-ts','middle'))
        b.append(T(x+56,72,h,'d-th','middle'))
        for j,l in enumerate(s.split('、')): b.append(T(x+56,98+j*18,l,'d-t','middle'))
        if i<5: b.append(L(x+112,96,x+122,96,'d-line','a12'))
    b.append(R(24,170,722,44,'d-tw')); b.append(T(385,197,'國軍應對：灘後縱深決勝、濱海城鎮逐次遲滯、阻絕港口機場、反擊集中、全社會韌性','d-twt','middle'))
    return svg(760,226,'登陸後縱深作戰階段',b)

import maps
html=open('template.html').read()
for k,f in [('FIG1',fig1),('FIG2',fig2),('FIG3',fig3),('FIG4',fig4),('FIG5',fig5),('FIG6',fig6),('FIG9',fig9),('FIG10',fig10),('FIG11',fig11),('MAPA',maps.mapA),('MAPB',maps.mapB),('MAPC',maps.mapC),('FIG12',fig12)]:
    html=html.replace('{{%s}}'%k,f())
assert '{{' not in html
open('pla-taiwan-report.html','w').write(html); print(len(html))
