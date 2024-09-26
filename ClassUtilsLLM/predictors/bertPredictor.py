import numpy as np
import tensorflow as tf
from transformers import BertTokenizer, TFBertForSequenceClassification
from sklearn.utils.class_weight import compute_class_weight
from sklearn.metrics import classification_report
import matplotlib.pyplot as plt

class BertPredictor():
  def __init__(self,num_labels,verbose=True):
    # Carregar o tokenizador e o modelo pré-treinado BERT
    self.tokenizer = BertTokenizer.from_pretrained('bert-base-uncased')
    self.model = TFBertForSequenceClassification.from_pretrained('bert-base-uncased', num_labels=num_labels)
    self.verbose = verbose
  def compile(self,
                  optimizer=tf.keras.optimizers.legacy.Adam(learning_rate=3e-5),
                  loss=tf.keras.losses.SparseCategoricalCrossentropy(from_logits=True),
                  metrics=[tf.keras.metrics.SparseCategoricalAccuracy()]):
    """
    Compilation function
    Args:
      optimizer [default = tf.keras.optimizers.legacy.Adam(learning_rate=3e-5)]
      loss [default = tf.keras.losses.SparseCategoricalCrossentropy(from_logits=True)]
      metrics [default = [tf.keras.metrics.SparseCategoricalAccuracy()])]
    """
    self.model.compile(optimizer=optimizer, loss=loss, metrics=metrics)
    if self.verbose:self.model.summary()
  def __preprocess__(self,texts,labels=None,max_length=128):
    """
    Function to do the preprocess step, applying tokenization
    
    Args:
      texts:list[str]
      labels:list[int] [default = None] - text labels
      max_length:int - parameter of tokenization
  
    Returns:
      inputs_ids - tf inputs ids
      attention_masks - tf attention masks
    """
    input_ids = []
    attention_masks = []
    for text in texts:
        encoded_dict = self.tokenizer.encode_plus(
                            text,
                            add_special_tokens = True,
                            max_length = max_length,
                            padding = True,
                            return_attention_mask = True,
                            return_tensors = 'tf',
                       )
        input_ids.append(encoded_dict['input_ids'])
        attention_masks.append(encoded_dict['attention_mask'])

    input_ids = tf.concat(input_ids, axis=0)
    attention_masks = tf.concat(attention_masks, axis=0)

    if labels is not None:
      labels = tf.convert_to_tensor(labels)
      return input_ids, attention_masks, labels
    return input_ids,attention_masks
  
  def fit(self,X,Y,
          epochs=10,
          batch_size=8,
          callbacks = [
              tf.keras.callbacks.EarlyStopping(monitor='sparse_categorical_accuracy', patience=9),
              tf.keras.callbacks.ReduceLROnPlateau(monitor='sparse_categorical_accuracy', factor=0.07, patience=3)
          ],
          validation_data = None# colocar como [X,Y]
          ):
    """
    Finetuning function
    
    Args:
      X:list[str] - data to training
      Y:list[int] - labels of data
      epochs:int - number of epochs
      batch_size:int - batch size
      callbacks:list [default = [EarlyStopping, ReduceLROnPlateau]] - list of callback events
      validation_data:tuple(X,Y) [default=None] - put X and Y validation data if you want
    
    Returns:
      history - the history of the training
    """

    train_input_ids,train_attention_masks,train_labels = self.__preprocess__(X,Y)

    if validation_data is not None:
      run_with_validation = True
      test_input_ids, test_attention_masks,test_labels = self.__preprocess__(validation_data[0],validation_data[1])
    else:
      run_with_validation = False

    class_weights = compute_class_weight('balanced', classes=np.unique(train_labels), y=train_labels.numpy())
    self.class_weights_dict = dict(enumerate(class_weights))
    
    self.history = self.model.fit(
        [train_input_ids, train_attention_masks],
        train_labels,
        validation_data= None if not run_with_validation else ([test_input_ids, test_attention_masks], test_labels),
        epochs=epochs,  # Número de épocas
        batch_size=batch_size,  # Tamanho do lote
        callbacks=callbacks,
        class_weight=self.class_weights_dict
    )
    return self.history

  @staticmethod
  def plot_history(history):
    """
    Plot the history of training
    Args:
      history - the history of fit process
    """
    for key in history.history.keys():
      plt.plot(history.history[key], label=key)
    plt.legend()
    plt.show()
  
  def predict(self,X):
    """
    Predict function
    
    Args:
      X:list[str] - text data to predict labels
    
    Returns:
      predicted_labels:list[int] - predicted labels 
    """
    input_ids, attention_masks = self.__preprocess__(X)
    predictions = self.model.predict([input_ids, attention_masks])
    predicted_labels = np.argmax(predictions.logits, axis=1)
    return predicted_labels
