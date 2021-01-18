from gen_Data_build_model import *
import numpy as np
import tensorflow as tf
from tensorflow import keras
from tensorflow.python.keras import Model
from tensorflow.python.keras.layers import LSTM, Dense, Dropout, Embedding
from tensorflow.python.keras import callbacks as tf_cb



def build_model(max_features, maxlen):
    """Build LSTM model"""
    model = Sequential()
    model.add(Embedding(max_features, 128, input_length=maxlen))
    model.add(LSTM(128))
    model.add(Dropout(0.5))
    model.add(Dense(1))
    model.add(Activation('sigmoid'))

    model.compile(loss='binary_crossentropy',
                  optimizer='rmsprop')
    return model

def lstm(in_dim, in_shape,batch_Size):
    model = keras.models.Sequential([
        Embedding(in_dim, 128, input_length=in_shape,batch_size = batch_Size),
        LSTM(128),
        Dropout(0.15),
        Dense(1, activation='sigmoid'),

    ])
    return model

def callb(path_checkpoint):
    callback_checkpoint = tf_cb.ModelCheckpoint(
        filepath=path_checkpoint, monitor = 'loss', verbose=1,
        save_weights_only=True, save_best_only=True)

    callback_earlystopping = tf_cb.EarlyStopping(monitor='loss',
                                                 patience=20, verbose=1)
    callback_reduce_lr = tf_cb.ReduceLROnPlateau(monitor='loss',
                                                 factor=0.98,
                                                 min_lr=0.3e-4,
                                                 patience=0,
                                                 verbose=1)
    callBacks = [
        callback_checkpoint,
        callback_earlystopping,
        callback_reduce_lr
    ]
    return callBacks

def load_data(data_file):
    indata = pickle.load(open(data_file, 'rb'))
    print('DGA load successfully')
    X = [x[1] for x in indata]
    labels = [x[0] for x in indata]

    # Generate a dictionary of valid characters
    valid_char_dict = {x: idx + 1 for idx, x in enumerate(set(''.join(X)))}

    max_features = len(valid_char_dict) + 1
    maxlen = np.max([len(x) for x in X])

    print('maxlen:', maxlen)
    # Convert characters to int and pad
    X = [[valid_char_dict[y] for y in x] for x in X]
    X = sequence.pad_sequences(X, maxlen=maxlen)

    # Convert labels to 0-1
    y = [0 if x == 'benign' else 1 for x in labels]
    print('data preprocessing finished')
    return X, y, valid_char_dict

if __name__ == '__main__':
    tf.random.set_seed(777)
    gpus = tf.config.experimental.list_physical_devices('GPU')
    for gpu in gpus:
        tf.config.experimental.set_memory_growth(gpu, True)


    X, y, DGA_char = load_data('traindata.pkl')
    print(X.shape)
    Batch_Size = 128
    Epochs=150
    features = len(DGA_char) + 1
    length = X.shape[1]

    ## not using batch func
    end_point = len(X)//Batch_Size * Batch_Size
    n_batch = end_point/Batch_Size
    X, y = X[:end_point,:], y[:end_point]
    ds_split = int(n_batch*0.88)*Batch_Size
    trn_x, tst_x = X[:ds_split,:], X[ds_split:,:]
    trn_y, tst_y = np.array(y[:ds_split]), np.array(y[ds_split:])


    ### using batch func
    # ds_split = int(len(X)*0.88)
    # trn_x,tst_x = X[:ds_split,:], X[ds_split:,:]
    # trn_y, tst_y = np.array(y[:ds_split]), np.array(y[ds_split:])
    # trn_ds = tf.data.Dataset.from_tensor_slices((trn_x, trn_y))
    # tst_ds = tf.data.Dataset.from_tensor_slices((tst_x, tst_y))
    # trn_ds = trn_ds.batch(Batch_Size, drop_remainder=True)
    # tst_ds = tst_ds.batch(Batch_Size, drop_remainder=True)
    print('start  training')

    model = lstm(features,length,Batch_Size)
    model.compile(loss='binary_crossentropy',optimizer=keras.optimizers.RMSprop(learning_rate=1e-4),metrics=['accuracy'])
    callbacks = callb(path_checkpoint='./lstm.tf')
    hist = model.fit(trn_x, trn_y,epochs=Epochs,
                     batch_size=Batch_Size,
                     verbose=1, shuffle=True,
                     validation_data=(tst_x, tst_y),
                     callbacks=callbacks,
                    )

    # model.fit(trn_ds,epochs=Epochs,
    #           # batch_size=Batch_Size,
    #           verbose=1, shuffle=True,
    #           validation_data=tst_ds,
    #           )