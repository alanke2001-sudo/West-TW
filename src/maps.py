import math
CN=[(122.0,29.9),(121.9,29.0),(121.6,28.5),(121.2,28.1),(120.8,27.6),(120.5,27.2),(120.2,26.8),(119.9,26.6),(119.7,26.3),(119.6,26.0),(119.8,25.6),(119.6,25.4),(119.2,25.2),(118.9,24.9),(118.6,24.6),(118.2,24.5),(117.9,24.2),(117.5,23.8),(117.1,23.5),(116.7,23.3),(116.3,23.0),(115.6,22.8),(114.8,22.6),(114.2,22.3),(113.5,22.2),(112.0,21.8),(110.5,21.3),(110.5,32),(123,32)]
TW=[(121.54,25.30),(121.75,25.15),(122.00,25.01),(121.85,24.75),(121.86,24.59),(121.62,23.98),(121.38,23.10),(121.15,22.75),(120.90,22.35),(120.85,21.90),(120.73,21.93),(120.58,22.37),(120.27,22.60),(120.10,23.00),(120.15,23.38),(120.18,23.70),(120.38,24.10),(120.50,24.27),(120.62,24.42),(120.85,24.70),(120.92,24.85),(121.10,25.05),(121.40,25.18)]
class P:
    def __init__(s,lon0,lon1,lat0,lat1,kx):
        s.lon0,s.lat1,s.kx=lon0,lat1,kx; s.ky=kx/math.cos(math.radians(24))
        s.W=round((lon1-lon0)*kx); s.H=round((lat1-lat0)*s.ky)
    def xy(s,lon,lat): return (round((lon-s.lon0)*s.kx,1), round((s.lat1-lat)*s.ky,1))
    def poly(s,pts,cls): return '<polygon class="%s" points="%s"/>'%(cls,' '.join('%s,%s'%s.xy(*p) for p in pts))
    def dot(s,lon,lat,r,cls): x,y=s.xy(lon,lat); return '<circle class="%s" cx="%s" cy="%s" r="%s"/>'%(cls,x,y,r)
    def text(s,lon,lat,t,cls='m-t',anchor='start',dx=0,dy=0):
        x,y=s.xy(lon,lat); return '<text class="%s" x="%s" y="%s" text-anchor="%s">%s</text>'%(cls,round(x+dx,1),round(y+dy,1),anchor,t)
def islands(p):
    o=[p.poly(TW,'tw')]
    o.append(p.poly([(119.52,23.70),(119.68,23.66),(119.70,23.52),(119.55,23.50)],'tw'))  # Penghu
    o.append(p.dot(118.35,24.45,4,'tw')); o.append(p.dot(119.95,26.16,3,'tw')); o.append(p.dot(121.55,22.05,2.5,'tw'))
    return o
def grid(p,lons,lats):
    o=[]
    for lo in lons:
        x,_=p.xy(lo,0); o.append('<line class="grid" x1="%s" y1="0" x2="%s" y2="%s"/>'%(x,x,p.H)); o.append('<text class="m-g" x="%s" y="%s">%s°E</text>'%(x+3,p.H-6,lo))
    for la in lats:
        _,y=p.xy(0,la); o.append('<line class="grid" x1="0" y1="%s" x2="%s" y2="%s"/>'%(y,p.W,y)); o.append('<text class="m-g" x="4" y="%s">%s°N</text>'%(y-4,la))
    return o
def port(p,lon,lat,name,anchor='start',dx=8,dy=4,cls='port'):
    return p.dot(lon,lat,4.5,cls)+p.text(lon,lat,name,'m-s',anchor,dx,dy)

