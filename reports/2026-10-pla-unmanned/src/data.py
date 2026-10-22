# -*- coding: utf-8 -*-
"""資料庫內容：參考資料、章節與條目。build.py 讀取本檔產生網頁、JSON、CSV 與 Word 檔。

判讀層級 label：fact 事實／off 官方評估／est 推估／calc 本報告推算／gap 資料缺口
"""

REFS = {
 1: ("Wikipedia, “2025 China Victory Day Parade”（閱兵受閱裝備清單）", "https://en.wikipedia.org/wiki/2025_China_Victory_Day_Parade"),
 2: ("The War Zone, “China’s Imposing LY-1 High-Power Laser Weapon Unveiled At Huge Military Parade,” 2025-09", "https://www.twz.com/news-features/chinas-imposing-ly-1-high-power-laser-weapon-unveiled-at-huge-military-parade"),
 3: ("Unmanned Airspace, “China’s new integrated direct-energy C-UAV capabilities go on display,” 2025-09", "https://www.unmannedairspace.info/counter-uas-systems-and-policies/chinas-new-integrated-direct-energy-c-uav-capabilities-go-on-display/"),
 4: ("環球時報（Global Times）, “Tank and artillery, unmanned ship and underwater vehicles, high-energy weapons, hypersonic missiles shine at parade,” 2025-09", "https://www.globaltimes.cn/page/202509/1342575.shtml"),
 5: ("Naval News, “Chinese Military Parade Highlights Naval Drones And Missiles,” 2025-09", "https://www.navalnews.com/naval-news/2025/09/chinese-military-parade-highlights-naval-drones-and-missiles/"),
 6: ("Wikipedia, “Hongdu GJ-11”", "https://en.wikipedia.org/wiki/Hongdu_GJ-11"),
 7: ("Janes, “China deploys UAVs near Taiwan, Japan”", "https://www.janes.com/defence-intelligence-insights/defence-news/defence/china-deploys-uavs-near-taiwan-japan"),
 8: ("Janes, “China fields EW-equipped BZK-005 UAV variants for long-range ELINT operations”", "https://www.janes.com/defence-intelligence-insights/defence-news/air/china-fields-ew-equipped-bzk-005-uav-variants-for-long-range-elint-operations"),
 9: ("中央社，〈國防部：共軍BZK-005偵察型無人機 擾台西南ADIZ〉，2022-09-09", "https://www.cna.com.tw/news/aipl/202209090212.aspx"),
 10: ("The Defense Post, “Chinese ‘Scorpion’ Combat Drone Circles Taiwan,” 2023-04-28", "https://www.thedefensepost.com/2023/04/28/chinese-drone-circles-taiwan"),
 11: ("The War Zone, “Japanese Fighters Intercept China’s High-Flying WZ-7 Drone For First Time,” 2023-01", "https://www.twz.com/japanese-fighters-intercept-chinas-high-flying-wz-7-drone-for-first-time"),
 12: ("Wikipedia, “AVIC WZ-8”（含 2023 年外洩美國 NGA/NASIC 報告內容）", "https://en.wikipedia.org/wiki/AVIC_WZ-8"),
 13: ("Janes, “Wing Loong II UAV recorded in Taiwan ADIZ for first time,” 2023-10", "https://www.janes.com/osint-insights/defence-news/defence/wing-loong-ii-uav-recorded-in-taiwan-adiz-for-first-time"),
 14: ("The War Zone, “China’s High-Flying Swarm Mothership Drone Has Flown,” 2025-12-11", "https://www.twz.com/air/chinas-high-flying-swarm-mothership-drone-has-flown"),
 15: ("CNA（美國海軍分析中心）, Timothy Ditter, “China Readies Drone Swarms for Future War,” 2025-09-24", "https://www.cna.org/our-media/indepth/2025/09/china-readies-drone-swarms-for-future-war"),
 16: ("The Defense Post, “China unveils loyal wingman drone …”, 2024-12-16", "https://thedefensepost.com/2024/12/16/china-loyal-wingman-us"),
 17: ("The War Zone, “China’s Stealthy CH-7 Flying Wing Drone Has Flown,” 2025-12", "https://www.twz.com/air/chinas-stealthy-ch-7-long-endurance-drone-is-now-flying"),
 18: ("China Global South Project, “China Stations Jets-Turned-Drones at Bases Near Taiwan Strait, Report Says,” 2026-03-27（引 Mitchell Institute〈China Airpower Tracker〉）", "https://chinaglobalsouth.com/2026/03/27/china-jet-drones-taiwan-strait-pla-air-defense-strategy/"),
 19: ("Wikipedia, “Feilong (loitering munition)”", "https://en.wikipedia.org/wiki/Feilong_(loitering_munition)"),
 20: ("Army Recognition, “China tests ASN-301 anti-radar drone raising new threats for U.S. and allied forces,” 2025-10-27", "https://www.armyrecognition.com/archives/archives-land-defense/defense-news-army-2025/china-tests-asn-301-anti-radar-drone-raising-new-threats-for-u-s-and-allied-forces"),
 21: ("Janes, “China conducts vehicle-launched loitering munition live-fire exercise,” 2025-10", "https://www.janes.com/defence-intelligence-insights/defence-news/defence/china-conducts-vehicle-launched-loitering-munition-live-fire-exercise"),
 22: ("The War Zone, “Chinese Soldiers Train To Fend Off FPV Drones,” 2024-05-20", "https://www.twz.com/news-features/chinese-soldiers-train-to-fend-off-fpv-drones"),
 23: ("Army Technology, “China conducts plateau flight test of unmanned helicopter,” 2020-09-29", "https://army-technology.com/news/china-plateau-flight-test-unmanned-helicopter"),
 24: ("South China Morning Post, “China’s Type 076 amphibious assault ship Sichuan in final tests …”, 2026-07-29", "https://www.scmp.com/news/china/military/article/3362271/chinas-type-076-amphibious-assault-ship-sichuan-final-tests-drone-catapult"),
 25: ("Wikipedia, “JARI USV”", "https://en.wikipedia.org/wiki/JARI_USV"),
 26: ("South China Morning Post, “PLA sends drone into airspace near Taiwan-held Pratas Island in South China Sea,” 2026-01-18", "https://www.scmp.com/news/china/military/article/3340297/pla-sends-drone-airspace-near-taiwan-held-pratas-island-south-china-sea"),
 27: ("Wikipedia, “Justice Mission 2025”（正義使命-2025 演習）", "https://en.wikipedia.org/wiki/Justice_Mission_2025"),
 28: ("Radio Free Asia, “Taiwan threatens to shoot down Chinese drones following further incursions,” 2022-08-30", "https://www.rfa.org/english/news/china/taiwan-threatens-to-shoot-down-drones-08302022025101.html"),
 29: ("Army Recognition, “Chinese military drones double up against Taiwan …”, 2024-08", "https://www.armyrecognition.com/archives/archives-aerospace-defense/2024/chinese-military-drones-double-up-against-taiwan-while-placing-troops-near-taiwans-strait"),
 30: ("Army Recognition, “Chinese army demonstrates machine gun-equipped robotic dogs in joint exercise with Cambodia,” 2024", "https://www.armyrecognition.com/archives/archives-land-defense/land-defense-2024/chinese-army-demonstrates-machine-gun-equipped-robotic-dogs-in-joint-exercise-with-cambodia"),
 31: ("Militär Aktuell, “Beijing’s pack of wolves: armed robot dogs as the spearhead of the People’s Liberation Army,” 2026-08", "https://militaeraktuell.at/en/beijings-pack-of-wolves-armed-robot-dogs-as-the-spearhead-of-the-peoples-liberation-army/"),
 32: ("世界日報，〈中國曝光最新無人化作戰模式 「機器狼」分工射擊畫面引熱議〉，2025-08-06", "https://www.worldjournal.com/wj/amp/story/121339/8920961"),
 33: ("Kharon, “Unitree Robotics IPO, China PLA, robot wolf,” 2026", "https://www.kharon.com/brief/unitree-robotics-ipo-china-pla-robot-wolf"),
 34: ("Defense One, “China’s counter-UAV efforts reveal more technological advancement,” 2025-05", "https://www.defenseone.com/technology/2025/05/chinas-counter-uav-efforts-reveal-more-technological-advancement/405031"),
 35: ("Asia Times, “China’s Hurricane 3000 casts an electric storm in the Taiwan Strait,” 2026-01", "https://asiatimes.com/2026/01/chinas-hurricane-3000-casts-an-electric-storm-in-the-taiwan-strait/"),
 36: ("Interesting Engineering, “New Chinese weapon uses microwave energy …”（颶風-3000），2026-01", "https://interestingengineering.com/military/new-chinese-weapon-microwave-energy"),
 37: ("U.S. Army War College SSI, Jake Rinaldi & Jake Vartanian, “Rethinking Denial: The People’s Liberation Army’s Laser Systems …”, 2025-01-14", "https://ssi.armywarcollege.edu/SSI-Media/Recent-Publications/Article/4029077/rethinking-denial-the-peoples-liberation-armys-laser-systems-and-the-future-cha/"),
 38: ("EurAsian Times, “China shoots down suicide drones attacking its AWACS aircraft …”, 2023-10-15", "https://www.eurasiantimes.com/china-shoots-down-suicide-drones-attacking-its-awacs-aircraft-as-pla-tries-replicating-ukraine-russia-war"),
 39: ("Defence Blog, “China shows its drone-killing monster in action,” 2023-12-29", "https://defence-blog.com/china-unveils-type-625-air-defense-system/"),
 40: ("Defence Blog, “China shows dozen drone-killers in live-fire exercise,” 2025-06-08", "https://defence-blog.com/china-shows-dozen-drone-killers-in-live-fire-exercise/"),
 41: ("Army Recognition, “Chinese HQ-17A SHORAD air defense system deployed by PLA 78th Army Group,” 2020-07-22", "https://www.armyrecognition.com/archives/archives-land-defense/land-defense-2020/chinese-hq-17a-shorad-air-defense-system-deployed-by-pla-78th-army-group"),
 42: ("Wikipedia, “QW missile”（前衛系列）", "https://en.wikipedia.org/wiki/QW_missile"),
 43: ("Army Recognition, “Iran Chinese MANPADS missile deal: QW-12, FN-16,” 2026", "https://www.armyrecognition.com/news/army-news/2026/iran-chinese-manpads-missile-deal-qw12-fn16"),
 44: ("EurAsian Times, 解放軍軍官於官媒紀錄片談單兵防空武器對直升機威脅，2024-09-17", "https://www.eurasiantimes.com/chinas-military-commander-identifies"),
 45: ("The Aviationist, “Chinese J-10 Drops Flares In front Of Australian MH-60R During ‘Unprofessional’ Intercept,” 2024-05-08", "https://theaviationist.com/2024/05/08/chinese-j-10-intercept-of-mh-60r-helicopter/"),
 46: ("加拿大國防部, “Statement from the Canadian Armed Forces Regarding Unsafe Intercept of Royal Canadian Air Force Helicopter,” 2023-11", "https://www.canada.ca/en/department-national-defence/news/2023/11/statement-from-the-canadian-armed-forces-regarding-unsafe-intercept-of-royal-canadian-air-force-helicopter.html"),
 47: ("The War Zone, “German Surveillance Plane Targeted By Chinese Warship’s Laser In Red Sea Points To Disturbing Pattern,” 2025-07", "https://www.twz.com/sea/german-surveillance-plane-targeted-by-chinese-warships-laser-in-red-sea-points-to-disturbing-pattern"),
 48: ("BenarNews, “Manila: Chinese helicopter came within 3 meters of Philippine aircraft,” 2025-02-18", "https://www.benarnews.org/english/news/philippine/south-china-sea-coast-guard-helicopter-02182025141538.html"),
 49: ("Wikipedia, “List of active People’s Liberation Army aircraft”", "https://en.wikipedia.org/wiki/List_of_active_People%27s_Liberation_Army_aircraft"),
 50: ("中央社，〈共軍BZK-005無人機順時針繞台 國防部嚴密監控〉，2023-05-03", "https://www.cna.com.tw/news/aipl/202305030033.aspx"),
 51: ("Army Recognition, “PLA Chinese army demonstrates capabilities of QW-12 portable air defense missile,” 2022", "https://www.armyrecognition.com/news/army-news/2022/pla-chinese-army-demonstrates-capabilities-of-qw-12-portable-air-defense-missile"),
}

