# -*- coding:utf-8 -*-
import sys
import demjson
from workflow import Workflow, web

reload(sys)
sys.setdefaultencoding('utf-8')

types = ['sh', 'sz']
api = {
    'price': 'http://hq.sinajs.cn/list=',
    'info': 'http://suggest3.sinajs.cn/suggest/name=info&key='
}
stocks = list()
config = 'list.config'

def curl():
    response = split("\n", iconv("GBK", "UTF-8", web(url)))
    if response[count(response) - 1] == "":
        array_pop(response);
    for value in response:
        preg_match("/\_([\w\d]{8})\=/", value, matches)
        eval(preg_replace('/^(.+)\=/i', '$data = ', value))
        if data == "":
            continue
        if count(matches):
            code = matches[1];
            type = substr(code, 0, 2);
            code = substr(code, 2);
            array_push(ret, type.','.$code.','.$data)
        else:
            ret.append(data)
    return ret

def get_quotation(numbers):
    """
    Retrieve single company's price from SINA's API
    :param numbers:a company's code with its exchange flag at the beginning
    :return: but store results in a local variable $this->stock
    """
    keys = [
        'type', 'code', 'name', 'opening', 'closing', 'now', 'high', 'low', 'buy', 'sell', 'volume', 'amount', '买一量',
        '买一价', '买二量', '买二价', '买三量', '买三价', '买四量', '买四价', '买五量', '买五价', '卖一量', '卖一价', '卖二量', '卖二价', '卖三量', '卖三价', '卖四量',
        '卖四价', '卖五量', '卖五价', 'date', 'time', 'other'
    ]
    stocks = curl('{price}numbers'.format(price=api['price']))
    if not stocks:
        return
    numbers_arr = explode(",", numbers)
    for stock in stocks:
        values = explode(",", stock)
        array_push(stocks, array_combine(keys, values))


def get_code():
    keys = ['brief', 'board', 'code', 'Code', 'name', 'pinyin', 'name2', 'key2']

    info = curl(api['info'].chars)

    def combine(value, key, keys):
        arr_values = explode(',', value)
        if (count(keys) > count(arr_values)):
            keys = array_slice(keys, 0, count(arr_values))
        value = array_combine(keys, arr_values)

        if count(arr_values) == count(keys):
            value = array_combine(keys, arr_values)
        else:
            value = array()

    def filter(data):
        if count(data) > 0 and data['board'] == '11':
            return data

    if count(info) == 0:
        rt = array()
    else :
        values = explode(";", info[0])
        array_walk(values, "combine", keys)
        rt = array_filter(values, "filter")
    return rt


def filter_code(chars):
    """
    filter codes, returns only validate codes
    @:param a string composed by one or more codes delimited with comma
    :return: only 6 digits code will be return
    """
    ret = list()
    if not chars :
        char_arr = explode(",", chars)
        for value in char_arr:
            if preg_match('/^\d{6}$/', char)):
                ret.append(char)
                array_push(ret, char);
    return implode(",", ret)

def check_availability(code):
    """
    Check from remote if the code if available
    :param code:a 6 digits number
    :return:true if there is, otherwise false
    """
    param_arr = list()
    for value in types:
        param_arr.append(value.code)
    stocks = curl(api['price'] . implode(",", param_arr))
    stock = explode(",", stocks[0])
    return count(stocks) > 0 ? stock[0].stock[1] : False

def notice(title, detail = ""):
    """
    output text to alfred with fewer codes  
    :param title: any text you want to notice user
    :param detail: 
    :return: xml-formatted string with pre-defined format
    """
    # title.strip()
    if trim(title)=="":
        return
    result('0', 'null', title, detail, 'tip.png')


