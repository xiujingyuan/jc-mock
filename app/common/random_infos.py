#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
 @author: snow
 @software: PyCharm
 @time: 2019/05/07
 @file: random_infos.py
 @site:
 @email:
"""
import codecs
import datetime
import os
import random
import string
from datetime import date, timedelta

import chardet

BASE_DIR = os.path.dirname(os.path.abspath(__file__))

DC_PATH = os.path.join(BASE_DIR, "districtcode.txt")

last_names = ['赵', '钱', '孙', '李', '周', '吴', '郑', '王', '冯', '陈', '褚', '卫', '蒋', '沈', '韩', '杨', '朱', '秦', '尤', '许',
              '何', '吕', '施', '张', '孔', '曹', '严', '华', '金', '魏', '陶', '姜', '戚', '谢', '邹', '喻', '柏', '水', '窦', '章',
              '云', '苏', '潘', '葛', '奚', '范', '彭', '郎', '鲁', '韦', '昌', '马', '苗', '凤', '花', '方', '俞', '任', '袁', '柳',
              '酆', '鲍', '史', '唐', '费', '廉', '岑', '薛', '雷', '贺', '倪', '汤', '滕', '殷', '罗', '毕', '郝', '邬', '安', '常',
              '乐', '于', '时', '傅', '皮', '卞', '齐', '康', '伍', '余', '元', '卜', '顾', '孟', '平', '黄', '和', '穆', '萧', '尹',
              '姚', '邵', '堪', '汪', '祁', '毛', '禹', '狄', '米', '贝', '明', '臧', '计', '伏', '成', '戴', '谈', '宋', '茅', '庞',
              '熊', '纪', '舒', '屈', '项', '祝', '董', '梁']

first_names = ['的', '一', '是', '了', '我', '不', '人', '在', '他', '有', '这', '个', '上', '们', '来', '到', '时', '大', '地', '为',
               '子', '中', '你', '说', '生', '国', '年', '着', '就', '那', '和', '要', '她', '出', '也', '得', '里', '后', '自', '以',
               '会', '家', '可', '下', '而', '过', '天', '去', '能', '对', '小', '多', '然', '于', '心', '学', '么', '之', '都', '好',
               '看', '起', '发', '当', '没', '成', '只', '如', '事', '把', '还', '用', '第', '样', '道', '想', '作', '种', '开', '美',
               '总', '从', '无', '情', '己', '面', '最', '女', '但', '现', '前', '些', '所', '同', '日', '手', '又', '行', '意', '动',
               '方', '期', '它', '头', '经', '长', '儿', '回', '位', '分', '爱', '老', '因', '很', '给', '名', '法', '间', '斯', '知',
               '世', '什', '两', '次', '使', '身', '者', '被', '高', '已', '亲', '其', '进', '此', '话', '常', '与', '活', '正', '感',
               '见', '明', '问', '力', '理', '尔', '点', '文', '几', '定', '本', '公', '特', '做', '外', '孩', '相', '西', '果', '走',
               '将', '月', '十', '实', '向', '声', '车', '全', '信', '重', '三', '机', '工', '物', '气', '每', '并', '别', '真', '打',
               '太', '新', '比', '才', '便', '夫', '再', '书', '部', '水', '像', '眼', '等', '体', '却', '加', '电', '主', '界', '门',
               '利', '海', '受', '听', '表', '德', '少', '克', '代', '员', '许', '稜', '先', '口', '由', '死', '安', '写', '性', '马',
               '光', '白', '或', '住', '难', '望', '教', '命', '花', '结', '乐', '色', '更', '拉', '东', '神', '记', '处', '让', '母',
               '父', '应', '直', '字', '场', '平', '报', '友', '关', '放', '至', '张', '认', '接', '告', '入', '笑', '内', '英', '军',
               '候', '民', '岁', '往', '何', '度', '山', '觉', '路', '带', '万', '男', '边', '风', '解', '叫', '任', '金', '快', '原',
               '吃', '妈', '变', '通', '师', '立', '象', '数', '四', '失', '满', '战', '远', '格', '士', '音', '轻', '目', '条', '呢',
               '病', '始', '达', '深', '完', '今', '提', '求', '清', '王', '化', '空', '业', '思', '切', '怎', '非', '找', '片', '罗',
               '钱', '紶', '吗', '语', '元', '喜', '曾', '离', '飞', '科', '言', '干', '流', '欢', '约', '各', '即', '指', '合', '反',
               '题', '必', '该', '论', '交', '终', '林', '请', '医', '晚', '制', '球', '决', '窢', '传', '画', '保', '读', '运', '及',
               '则', '房', '早', '院', '量', '苦', '火', '布', '品', '近', '坐', '产', '答', '星', '精', '视', '五', '连', '司', '巴',
               '奇', '管', '类', '未', '朋', '且', '婚', '台', '夜', '青', '北', '队', '久', '乎', '越', '观', '落', '尽', '形', '影',
               '红', '爸', '百', '令', '周', '吧', '识', '步', '希', '亚', '术', '留', '市', '半', '热', '送', '兴', '造', '谈', '容',
               '极', '随', '演', '收', '首', '根', '讲', '整', '式', '取', '照', '办', '强', '石', '古', '华', '諣', '拿', '计', '您',
               '装', '似', '足', '双', '妻', '尼', '转', '诉', '米', '称', '丽', '客', '南', '领', '节', '衣', '站', '黑', '刻', '统',
               '断', '福', '城', '故', '历', '惊', '脸', '选', '包', '紧', '争', '另', '建', '维', '绝', '树', '系', '伤', '示', '愿',
               '持', '千', '史', '谁', '准', '联', '妇', '纪', '基', '买', '志', '静', '阿', '诗', '独', '复', '痛', '消', '社', '算',
               '义', '竟', '确', '酒', '需', '单', '治', '卡', '幸', '兰', '念', '举', '仅', '钟', '怕', '共', '毛', '句', '息', '功',
               '官', '待', '究', '跟', '穿', '室', '易', '游', '程', '号', '居', '考', '突', '皮', '哪', '费', '倒', '价', '图', '具',
               '刚', '脑', '永', '歌', '响', '商', '礼', '细', '专', '黄', '块', '脚', '味', '灵', '改', '据', '般', '破', '引', '食',
               '仍', '存', '众', '注', '笔', '甚', '某', '沉', '血', '备', '习', '校', '默', '务', '土', '微', '娘', '须', '试', '怀',
               '料', '调', '广', '蜖', '苏', '显', '赛', '查', '密', '议', '底', '列', '富', '梦', '错', '座', '参', '八', '除', '跑',
               '亮', '假', '印', '设', '线', '温', '虽', '掉', '京', '初', '养', '香', '停', '际', '致', '阳', '纸', '李', '纳', '验',
               '助', '激', '够', '严', '证', '帝', '饭', '忘', '趣', '支', '春', '集', '丈', '木', '研', '班', '普', '导', '顿', '睡',
               '展', '跳', '获', '艺', '六', '波', '察', '群', '皇', '段', '急', '庭', '创', '区', '奥', '器', '谢', '弟', '店', '否',
               '害', '草', '排', '背', '止', '组', '州', '朝', '封', '睛', '板', '角', '况', '曲', '馆', '育', '忙', '质', '河', '续',
               '哥', '呼', '若', '推', '境', '遇', '雨', '标', '姐', '充', '围', '案', '伦', '护', '冷', '警', '贝', '著', '雪', '索',
               '剧', '啊', '船', '险', '烟', '依', '斗', '值', '帮', '汉', '慢', '佛', '肯', '闻', '唱', '沙', '局', '伯', '族', '低',
               '玩', '资', '屋', '击', '速', '顾', '泪', '洲', '团', '圣', '旁', '堂', '兵', '七', '露', '园', '牛', '哭', '旅', '街',
               '劳', '型', '烈', '姑', '陈', '莫', '鱼', '异', '抱', '宝', '权', '鲁', '简', '态', '级', '票', '怪', '寻', '杀', '律',
               '胜', '份', '汽', '右', '洋', '范', '床', '舞', '秘', '午', '登', '楼', '贵', '吸', '责', '例', '追', '较', '职', '属',
               '渐', '左', '录', '丝', '牙', '党', '继', '托', '赶', '章', '智', '冲', '叶', '胡', '吉', '卖', '坚', '喝', '肉', '遗',
               '救', '修', '松', '临', '藏', '担', '戏', '善', '卫', '药', '悲', '敢', '靠', '伊', '村', '戴', '词', '森', '耳', '差',
               '短', '祖', '云', '规', '窗', '散', '迷', '油', '旧', '适', '乡', '架', '恩', '投', '弹', '铁', '博', '雷', '府', '压',
               '超', '负', '勒', '杂', '醒', '洗', '采', '毫', '嘴', '毕', '九', '冰', '既', '状', '乱', '景', '席', '珍', '童', '顶',
               '派', '素', '脱', '农', '疑', '练', '野', '按', '犯', '拍', '征', '坏', '骨', '余', '承', '置', '臓', '彩', '灯', '巨',
               '琴', '免', '环', '姆', '暗', '换', '技', '翻', '束', '增', '忍', '餐', '洛', '塞', '缺', '忆', '判', '欧', '层', '付',
               '阵', '玛', '批', '岛', '项', '狗', '休', '懂', '武', '革', '良', '恶', '恋', '委', '拥', '娜', '妙', '探', '呀', '营',
               '退', '摇', '弄', '桌', '熟', '诺', '宣', '银', '势', '奖', '宫', '忽', '套', '康', '供', '优', '课', '鸟', '喊', '降',
               '夏', '困', '刘', '罪', '亡', '鞋', '健', '模', '败', '伴', '守', '挥', '鲜', '财', '孤', '枪', '禁', '恐', '伙', '杰',
               '迹', '妹', '藸', '遍', '盖', '副', '坦', '牌', '江', '顺', '秋', '萨', '菜', '划', '授', '归', '浪', '听', '凡', '预',
               '奶', '雄', '升', '碃', '编', '典', '袋', '莱', '含', '盛', '济', '蒙', '棋', '端', '腿', '招', '释', '介', '烧', '误',
               '乾', '坤']

oversea_names = ['Gabriel', 'Sandeep', 'Vivek Singh', 'Vijay', 'Pankaj', 'Prakash', 'Sunil', 'Kamlesh', 'Amit',
                 'Akshay', 'Sushma', 'Sushant', 'Kamal', 'Sagar', 'Neha Kumari', 'Manisha', 'Sonu', 'Raju', 'Rahul',
                 'Karuna', 'Sachin', 'Rashmi', 'Rahul Singh', 'Mumtaz', 'Krishna', 'Satish', 'Vimla', 'Ashok', 'Suraj',
                 'Prem Singh', 'ANIKET SANJAY PARDE', 'Vinay', 'Dinesh', 'Harsh', 'Darshan', 'Ravi', 'Ashish',
                 'PRADEEP', 'Ganesh Kumar', 'Sakir', 'Tarun', 'Abhishek', 'Sandeep S', 'Ravi P', 'Ajay', 'Rohit',
                 'Hemraj', 'Santosh', 'Anil', 'Hemant', 'Pardeep', 'Manoj', 'Sameer', 'Vikas', 'Akash', 'Badal',
                 'Mamta', 'SWEETY', 'Yogesh', 'Ganesh', 'Gaurav', 'Sathish Kumar', 'Meena', 'Murali', 'Manju', 'Siva',
                 'Kandasamy', 'Mohan Kumar', 'Karthik', 'Vignesh', 'Lakshmi', 'Priyanka', 'Ramya', 'Suresh', 'Nirmala',
                 'Ramkumar', 'Ranjith', 'Sivakumar', 'Rajkumar', 'Rajan', 'Karthikeyan', 'Sivalingam', 'Ravi Kumar',
                 'Rakesh', 'Ramesh Yadav', 'Suman Kumar', 'Nasir', 'Mahendra', 'Prabhu', 'Masthan', 'Prathap', 'Yusuf',
                 'Yasin', 'Madan lal', 'Pinki', 'Anjali', 'Sandeep Kumar', 'Sanjay Gupta', 'Lokesh', 'Saravanan']


def getdistrictcode():
    codelist = []
    detect_dict = chardet.detect(open(DC_PATH, 'rb').read(4096))
    _, encodings = detect_dict['confidence'], detect_dict['encoding']
    with codecs.open(DC_PATH, encoding=encodings) as file:
        data = file.read()
        districtlist = data.split('\n')
    for node in districtlist:
        # print node
        if node[10:11] != ' ':
            state = node[10:].strip()
        if node[10:11] == ' ' and node[12:13] != ' ':
            city = node[12:].strip()
        if node[10:11] == ' ' and node[12:13] == ' ':
            district = node[14:].strip()
            code = node[0:6]
            codelist.append({"state": state, "city": city, "district": district, "code": code})
    return codelist


def gennerator():
    codelist = getdistrictcode()
    while True:
        try:
            id_card = codelist[random.randint(0, len(codelist))]['code']
            # 地区项
        except:
            continue
        else:
            break
    id_card += str(random.randint(1970, 1996))
    # 年份项
    da = date.today() + timedelta(days=random.randint(1, 366))
    # 月份和日期项
    id_card += da.strftime('%m%d')
    id_card += str(random.randint(100, 300))
    # 顺序号简单处理

    i = 0
    count = 0
    weight = [7, 9, 10, 5, 8, 4, 2, 1, 6, 3, 7, 9, 10, 5, 8, 4, 2]
    # 权重项
    checkcode = {'0': '1', '1': '0', '2': 'X', '3': '9', '4': '8', '5': '7',
                 '6': '6', '7': '5', '8': '5', '9': '3', '10': '2'}
    # 校验码映射
    for i in range(0, len(id_card)):
        count = count + int(id_card[i]) * weight[i]
    id_card += checkcode[str(count % 11)]
    # 算出校验码
    return id_card


def random_name():
    has_name = random.choice((1, 2))
    if has_name == 0:
        return ""
    ret = random.choice(last_names)
    for _ in range(random.randint(1, 2)):
        ret += random.choice(first_names)
    return ret


def random_tele(is_false=True):
    num_start = ['134', '135', '136', '137', '138', '139', '150', '151', '152', '158', '159', '157', '182', '187',
                 '188', '147', '130', '131', '132', '155', '156', '170', '185', '186', '133', '153', '180', '189',
                 '190']
    start = "2" + random.choice(num_start)[1:] if is_false else random.choice(num_start)
    end = ''.join(random.sample(string.digits, 8))
    ret = start + end
    return ret


def get_num(start, end):
    return random.random() * (end - start + 1) + start


def random_road():
    road = ["重庆大厦", "黑龙江路", "十梅庵街", "遵义路", "湘潭街", "瑞金广场", "仙山街", "仙山东路", "仙山西大厦", "白沙河路", "赵红广场", "机场路", "民航街", "长城南路",
            "流亭立交桥", "虹桥广场", "长城大厦", "礼阳路", "风岗街", "中川路", "白塔广场", "兴阳路", "文阳街", "绣城路", "河城大厦", "锦城广场", "崇阳街", "华城路",
            "康城街", "正阳路", "和阳广场", "中城路", "江城大厦", "顺城路", "安城街", "山城广场", "春城街", "国城路", "泰城街", "德阳路", "明阳大厦", "春阳路", "艳阳街",
            "秋阳路", "硕阳街", "青威高速", "瑞阳街", "丰海路", "双元大厦", "惜福镇街道", "夏庄街道", "古庙工业园", "中山街", "太平路", "广西街", "潍县广场", "博山大厦",
            "湖南路", "济宁街", "芝罘路", "易州广场", "荷泽四路", "荷泽二街", "荷泽一路", "荷泽三大厦", "观海二广场", "广西支街", "观海一路", "济宁支街", "莒县路",
            "平度广场", "明水路", "蒙阴大厦", "青岛路", "湖北街", "江宁广场", "郯城街", "天津路", "保定街", "安徽路", "河北大厦", "黄岛路", "北京街", "莘县路", "济南街",
            "宁阳广场", "日照街", "德县路", "新泰大厦", "荷泽路", "山西广场", "沂水路", "肥城街", "兰山路", "四方街", "平原广场", "泗水大厦", "浙江路", "曲阜街",
            "寿康路", "河南广场", "泰安路", "大沽街", "红山峡支路", "西陵峡一大厦", "台西纬一广场", "台西纬四街", "台西纬二路", "西陵峡二街", "西陵峡三路", "台西纬三广场",
            "台西纬五路", "明月峡大厦", "青铜峡路", "台西二街", "观音峡广场", "瞿塘峡街", "团岛二路", "团岛一街", "台西三路", "台西一大厦", "郓城南路", "团岛三街", "刘家峡路",
            "西藏二街", "西藏一广场", "台西四街", "三门峡路", "城武支大厦", "红山峡路", "郓城北广场", "龙羊峡路", "西陵峡街", "台西五路", "团岛四街", "石村广场", "巫峡大厦",
            "四川路", "寿张街", "嘉祥路", "南村广场", "范县路", "西康街", "云南路", "巨野大厦", "西江广场", "鱼台街", "单县路", "定陶街", "滕县路", "钜野广场", "观城路",
            "汶上大厦", "朝城路", "滋阳街", "邹县广场", "濮县街", "磁山路", "汶水街", "西藏路", "城武大厦", "团岛路", "南阳街", "广州路", "东平街", "枣庄广场", "贵州街",
            "费县路", "南海大厦", "登州路", "文登广场", "信号山支路", "延安一街", "信号山路", "兴安支街", "福山支广场", "红岛支大厦", "莱芜二路", "吴县一街", "金口三路",
            "金口一广场", "伏龙山路", "鱼山支街", "观象二路", "吴县二大厦", "莱芜一广场", "金口二街", "海阳路", "龙口街", "恒山路", "鱼山广场", "掖县路", "福山大厦",
            "红岛路", "常州街", "大学广场", "龙华街", "齐河路", "莱阳街", "黄县路", "张店大厦", "祚山路", "苏州街", "华山路", "伏龙街", "江苏广场", "龙江街", "王村路",
            "琴屿大厦", "齐东路", "京山广场", "龙山路", "牟平街", "延安三路", "延吉街", "南京广场", "东海东大厦", "银川西路", "海口街", "山东路", "绍兴广场", "芝泉路",
            "东海中街", "宁夏路", "香港西大厦", "隆德广场", "扬州街", "郧阳路", "太平角一街", "宁国二支路", "太平角二广场", "天台东一路", "太平角三大厦", "漳州路一路",
            "漳州街二街", "宁国一支广场", "太平角六街", "太平角四路", "天台东二街", "太平角五路", "宁国三大厦", "澳门三路", "江西支街", "澳门二路", "宁国四街", "大尧一广场",
            "咸阳支街", "洪泽湖路", "吴兴二大厦", "澄海三路", "天台一广场", "新湛二路", "三明北街", "新湛支路", "湛山五街", "泰州三广场", "湛山四大厦", "闽江三路", "澳门四街",
            "南海支路", "吴兴三广场", "三明南路", "湛山二街", "二轻新村镇", "江南大厦", "吴兴一广场", "珠海二街", "嘉峪关路", "高邮湖街", "湛山三路", "澳门六广场", "泰州二路",
            "东海一大厦", "天台二路", "微山湖街", "洞庭湖广场", "珠海支街", "福州南路", "澄海二街", "泰州四路", "香港中大厦", "澳门五路", "新湛三街", "澳门一路", "正阳关街",
            "宁武关广场", "闽江四街", "新湛一路", "宁国一大厦", "王家麦岛", "澳门七广场", "泰州一路", "泰州六街", "大尧二路", "青大一街", "闽江二广场", "闽江一大厦", "屏东支路",
            "湛山一街", "东海西路", "徐家麦岛函谷关广场", "大尧三路", "晓望支街", "秀湛二路", "逍遥三大厦", "澳门九广场", "泰州五街", "澄海一路", "澳门八街", "福州北路",
            "珠海一广场", "宁国二路", "临淮关大厦", "燕儿岛路", "紫荆关街", "武胜关广场", "逍遥一街", "秀湛四路", "居庸关街", "山海关路", "鄱阳湖大厦", "新湛路", "漳州街",
            "仙游路", "花莲街", "乐清广场", "巢湖街", "台南路", "吴兴大厦", "新田路", "福清广场", "澄海路", "莆田街", "海游路", "镇江街", "石岛广场", "宜兴大厦",
            "三明路", "仰口街", "沛县路", "漳浦广场", "大麦岛", "台湾街", "天台路", "金湖大厦", "高雄广场", "海江街", "岳阳路", "善化街", "荣成路", "澳门广场", "武昌路",
            "闽江大厦", "台北路", "龙岩街", "咸阳广场", "宁德街", "龙泉路", "丽水街", "海川路", "彰化大厦", "金田路", "泰州街", "太湖路", "江西街", "泰兴广场", "青大街",
            "金门路", "南通大厦", "旌德路", "汇泉广场", "宁国路", "泉州街", "如东路", "奉化街", "鹊山广场", "莲岛大厦", "华严路", "嘉义街", "古田路", "南平广场",
            "秀湛路", "长汀街", "湛山路", "徐州大厦", "丰县广场", "汕头街", "新竹路", "黄海街", "安庆路", "基隆广场", "韶关路", "云霄大厦", "新安路", "仙居街",
            "屏东广场", "晓望街", "海门路", "珠海街", "上杭路", "永嘉大厦", "漳平路", "盐城街", "新浦路", "新昌街", "高田广场", "市场三街", "金乡东路", "市场二大厦",
            "上海支路", "李村支广场", "惠民南路", "市场纬街", "长安南路", "陵县支街", "冠县支广场", "小港一大厦", "市场一路", "小港二街", "清平路", "广东广场", "新疆路",
            "博平街", "港通路", "小港沿", "福建广场", "高唐街", "茌平路", "港青街", "高密路", "阳谷广场", "平阴路", "夏津大厦", "邱县路", "渤海街", "恩县广场", "旅顺街",
            "堂邑路", "李村街", "即墨路", "港华大厦", "港环路", "馆陶街", "普集路", "朝阳街", "甘肃广场", "港夏街", "港联路", "陵县大厦", "上海路", "宝山广场", "武定路",
            "长清街", "长安路", "惠民街", "武城广场", "聊城大厦", "海泊路", "沧口街", "宁波路", "胶州广场", "莱州路", "招远街", "冠县路", "六码头", "金乡广场", "禹城街",
            "临清路", "东阿街", "吴淞路", "大港沿", "辽宁路", "棣纬二大厦", "大港纬一路", "贮水山支街", "无棣纬一广场", "大港纬三街", "大港纬五路", "大港纬四街", "大港纬二路",
            "无棣二大厦", "吉林支路", "大港四街", "普集支路", "无棣三街", "黄台支广场", "大港三街", "无棣一路", "贮水山大厦", "泰山支路", "大港一广场", "无棣四路", "大连支街",
            "大港二路", "锦州支街", "德平广场", "高苑大厦", "长山路", "乐陵街", "临邑路", "嫩江广场", "合江路", "大连街", "博兴路", "蒲台大厦", "黄台广场", "城阳街",
            "临淄路", "安邱街", "临朐路", "青城广场", "商河路", "热河大厦", "济阳路", "承德街", "淄川广场", "辽北街", "阳信路", "益都街", "松江路", "流亭大厦", "吉林路",
            "恒台街", "包头路", "无棣街", "铁山广场", "锦州街", "桓台路", "兴安大厦", "邹平路", "胶东广场", "章丘路", "丹东街", "华阳路", "青海街", "泰山广场",
            "周村大厦", "四平路", "台东西七街", "台东东二路", "台东东七广场", "台东西二路", "东五街", "云门二路", "芙蓉山村", "延安二广场", "云门一街", "台东四路", "台东一街",
            "台东二路", "杭州支广场", "内蒙古路", "台东七大厦", "台东六路", "广饶支街", "台东八广场", "台东三街", "四平支路", "郭口东街", "青海支路", "沈阳支大厦", "菜市二路",
            "菜市一街", "北仲三路", "瑞云街", "滨县广场", "庆祥街", "万寿路", "大成大厦", "芙蓉路", "历城广场", "大名路", "昌平街", "平定路", "长兴街", "浦口广场",
            "诸城大厦", "和兴路", "德盛街", "宁海路", "威海广场", "东山路", "清和街", "姜沟路", "雒口大厦", "松山广场", "长春街", "昆明路", "顺兴街", "利津路",
            "阳明广场", "人和路", "郭口大厦", "营口路", "昌邑街", "孟庄广场", "丰盛街", "埕口路", "丹阳街", "汉口路", "洮南大厦", "桑梓路", "沾化街", "山口路", "沈阳街",
            "南口广场", "振兴街", "通化路", "福寺大厦", "峄县路", "寿光广场", "曹县路", "昌乐街", "道口路", "南九水街", "台湛广场", "东光大厦", "驼峰路", "太平山",
            "标山路", "云溪广场", "太清路"]
    index = int(get_num(0, len(road) - 1))
    first = str(road[index])
    second = str(random.randint(1, 50)) + "号"
    third = "-" + str(random.randint(1, 99)) + "-" + str(random.randint(1, 99))
    return first + second + third


def random_company():
    company_list = ["合肥世纪精信机械有限公司", "连云港远联物流（合肥）新都会2站", "陆河县消防中队", "大理市公安局洱海派出所", "顺暴苑物业部", "广东建安消防机电工程有限公司", "河北金靓派服装有限公司", "伊宁市恒大地产", "岳口镇交警大队",
                    "大庆石化公司消防支队一大队", "武警西藏总队", "彭城镇人民政府", "茶小西奶茶店", "三沙市国家税务局", "马鞍山市金迈机械科技发展有限公司", "特勤二中队", "甜咪公主烘焙坊", "深圳市罗湖区清水河泥岗派出所",
                    "康佳集团股份有限公司",
                    "厦门鸿韦达五金有限公司", "南沙区南沙边防派出所", "龙岩市新罗区申通快递有限公司", "蔡家关派出所", "中国解放军68076部队", "山南城市建设投资有限责任公司", "广西壹昱元投资有限公司", "拉萨市山水石材厂",
                    "北京爱车伴侣科技有限公司",
                    "中国石油重庆销售分公司", "苏州市度假区光福镇光福交警中队", "郑州公安局嵩山路分局治安三中队", "鄂温克旗政府", "和林格尔县振华通讯", "南方货运", "晟光科技股份有限公司", "老廖钣金烤漆", "两江新区美弘日用品经营部",
                    "吉林省邮政公司长春市分公司",
                    "昊天保安有限公司", "丹水百姓家私实木家具批发总汇", "花园国际大酒店", "万人迷名品店", "蚌埠市武装押运公司", "西安汉唐金融财税研究院", "妮妮彩妆绣", "永达理保险经纪公司", "迁安市城市管理综合执法大队", "武义吉利汽车直营店",
                    "徐家小厨",
                    "乐有家控股集团", "江苏省华海消防安装有限公司", "华塘镇人民政府", "中国人民解放军69222部队54分队", "武汉市化工区城管局", "博罗县公庄镇三乡中学", "学子餐饮管理有限公司", "福建达成安装工程有限公司", "南源综合行政执法队",
                    "西峡县交通执法局", "贵州军鹏吉顺汽车服务有限公司", "厦门立方艺品有限公司", "铁锋区政府", "小横垅乡人民政府", "湖南省汨罗市城管队", "海南省三亚市吉阳区92474部队41", "城市管理综合执法局", "广东电视周报", "个体户",
                    "当涂县乌溪镇人民政府", "湖南博瑷化妆品贸易有限公司", "溧阳市人民政府", "迁安市万嘉科技有限公司", "中成天坛假日酒店", "昆山市小康园连锁超市", "公安局交警大队", "上海莘松路证券营业部", "中国移动通信集团湖北有限公司公安分公",
                    "糖果儿童装",
                    "太平洋纺织品有限公司", "王寨派出所", "封开县水务局", "安泽县彦亮装饰材料经销部", "小天府川菜馆", "从达商贸有限公司", "宣和麻将机专卖店", "海口交警支队", "六哨乡九年一贯制学校", "太原市昌茂消防有限公司",
                    "吉林省四平市第二中学",
                    "个体工商户", "兴宁市罗岗镇人民政府", "河北法制报社", "唐山广野食品集团有限公司", "乐博机器人长阳科技有限公司", "城东区政法委", "德国马牌", "永安市文化市场综合执法大队", "肇源县新站镇淘气堡儿童乐园"]
    index = int(get_num(0, len(company_list) - 1))
    company = company_list[index]
    return company


def random_work_tel():
    work_tel_first = ['0310-', '0311-', '0312-', '0313-', '0314-', '0315-', '0316-', '0317-', '0318-', '0319-', '0335-',
                      '0570-', '0571-', '0572-', '0573-', '0574-', '0575-', '0576-', '0577-', '0578-', '0579-', '0580-',
                      '024-', '0410-', '0411-', '0412-', '0413-', '0414-', '0415-', '0416-', '0417-', '0418-', '0419-',
                      '0421-', '0427-', '0429-', '027-', '0710-', '0711-', '0712-', '0713-', '0714-', '0715-', '0716-',
                      '0717-', '0718-', '0719-', '0722-', '0724-', '0728-', '025-', '0510-', '0511-', '0512-', '0513-',
                      '0514-', '0515-', '0516-', '0517-', '0517-', '0518-', '0519-', '0523-', '0470-', '0471-', '0472-',
                      '0473-', '0474-', '0475-', '0476-', '0477-', '0478-', '0479-', '0482-', '0483-', '0790-', '0791-',
                      '0792-', '0793-', '0794-', '0795-', '0796-', '0797-', '0798-', '0799-', '0701-', '0350-', '0351-',
                      '0352-', '0353-', '0354-', '0355-', '0356-', '0357-', '0358-', '0359-', '0930-', '0931-', '0932-',
                      '0933-', '0934-', '0935-', '0936-', '0937-', '0938-', '0941-', '0943-', '0530-', '0531-', '0532-',
                      '0533-', '0534-', '0535-', '0536-', '0537-', '0538-', '0539-', '0450-', '0451-', '0452-', '0453-',
                      '0454-', '0455-', '0456-', '0457-', '0458-', '0459-', '0591-', '0592-', '0593-', '0594-', '0595-',
                      '0595-', '0596-', '0597-', '0598-', '0599-', '020-', '0751-', '0752-', '0753-', '0754-', '0755-',
                      '0756-', '0757-', '0758-', '0759-', '0760-', '0762-', '0763-', '0765-', '0766-', '0768-', '0769-',
                      '0660-', '0661-', '0662-', '0663-', '028-', '0810-', '0811-', '0812-', '0813-', '0814-', '0816-',
                      '0817-', '0818-', '0819-', '0825-', '0826-', '0827-', '0830-', '0831-', '0832-', '0833-', '0834-',
                      '0835-', '0836-', '0837-', '0838-', '0839-', '0840-', '0730-', '0731-', '0732-', '0733-', '0734-',
                      '0735-', '0736-', '0737-', '0738-', '0739-', '0743-', '0744-', '0745-', '0746-', '0370-', '0371-',
                      '0372-', '0373-', '0374-', '0375-', '0376-', '0377-', '0378-', '0379-', '0391-', '0392-', '0393-',
                      '0394-', '0395-', '0396-', '0398-', '0870-', '0871-', '0872-', '0873-', '0874-', '0875-', '0876-',
                      '0877-', '0878-', '0879-', '0691-', '0692-', '0881-', '0883-', '0886-', '0887-', '0888-', '0550-',
                      '0551-', '0552-', '0553-', '0554-', '0555-', '0556-', '0557-', '0558-', '0559-', '0561-', '0562-',
                      '0563-', '0564-', '0565-', '0566-', '0951-', '0952-', '0953-', '0954-', '0431-', '0432-', '0433-',
                      '0434-', '0435-', '0436-', '0437-', '0438-', '0439-', '0440-', '0770-', '0771-', '0772-', '0773-',
                      '0774-', '0775-', '0776-', '0777-', '0778-', '0779-', '0851-', '0852-', '0853-', '0854-', '0855-',
                      '0856-', '0857-', '0858-', '0859-', '029-', '0910-', '0911-', '0912-', '0913-', '0914-', '0915-',
                      '0916-', '0917-', '0919-', '0971-', '0972-', '0973-', '0974-', '0975-', '0976-', '0977-', '0890-',
                      '0898-', '0899-', '0891-', '0892-', '0893-']
    first = str(random.choice(work_tel_first))
    second = str(random.randint(1, 9999999))
    return first + second


def random_nation():
    nation_list = ["壮族", "藏族", "裕固族", "彝族", "瑶族", "锡伯族", "乌孜别克族", "维吾尔族", "佤族", "土家族", "土族", "塔塔尔族", "塔吉克族", "水族", "畲族",
                   "撒拉族", "羌族", "普米族", "怒族", "纳西族", "仫佬族", "苗族", "蒙古族", "门巴族", "毛南族", "满族", "珞巴族", "僳僳族", "黎族",
                   "拉祜族", "柯尔克孜族", "景颇族", "京族", "基诺族", "回族", "赫哲族", "哈萨克族", "哈尼族", "仡佬族", "高山族", "鄂温克族", "俄罗斯族", "鄂伦春族",
                   "独龙族", "东乡族", "侗族", "德昂族", "傣族", "达斡尔族", "朝鲜族", "布依族", "布朗族", "保安族", "白族", "阿昌族", "汉族"]
    index = int(get_num(0, len(nation_list) - 1))
    nation = nation_list[index]
    return nation


def get_before_date(overdue_days, days, n):
    days_ago = (datetime.datetime.now() - datetime.timedelta(overdue_days - days * n)).strftime("%Y-%m-%d")
    return days_ago


def random_oversea_name():
    ret = random.choice(oversea_names)
    return ret


# 泰国手机号码前两位是06或08或09的10位数字
def random_th_tel():
    num_start = ['06', '08', '09']
    start = random.choice(num_start)
    end = ''.join(random.sample(string.digits, 8))
    ret = start + end
    return ret


# 印度手机号码10位数字
def random_ind_tel():
    num_start = ['1', '2', '3', '4', '5', '6', '7', '8', '9']
    start = random.choice(num_start)
    end = ''.join(random.sample(string.digits, 9))
    ret = start + end
    return ret


# 菲律宾手机号码9开头的10位数字
def random_php_tel():
    num_start = ['9']
    start = random.choice(num_start)
    end = ''.join(random.sample(string.digits, 9))
    ret = start + end
    return ret


# 海外，印度aadhaar卡号码12位
def random_oversea_ind_gennerator():
    num_start = ['20', '21', '30', '88']
    start = random.choice(num_start)
    end = ''.join(random.sample(string.digits, 10))
    ret = start + end
    return ret


# 海外，印度pan卡号码10位，[A-Z0-9]
def random_oversea_ind_pan_id_card():
    # string.digits:生成所有数字0-9, string.ascii_uppercase:生成所有字母，从A-Z
    ret = ''.join(random.sample(string.ascii_uppercase + string.digits, 10))
    return ret


# 海外，菲律宾Passport：第一位字母，后8位数字或字母，一共九位。
def random_oversea_ph_passport_id_card():
    # string.digits:生成所有数字0-9, string.ascii_uppercase:生成所有字母，从A-Z
    first = ''.join(random.sample(string.ascii_uppercase, 1))
    second = ''.join(random.sample(string.ascii_uppercase + string.digits, 8))
    ret = first + second
    return ret


# 海外，菲律宾Driver license: 11位，第一位字母，后10位数字。
def random_oversea_ph_driver_license_id_card():
    # string.digits:生成所有数字0-9, string.ascii_uppercase:生成所有字母，从A-Z
    first = ''.join(random.sample(string.ascii_uppercase, 1))
    second = ''.join(random.sample(string.digits, 10))
    ret = first + second
    return ret


# 海外，菲律宾TIN：9-14位数字。
def random_oversea_ph_tin_id_card():
    first = random.randint(1, 9)
    random_b = random.randint(8, 13)
    second = ""
    for i in range(random_b):
        ch = chr(random.randrange(ord('0'), ord('9') + 1))
        second += ch
    ret = str(first) + second
    return ret


# 海外，菲律宾UMID:12位数字,PhiHealth：12位数字（只允许输入纯数字）
def random_oversea_ph_umid_phihealth_id_card():
    first = random.randint(1, 9)
    second = ""
    for i in range(11):
        ch = chr(random.randrange(ord('0'), ord('9') + 1))
        second += ch
    ret = str(first) + second
    return ret


# 海外，菲律宾SSS：10位数字。
def random_oversea_ph_sss_id_card():
    first = random.randint(1, 9)
    # string.digits:生成所有数字0-9
    ret = first + ''.join(random.sample(string.digits, 9))
    return ret


# 海外，菲律宾Voter's ID：22位字母+数字（只允许输入数字和字母，大小写不限）
def random_oversea_ph_voter_id_card():
    # string.digits:生成所有数字0-9, string.ascii_uppercase:生成所有字母，从A-Z
    ret = ''.join(random.sample(string.ascii_uppercase + string.digits, 22))
    return ret


# 海外，菲律宾Postal Card：12-13位字母+数字（只允许输入数字和字母，大小写不限）
def random_oversea_ph_postal_card_id_card():
    first = random.randint(12, 13)
    # string.digits:生成所有数字0-9, string.ascii_uppercase:生成所有字母，从A-Z
    ret = ''.join(random.sample(string.ascii_uppercase + string.digits, first))
    return ret


# 海外，菲律宾National ID：16位数字（只允许输入纯数字）
def random_oversea_ph_national_id_card():
    first = random.randint(1, 9)
    second = ""
    for i in range(15):
        ch = chr(random.randrange(ord('0'), ord('9') + 1))
        second += ch
    ret = str(first) + second
    return ret


# 菲律宾证件类型：
# "1": "UMID (unified multi-purpose ID)",
# "2": "TIN（Taxpayer Identification Number）",
# "3": "SSS (Social Security System ID)",
# "4": "Passport",
# "5": "Driver's License",
# "6": "PhiHealth",
# "7": "Voter's ID",
# "8": "Postal Card",
# "9": "National ID"
def random_ph_id_card_type(id_card_type):
    ret = ""
    if id_card_type == 1:
        ret = random_oversea_ph_umid_phihealth_id_card()
    if id_card_type == 2:
        ret = random_oversea_ph_tin_id_card()
    if id_card_type == 3:
        ret = random_oversea_ph_sss_id_card()
    if id_card_type == 4:
        ret = random_oversea_ph_passport_id_card()
    if id_card_type == 5:
        ret = random_oversea_ph_driver_license_id_card()
    if id_card_type == 6:
        ret = random_oversea_ph_umid_phihealth_id_card()
    if id_card_type == 7:
        ret = random_oversea_ph_voter_id_card()
    if id_card_type == 8:
        ret = random_oversea_ph_postal_card_id_card()
    if id_card_type == 9:
        ret = random_oversea_ph_national_id_card()
    return ret


# 海外，泰国身份证号码13位
def random_oversea_gennerator():
    num_start = ['180', '110', '343', '881']
    start = random.choice(num_start)
    end = ''.join(random.sample(string.digits, 10))
    ret = start + end
    return ret


# 海外，印尼身份证号码16位
def random_id_gennerator():
    num_start = ['11', '32', '62', '51', '14', '31']
    ret = random.choice(num_start)
    for i in range(14):
        ch = chr(random.randrange(ord('0'), ord('9') + 1))
        ret += ch
    return ret


def random_oversea_email():
    num_start = random_tele(is_false=False)
    ret = num_start + "@home.com"
    return ret


# 泰国工作类型
def random_job_type():
    job_list = ["คนจัดสวน", "ช่าง", "ทหารประจำการ", "นักมวย", "ผู้ประกอบการธุรกิจส่วนตัว", "พนักงานขับรถ", "พนักงานขาย", "พนักงานส่งของ", "สถาปนิก",
                "อื่นๆ",
                "เกี่ยวกับทางศาสนา", "เจ้าหน้าที่ความปลอดภัย", "แรงงานรับ",
                ]
    ret = random.choice(job_list)
    return ret


def random_education_level():
    education_level_list = ["DIPLOMA I", "DIPLOMA Ⅱ", "DIPLOMA Ⅲ", "S1 - bachelor", "S2 - master", "SD - primary school", "SLTA - high school",
                            "SLTP - junior high school"
                            ]
    ret = random.choice(education_level_list)
    return ret


# 泰国婚姻状态
def random_th_marital_status():
    marital_status_list = ["การหย่าร้าง", "เดียว", "แต่งงานแล้ว", ]
    ret = random.choice(marital_status_list)
    return ret


def random_number_of_offspring():
    number_of_offspring_list = ['0', '1', '2', '3', '4', 'more than 4']
    ret = random.choice(number_of_offspring_list)
    return ret


# 泰国月收入
def random_th_monthly_income():
    monthly_income_list = ["น้อยกว่า THB9,000", "THB9,001- THB15,000", "THB15,001-THB20,000", "THB20,001-THB25,000", "THB25,001-THB30,000",
                           "มากกว่า THB30,000"]
    ret = random.choice(monthly_income_list)
    return ret


def random_card_uuid():
    card_uuid = ""
    for i in range(13):
        ch = chr(random.randrange(ord('0'), ord('9') + 1))
        card_uuid += ch
    return card_uuid


def random_bank_card_account_number():
    bank_card_account_number = ""
    for i in range(10):
        ch = chr(random.randrange(ord('0'), ord('9') + 1))
        bank_card_account_number += ch
    return bank_card_account_number


def random_upi_account_number():
    pre = ""
    suffix_list = ["@okaxis", "@paytm"]
    tail = random.choice(suffix_list)
    for i in range(6):
        ch = chr(random.randrange(ord('0'), ord('9') + 1))
        pre += ch
    upi = pre + tail
    return upi


def random_bank_name():
    bank_name_list = ["BANGKOK BANK PUBLIC COMPANY LTD.",
                      "BANK FOR AGRICULTURE AND AGRICULTURAL CO-OPERATIVESMIZUHO BANK LTD.",
                      "BANK OF AYUDHYA",
                      "CIMB(THAI) PUBLIC COMPANY LIMITED",
                      "GOVERNMENT HOUSING BANK",
                      "GOVERNMENT SAVING BANK",
                      "KASI KORN BANK PUBLIC COMPANY LIMITED",
                      "KIA TN AKIN BANK PUBLIC COMPANY LIMITED",
                      "KRUNG THAI BANK PUBLIC COMPANY LTD.",
                      "LAND AND HOUSES RETAIL BANK PUBLIC COMPANY LIMITED",
                      "SIAM COMMERCIAL BANK PUBLIC COMPANY LTD.",
                      "THAN A CHART BANK PUBLIC COMPANY LIMITED",
                      "TMB BANK PUBLIC COMPANY LIMITED",
                      "UNITED OVERSEAS BANK(THAD PUE LIC COMPANY LIMITED", ]
    ret = random.choice(bank_name_list)
    return ret


# 菲律宾，证件类型
def random_ph_id_type():
    id_card_type = ["UMID (unified multi-purpose ID)",
                    "SSS (social security system id)",
                    "Taxpayer Identification number (TIN)",
                    "Driver's License", "Passport"]
    ret = random.choice(id_card_type)
    return ret


# 菲律宾，受教育等级
def random_ph_education_level():
    education_level = ["None",
                       "Primary school/grade school",
                       "secondary/high school",
                       "certification/vocational courses",
                       "bachelors degree",
                       "master degree",
                       "PhD", ]
    ret = random.choice(education_level)
    return ret


# 菲律宾，婚姻状态
def random_ph_marital_status():
    marital_status = ["None",
                      "Primary school/grade school",
                      "secondary/high school",
                      "certification/vocational courses",
                      "bachelors degree",
                      "master degree",
                      "PhD", ]
    ret = random.choice(marital_status)
    return ret


# 菲律宾，户籍地住址时长
def random_ph_duration_of_stay():
    duration_of_stay = ["<3 months",
                        "3-6 months",
                        "6-12 months",
                        "1-2 years",
                        "2-3 years",
                        "3 years+", ]
    ret = random.choice(duration_of_stay)
    return ret


# 菲律宾，工作类型
def random_ph_occupation():
    occupation = ["Staff/Factory worker",
                  "Office worker",
                  "Police/Military employee",
                  "Pensioner/Retired",
                  "Housewife",
                  "Unemployed",
                  "Student",
                  "Attorney/Lawyer/Notary",
                  "Self-employed",
                  "Government Employee",
                  "Manager/Professional specialist",
                  "Contact Employee",
                  "Business owner", ]
    ret = random.choice(occupation)
    return ret


# 菲律宾，职级
def random_ph_position_level():
    position_level = ["fresh grad",
                      "general staff",
                      "manager",
                      "supervisor",
                      "owner",
                      "freelancer", ]
    ret = random.choice(position_level)
    return ret


# 菲律宾，工作时长
def random_ph_working_years():
    working_years = ["within 3 months",
                     "3-6 months",
                     "6-12 months",
                     "1-2 years",
                     "2 years above", ]
    ret = random.choice(working_years)
    return ret


# 墨西哥，身份证号码18位（含字母、数字）
# CURP代码由18个字符组成，分配如下：
# 第一姓氏的初始和第一个内部元音;
# 第二姓的首字母（或字母“X”，如果像某些外国人那样，那个人没有第二姓）;
# 第一个给定的名字的初始;
# 出生日期（年份2位，月份2位，日期2位）;
# 一个字母的性别指标（H表示男性（西班牙语中的hombre），M表示女性（西班牙语中的mujer））;
# 一个双字母代码，表示该人出生的州;对于在国外出生的人，使用NE（nacido en el extranjero）代码;
# 第一个姓氏的第二个辅音;
# 第二姓氏的第二个辅音;
# 第一个名字的第二个辅音;和
# 2000年以前出生的人为0-9，2000年以后出生的人为A-Z;这些字符是由全国人口登记处生成的，以防止相同的条目。
# 已婚妇女只能使用婚前名字。
# 例如，一个名为Gloria Hernández García的假设人员的CURP代码是1956年4月27日在韦拉克鲁斯州出生的女性，可能是HEGG560427MVZRRL04。
# 对应正则：^[a-zA-Z]{4}(([0-9][0-9])([0][0-9]|[1][0-2])([0-9][0-9]))[MHmh](AS|BC|BS|CC|CL|CM|CS|CH|DF|DG|GT|GR|HG|JC|MC|MN|MS|NT|NL|OC|PL|QT|QR|SP|SL|SR|TC|TS|TL|VZ|YN|ZS|NE)\w{5}$
def random_mex_id_number():
    letters = ''.join(random.sample(string.ascii_uppercase, 4))
    birth_year = ''.join(random.sample(string.digits, 2))

    # 年份项
    da = date.today() + timedelta(days=random.randint(1, 366))
    # 月份和日期项
    birth_date = da.strftime('%m%d')

    gender = ''.join(random.sample('MH', 1))
    # 墨西哥州简称代码
    state_list = ["AS", "BC", "BS", "CC", "CL", "CM", "CS", "CH", "DF", "DG", "GT", "GR", "HG", "JC", "MC", "MN", "MS", "NT", "NL", "OC", "PL", "QT",
                  "QR",
                  "SP", "SL", "SR", "TC", "TS", "TL", "VZ", "YN", "ZS", "NE"]
    state = random.choice(state_list)
    # string.digits:生成所有数字0-9, string.ascii_uppercase:生成所有字母，从A-Z
    tail = ''.join(random.sample(string.digits + string.ascii_uppercase, 5))
    ret = letters + birth_year + birth_date + gender + state + tail
    return ret


# 墨西哥手机号码10位数字
def random_mex_tel():
    num_start = random.randint(1, 9)
    start = random.choice(str(num_start))
    end = ''.join(random.sample(string.digits, 9))
    ret = start + end
    return ret


# 巴基斯坦手机号码03开头的11位数字
def random_pk_tel():
    num_start = ['03']
    start = random.choice(num_start)
    end = ''.join(random.sample(string.digits, 9))
    ret = start + end
    return ret


# 随机生成4-10位的邮箱地址，0~9 A~Z a~z
def random_email():
    number = random.randint(4, 10)
    start = ''.join(random.sample(string.digits + string.ascii_uppercase + string.ascii_lowercase, number))
    email_type = ["@qq.com", "@163.com", "@126.com", "@189.com"]
    end = random.choice(email_type)
    ret = start + end
    return ret


if __name__ == '__main__':
    rs = random_email()
    print(rs)