# 章節：anchor, 編號, 標題, 引言
CHAPTERS = [
 ("c1", "第一章", "無人飛行載具", "依任務分為高空偵察、中空長航時、隱身攻擊與忠誠僚機、母機與蜂群、巡飛彈、戰術小型與艦載旋翼機，並列入可作為無人機載台的 076 型艦。"),
 ("c2", "第二章", "機器狗與無人地面載具", "解放軍以四足機器人（機器狗、機器狼）與輪式無人車推動「有人／無人協同」，目前公開所見仍以演習、展覽與官媒畫面為主。"),
 ("c3", "第三章", "無人水面與水下載具", "2025 年閱兵首度集中展示大型無人潛航器與無人艇，任務包括情蒐、反潛、布雷與掃雷。"),
 ("c4", "第四章", "反無人機與電子干擾體系", "解放軍以「偵測、干擾、硬殺傷」分層建構反無人機能力，涵蓋雷射、高功率微波、彈砲合一系統、單兵干擾槍與整合指管網路。"),
 ("c5", "第五章", "威脅直升機飛行的作為", "包括可攻擊低空直升機的便攜與野戰防空武器、以戰機熱焰彈或近距離逼近干擾直升機的實際事件、艦艇雷射照射航空器紀錄，以及無人機與定向能武器的潛在威脅。"),
]