def mapA():
    p=P(118.0,124.2,21.0,26.6,116)
    o=['<svg viewBox="0 0 %d %d" role="img" aria-label="解放軍封鎖台灣示意圖">'%(p.W,p.H),'<rect class="sea" x="0" y="0" width="%d" height="%d"/>'%(p.W,p.H)]
    o+=grid(p,[119,120,121,122,123,124],[22,23,24,25,26])
    o.append(p.poly(CN,'cn')); o+=islands(p)
    o.append(p.poly([(122.95,24.47),(123.05,24.48),(123.05,24.43),(122.95,24.43)],'jp')); o.append(p.text(123.05,24.45,'與那國島（日）','m-s','start',6,4))
    # zones (schematic)
    zones=[(121.75,25.75,'N','北部：基隆外海'),(122.7,24.35,'E1','東北：宜蘭外海'),(122.75,23.2,'E2','東部：花蓮外海'),(121.6,21.55,'S','南部：巴士海峽'),(119.55,22.45,'SW','西南：高雄外海'),(119.3,24.8,'W','中部：海峽中線附近'),(120.45,25.9,'NW','西北：台北港外海')]
    for lon,lat,k,name in zones:
        x,y=p.xy(lon,lat); o.append('<rect class="zone" x="%s" y="%s" width="78" height="52" rx="4"/>'%(x-39,y-26))
        o.append('<text class="m-z" x="%s" y="%s" text-anchor="middle">%s</text>'%(x,y+4,name.split('：')[0]))
        o.append('<text class="m-s" x="%s" y="%s" text-anchor="middle">%s</text>'%(x,y+42,name.split('：')[1]))
    # carrier east
    x,y=p.xy(123.65,22.6); o.append('<path class="cv" d="M%s %s l14 -8 l14 8 l-14 8z"/>'%(x-14,y)); o.append('<text class="m-s" x="%s" y="%s" text-anchor="middle">航艦編隊</text>'%(x,y+24)); o.append('<text class="m-s" x="%s" y="%s" text-anchor="middle">（台灣以東）</text>'%(x,y+40))
    # CCG ring dashed
    cx,cy=p.xy(120.95,23.65); o.append('<ellipse class="ccg" cx="%s" cy="%s" rx="%s" ry="%s"/>'%(cx,cy,round(1.35*p.kx),round(2.25*p.ky)))
    o.append(p.text(118.6,21.6,'虛線：海警「執法巡查」環線（示意）','m-s'))
    # rocket impact
    x,y=p.xy(120.05,25.35); o.append('<path class="impact" d="M%s %s l6 6 m0 -6 l-6 6"/>'%(x-3,y-3))
    # ports & energy
    o.append(port(p,121.74,25.14,'基隆港'))
    o.append(port(p,121.38,25.16,'台北港','end',-8,-6))
    o.append(port(p,120.50,24.28,'台中港／LNG','start',8,-8))
    o.append(port(p,120.28,22.60,'高雄港','end',-8,4))
    o.append(port(p,120.25,22.82,'永安LNG','end',-8,-6,'energy'))
    o.append(port(p,121.63,24.00,'花蓮港','start',8,4))
    o.append(port(p,121.86,24.60,'蘇澳港','start',8,4))
    o.append(p.text(120.95,23.65,'台灣','m-b','middle'))
    o.append(p.text(119.0,25.9,'福建','m-b','middle'))
    o.append(p.text(119.6,23.38,'澎湖','m-s','middle'))
    o.append(p.text(118.35,24.45,'金門','m-s','middle',0,-10))
    o.append(p.text(119.95,26.16,'馬祖','m-s','start',8,4))
    o.append(p.text(121.55,22.05,'蘭嶼','m-s','start',6,4)); o.append(p.text(123.4,25.9,'東海','m-g','middle')); o.append(p.text(123.4,21.4,'菲律賓海','m-g','middle'))
    o.append('</svg>'); return '\n'.join(o)

