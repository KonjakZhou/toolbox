# encoding: utf-8
# Auther: zhoubowen.929
# Created At: Sat 29 October 2022 19:43:00 CST
# MagIc C0de: 04c151c9379b

import tensorflow as tf

with tf.Session() as sess:
    features = {
        'department': [[1,2,3], [4,5,6], [1,1,1]],
    }

    boundaries = [1.5,2.5,3.5,4.5,5.5]
    department = tf.feature_column.numeric_column('department', dimension=3, dtype=tf.float32)
    department = tf.feature_column.bucketized_column(department, boundaries)
    
    columns = [
        department
    ]

    #输入层（数据，特征列）
    inputs = tf.feature_column.input_layer(features, columns)
    inputs = tf.stack(tf.split(inputs, 3, axis = 1), axis = 1)

    #初始化并运行
    init = tf.global_variables_initializer()
    sess.run(tf.tables_initializer())
    sess.run(init)

    v=sess.run(inputs)
    print(v)

# defination&usage of sequence feature colums
# 序列类特征的定义与使用
with tf.Session() as sess:
    features = {'user_item': [[1, 2, 3], [1, 3, 5], [2, 4, 6], [1, 2, 3]]}
    user_item = tf.feature_column.sequence_categorical_column_with_vocabulary_list("user_item",
                                                                                vocabulary_list=[1, 2, 3, 4, 5, 6],
                                                                                default_value=0)
    user_item = tf.feature_column.indicator_column(user_item)
    user_item = [user_item]

    # # 输入层（数据，特征列）
    inputs = tf.contrib.feature_column.sequence_input_layer(features, user_item)
    
    init = tf.global_variables_initializer()
    sess.run(tf.tables_initializer())
    sess.run(init)

    v=sess.run(inputs)
    print(v)