# 條目欄位：id, ch, sub(小節), name, alias, kind, maker, status, specs, activity, assess(研判), label(主判讀), alabel(研判判讀), refs, tags
E = []
def add(**k):
    k.setdefault('alias', ''); k.setdefault('maker', '未公開'); k.setdefault('specs', ''); k.setdefault('activity', '')
    k.setdefault('assess', ''); k.setdefault('alabel', 'est'); k.setdefault('label', 'fact'); k.setdefault('tags', [])
    E.append(k)

# ── 第一章 無人飛行載具 ──
add(id="U01", ch="c1", sub="高空長航時偵察", name="無偵-7（WZ-7）「翔龍」", alias="Soaring Dragon", kind="高空長航時偵察無人機",
    maker="貴州航空工業", status="服役（海軍、空軍）",
    specs="噴射動力、菱形連翼構型；估計航程約 7,000 公里，升限約 18,000 公尺（6 萬呎），滯空至少約 10 小時。",
    activity="2021 年珠海航展首度公開。2023-01-01 日本首度派戰機應對，航線經宮古海峽進入菲律賓海、繞至先島群島以南，隔日同航線再飛。也曾在西藏、中朝邊境一帶執勤。",
    assess="類似美軍 RQ-4 全球鷹，可對台灣東部海域與美日部隊長時間監視，並可能擔任海上編隊的超視距通信中繼。",
    refs=[11], tags=["高空偵察", "情監偵", "東部海域"])
add(id="U02", ch="c1", sub="高空長航時偵察", name="無偵-8（WZ-8）", alias="超音速偵察無人機", kind="空射超音速偵察無人機",
    maker="中國航空工業集團（AVIC）", status="服役（空軍）",
    specs="無法自行起飛，由轟-6M 轟炸機掛載投放後點燃火箭發動機；廠商宣稱巡航速度約 3 馬赫，裝有光電與合成孔徑雷達。",
    activity="2023 年外洩的美國國家地理空間情報局報告稱，解放軍「幾乎可以確定」已在安徽六安基地成立首支超音速無人機部隊，由東部戰區空軍操作。",
    assess="適合戰前目標偵察與打擊後毀傷評估；台灣學者認為主要用途可能是偵察美軍太平洋基地，屬反介入／區域拒止體系。",
    refs=[12], tags=["高空偵察", "東部戰區", "美國國防部"])
add(id="U03", ch="c1", sub="高空長航時偵察", name="彩虹-7（CH-7）", alias="", kind="高空長航時隱身飛翼無人機",
    maker="中國航天科技集團（CASC）第十一研究院", status="試飛中",
    specs="暫定數據：長 10 公尺、最大起飛重量 10 噸、最大速度約 926 公里／時、續航最長 15 小時。",
    activity="官媒於 2025-12-15 公布首飛影像，疑在陝西蒲城機場。",
    assess="主要用於隱身偵察；總設計師稱「必要時打擊目標」，但影像未清楚顯示內置彈艙，打擊能力待觀察。",
    refs=[17], tags=["高空偵察", "隱身無人機"])
add(id="U04", ch="c1", sub="中空長航時", name="BZK-005「長鷹」及電戰變型", alias="BZK-005B／D／E", kind="中空長航時偵察／電子情報無人機",
    maker="北京航空航天大學", status="服役（陸、海、空軍）",
    specs="BZK-005E：翼展 18 公尺、最大起飛重量 1,500 公斤、酬載 370 公斤、巡航約 180 公里／時、升限 7,500 公尺。已知至少三種特種變型，加裝電子情報莢艙或機載電戰系統。",
    activity="空軍約 2007 年、海軍 2009 年開始使用。台、日國防部門長期記錄其經巴士海峽、台灣海峽、宮古海峽活動；2022-09 進入台灣西南空域，2023-05 順時針繞台。",
    assess="是目前對台頻率最高的無人機之一，兼具影像偵察與電子情報蒐集，可長期描繪台灣雷達與通信電磁特徵。",
    refs=[7, 8, 9, 50], tags=["中空長航時", "電子戰", "情監偵", "台灣國防部"])
add(id="U05", ch="c1", sub="中空長航時", name="TB-001「雙尾蠍」", alias="Twin-Tailed Scorpion", kind="中空長航時察打一體無人機",
    maker="四川騰盾科技", status="使用中",
    specs="中國最大型無人機之一，航程約 6,000 公里，可攜帶大量武器。",
    activity="2023-04-27 至 28 日首度由台海中線南端越線、沿台灣東岸繞行後返回，為國防部首次公布共機由中線一端繞到另一端；也曾與 BZK-005 經宮古海峽飛往先島群島以南。",
    assess="繞台航線顯示解放軍在演練以無人機在台灣東側長時間監控與潛在打擊。",
    refs=[10, 7], tags=["中空長航時", "察打一體", "東部海域", "台灣國防部"])
add(id="U06", ch="c1", sub="中空長航時", name="攻擊-2（GJ-2）／翼龍-2", alias="Wing Loong II", kind="中空長航時察打一體無人機",
    maker="中國航空工業集團成都所", status="服役（空軍，2018 年起）",
    specs="六個翼下武器掛點，可執行情監偵與對地攻擊；已大量外銷。",
    activity="2023-10-03 首度出現在台灣防空識別區西南角（東沙以北）。2025 年閱兵無人作戰方隊受閱。",
    assess="Janes 研判首次進入識別區可能是在測試新能力或新系統。",
    refs=[13, 1], tags=["中空長航時", "察打一體", "台灣國防部"])
add(id="U07", ch="c1", sub="中空長航時", name="其他 BZK 系列與彩虹-4B", alias="BZK-006／007／008／009、CH-4B", kind="戰術至中空長航時無人機",
    maker="貴州、愛生、航天科技、瀋陽等", status="服役（依公開清單）",
    specs="公開清單列出 BZK-006、BZK-007、BZK-008、BZK-009 與 CH-4B（至少 5 架），多數未公開數量與性能。",
    activity="",
    assess="屬於維基百科彙整的現役清單，數量與編配仍需其他來源佐證。",
    refs=[49], tags=["中空長航時", "情監偵"])
