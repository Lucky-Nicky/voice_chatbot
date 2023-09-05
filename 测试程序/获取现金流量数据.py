import baostock as bs
import pandas as pd

# 登陆系统
lg = bs.login()
# 显示登陆返回信息
print('login respond error_code:' + lg.error_code)
print('login respond  error_msg:' + lg.error_msg)

df_list = []
for year in range(2019, 2024):
    for quarter in [1, 2, 3, 4]:
        # 季频现金流量
        cash_flow_list = []
        rs_cash_flow = bs.query_cash_flow_data(
            code="sh.600000", year=year, quarter=quarter)
        while (rs_cash_flow.error_code == '0') & rs_cash_flow.next():
            cash_flow_list.append(rs_cash_flow.get_row_data())
        result_cash_flow = pd.DataFrame(cash_flow_list, columns=rs_cash_flow.fields)
        df_list.append(result_cash_flow)
    # 打印输出
# 结果集输出到csv文件
# result_cash_flow.to_csv("D:\\cash_flow_data.csv", encoding="gbk", index=False)
df_merge = pd.concat(df_list)
print(df_merge.to_string())

# 登出系统
bs.logout()
