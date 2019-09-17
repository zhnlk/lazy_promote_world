# -*- coding:utf-8 -*-
import ast
import json
import sys
from datetime import datetime
import demjson
from workflow import Workflow, web

reload(sys)
sys.setdefaultencoding('utf-8')


# 返回某日是星期几
def the_contract(key):
    zhengzhou_node_dict = {
        'ta': 'pta_qh', 'oi': 'czy_qh', 'zc': 'dlm_qh', 'wh': 'qm_qh', 'jr': 'jdm_qh', 'sr': 'bst_qh',
        'cf': 'mh_qh', 'ri': 'zxd_qh', 'ma': 'zc_qh', 'fg': 'bl_qh', 'lr': 'wxd_qh', 'sf': 'gt_qh', 'sm': 'mg_qh',
        'cy': 'ms_qh', 'ap': 'xpg_qh', 'cj': 'hz_qh', 'ur': 'ns_qh'
    }

    shanghai_node_dict = {
        'fu': 'ry_qh', 'sc': 'yy_qh', 'al': 'lv_qh', 'ru': 'xj_qh', 'zn': 'xing_qh', 'cu': 'tong_qh', 'au': 'hj_qh',
        'rb': 'lwg_qh', 'wr': 'xc_qh', 'pb': 'qian_qh', 'ag': 'by_qh', 'bu': 'lq_qh', 'hc': 'rzjb_qh', 'sn': 'xi_qh',
        'ni': 'ni_qh', 'sp': 'zj_qh', 'nr': 'ehj_qh'
    }

    dalian_node_dict = {
        'vc': 'pvc_qh', 'p': 'zly_qh', 'b': 'de_qh', 'm': 'dp_qh', 'i': 'tks_qh', 'jd': 'jd_qh', 'l': 'lldpe_qh',
        'pp': 'jbx_qh', 'fb': 'xwb_qh', 'bb': 'jhb_qh', 'y': 'dy_qh', 'c': 'hym_qh', 'a': 'dd_qh', 'j': 'jt_qh',
        'jm': 'jm_qh', 'cs': 'ymdf_qh', 'eg': 'yec_qh', 'rr': 'gm_qh'
    }

    if zhengzhou_node_dict.has_key(key):
        return zhengzhou_node_dict[key]
    elif shanghai_node_dict.has_key(key):
        return shanghai_node_dict[key]
    elif dalian_node_dict.has_key(key):
        return dalian_node_dict[key]


def curl(key):
    url = 'http://vip.stock.finance.sina.com.cn/quotes_service/api/json_v2.php/Market_Center.getHQFuturesData?page={page}&num={num}&sort={sort}&asc={asc}&node={node}&base={base}'.format(
        page=1, num=5, sort='position', asc=0, node=the_contract(key), base='futures')

    keys = [
        'ask', 'askvol', 'bid', 'bidvol', 'changepercent', 'close', 'contract', 'currentvol', 'high', 'low', 'market',
        'name', 'open', 'position', 'prevsettlement', 'settlement', 'symbol', 'ticktime', 'trade', 'tradedate', 'volume'
    ]
    resp = web.get(url).content.decode('gbk')

    return demjson.decode(resp)

def main(wf):
    key = sys.argv[1]
    resp = curl(key)
    # d = data['HeWeather data service 3.0'][0]
    # city = d['basic']['city']

    # 获取一周内的数据
    # for n in range(0, 7):
    for r in resp:
        # 交易所
        exchange = r['exchange']
        # 交易日期
        tradedate = r['tradedate']
        # 交易时间
        ticktime = r['ticktime']

        # 交易品种
        symbol = r['symbol']
        # 标的名称
        name = r['name']

        bidprice1 = r['bidprice1']
        askprice1 = r['askprice1']
        askvol1 = r['askvol1']
        bidvol1 = r['bidvol1']
        changepercent = r['changepercent']

        preclose = r['preclose']
        open = r['open']
        close = r['close']
        low = r['low']
        high = r['high']

        trade = r['trade']
        settlement = r['settlement']
        bid = r['bid']
        volume = r['volume']
        ask = r['ask']
        position = r['position']

        prevsettlement = r['prevsettlement']
        # 昨日结算
        presettlement = r['presettlement']

        # day = d['daily_forecast'][n]

        # 把API获取的天气、温度、风力等信息拼接成 alfred条目的标题、副标题
        title = '{symbol}@{exchange} {name}'.format(symbol=r['symbol'], name=r['name'], exchange=r['exchange'])

        # 代码 名称 涨跌幅 最新价 昨收 今开 最高	最低	买入	卖出	动态结算	昨日结算	买量 卖量 成交量 持仓量
        subtitle = '涨跌幅{changepercent}% 最新价{trade} 昨收{preclose} ' \
                   '今开{open} 最高{high} 最低{low} 买入{ask} 卖出{bid} 动态结算{settlement} 昨日结算 {presettlement}' \
                   '买量{askvol1} 卖量{bidvol1} 成交量{volume} 持仓量{position}'.format(
            changepercent=r['changepercent'], trade=r['trade'],
            preclose=r['preclose'],
            open=r['open'], high=r['high'], low=r['low'], ask=r['ask'], bid=r['bid'], settlement=r['settlement'],
            presettlement=r['presettlement'],
            askvol1=r['askvol1'], bidvol1=r['bidvol1'], volume=r['volume'], position=r['position']
        )
        # print(title)
        # print(subtitle)

        # 向alfred添加条目,传标题、副标题、图片路径(图片直接用的和风天气提供的天气图,每个图片的命名对应天气状态码)
        # wf.add_item(title=title, subtitle=subtitle,icon='images/{code}.png'.format(code=day['cond']['code_d']))
        wf.add_item(title=title, subtitle=subtitle)
    wf.send_feedback()


if __name__ == '__main__':
    wf = Workflow()
    sys.exit(wf.run(main))