add(id="U08", ch="c1", sub="隱身攻擊與忠誠僚機", name="攻擊-11（GJ-11）「利劍」", alias="Sharp Sword", kind="隱身無人作戰機",
    maker="洪都航空、瀋陽飛機設計研究所", status="可能已服役",
    specs="無尾飛翼、單發渦扇、兩個內置彈艙；長 12.2 公尺、翼展 14.4 公尺。可執行精確打擊、偵察，並可投放誘餌或電戰載荷。",
    activity="2013 年首飛，2021 年珠海航展展示，2024 年多架出現在新疆馬蘭基地並測試有人／無人協同，2025 年閱兵受閱；維基百科稱 2025-09 時「很可能已服役」。",
    assess="被解放軍稱為「忠誠僚機」，可與殲-20 等有人機協同，先行突入台灣防空網偵察或打擊。",
    refs=[6, 1], tags=["隱身無人機", "忠誠僚機", "有人無人協同"])
add(id="U09", ch="c1", sub="隱身攻擊與忠誠僚機", name="攻擊-21（GJ-21）艦載型", alias="GJ-11J", kind="艦載隱身無人作戰機",
    maker="洪都航空、瀋陽飛機設計研究所", status="試飛中",
    specs="折疊翼、尾鉤、雙前輪與彈射桿，適用電磁彈射起降。",
    activity="2025 年閱兵出現兩架（編號 21、22）；2026-01 在 076 型艦甲板發現模型，2026-05 原型機試飛。",
    assess="預料將成為 076 型艦航空聯隊的一部分，使兩棲艦隊具備艦載無人打擊能力。",
    refs=[6, 5, 24], tags=["隱身無人機", "艦載無人機", "兩棲艦艇"])
add(id="U10", ch="c1", sub="隱身攻擊與忠誠僚機", name="2025 年閱兵新型無人作戰機（A、B、D、E 型）", alias="", kind="無人作戰機／協同作戰飛機",
    maker="未公開", status="展示",
    specs="閱兵資料分類為：A 型無尾 λ 翼、B 型無尾修改三角翼、D 型斜尾三角翼有人／無人協同機、E 型斜尾後掠翼有人／無人協同機。",
    activity="2025-09-03 北京閱兵無人作戰方隊首度公開。",
    assess="CNA 指出其中戰鬥機尺寸的無人機可能是「協同作戰飛機」，若已形成戰力，可能是全球首種達初始作戰能力的同類機型；是否量產仍待觀察。",
    refs=[1, 15], tags=["隱身無人機", "忠誠僚機", "閱兵"])
add(id="U11", ch="c1", sub="隱身攻擊與忠誠僚機", name="飛鴻-97A（FH-97A）", alias="", kind="忠誠僚機",
    status="研發展示",
    specs="具內置彈艙，可掛空對空與空對地彈藥；可引導小型無人機蜂群或擔任殲-20 僚機，亦可由航艦彈射。",
    activity="2024 年珠海航展展示。",
    assess="分析人士估計至少五年後才可能大規模部署。",
    refs=[16], tags=["忠誠僚機", "有人無人協同"])
add(id="U12", ch="c1", sub="隱身攻擊與忠誠僚機", name="殲-6 改裝無人機", alias="J-6 drone conversion", kind="舊式戰機改裝攻擊無人機",
    maker="解放軍空軍", status="部署",
    specs="以 1960 年代起服役的殲-6 戰機改裝為攻擊無人機。",
    activity="美國 Mitchell 航太研究所依衛星影像，指其部署於台海周邊 6 座空軍基地（福建 5 座、廣東 1 座）；2026-03-10 商業衛星影像顯示福建龍田基地跑道旁成排停放。",
    assess="本報告推估：可在開戰初期大量出動，消耗台灣防空飛彈或誘使雷達開機，為後續打擊開路。",
    refs=[18], tags=["攻擊無人機", "台灣海峽", "東部戰區"])
add(id="U13", ch="c1", sub="母機與蜂群", name="九天（Jiu Tian）無人機母機", alias="SS-UAV", kind="高空長航時蜂群母機",
    maker="中國航空工業集團（AVIC）", status="試飛中",
    specs="長約 16.35 公尺、翼展 25 公尺、最大起飛重量約 16 噸、酬載約 6,000 公斤、轉場航程約 7,000 公里、續航 12 小時、升限 15,000 公尺；模組化酬載艙可投放無人機蜂群。",
    activity="2025-12-11 於陝西蒲城首飛。",
    assess="CNA 稱可由兩個內艙釋放 100 至 150 架小型巡飛彈；可在台灣防空射程外投放蜂群，飽和攻擊雷達、防空陣地與港口。",
    refs=[14, 15], tags=["蜂群", "母機", "巡飛彈"])
add(id="U14", ch="c1", sub="母機與蜂群", name="固定翼無人機蜂群（中國電科）", alias="", kind="蜂群偵察與打擊",
    maker="中國電子科技集團（CETC）", status="試驗",
    specs="2020 年以地面發射器一次釋放 48 架固定翼無人機，並搭配直升機投放；2021-05 測試可發射 200 架的發射器。",
    activity="解放軍在兩棲登陸演習中使用偵察蜂群，並以台灣外形的目標測試無人機編隊。2025-08 演練無人機蜂群與機器狼的城鎮戰協同。",
    assess="CNA 指出蜂群的實際自主程度仍不清楚。",
    refs=[15], tags=["蜂群", "登陸作戰", "城鎮戰"])
add(id="U15", ch="c1", sub="巡飛彈", name="ASN-301／飛龍-300A 反輻射巡飛彈", alias="", kind="反輻射巡飛彈（壓制防空）",
    maker="中國航空工業集團（AVIC）", status="部署（東部戰區實射）",
    specs="仿以色列「哈比」反輻射無人機。重約 135 公斤、航程約 288 公里、滯空近 4 小時、最大速度約 220 公里／時；被動雷達導引頭涵蓋 2 至 16 GHz，雷射近炸引信可散布約 7,000 枚預製破片。卡車載六聯裝發射箱。",
    activity="2017 年阿布達比防務展公開。央視 2025-10-27 報導東部戰區以車載六聯裝發射箱實施實彈射擊。",
    assess="專門獵殺開機中的防空與預警雷達，對台灣防空網構成直接威脅。",
    refs=[19, 20, 21], tags=["巡飛彈", "反輻射", "東部戰區", "演習報導"])
add(id="U16", ch="c1", sub="巡飛彈", name="飛龍系列巡飛彈", alias="Feilong-5A／10A／30／60A／60B／300D", kind="巡飛彈家族",
    maker="中國兵器工業集團（北方工業）", status="研發／外銷；解放軍列裝未證實",
    specs="5A 為小型四旋翼；10A 以迫擊砲式發射器發射；30 可由卡車、裝甲車與艦艇發射；60A／60B 由 SR-5 多管火箭發射；300D 報稱航程約 1,000 公里。",
    activity="2022 年珠海航展展出多款；2025-03 報導火箭發射型完成研發。",
    assess="若納入陸軍火箭砲部隊，可使多管火箭兼具遠程偵察與精確打擊。",
    refs=[19], tags=["巡飛彈"])
