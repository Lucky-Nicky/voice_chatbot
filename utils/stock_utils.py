import baostock as bs
import pandas as pd
from datetime import datetime, timedelta


def get_hs300_stocks():
    """获取沪深300的成分股票"""
    lg = bs.login()

    # 获取沪深300成分股
    rs = bs.query_hs300_stocks()

    hs300_stocks = []
    while (rs.error_code == '0') & rs.next():
        # 获取一条记录，将记录合并在一起
        hs300_stocks.append(rs.get_row_data())

    # 登出系统
    bs.logout()
    return pd.DataFrame(hs300_stocks, columns=rs.fields)


def get_k_data_plus(code, start, end):
    """获取股票的K线数据"""

    lg = bs.login()
    rs = bs.query_history_k_data_plus(code,
                                      "date,code,open,high,low,close,volume,amount",
                                      start_date=start, end_date=end,
                                      frequency="d", adjustflag="3")

    data_list = []
    while (rs.error_code == '0') & rs.next():
        # 获取一条记录，将记录合并在一起
        data_list.append(rs.get_row_data())

    bs.logout()

    return pd.DataFrame(data_list, columns=rs.fields)


def get_k_data_before_days(code, before_days):
    """获取今天以前before_days天数的数据"""
    cur_datetime = datetime.now()
    yesterday = (cur_datetime - timedelta(days=1)).strftime("%Y-%m-%d")
    day_date = (cur_datetime - timedelta(days=before_days)).strftime("%Y-%m-%d")
    return get_k_data_plus(code, start=day_date, end=yesterday)


def get_stock_cashes(code):
    # 登陆系统
    lg = bs.login()
    curr_year = int(datetime.now().strftime("%Y"))
    df_list = []
    for year in range(curr_year - 5, curr_year + 1):
        for quarter in [1, 2, 3, 4]:
            # 季频现金流量
            cash_flow_list = []
            rs_cash_flow = bs.query_cash_flow_data(
                code=code, year=year, quarter=quarter)
            try:
                while (rs_cash_flow.error_code == '0') & rs_cash_flow.next():
                    cash_flow_list.append(rs_cash_flow.get_row_data())
            except:
                continue
            result_cash_flow = pd.DataFrame(cash_flow_list, columns=rs_cash_flow.fields)
            df_list.append(result_cash_flow)

    # 登出系统
    bs.logout()
    df_all = pd.concat(df_list)
    no_data_columns = ["CAToAsset", "NCAToAsset", "tangibleAssetToAsset", "ebitToInterest"]
    df_all = df_all[[x for x in df_all.columns if x not in no_data_columns]]
    return df_all


if __name__ == "__main__":
    # stocks = get_hs300_stocks()
    # print(stocks)

    # stock = get_k_data_plus(
    #    "sh.600000", start="2023-03-10", end="2023-04-04")
    # print(stock)
    # print(get_k_data_before_days("sh.600000", 30).to_string())
    print(get_stock_cashes("sh.600000"))
