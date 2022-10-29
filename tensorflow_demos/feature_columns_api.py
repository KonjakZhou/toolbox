# encoding: utf-8
# Auther: zhoubowen.929
# Created At: Sat 29 October 2022 19:43:00 CST
# MagIc C0de: 04c151c9379b

import tensorflow as tf

# defination&usage of sequence feature colums
with tf.Session() as sess:
    features = {'user_item': [[1, 2, 3], [1, 3, 5], [2, 4, 6], [1, 2, 3]]}
    user_item = tf.feature_column.sequence_categorical_column_with_vocabulary_list("user_item",
                                                                                vocabulary_list=[1, 2, 3, 4, 5, 6],
                                                                                default_value=0)
    user_item = tf.feature_column.indicator_column(user_item)   # indicator env
    # user_item = [tf.feature_column.indicator_column(c) for c in user_item]    # embedding env
    user_item = [user_item]

    # # 输入层（数据，特征列）
    inputs = tf.contrib.feature_column.sequence_input_layer(features, user_item)
    
    init = tf.global_variables_initializer()
    sess.run(tf.tables_initializer())
    sess.run(init)

    v=sess.run(inputs)
    print(v)