add(id="U17", ch="c1", sub="戰術小型", name="第一人稱視角（FPV）與小型多旋翼無人機", alias="FPV", kind="戰術攻擊／偵察小型無人機",
    maker="民用與軍工多家", status="部隊訓練中",
    specs="手擲起飛，可攜爆裂物攻擊裝甲車與陣地，或在建物間偵察。",
    activity="2024 年解放軍與武警公開 FPV 攻擊裝甲車、模擬陣地及城鎮障礙飛行訓練；2025-07 第 76 集團軍結合機器狗與 FPV 演練突擊。",
    assess="借鑑烏克蘭戰場經驗；對灘岸防禦陣地、裝甲車與低空懸停直升機都可能構成威脅。",
    refs=[22, 31], tags=["FPV", "城鎮戰", "有人無人協同"])
add(id="U18", ch="c1", sub="艦載與旋翼", name="艦載無人直升機（AR-2000 類）", alias="", kind="艦載垂直起降無人機",
    maker="中國航空工業集團（推測）", status="展示",
    specs="折疊旋翼，供艦艇起降。",
    activity="2025 年閱兵受閱，外型近似 AR-2000，與 075、076 型兩棲艦附近出現的模型相符。",
    assess="可為兩棲艦隊提供艦載偵察與目標指示。",
    refs=[5, 1], tags=["艦載無人機", "兩棲艦艇"])
add(id="U19", ch="c1", sub="艦載與旋翼", name="AR-500C 無人直升機", alias="", kind="無人直升機",
    maker="中國航空工業集團（AVIC）", status="試驗",
    specs="可攜 80 公斤酬載飛行 5 小時以上。",
    activity="2020 年在四川稻城亞丁機場完成高原試飛。",
    assess="廠商稱可用於偵察、通信、電子干擾、目標指示、火力打擊與物資運送。",
    refs=[23], tags=["無人直升機", "電子戰"])
add(id="U20", ch="c1", sub="艦載與旋翼", name="076 型兩棲攻擊艦「四川艦」", alias="無人機載台", kind="具電磁彈射的兩棲攻擊艦",
    status="最後測試階段",
    specs="排水量約 4 萬噸，飛行甲板長 250 公尺、寬 62 公尺，配備彈射器與攔阻裝置。",
    activity="2026-07 甲板標線完成，進入最後測試，下一步為艦機整合訓練。",
    assess="可搭載攻擊-21 等艦載無人機，使兩棲突擊群在登陸時具備自帶的無人機偵察與打擊能力。",
    refs=[24, 5], tags=["兩棲艦艇", "艦載無人機", "登陸作戰"])

# ── 第二章 機器狗與無人地面載具 ──
add(id="G01", ch="c2", sub="四足機器人", name="武裝機器狗（金龍-2024 演習）", alias="宇樹科技平台", kind="四足偵察／打擊機器人",
    maker="宇樹科技（Unitree）", status="演習使用",
    specs="輕型約 15 公斤，具 4D 廣角感知、續航 2 至 4 小時、即時偵察回傳與自主避障；重型約 50 公斤，背負突擊步槍，可執行偵察與目標打擊。",
    activity="2024-05 中柬「金龍-2024」聯合演習公開；央視畫面顯示由機器狗引導攻擊模擬城鎮建物。",
    assess="定位為城鎮戰前導，以降低步兵傷亡。",
    refs=[30], tags=["機器狗", "城鎮戰", "演習報導"])
add(id="G02", ch="c2", sub="四足機器人", name="「機器狼」群無人作戰系統", alias="Machine Wolf", kind="四足機器人作戰群",
    maker="中國兵器裝備集團（武巴智能科技）", status="展示、演習",
    specs="分工為「頭狼」偵察、「射手」掛步槍或機槍打擊、「輔助」自動跟隨運送彈藥物資；可背負約 20 公斤，宣稱可「百米精確打擊」。後續型號可掛微型飛彈與榴彈發射器，可自主識別並瞄準目標，由人員決定是否射擊。",
    activity="2024 年第 15 屆珠海航展首度亮相；2025-08 央視節目公開分工射擊畫面；2025 年閱兵由 CWB221 無人運輸車載運；2026-03-26 央視公開城鎮戰演練。",
    assess="屬「有人／無人協同」城鎮戰編組，與攻台後縱深城鎮作戰想定相關。",
    refs=[32, 33, 1, 31], tags=["機器狗", "城鎮戰", "有人無人協同"])
add(id="G03", ch="c2", sub="四足機器人", name="機器狗部隊試驗與對台登陸演練", alias="", kind="部隊運用",
    maker="—", status="試驗",
    specs="",
    activity="外媒彙整：新疆軍區 2025 年初測試後勤運輸；第 73 集團軍（福建）用於核生化偵察；第 76 集團軍 2025-07 結合 FPV 演練突擊；第 72 集團軍 2025 年底登陸演練中，機器狗攜爆裂物清除灘岸障礙並運送彈藥，其中一台在開闊灘頭遭「擊毀」；武警正將其納入城鎮戰程序。",
    assess="此段為單一外媒彙整，原始影像未逐一查證。若屬實，代表機器狗已被納入對台登陸的破障與運補環節。",
    refs=[31], tags=["機器狗", "登陸作戰", "東部戰區"])
add(id="G04", ch="c2", sub="四足機器人", name="宇樹科技與軍方關聯", alias="Unitree Robotics", kind="產業與供應鏈",
    maker="宇樹科技", status="—",
    specs="",
    activity="宇樹 2022 年公開承諾不將機器人武器化；但其四足機器人出現在解放軍訓練影片，美國國防部曾短暫將其列為「中國軍事企業」，並被指與國企背景公司合作。其部分晶片與感測器仰賴進口。",
    assess="民用量產機器狗價格低廉，可能以軍民融合方式快速轉為軍用。",
    refs=[33, 31], tags=["機器狗", "軍民融合"])
add(id="G05", ch="c2", sub="四足機器人", name="PF-070 反戰車機器狗", alias="", kind="四足反戰車飛彈載台（外銷）",
    status="外銷展示；未見解放軍列裝",
    specs="搭載 4 枚反戰車飛彈，宣稱射程 2 至 4 公里。",
    activity="2026 年沙烏地阿拉伯利雅德世界防務展展出。",
    assess="",
    refs=[31], tags=["機器狗"])
add(id="G06", ch="c2", sub="輪式與履帶無人車", name="閱兵無人地面車輛", alias="ZRY222、ZRZ100、GPJ221、CWB221", kind="無人地面作戰／掃雷／運輸車",
    maker="未公開", status="展示",
    specs="ZRY222 與 ZRZ100 為無人地面作戰車；GPJ221 為無人掃雷車；CWB221 為無人運輸車，可搭載四旋翼無人機與機器狼。",
    activity="2025-09-03 閱兵無人地面作戰方隊受閱。",
    assess="掃雷與運輸車可能用於登陸後破除灘岸障礙與前送補給。",
    refs=[1], tags=["無人地面車", "閱兵", "登陸作戰"])

