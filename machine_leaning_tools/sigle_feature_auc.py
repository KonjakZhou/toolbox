# encoding: utf-8
# Auther: zhoubowen.929
# Created At: Mon 28 November 2022 19:39:17 CST
# MagIc C0de: 3087753610bc

import pandas as pd

BUCKET_NUMS = 16
feature_enumerate_col_list = [

]

feature_continuous_col_list = [

]

def compute_single_feature_auc(pos_sample_feature_proportion_list, neg_sample_feature_proportion_list):
    """
    计算单特征auc
    :param pos_sample_feature_proportion_list: list of feature_proportion in pos samples
    :param neg_sample_feature_proportion_list: list of feature_proportion in neg samples
    """
    total_count = len(pos_sample_feature_proportion_list) * len(neg_sample_feature_proportion_list)
    if total_count == 0:
        return 0
    
    compare_score = 0
    for pos_proportion in pos_sample_feature_proportion_list:
        for neg_proportion in neg_sample_feature_proportion_list:
            if pos_proportion > neg_proportion:
                compare_score += 1.0
            elif pos_proportion == neg_proportion:
                compare_score += 0.5
            else:   # pos_proportion < neg_proportion:
                pass

    auc_score = compare_score / total_count
    return auc_score

def get_enumerate_feature_proportion_dict(train_df, feature_col, label_col="label"):
    """
    获得离散特征列的各类别的占比字典
    """
    train_df_groupby = train_df.groupby(feature_col)
    ans_dict = dict()
    for col_value, tmp_df in train_df_groupby:
        total_count = len(tmp_df)
        postive_count = len(tmp_df[tmp_df[label_col]==1])
        ans_dict[col_value] = float(postive_count)/total_count

    return ans_dict

def get_enumerate_feature_proportion_col(feature_col_series, porportion_dict):
    """
    根据各枚举值占比字典获取离散特征列的分布列
    """
    return feature_col_series.apply(lambda x: porportion_dict.get(x))

def get_continuous_feature_proportion_dict(train_df, feature_col, label_col="label"):
    """
    获得连续特征列的各个区间的占比字典
    """
    train_df_groupby = train_df.groupby(pd.qcut(train_df[feature_col], q=BUCKET_NUMS, duplicates='drop'))

    ans_dict = dict()
    for col_range, tmp_df in train_df_groupby:
        total_count = len(tmp_df)
        postive_count = len(tmp_df[tmp_df[label_col]==1])
        ans_dict[col_range] = float(postive_count)/total_count
    
    return ans_dict

def get_continuous_feature_proportion_col(feature_col_series, proportion_dict):
    """
    根据各分箱占比字典获取连续特征列的分布列
    """
    intervals = pd.IntervalIndex(list(proportion_dict.keys()))
    ans_series = pd.cut(feature_col_series, intervals)
    return ans_series.apply(lambda x: proportion_dict.get(x))

def main():
    train_df_dir = ""
    test_df_dir = ""

    train_df = pd.read_csv(train_df_dir)
    test_df = pd.read_csv(test_df_dir)

    # 获取训练集正样本中的列分布，并为测试集增加分布列
    feat_proportion_dict = {}
    for col_enum in feature_enumerate_col_list:
        feat_proportion_dict[col_enum] = get_enumerate_feature_proportion_dict(train_df[[col_enum, "label"]], col_enum)
        test_df[col_enum + "proportion"] = get_enumerate_feature_proportion_col(test_df[col_enum], feat_proportion_dict[col_enum])

    for col_enum in feature_continuous_col_list:
        feat_proportion_dict[col_enum] = get_continuous_feature_proportion_dict(train_df[[col_enum, "label"]], col_enum)
        test_df[col_enum + "proportion"] = get_continuous_feature_proportion_col(test_df[col_enum], feat_proportion_dict[col_enum])

    # 计算测试集中各列的单特征auc
    test_pos_df = test_df[test_df["label"] == 1]
    test_neg_df = test_df[test_df["label"] == 0]
    single_feature_auc_dict = {}
    for col_enum in feature_enumerate_col_list + feature_continuous_col_list:
        single_feature_auc_dict[col_enum] = \
        compute_single_feature_auc(test_pos_df[col_enum + "proportion"].tolist(), test_neg_df[col_enum + "proportion"].tolist())
    
    print(single_feature_auc_dict)

if __name__ == '__main__':
    main()