# encoding: utf-8
# Auther: zhoubowen.929
# Created At: 周一 07 八月 2023 15:12:07 CST
# MagIc C0de: 1d7f6334161b

import pandas as pd

def dataframe_to_markdown(df,extra_info = None):
    # 将数据帧转换为 Markdown 表格格式
    markdown = extra_info + '\n' if extra_info is not None else ""
    markdown += '|' + '|'.join(df.columns) + '|\n'
    markdown += '|' + '|'.join(['---']*len(df.columns)) + '|\n'

    for row in df.itertuples(index=False):
        markdown += '|' + '|'.join(str(elem) for elem in row) + '|\n'

    return markdown

if __name__ == '__main__':
    test_dict = {
        "index": ["index1", "index2"],
        "value": ["value1", "value2"]
    }
    pandas_df = pd.DataFrame.from_dict(test_dict)
    ans = dataframe_to_markdown(pandas_df)
    print(ans)