# ── 第三章 無人水面與水下載具 ──
add(id="M01", ch="c3", sub="無人水面艇", name="JARI「虎鯨」無人作戰艇", alias="JARI USV／Orca", kind="大型無人水面作戰艇",
    maker="中國船舶重工集團 716 所、702 所", status="原型艦",
    specs="長約 58 公尺、排水量約 420 至 500 噸、航程 4,000 浬、最高航速 42 節；30 公厘遙控武器站與 8 個垂直發射單元，可選配火箭、魚雷與反潛聲納。",
    activity="2019-08 下水並宣布具初始作戰能力，2020 年初確認海試。",
    assess="可在台海周邊執行巡邏、反潛與封鎖警戒，降低有人艦艇風險。",
    refs=[25], tags=["無人艇", "封鎖", "反潛"])
add(id="M02", ch="c3", sub="無人水面艇", name="無人掃雷／作戰艇", alias="", kind="匿蹤無人水面艇",
    maker="未公開", status="展示",
    specs="具降低訊跡外形、尾部絞車可拖曳反水雷裝備、艏部中口徑機砲，雙噴水推進。",
    activity="2025 年閱兵海上無人作戰方隊受閱。",
    assess="Naval News 研判可能取代舊式 529 型遙控掃雷艇，適合淺水與近岸作業。",
    refs=[5], tags=["無人艇", "水雷戰"])
add(id="M03", ch="c3", sub="無人潛航器", name="HSU100 大型無人潛航器", alias="", kind="監偵情蒐 UUV",
    maker="未公開", status="展示",
    specs="艇身側邊聲納陣列、艏部開口，上方可升起感測與通信桅桿；導管推進器、X 形尾舵，須由大型船艦或港口設施布放。",
    activity="2025 年閱兵首度公開。",
    assess="環球時報稱可執行偵察、反潛與封鎖任務，成本低且無人員風險。",
    refs=[5, 4, 1], tags=["無人潛航器", "封鎖", "反潛"])
add(id="M04", ch="c3", sub="無人潛航器", name="AJX002 超大型無人潛航器", alias="", kind="水雷戰 UUV",
    maker="未公開", status="展示",
    specs="艇身較 HSU100 細長，導管推進器；官方說明為無人布雷能力。",
    activity="2025 年閱兵首度公開。",
    assess="可在不暴露有人艦艇的情況下，於台灣港口與航道外布雷，與封鎖作戰直接相關。",
    refs=[5, 4], tags=["無人潛航器", "水雷戰", "封鎖"])

# ── 第四章 反無人機與電子干擾體系 ──
add(id="C01", ch="c4", sub="定向能", name="LY-1 高能雷射武器", kind="車載／艦載雷射防空系統",
    maker="未公開", status="閱兵公開，服役狀態未知",
    specs="八輪卡車載旋轉砲塔，一個大型光束出口與多個光電、紅外線追蹤鏡頭；功率未公開。",
    activity="2025-09-03 閱兵列入海上防空方隊，與海紅旗-10 等組成四種艦艇防空系統。",
    assess="主要用於艦艇自衛，攔截無人機與反艦飛彈，單次攔截成本低；也可陸上使用。",
    refs=[2, 3, 1, 4], tags=["雷射", "反無人機", "閱兵"])
add(id="C02", ch="c4", sub="定向能", name="颶風-3000 高功率微波武器", alias="Hurricane 3000", kind="車載高功率微波反無人機系統",
    maker="中國兵器工業集團（北方工業）", status="閱兵公開",
    specs="雷達偵測追蹤、光電精確鎖定後發射微波破壞無人機電子元件；兵器工業專家稱對輕小型無人機及蜂群有效攔截距離超過 3 公里，可單獨或與雷射、高砲組網。",
    activity="2024 年珠海航展首展，2025 年閱兵受閱，2026-01 公布技術細節。",
    assess="美國智庫評估解放軍將以高功率微波保護部隊與機場，削弱台、美無人機蜂群效果；限制為射程短、可能干擾友軍電子設備。",
    refs=[34, 35, 36], tags=["高功率微波", "反無人機", "蜂群"])
add(id="C03", ch="c4", sub="定向能", name="颶風-2000 高功率微波武器", alias="Hurricane 2000", kind="裝甲車載高功率微波系統",
    maker="中國兵器工業集團", status="展示",
    specs="颶風-3000 的小型機動版，裝於裝甲車。",
    activity="",
    assess="可隨伴機械化部隊提供近距離反無人機防護。",
    refs=[34], tags=["高功率微波", "反無人機"])
add(id="C04", ch="c4", sub="定向能", name="沉默獵手雷射系統", alias="Silent Hunter", kind="光纖雷射反無人機系統",
    maker="中國保利科技", status="國內使用、外銷",
    specs="30 千瓦光纖雷射，可攻擊 4 公里內低飛無人機。",
    activity="報導指已在國內使用，並由沙烏地阿拉伯採用，曾攔截胡塞無人機。",
    assess="",
    refs=[34], tags=["雷射", "反無人機"])
add(id="C05", ch="c4", sub="定向能", name="LW-30／LW-60 雷射武器", alias="", kind="車載雷射防空系統",
    maker="中國航天科工集團（CASIC）", status="2022 年公開",
    specs="LW-30 為 30 千瓦，具機動組網能力，可在 6 秒內追蹤鎖定 25 公里外低空目標；LW-60 為 60 千瓦。",
    activity="2022 年以「全域攻防武器」名義公開。",
    assess="美國陸軍戰院研究指出中方正發展 50 千瓦以上雷射；10 千瓦可損壞無人機感測器，50 千瓦可摧毀無人機。",
    refs=[37, 34], tags=["雷射", "反無人機"])
add(id="C06", ch="c4", sub="定向能", name="光箭、天盾系列雷射", alias="", kind="車載雷射反無人機系統",
    maker="中國航空工業集團（AVIC）", status="展示",
    specs="車載、具人工智慧自動化與多波段瞄準。",
    activity="",
    assess="",
    refs=[34], tags=["雷射", "反無人機"])
add(id="C07", ch="c4", sub="整合網路與偵測", name="天穹（Sky Dome）與遠漠指管系統", alias="", kind="整合式反無人機網路",
    maker="中國電子科技集團（CETC）", status="展示",
    specs="天穹整合雷達、干擾與定向能，自動化組網；遠漠為指管系統，同步雷達、光電與電戰資料。",
    activity="",
    assess="顯示解放軍正把各種反無人機手段整合為自動化的「殺傷鏈」，而非單一武器。",
    refs=[34], tags=["反無人機", "電子戰", "指管"])
