# encoding: utf-8
# Auther: zhoubowen.929
# Created At: 周一 07 八月 2023 18:07:07 CST
# MagIc C0de: f655eaf3ad99
import tensorflow as tf

def bi_lstm(input_embs, input_lengths, lstm_hidden_dim, lstm_layers_num=1, name = None):
        lstm_inputs = input_embs
        with tf.variable_scope(name + "bi_lstm" if name is not None else "bi_lstm"):
            
            for i in range(lstm_layers_num):
                lstm_cell_fw = tf.contrib.rnn.LSTMCell(lstm_hidden_dim, name = "fw_layer_{:d}".format(i))
                lstm_cell_bw = tf.contrib.rnn.LSTMCell(lstm_hidden_dim, name = "bw_layer_{:d}".format(i))
                (outputs, states) = tf.nn.bidirectional_dynamic_rnn(
                    cell_fw=lstm_cell_fw,
                    cell_bw=lstm_cell_bw,
                    inputs=lstm_inputs, 
                    sequence_length=input_lengths,
                    dtype=tf.float32
                    )
                lstm_inputs = tf.concat(outputs, axis = -1, name="layer_{:d}_input".format(i+1))
            concated_output = tf.concat(outputs, axis = -1, name = "layer_output")
        return outputs, states, concated_output

if __name__ == '__main__':
    input_list = [
        [
            [1, 1],
            [1, 2],
            [1, 3],      
        ],
        [
            [2, 1],
            [2, 2],
            [2, 0]
        ],
    ]   # [BS, SL, Dim]

    input_length = [3, 2]

    input_tf = tf.Variable(input_list, dtype=tf.float32)
    input_length_tf = tf.Variable(input_length)
    _, _, concated_output = bi_lstm(input_embs = input_tf, input_lengths = input_length_tf, lstm_hidden_dim = 32, lstm_layers_num=1)
    print(concated_output)   # [BS, SL, DIM*2]

    pass