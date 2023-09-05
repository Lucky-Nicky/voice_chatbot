import baostock as bs
import pandas as pd

# 登陆系统
lg = bs.login()
# 显示登陆返回信息
print('login respond error_code:'+lg.error_code)
print('login respond  error_msg:'+lg.error_msg)

df_list = []
for year in range(2019, 2024):
    for quarter in [1, 2, 3, 4]:
        # 查询季频估值指标盈利能力
        profit_list = []
        rs_profit = bs.query_profit_data(code="sh.600000", year=year, quarter=quarter)
        while (rs_profit.error_code == '0') & rs_profit.next():
            profit_list.append(rs_profit.get_row_data())
        result_profit = pd.DataFrame(profit_list, columns=rs_profit.fields)
        df_list.append(result_profit)

df_merge = pd.concat(df_list)
print(df_merge.to_string())

# 登出系统
bs.logout()