add(id="C08", ch="c4", sub="整合網路與偵測", name="YLC-48 與 DWL002 偵測雷達", alias="", kind="反無人機偵測雷達",
    maker="未公開", status="使用中",
    specs="YLC-48「無人機終結者」為可攜式 360 度相位陣列雷達；DWL002 為被動雷達，不發射訊號即可偵測無人機，較不易被電戰壓制或反輻射攻擊。",
    activity="",
    assess="",
    refs=[34], tags=["反無人機", "雷達"])
add(id="C09", ch="c4", sub="彈砲與動能", name="閱兵反無人機方隊", alias="OW5-A10、OW5-A50、PLB-625、FK-3000", kind="雷射、機砲、飛彈組合",
    maker="未公開", status="展示",
    specs="社群貼文列出：OW5-A10「雷射猛士」、OW5-A50 雷射車、PLB-625 六管 25 公厘機砲、FK-3000 30 公厘機砲加反無人機飛彈；另有反無人機彈砲一體系統整合雷達與光電。",
    activity="2025-09-03 閱兵首度公開反無人機方隊與高功率微波武器。",
    assess="代表反無人機已成為獨立受閱方隊，從「附加任務」升級為正式作戰體系。",
    refs=[2, 3], tags=["反無人機", "雷射", "閱兵"])
add(id="C10", ch="c4", sub="彈砲與動能", name="625 型彈砲合一防空系統", alias="PGL-625", kind="輪式彈砲合一低空防空系統",
    maker="未公開", status="服役",
    specs="8×8 輪式底盤，六管 25 公厘加特林機砲與 4 枚短程防空飛彈，配雷達與光電；其中一型雷達可偵測極小反射面積目標。",
    activity="2023 年第 77 集團軍某合成旅實彈射擊公開；2025 年演習一次展示約十餘輛，射擊無人機靶機。",
    assess="主要針對直升機、低飛攻擊機與無人機，詳見第五章。",
    refs=[39, 40], tags=["反無人機", "野戰防空", "直升機威脅"])
add(id="C11", ch="c4", sub="單兵與基地防護", name="單兵干擾槍、網捕與基地反無人機演練", alias="", kind="軟殺傷與近距離攔截",
    maker="多家", status="使用中",
    specs="手持干擾槍、網捕彈、固定式干擾站、車載偵測雷達，以及可發射捕捉網的攔截四旋翼。",
    activity="2024 年央視公開士兵以干擾槍與網捕彈對抗 FPV；2023-10 上海大場基地演練保護空警-500 預警機免遭模擬無人機攻擊。",
    assess="上海演練被認為借鑑烏克蘭襲擊俄軍預警機的案例，並以台灣無人機為假想威脅。",
    refs=[22, 38], tags=["反無人機", "電子干擾", "FPV"])
add(id="C12", ch="c4", sub="電子對抗", name="電子對抗裝備（閱兵）", alias="5 型電子對抗系統、殲-16D、運-9LG", kind="電子戰系統與平台",
    maker="未公開", status="服役／展示",
    specs="閱兵電子對抗方隊展示 5 型電子對抗系統，戰機梯隊含殲-16D 電戰機，特種機梯隊含運-9LG 電戰機與運-9DZ 電子情報機。",
    activity="2025-09-03 閱兵。",
    assess="大範圍通信與導航干擾可同時壓制台灣無人機的資料鏈與衛星定位。",
    refs=[1], tags=["電子戰", "電子干擾", "閱兵"])
add(id="C13", ch="c4", sub="電子對抗", name="反無人機產業規模與實測表現", alias="", kind="產業與訓練評估",
    maker="—", status="—",
    specs="",
    activity="反無人機政府採購公告由 2022 年 87 件增至 2023 年 122 件、2024 年 205 件；全國有 3,000 家以上廠商生產相關裝備。某次夏季演訓中，反制手段僅擊落約 40% 來襲無人機。",
    assess="投入快速增加，但實際攔截效果仍有限。",
    refs=[34], tags=["反無人機", "軍民融合"])

# ── 第五章 威脅直升機飛行的作為 ──
add(id="H01", ch="c5", sub="便攜式防空飛彈", name="前衛（QW）系列便攜防空飛彈", alias="QW-1／2／3／4／18／19", kind="單兵肩射防空飛彈",
    status="服役",
    specs="QW-1：紅外線、射程 0.5–5 公里、高度 30–4,000 公尺，1997 年裝備前線部隊。QW-2：全向紅外線、0.5–6 公里、10–4,000 公尺。QW-3：半主動雷射、0.8–8 公里、4–5,000 公尺。QW-4：成像紅外線，2007 年服役。QW-18／19 降低最低攔截高度。",
    activity="",
    assess="最低攔截高度僅 4 至 30 公尺，涵蓋直升機貼地飛行、懸停與著陸的全部高度。",
    refs=[42], tags=["便攜防空", "直升機威脅"])
add(id="H02", ch="c5", sub="便攜式防空飛彈", name="QW-12 與飛弩-16（FN-16）", alias="", kind="新一代單兵肩射防空飛彈",
    maker="QW-12 為中國航天科工集團；FN-16 未載明", status="QW-12 有解放軍演示紀錄；FN-16 主要見於外銷",
    specs="FN-16：紅外線加紫外線雙通道準成像導引頭、雷射近炸引信，射程 0.5–6 公里、高度 10–4,000 公尺、速度逾 600 公尺／秒、反應約 5 秒。QW-12：被動紅外線射後不理，射程 0.5–6 公里、高度 10–4,000 公尺、約 1.8 馬赫。",
    activity="2022 年報導解放軍演示 QW-12 性能；2026 年報導兩型納入對伊朗軍售。",
    assess="FN-16 抗熱焰彈干擾能力較強，對裝有熱焰彈的直升機威脅較高。",
    refs=[43, 51], tags=["便攜防空", "直升機威脅"])
add(id="H03", ch="c5", sub="野戰防空", name="紅旗-17A（HQ-17A）短程防空系統", alias="", kind="輪式短程防空飛彈",
    maker="未公開", status="服役",
    specs="最大射程約 15 公里、射高約 10 公里；可攻擊直升機、無人機、定翼機、巡弋飛彈與精準導引彈藥。",
    activity="2019 年閱兵公開；第 78 集團軍部署。",
    assess="伴隨機械化部隊機動，可在登陸後對台灣攻擊直升機構成威脅。",
    refs=[41], tags=["野戰防空", "直升機威脅"])
