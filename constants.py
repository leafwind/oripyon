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