def mapB():
    p=P(116.6,123.0,21.8,28.0,108)
    o=['<svg viewBox="0 0 %d %d" role="img" aria-label="航渡規劃示意圖">'%(p.W,p.H),'<rect class="sea" x="0" y="0" width="%d" height="%d"/>'%(p.W,p.H)]
    o+=grid(p,[117,118,119,120,121,122],[22,23,24,25,26,27])
    o.append(p.poly(CN,'cn')); o+=islands(p)
    # lanes
    lanes=[((119.75,26.1),(121.1,25.06),'N'),((119.82,25.5),(120.55,24.28),'C'),((119.05,25.15),(120.5,24.25),'C'),((118.15,24.45),(120.12,23.02),'S'),((116.75,23.3),(120.12,22.98),'S'),((118.6,24.7),(119.6,23.6),'P')]
    for a,b,k in lanes:
        x1,y1=p.xy(*a); x2,y2=p.xy(*b); mx=(x1+x2)/2; my=(y1+y2)/2-18
        o.append('<path class="lane lane-%s" d="M%s %s Q%s %s %s %s" marker-end="url(#ah)"/>'%(k,x1,y1,round(mx,1),round(my,1),x2,y2))
    o.insert(1,'<defs><marker id="ah" viewBox="0 0 10 10" refX="8" refY="5" markerWidth="7" markerHeight="7" orient="auto-start-reverse"><path d="M0 0L10 5L0 10z" class="ahead"/></marker></defs>')
    # embark
    for lon,lat,n,an,dx,dy in [(119.65,26.1,'福州／連江','end',-10,4),(119.8,25.5,'平潭','end',-10,4),(119.05,25.2,'莆田（湄洲灣）','end',-10,4),(118.65,24.75,'泉州','end',-10,0),(118.1,24.5,'廈門','end',-10,10),(116.75,23.32,'汕頭（南部戰區）','start',8,-10)]:
        o.append(p.dot(lon,lat,6,'emb')+p.text(lon,lat,n,'m-s',an,dx,dy))
    # beaches
    for lon,lat,n,an,dx,dy in [(121.1,25.06,'桃園（觀音、竹圍）','start',4,-16),(120.5,24.25,'台中（草湳、大安）','start',10,4),(120.12,23.0,'台南（西海岸）','start',10,8)]:
        x,y=p.xy(lon,lat); o.append('<rect class="beach" x="%s" y="%s" width="12" height="12" transform="rotate(45 %s %s)"/>'%(x-6,y-6,x,y)); o.append(p.text(lon,lat,n,'m-r',an,dx,dy))
    # distance
    a=p.xy(119.8,25.45); b=p.xy(120.95,24.85); o.append('<line class="meas" x1="%s" y1="%s" x2="%s" y2="%s"/>'%(a[0],a[1],b[0],b[1]))
    o.append(p.text(122.9,26.9,'虛線：平潭至新竹','m-s','end')); o.append(p.text(122.9,26.9,'海峽最窄處約 130 公里','m-r','end',0,18))
    o.append(p.text(122.9,27.8,'↑ 舟山／寧波（圖外）','m-s','end')); o.append(p.text(122.9,27.8,'東部戰區海軍主要基地','m-s','end',0,16))
    o.append(p.text(120.95,23.65,'台灣','m-b','middle'))
    o.append(p.text(118.2,26.6,'福建','m-b','middle')); o.append(p.text(119.4,27.6,'浙江','m-b','middle'))
    o.append(p.text(119.52,23.6,'澎湖','m-s','end',-8,4))
    o.append(p.text(118.35,24.45,'金門','m-s','start',6,-8)); o.append(p.text(119.95,26.16,'馬祖','m-s','start',8,4))
    o.append(p.text(117.0,22.15,'↙ 湛江：水橋駁船 2025 試驗（圖外）','m-s'))
    o.append(p.text(122.4,27.4,'東海','m-g','middle'))
    o.append('</svg>'); return '\n'.join(o)
if __name__=='__main__':
    open('mapA.svg','w').write(mapA()); open('mapB.svg','w').write(mapB()); print('ok')