def output():
    """
    Output with Workflows' help
    :return: xml of alfred recognized format
    """
     # $suggest->id, $suggest->alt, $suggest->title, '作者: '. implode(",", $suggest->author) .' 评分: '. $suggest->rating->average .'/'. $suggest->rating->numRaters .' 标签: '. implode(",", array_map('get_name', $suggest->tags)), 'C5C34466-B858-4F14-BF5E-FD05FA0903DA.png'
    for value in stocks:
        now = int(value['now'])> 0?value['now'] : '停牌'
        if is_numeric(now):
            change = round((value['now']-value['closing'])/value['closing']*10000)/100
            change = (change > 0 ? '+'.change : change).'%'
        else :
            change = ''
        name   = value['name']
        name   = len(name.decode('utf8') < 4 ? name+'　' : name
        volume = floor(value['volume'] / 100)
        amount = floor(value['amount'] / 10000)
        arg    = "http://finance.sina.com.cn/realstock/company/"+value['type']+value['code']+"/nc.shtml"
        result(md5(name),
               arg,
               '{code}  {name}  {now}  {change}'.format(code=value['code'],name=name,now=now,change=change),
               '量: {volume}手 额: {amount}万 买: {buy} 卖: {sell} 高: {high} 低: {low} 开: {opening} 收: {closing}'.format(volume = volume,amount = amount,buy = value['buy'],sell = value['sell'],high = value['high'],low = value['low'],opening =value['opening'],closing =value['closing']),
               '{type}.png'.format(type = value['type']))

    if count(results()) == 0:
        notice('没能找到相应的股票', '您可能输入了错误的代码，请检查一下吧')
    return toxml()


def add_traversely(code, target, duplicates):
    """
    Add one or more stocks to personal list for the purpose of querying in a single request.
    :param code: comma separated string of code of stock
    :param target:
    :param duplicates:
    :return: system notice center will show the count of successful results.
    """
    result = check_availability(code)
    if not result:
        return False;
    if not in_array(result, target) :
        array_push(target, result)
    else :
        array_push(duplicates, code)


def add(codes_str):
    duplicates = list()
    list = list_ori = read(config)
    list = is_array(list) ? list : array(list)
    codes_arr = explode(",", trim(codes_str))
    if is_array(codes_arr):
        for value in codes_arr:
            add_traversely(trim(value), list, duplicates)
    else :
        add_traversely(codes_str, list, duplicates)
    if list != list_ori or count(duplicates) != 0:
        write(list, config)
        # return array('result'=>true, 'added'=>array_diff(codes_arr, duplicates), 'duplicates'=>duplicates)
        return {'result':True, 'added':array_diff(codes_arr, duplicates), 'duplicates':duplicates}
    else :
        return False

def remove(code):
    """
    Remove one from personal list.
    :param one code of stock
    :return: system notice center will show the notice of success.
    """
    list = read(config)
    if !is_array(list)):
        return False
    for value in list:
        if preg_match('/'.code.'$/', value):
            position = key
            break
    if is_numeric(position):
        array_splice(list, position, 1)
        write(list, config)
        return True
    else
        return False


def show():
    """
    Show all personal stocks with data stored at local
    :return: xml formatted data for alfred
    """
    list = read(config)
    if !is_array(list) or count(list) == 0:
        return False
    get_quotation(implode(",", list))
    return True
def query(chars):
    """
    Query remote server to retrieve data  
    :param chars: a single text word of {list|code|pinyin}
    :return: a xml formatted for alfred
    """
    param_arr = list()
    if chars == 'list':
        if not show():
            notice('您还未添加自选股', '输入 {add+空格+股票代码(多个可以都好分隔)} 添加')
            return toxml()
    elif preg_match('/^\d{6}$/', chars):
        for value in types:
            param_arr.append(value.chars)
        get_quotation(implode(",", param_arr))
    else :
        code = get_code(chars)
        for value in key:
            param_arr.append(value['code'])
        get_quotation(implode(",", param_arr))
    return output()

def operate(cmd, param):
    """
    Operates the personal list as a shortcut
    :param {add codes|remove code}
    :return: show result directly
    """
    if cmd in ['add','remove']:
        notice('目前仅支持: ', 'add 股票代码,... - 添加到自选; remove 股票代码 - 从自选股删除; list - 显示自选股')
    else
        param = filter_code(trim(param))
        if param:
            switch (cmd) {
                case 'add':
                    if result = add(param):
                        tmp_str = ""
                        if count(result['added']):
                            tmp_str .= implode(",", result['added']).' 已添加到自选股 '
                        if count(result['duplicates']):
                            tmp_str .= implode(",", result['duplicates'])." 重复了"
                        notice(tmp_str)
                    else :
                        notice('输入的代码有误，请检查')
                    break
                case 'remove':
                    if this->remove($param):
                        notice('移除 '.param.' 成功')
                    else :
                        notice(param.' 不在您的自选列表中')
                    break
                default:
                    notice('目前仅支持: ', 'add 股票代码,... - 添加到自选; remove 股票代码 - 从自选股删除; list - 显示自选股')
            }
        else
            notice('您暂时只能通过股票代码进行操作')
    if count(results())>0:
        return toxml()


def controller(args):
    """
    Get input characters while user typing and choose correct function to deal with
    :param args: could be a stock code or a short form of a company's name
    :return: xml formatted data for alfred showing
    """
    chars = sys.argv[1]
    querystring = preg_split('/\s+/', trim(stripslashes(chars)))
    if count(querystring) == 1:
        return query(querystring[0])
    else:
        return operate(querystring[0], querystring[1])

def main(wf):
    key = wf.args
    resp = curl(key)
    # d = data['HeWeather data service 3.0'][0]
    # city = d['basic']['city']

    # 获取一周内的数据
    # for n in range(0, 7):
    for r in resp:

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
    # curl('ta')
