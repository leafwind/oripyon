from app.group_reply import group_reply_test, group_reply_luna, group_reply_yebai, group_reply_maplestory, \
    group_reply_lineage_m, group_reply_mao_sino_alice, group_reply_nier_sino_alice, group_reply_taiwan_sino_alice, \
    group_reply_working, group_reply_mao, group_reply_mao_test

CWB_DB_PATH = '/var/sqlite/cwb.db'

TABLE_AQFN = 'table_AQI'

TABLE_AQI = 'table_AQI_now'


HUGE_GROUP_IDS = [
    'C770afed112311f3f980291e1e488e0ef'
]

GROUP_MAPPING = {
    'C1bebaeaf89242089f0d755d492df6cb6': {
        'name': '測試群組',
        'function': group_reply_test,
    },
    'C690e08d2fb900d5bbd873e103d500b92': {
        'name': '皇家御貓園',
        'function': group_reply_luna,
    },
    'C25add4301bc790a641e07b02b868a9b7': {
        'name': '葉白',
        'function': group_reply_yebai,
    },
    'C0cd56d37156c5ad3fe04b702624d50dd': {
        'name': '小路北七群',
        'function': group_reply_maplestory,
    },
    'C966396824051cbb00e35af7b4123a0a5': {
        'name': '天堂老司機',
        'function': group_reply_lineage_m,
    },
    'Cfb6a76351d112834244144a1cd4f0f57': {
        'name': '死愛魔王城',
        'function': group_reply_mao_sino_alice,
    },
    'C1e38a92f8c7b4ad377df882b9f3bf336': {
        'name': '尼爾主題餐廳',
        'function': group_reply_nier_sino_alice,
        'log_filename': 'nier_sino_alice',
    },
    'C15c762c0a497d62992c01b42ba9b39d9': {
        'name': '死愛台版交流區',
        'function': group_reply_taiwan_sino_alice,
    },
    'Cbc420349e56f3bae5d5f46fafb0ac5cb': {
        'name': '社畜人生的煩惱',
        'function': group_reply_working,
    },
    'C770afed112311f3f980291e1e488e0ef': {
        'name': '魔王城',
        'function': group_reply_mao,
        'log_filename': 'mao',
    },
    'Cf794cf7dc1970c3fba9122673cf3dcde': {
        'name': '魔王城測試',
        'function': group_reply_mao_test,
        'log_filename': 'mao_test',
    },
    'C498a6c669b4648d8dcb807415554fda1': {
        'name': 'sslin test',
        'function': group_reply_mao_test,
        'log_filename': 'mao_test2',
    }
}

TEACHER_HO = [
    '{name}先生，我有錄起來喔！',
    '我婆受因果業所困，身陷卡池，御主{name}發願，願獻我薪水，求彩光乍現',
    '不要停下來，繼續抽！很好，{name}你婆要出來了！',
    '{name}我跟你講，繼續抽下去，不要理會旁邊的聲音',
    '{name}你看到那個課金的按鈕了嗎？那是慈孤的化身，你一直按，慈孤觀音就會引導你得到你想要的東西。',
    '{name}橋下那些是歐洲人，他們正在被自己的業火焚燒，不要去管他們',
    '好，{name}你聽我說，你先把信用卡準備好，你家有沒有網路？有？好，那在手機前就可以了，叫卡池聽話，照我的話做，一定抽的到',
    '{name}你不要緊張，繼續抽就對了，啊有問題再打給我喔我都在！\n\n\n嘟嘟嘟嘟嘟嘟嘟嘟',
    '很好，你課下去了。你看到什麼？卡池？那是你的本命池。想見到老婆，要先內觀自己，順從你的慾望，抽下去。',
    '{name}喔，是，我知道、我知道\n這個喔，我跟你說～你不用緊張，抽五星急不得\n這個卡池本來就是歐洲一單、非洲十單抽到\n你要對營運有信心\n你要有耐心啊，不要去SKIP他、讓他慢慢跑\n不要連點他，好嗎？\n好，你有問題再來問，我都在，我一定幫忙！',
]