def mapC():
    p=P(119.3,122.3,21.8,25.45,190)
    o=['<svg viewBox="0 0 %d %d" role="img" aria-label="登陸後縱深作戰可能行動示意圖">'%(p.W,p.H),
       '<defs><marker id="ac" viewBox="0 0 10 10" refX="8" refY="5" markerWidth="6" markerHeight="6" orient="auto-start-reverse"><path d="M0 0L10 5L0 10z" class="ahead"/></marker><marker id="ab" viewBox="0 0 10 10" refX="8" refY="5" markerWidth="6" markerHeight="6" orient="auto-start-reverse"><path d="M0 0L10 5L0 10z" class="bhead"/></marker></defs>',
       '<rect class="sea" x="0" y="0" width="%d" height="%d"/>'%(p.W,p.H)]
    o+=grid(p,[120,121,122],[22,23,24,25])
    o+=islands(p)
    o.append(p.poly([(121.55,24.75),(121.45,24.3),(121.3,23.7),(121.1,23.1),(120.9,22.6),(120.8,22.3),(120.72,22.45),(120.78,23.0),(120.9,23.6),(121.05,24.15),(121.25,24.55),(121.4,24.8)],'mtn'))
    o.append(p.text(121.0,23.55,'中央山脈','m-g','middle'))
    def arr(pts,cls='push',m='ac'):
        d='M'+' L'.join('%s %s'%p.xy(*q) for q in pts); return '<path class="%s" d="%s" marker-end="url(#%s)"/>'%(cls,d,m)
    # lodgments
    for lon,lat in [(121.1,25.06),(120.5,24.25),(120.12,23.0)]:
        x,y=p.xy(lon,lat); o.append('<ellipse class="lodg" cx="%s" cy="%s" rx="22" ry="14"/>'%(x,y))
    o.append(arr([(121.12,25.05),(121.25,25.06),(121.42,25.04)]))
    o.append(arr([(121.38,25.15),(121.45,25.1),(121.5,25.06)]))
    o.append(arr([(120.55,24.3),(120.8,24.62),(120.95,24.78)]))
    o.append(arr([(120.5,24.2),(120.45,23.85),(120.45,23.55)],'push dash'))
    o.append(arr([(120.15,22.95),(120.22,22.75),(120.28,22.64)]))
    o.append(arr([(120.05,23.55),(120.3,23.5)],'push dash'))
    o.append(arr([(121.6,22.55),(121.25,22.72)],'push dash'))
    # airborne
    for lon,lat in [(121.23,25.08),(120.62,24.26),(119.62,23.57)]:
        x,y=p.xy(lon,lat); o.append('<path class="para" d="M%s %s a9 9 0 0 1 18 0 z M%s %s L%s %s M%s %s L%s %s"/>'%(x-9,y-12,x-9,y-12,x,y,x+9,y-12,x,y))
    # Taiwan counter
    o.append(arr([(120.55,23.15),(120.6,23.6),(120.68,24.0)],'counter','ab'))
    o.append(arr([(121.3,24.6),(121.2,24.85)],'counter','ab'))
    # places
    for lon,lat,n,an,dx,dy in [(121.52,25.04,'台北','start',8,4),(121.23,25.08,'桃園機場','end',-30,-14),(121.38,25.16,'台北港','start',8,-6),(120.97,24.8,'新竹','start',8,4),(120.62,24.26,'清泉崗','start',10,4),(120.5,24.28,'台中港','end',-26,-4),(120.45,23.48,'嘉義','start',8,4),(120.2,23.0,'台南','end',-30,4),(120.28,22.6,'高雄港','end',-10,4),(121.6,23.98,'花蓮','start',8,4),(121.15,22.75,'台東','end',-10,4),(121.75,24.75,'宜蘭','start',8,4)]:
        o.append(p.dot(lon,lat,4,'port')+p.text(lon,lat,n,'m-s',an,dx,dy))
    o.append(p.text(119.62,23.57,'澎湖','m-s','middle',0,22))
    o.append(p.text(119.4,25.3,'北部軸線：灘頭→桃園機場→林口→台北','m-r'))
    o.append(p.text(119.4,25.3,'中部：台中港與清泉崗，沿西部走廊南北推進','m-s','start',0,20))
    o.append(p.text(119.4,22.35,'虛線：間接路線推估（嘉義、東部）','m-s'))
    o.append(p.text(119.4,22.35,'藍色：國軍反擊集中方向（示意）','m-twt','start',0,18))
    o.append('</svg>'); return '\n'.join(o)
