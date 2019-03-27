import tensorflow as tf
import numpy as np
from datetime import datetime
import os
import pdb

# https://www.tensorflow.org/tutorials/estimators/cnn

def main():
    # Load training and eval data
    timestamp('Read in data')
    data_dir = '/Users/user/Code/midtown-rain/data/processed'
    train_data = np.load(os.path.join(data_dir, 'train_data.pkl'))
    train_labels = np.load(os.path.join(data_dir, 'train_labels.pkl'))
    eval_data = np.load(os.path.join(data_dir, 'cv_data.pkl'))
    eval_labels = np.load(os.path.join(data_dir, 'cv_labels.pkl'))

    # Reshape
    train_labels = train_labels.reshape(train_labels.size, 1)
    eval_labels = eval_labels.reshape(eval_labels.size, 1)

    # Set data types
    train_labels = train_labels.astype(np.int32)
    eval_labels = eval_labels.astype(np.int32)
    train_data = train_data/np.float32(255)
    eval_data = eval_data/np.float32(255)

    # Create the Estimator
    timestamp('Initialize estimator')
    classifier = tf.estimator.Estimator(
        model_fn=cnn_model_fn,
        model_dir="/Users/user/Code/midtown-rain/models/cnn")
    # Model output to directory in above argument

    # Set up logging for predictions
    tensors_to_log = {"probabilities": "softmax_tensor"}
    
    logging_hook = tf.train.LoggingTensorHook(
        tensors=tensors_to_log, every_n_iter=1)

    # Train the model
    timestamp('Train model')
    train_input_fn = tf.estimator.inputs.numpy_input_fn(
        x={"x": train_data},
        y=train_labels,
        batch_size=10,
        num_epochs=None,
        shuffle=True)
    
    # Train and display the probabilties
    classifier.train(input_fn=train_input_fn, steps=10)

    # Evaluate results
    timestamp('Evaluate model')
    eval_input_fn = tf.estimator.inputs.numpy_input_fn(
        x={"x": eval_data},
        y=eval_labels,
        num_epochs=1,
        shuffle=False)
    
    eval_results = classifier.evaluate(input_fn=eval_input_fn)
    print(eval_results)

    timestamp('Done!')
    
def cnn_model_fn(features, labels, mode):
  """Model function for CNN."""

  IMG_WD = 960
  IMG_HT = 540
  KS1 = [5, 5]  # kernal size
  S1 = 5        # set large stride in order to effectively downsample image
  KS2 = [5, 5]
  S2 = 1
  CN1 = 5  # nodes in convolution layer
  CN2 = 5
  DN = 8   # nodes in dense layer
  POOL_SIZE = [2, 2]
  POOL_STRIDE = 2

  # Input Layer
  # Set arguments for dimensions of the images (rows x cols)
  input_layer = tf.reshape(features["x"], [-1, IMG_HT, IMG_WD, 1])

  # Convolutional Layer #1
  # Specifies the convolutions over the 540x960 tensor
  conv1 = tf.layers.conv2d(
  # conv1 = tf.keras.layers.Conv2D(
      inputs=input_layer,
      filters=CN1,  # number of nodes in layer
      kernel_size=KS1,  # dims of filter
      strides=S1,
      padding="same",
      activation=tf.nn.relu)

  # Pooling Layer #1
  pool1 = tf.layers.max_pooling2d(inputs=conv1, pool_size=POOL_SIZE, strides=POOL_STRIDE)
  # pool1 = tf.keras.layers.Max_pooling2d(inputs=conv1, pool_size=POOL_SIZE, strides=POOL_STRIDE)

  # Convolutional Layer #2 and Pooling Layer #2
  # Specifies the filters with ReLU activation
  conv2 = tf.layers.conv2d(
  # conv2 = tf.keras.layers.Conv2D(
      inputs=pool1,
      filters=CN2,
      kernel_size=KS2,
      strides=S2,
      padding="same",
      activation=tf.nn.relu)

  # Pooling Layer #2
  pool2 = tf.layers.max_pooling2d(inputs=conv2, pool_size=POOL_SIZE, strides=POOL_STRIDE)
  # pool2 = keras.layers.max_pooling2d(inputs=conv2, pool_size=POOL_SIZE, strides=POOL_STRIDE)

  # Dense Layer
  feature_count = (IMG_HT / S1 / POOL_STRIDE ** 2) * (IMG_WD / S1 / POOL_STRIDE ** 2) * CN2
  pool2_flat = tf.reshape(pool2, [-1, feature_count])
  dense = tf.layers.dense(inputs=pool2_flat, units=DN, activation=tf.nn.relu)
#  dense = tf.keras.layers.dense(inputs=pool2_flat, units=DN, activation=tf.nn.relu)
  dropout = tf.layers.dropout(
#  dropout = tf.keras.layers.dropout(
      inputs=dense, rate=0.4, training=mode == tf.estimator.ModeKeys.TRAIN)

  # Logits Layer for binary classification
  logits = tf.layers.dense(inputs=dropout, units=1)

  predictions = {
      # Generate predictions (for PREDICT and EVAL mode)
      "classes": tf.argmax(input=logits, axis=1),
      # Add `softmax_tensor` to the graph. It is used for PREDICT and by the
      # `logging_hook`.
      "probabilities": tf.nn.softmax(logits, name="softmax_tensor")
  }

  if mode == tf.estimator.ModeKeys.PREDICT:
    return tf.estimator.EstimatorSpec(mode=mode, predictions=predictions)

  # Calculate Loss (for both TRAIN and EVAL modes)
  # Use sigmoid loss function for binary classification
  loss = tf.losses.sigmoid_cross_entropy(multi_class_labels=labels, logits=logits)
  # loss = tf.losses.sparse_softmax_cross_entropy(labels=labels, logits=logits)

  # Configure the Training Op (for TRAIN mode)
  if mode == tf.estimator.ModeKeys.TRAIN:
    optimizer = tf.train.GradientDescentOptimizer(learning_rate=0.001)
    train_op = optimizer.minimize(
        loss=loss,
        global_step=tf.train.get_global_step())
    return tf.estimator.EstimatorSpec(mode=mode, loss=loss, train_op=train_op)

  # Add evaluation metrics (for EVAL mode)
  eval_metric_ops = {
      "accuracy": tf.metrics.accuracy(
          labels=labels, predictions=predictions["classes"]),
      "precision": tf.metrics.precision(
          labels=labels, predictions=predictions["classes"]),
      "recall": tf.metrics.recall(
          labels=labels, predictions=predictions["classes"])
  }
  return tf.estimator.EstimatorSpec(
      mode=mode, loss=loss, eval_metric_ops=eval_metric_ops)

def timestamp(display_str=''):
    time_str = datetime.now().strftime('%H:%M:%S')
    if display_str:
        print(time_str + ': ' + display_str)
    else:
        print(time_str)

if __name__ == '__main__':
    main()