add(id="H04", ch="c5", sub="野戰防空", name="625 型彈砲合一系統（反直升機）", alias="PGL-625", kind="低空防空",
    maker="未公開", status="服役",
    specs="25 公厘六管加特林機砲與 4 枚短程飛彈，設計目標為直升機、低飛攻擊機與無人機。",
    activity="見第四章 C10。",
    assess="機砲適合攻擊低空懸停或貼地飛行的直升機，飛彈補足較遠距離。",
    refs=[39], tags=["野戰防空", "直升機威脅", "反無人機"])
add(id="H05", ch="c5", sub="野戰防空", name="紅旗-11 彈砲結合防空系統", alias="HQ-11", kind="中短程彈砲結合防空",
    maker="未公開", status="閱兵公開",
    specs="閱兵資料列為中短程飛彈與機砲結合的防空系統。",
    activity="2025-09-03 閱兵防空方隊。",
    assess="",
    refs=[1], tags=["野戰防空", "直升機威脅", "閱兵"])
add(id="H06", ch="c5", sub="實際干擾事件", name="戰機對直升機施放熱焰彈", alias="", kind="空中危險攔截",
    maker="—", status="已發生",
    specs="",
    activity="2023-10-29 南海：兩架殲-11 攔截加拿大 CH-148 直升機，一架近距離掠過造成亂流，另一架於直升機正前方施放熱焰彈。2024-05-04 黃海：殲-10 在澳洲 MH-60R 直升機前方約 300 公尺、上方約 60 公尺施放熱焰彈，直升機緊急閃避以免熱焰彈被吸入旋翼與進氣口。",
    assess="熱焰彈落入旋翼或進氣口可能造成墜機；屬可推諉的灰色地帶手段，可能用於驅離台灣或外國直升機。",
    refs=[46, 45], tags=["直升機威脅", "灰色地帶", "危險攔截"])
add(id="H07", ch="c5", sub="實際干擾事件", name="海軍直升機危險逼近他國航空器", alias="", kind="空中危險逼近",
    maker="—", status="已發生",
    specs="",
    activity="2025-02-18 黃岩島：解放軍海軍直升機飛到菲律賓漁業局巡邏機上方與左側約 3 公尺處。",
    assess="顯示解放軍直升機本身也被用於近距離逼退航空器。",
    refs=[48], tags=["直升機威脅", "灰色地帶", "危險攔截"])
add(id="H08", ch="c5", sub="實際干擾事件", name="艦艇雷射照射航空器", alias="", kind="雷射照射",
    maker="—", status="已發生（多次）",
    specs="",
    activity="2018-04 吉布地：中方人員多次以雷射照射美軍飛機，兩名 C-130 飛行員輕傷。2020-02 關島附近：海軍驅逐艦以軍用雷射照射美軍 P-8A。2022-02 澳洲北方：海軍艦艇照射澳洲 P-8A。2025-07-02 紅海：海軍巡防艦照射德國監視機，該機中止任務。",
    assess="直升機常在艦艇附近低空作業，艦載雷射可能使飛行員短暫失明或損壞光電感測器；LY-1 等雷射武器服役後風險可能升高。",
    refs=[47], tags=["雷射", "直升機威脅", "灰色地帶"])
add(id="H09", ch="c5", sub="解放軍自身評估", name="解放軍對直升機易損性的認知", alias="", kind="官媒公開言論",
    maker="—", status="—",
    specs="",
    activity="2024-09 官媒紀錄片中，解放軍軍官表示「隨著單兵防空武器在戰場上廣泛使用，直升機面臨的威脅越來越大」，並展示直升機與登陸部隊面對持便攜防空飛彈守軍的模擬突擊。",
    assess="反映解放軍了解便攜防空飛彈對直升機的威脅，同類武器也大量配置於解放軍自身部隊。",
    alabel="est", label="off",
    refs=[44], tags=["便攜防空", "直升機威脅", "空降兵"])
add(id="H10", ch="c5", sub="潛在威脅", name="無人機與定向能武器對直升機的潛在威脅", alias="", kind="本報告推估",
    maker="—", status="推估",
    specs="",
    activity="公開資料未見解放軍專門用於獵殺直升機的無人機。",
    assess="本報告推估：低空懸停、起降或在灘頭作業的直升機，可能遭 FPV、巡飛彈或蜂群攻擊；颶風-3000 等高功率微波與大範圍電子干擾也可能波及直升機航電與導航。",
    label="est", refs=[15, 36], tags=["直升機威脅", "蜂群", "高功率微波"])
add(id="H11", ch="c5", sub="潛在威脅", name="反直升機地雷", alias="", kind="資料缺口",
    maker="—", status="未見公開資料",
    specs="",
    activity="本次公開檢索未找到解放軍列裝或演練反直升機地雷的可靠報導。",
    assess="列為資料缺口，建議持續追蹤珠海航展與閱兵展品。",
    label="gap", alabel="gap", refs=[], tags=["直升機威脅"])

# 時間線（第六章）：日期、事件、refs
TIMELINE = [
 ("2022-08", "金門、烈嶼、獅嶼多次出現中國民用無人機，國軍宣布將擊落入侵無人機", [28]),
 ("2022-09", "BZK-005 偵察無人機進入台灣西南空域", [9]),
 ("2023-01", "無偵-7 首度經宮古海峽飛入菲律賓海，日本派機應對", [11]),
 ("2023-04", "TB-001 由台海中線南端越線，沿台灣東岸繞行", [10]),
 ("2023-05", "BZK-005 順時針繞台", [50]),
 ("2023-10", "攻擊-2（翼龍-2）首度進入台灣防空識別區", [13]),
 ("2024-05", "金龍-2024 演習公開武裝機器狗", [30]),
 ("2024-08", "兩架無人機沿台灣東岸、與那國附近北飛", [29]),
 ("2025-09", "北京閱兵公開無人空中、地面、海上作戰方隊與反無人機方隊", [1]),
 ("2025-10", "東部戰區以車載發射箱實射反輻射巡飛彈", [20, 21]),
 ("2025-12", "九天無人機母機首飛；正義使命-2025 演習", [14, 27]),
 ("2026-01", "解放軍無人機進入東沙島空域約 4 分鐘", [26]),
 ("2026-03", "衛星影像顯示殲-6 改裝無人機部署於福建基地；央視公開機器狼城鎮戰演練", [18, 33]),
 ("2026-07", "076 型四川艦進入最後測試階段", [24]),
]

# 圖二：可威脅直升機的武器射程（公里）與最低攔截高度（公尺）
RANGE_CHART = [
 ("QW-1", 5, 30, "便攜"), ("QW-2", 6, 10, "便攜"), ("QW-12", 6, 10, "便攜"), ("FN-16", 6, 10, "便攜"),
 ("QW-3", 8, 4, "便攜"), ("HQ-17A", 15, None, "野戰"), ("沉默獵手（雷射）", 4, None, "定向能"),
 ("颶風-3000（微波）", 3, None, "定向能"),
]
