import requests

def get_watchlist_data(watch_list):
    import requests

    url = "https://apidojo-yahoo-finance-v1.p.rapidapi.com/market/get-watchlist-detail"

    querystring = {"userId":"X3NJ2A7VDSABUI4URBWME2PZNM","pfId":watch_list}

    headers = {
        'x-rapidapi-key': "fbf7be51famsh81db55c838a3d9ap179540jsn1ce7839c393c",
        'x-rapidapi-host': "apidojo-yahoo-finance-v1.p.rapidapi.com"
        }

    response = requests.request("GET", url, headers=headers, params=querystring)

    return response.json()['finance']['result'][0]['quotes']


def get_stock_data_list(symbol):
    url = "https://apidojo-yahoo-finance-v1.p.rapidapi.com/stock/v3/get-historical-data"

    querystring = {"symbol": symbol, "region": "US"}

    headers = {
        'x-rapidapi-key': "fbf7be51famsh81db55c838a3d9ap179540jsn1ce7839c393c",
        'x-rapidapi-host': "apidojo-yahoo-finance-v1.p.rapidapi.com"
    }

    response = requests.request("GET", url, headers=headers, params=querystring)
    data_list = response.json()['prices']
    return data_list

def get_price_list(data_list, count):
    price_list = list()
    # print(len(data_list))
    for data in data_list:
        if (count == 0):
            break
        # print(data)
        try:
            # print('count = ' + str(50 - count) + '| ' + str(data['close']))
            price_list.append(data['close'])
        except:
            continue
        count = count - 1
    return price_list

def get_price_back_to(price_list, n):
    return price_list[n]

def get_EM_n_on_the_day(price_list, n, the_day):
    sum = 0
    for i in range(n):
        sum = sum + price_list[the_day + i]
    return sum / n

def get_EM_n_line_for_previous_days(price_list, n, days):
    lst = list()
    for i in range(days):
        em = get_EM_n_on_the_day(price_list, n, i)
        lst.append(em)
    return lst

def get_weighted_EM_slope_for_one_line(line):
    import math
    sum = 0
    for i in range(len(line) - 1):
        weight = math.exp(len(line) - 1 - i)
        sum = sum + ((line[i] - line[i + 1]) / line[i + 1]) * weight
    return sum

def get_weighted_EM_slope_for_all_lines(line_0, line_1, line_2):
    import math
    s0 = get_weighted_EM_slope_for_one_line(line_0)
    s1 = get_weighted_EM_slope_for_one_line(line_1)
    s2 = get_weighted_EM_slope_for_one_line(line_2)
    return math.exp(2) * s0 + math.exp(1) * s1 + math.exp(0) * s2

def dispersion_on_the_day(a, b, c):
    dispersion_sum = (abs(a - b) / min(a, b) + abs(b - c) / min(b, c) + abs(a - c) / min(a, c))
    return dispersion_sum

def dispersion_for_previous_days(line_0, line_1, line_2, days):
    sum = 0
    for i in range(days):
        # print(str(line_0[i]) + ' | ' +  str(line_1[i]) + ' | ' + str(line_2[i]))
        dispersion = dispersion_on_the_day(line_0[i], line_1[i], line_2[i])
        sum = sum + dispersion
        # print('dispersion = ' + str(dispersion))
        # print()
    return sum

def sort_value_for_dict(dict, reverse):
    return {k: v for k, v in sorted(dict.items(), key=lambda item: item[1], reverse = reverse)}

def check_increasing_for_line(line):
    for i in range(len(line) - 1):
        if (line[i] < line[i + 1]):
            return False
    return True

def get_EM_lines(continuous_days, symbol):
    data_list = get_stock_data_list(symbol)
    if (len(data_list) < 50):
        print('Length is small!')
        return None
    price_list = get_price_list(data_list, 50)


    em_3_line = get_EM_n_line_for_previous_days(price_list, 3, continuous_days)
    if (check_increasing_for_line(em_3_line) == False):
        print('EM line is not increase!')
        return None
    em_10_line = get_EM_n_line_for_previous_days(price_list, 10, continuous_days)
    if (check_increasing_for_line(em_10_line) == False):
        print('EM line is not increase!')
        return None
    em_20_line = get_EM_n_line_for_previous_days(price_list, 20, continuous_days)
    if (check_increasing_for_line(em_20_line) == False):
        print('EM line is not increase!')
        return None
    return (em_3_line, em_10_line, em_20_line)

def my_main(continuous_days, lines):

    em_3_line = lines[0]
    em_10_line = lines[1]
    em_20_line = lines[2]

    dispersion_sum = dispersion_for_previous_days(em_3_line, em_10_line, em_20_line, continuous_days)
    print(dispersion_sum)
    slope_sum = get_weighted_EM_slope_for_all_lines(em_3_line, em_10_line, em_20_line)
    print('slope_sum = ' + str(slope_sum))
    return (slope_sum, dispersion_sum)

def read_file(file_name):
    f = open(file_name)
    lines = f.readlines()
    parsed_lines = []
    for line in lines:
        parsed_lines.append(str.strip(line))
    return parsed_lines


def get_final_scores(a, b):
    final_dict = {}
    length = len(a)
    count = length
    for symbol in a:
        if symbol not in final_dict:
            final_dict[symbol] = 0
        final_dict[symbol] = final_dict[symbol] + count * 1.1
        count = count - 1

    count = length
    for symbol in b:
        if symbol not in final_dict:
            final_dict[symbol] = 0
        final_dict[symbol] = final_dict[symbol] + count
        count = count - 1
    res = sort_value_for_dict(final_dict, True)
    print(res)
    return res

# ---------------------------------------------------------
                    # Main
# ---------------------------------------------------------

# read watchlist:
def parse_name(s):
    s = s.lower()
    s = s.replace(' ', '_')
    return s
watch_list = 'E_commerce Stocks'

symbols = get_watchlist_data(parse_name(watch_list))

# read watchlist:
# watch_list = 'stocks.txt'
# symbols = read_file(watch_list)


slope_dict = {}
dispersion_dict = {}
count = len(symbols)
file = open(watch_list + '_analysis.txt', 'w')


for symbol in symbols:
    try:
        print('Symbols number left = ' + str(count))
        count = count - 1
        print(symbol)
        lines = get_EM_lines(3, symbol)
        if (lines == None):
            print('-----------------------------------------------')
            continue
        analysis = my_main(3, lines)

        slope_sum = analysis[0]
        slope_dict[symbol] = slope_sum

        dispersion = analysis[1]
        dispersion_dict[symbol] = dispersion
        print('-----------------------------------------------')
    except:
        continue

slope_scores = sort_value_for_dict(slope_dict, True)
dispersion_scores = sort_value_for_dict(dispersion_dict, False)
print(slope_scores)
print(dispersion_scores)
file.write('Increasing rate rank: ' + str(slope_scores) + '\n')
file.write('EM lines dispersion rate rank: ' + str(dispersion_scores) + '\n')
file.write('Final scores:' + '\n')
res = get_final_scores(slope_scores, dispersion_scores)
for a in res:
    file.write(str(a) + ': ' + str(res[a]) + '\n')


