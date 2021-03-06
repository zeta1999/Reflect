import tensorflow as tf
from tf2_models.common_layers import get_initializer, shape_list
from tf2_models.embedding import SharedEmbeddings
from tf2_models.transformer_layers import Block


class GPT2(tf.keras.layers.Layer):
  def __init__(self, hparams, *inputs, **kwargs):
    super(GPT2, self).__init__(hparams, *inputs, **kwargs)

    self.output_hidden_states = hparams.output_hidden_states
    self.output_attentions = hparams.output_attentions
    self.output_embeddings = hparams.output_embeddings

    self.num_hidden_layers = hparams.depth
    self.vocab_size = hparams.vocab_size
    self.embedding_dim = hparams.embedding_dim
    self.regularizer = tf.keras.regularizers.l1_l2(l1=0.00,
                                                   l2=0.0001)

    self.create_vars(hparams)


  @tf.function
  def create_vars(self, hparams):
    self.wte = SharedEmbeddings(self.vocab_size,
                                hparams.hidden_size,
                                initializer_range=hparams.initializer_range,
                                regularizer=self.regularizer,
                                name='wte')
    self.wpe = tf.keras.layers.Embedding(hparams.n_positions,
                                         hparams.embedding_dim,
                                         embeddings_initializer=get_initializer(hparams.initializer_range),
                                         embeddings_regularizer=self.regularizer,
                                         name='wpe')
    self.drop = tf.keras.layers.Dropout(hparams.embd_pdrop)
    self.h = [Block(hparams.n_ctx,
                    hparams,
                    regularizer=self.regularizer,
                    scale=True,
                    name='h_._{}'.format(i)) for i in range(hparams.depth)]
    self.ln_f = tf.keras.layers.LayerNormalization(epsilon=hparams.layer_norm_epsilon, name='ln_f')


  def call(self, inputs, past=None, attention_mask=None, token_type_ids=None, position_ids=None,
           training=False):

    @tf.function(experimental_relax_shapes=True)
    def _call(inputs, past, attention_mask, token_type_ids, position_ids,
           training):

      if past is None:
        past_length = 0
        past = [None] * len(self.h)
      else:
        past_length = shape_list(past[0][0])[-2]
      if position_ids is None:
        position_ids = tf.range(past_length, shape_list(inputs)[-1] + past_length, dtype=tf.int32)[tf.newaxis, :]


      if attention_mask is not None:
        attention_mask = attention_mask[:, tf.newaxis, tf.newaxis, :]
        attention_mask = tf.cast(attention_mask, tf.float32)
        attention_mask = (1.0 - attention_mask) * -10000.0

      padding_mask = tf.cast(tf.not_equal(inputs, tf.zeros_like(inputs))[:,tf.newaxis,:,tf.newaxis],
                             dtype=tf.float32)

      if attention_mask is None:
        attention_mask = padding_mask
      else:
        attention_mask = attention_mask*padding_mask

      input_shape = shape_list(inputs)
      input_ids = tf.reshape(inputs, [-1, input_shape[-1]])
      position_ids = tf.reshape(position_ids, [-1, shape_list(position_ids)[-1]])

      inputs_embeds = self.wte(input_ids, mode='embedding')
      position_embeds = self.wpe(position_ids)

      if token_type_ids is not None:
        token_type_ids = tf.reshape(token_type_ids, [-1, shape_list(token_type_ids)[-1]])
        token_type_embeds = self.wte(token_type_ids, mode='embedding')
      else:
        token_type_embeds = 0

      hidden_states = inputs_embeds + position_embeds + token_type_embeds
      hidden_states = self.drop(hidden_states, training=training)

      output_shape = input_shape + [shape_list(hidden_states)[-1]]

      presents = ()
      all_attentions = []
      all_hidden_states = ()
      for i, (block, layer_past) in enumerate(zip(self.h, past)):
        if self.output_hidden_states:
          all_hidden_states = all_hidden_states + (tf.reshape(hidden_states, output_shape),)

        outputs = block([hidden_states, layer_past, attention_mask], training=training)

        hidden_states, present = outputs[:2]
        presents = presents + (present,)

        if self.output_attentions:
          all_attentions.append(outputs[2])

      hidden_states = self.ln_f(hidden_states)
      hidden_states = tf.reshape(hidden_states, output_shape)

      # Add last hidden state
      if self.output_hidden_states:
        all_hidden_states = all_hidden_states + (hidden_states,)

      outputs = (hidden_states, presents)

      if self.output_hidden_states:
        outputs = outputs + (all_hidden_states,)
      if self.output_attentions:
        # let the number of heads free (-1) so we can extract attention even after head pruning
        attention_output_shape = input_shape[:-1] + [-1] + shape_list(all_attentions[0])[-2:]
        all_attentions = tuple(tf.reshape(t, attention_output_shape) for t in all_attentions)
        outputs = outputs + (all_attentions,)
      if self.output_embeddings:
          outputs = outputs + (inputs_embeds,)
      return outputs  # last hidden state, presents, (all hidden_states), (attentions)

    return _call(inputs, past, attention_mask, token_type_ids, position_ids,
           training)

class GPT2SharedWeights(GPT2):
  def __init__(self, hparams, *inputs, **kwargs):
    super(GPT2SharedWeights, self).__init__(hparams, *inputs, **kwargs)

  @tf.function
  def create_vars(self, hparams):
    self.wte = SharedEmbeddings(self.vocab_size ,
                                hparams.hidden_size,
                                initializer_range=hparams.initializer_range,
                                regularizer=self.regularizer,
                                name='wte')
    self.wpe = tf.keras.layers.Embedding(hparams.n_positions,
                                         hparams.embedding_dim,
                                         embeddings_initializer=get_initializer(hparams.initializer_range),
                                         embeddings_regularizer=self.regularizer,
                                         name='wpe')
    self.drop = tf.keras.layers.Dropout(hparams.embd_pdrop)
    attention_block = Block(hparams.n_ctx,
                      hparams,
                      regularizer=self.regularizer,
                      scale=True,
                      name='h')
    self.h = [attention_block for i in range(hparams.depth)]
    self.ln_f = tf.keras.layers.LayerNormalization(epsilon=hparams.layer_norm_epsilon, name='ln_f')

class Bert(tf.keras.layers.Layer):
  def __init__(self, hparams, *inputs, **kwargs):
    super(Bert, self).__init__(hparams, *inputs, **kwargs)

    self.output_hidden_states = hparams.output_hidden_states
    self.output_attentions = hparams.output_attentions
    self.output_embeddings = hparams.output_embeddings

    self.num_hidden_layers = hparams.depth
    self.vocab_size = hparams.vocab_size
    self.embedding_dim = hparams.embedding_dim
    self.regularizer = tf.keras.regularizers.l1_l2(l1=0.00,
                                                   l2=0.0001)

    self.create_vars(hparams)

  @tf.function
  def create_vars(self, hparams):
    self.wte = SharedEmbeddings(self.vocab_size,
                                hparams.hidden_size,
                                initializer_range=hparams.initializer_range,
                                regularizer=self.regularizer,
                                name='wte')
    self.wpe = tf.keras.layers.Embedding(hparams.n_positions,
                                         hparams.embedding_dim,
                                         embeddings_initializer=get_initializer(hparams.initializer_range),
                                         embeddings_regularizer=self.regularizer,
                                         name='wpe')
    self.drop = tf.keras.layers.Dropout(hparams.embd_pdrop)
    self.h = [Block(hparams.n_ctx,
                    hparams,
                    regularizer=self.regularizer,
                    scale=True,
                    casual_masking=False,
                    name='h_._{}'.format(i)) for i in range(hparams.depth)]
    self.ln_f = tf.keras.layers.LayerNormalization(epsilon=hparams.layer_norm_epsilon, name='ln_f')

  def get_input_embeddings(self, inputs, past=None, attention_mask=None, token_type_ids=None, position_ids=None,
           training=False):
    if past is None:
      past_length = 0
      past = [None] * len(self.h)
    else:
      past_length = shape_list(past[0][0])[-2]
    if position_ids is None:
      position_ids = tf.range(past_length, shape_list(inputs)[-1] + past_length, dtype=tf.int32)[tf.newaxis, :]


    input_shape = shape_list(inputs)

    input_ids = tf.reshape(inputs, [-1, input_shape[-1]])
    position_ids = tf.reshape(position_ids, [-1, shape_list(position_ids)[-1]])

    inputs_embeds = self.wte(input_ids, mode='embedding')
    position_embeds = self.wpe(position_ids)

    if token_type_ids is not None:
      token_type_ids = tf.reshape(token_type_ids, [-1, shape_list(token_type_ids)[-1]])
      token_type_embeds = self.wte(token_type_ids, mode='embedding')
    else:
      token_type_embeds = 0

    input_embeddings = inputs_embeds + position_embeds + token_type_embeds

    padding_mask = tf.cast(tf.not_equal(inputs, tf.zeros_like(inputs))[:, tf.newaxis, :, tf.newaxis],
                           dtype=tf.float32)

    return input_embeddings, input_shape, padding_mask, past

  def call_with_embeddings(self, input_embeddings, input_shape, padding_mask, past, attention_mask=None,
           training=False):
    @tf.function(experimental_relax_shapes=True)
    def _call(input_embeddings, input_shape, padding_mask, past, attention_mask,
           training):

      if attention_mask is not None:
        attention_mask = attention_mask[:, tf.newaxis, tf.newaxis, :]
        attention_mask = tf.cast(attention_mask, tf.float32)
        attention_mask = (1.0 - attention_mask) * -10000.0

      if attention_mask is None:
        attention_mask = padding_mask
      else:
        attention_mask = attention_mask*padding_mask

      hidden_states = input_embeddings
      hidden_states = self.drop(hidden_states, training=training)

      output_shape = input_shape + [shape_list(hidden_states)[-1]]

      presents = ()
      all_attentions = []
      all_hidden_states = ()
      for i, (block, layer_past) in enumerate(zip(self.h, past)):
        if self.output_hidden_states:
          all_hidden_states = all_hidden_states + (tf.reshape(hidden_states, output_shape),)

        outputs = block([hidden_states, layer_past, attention_mask], training=training)

        hidden_states, present = outputs[:2]
        presents = presents + (present,)

        if self.output_attentions:
          all_attentions.append(outputs[2])

      hidden_states = self.ln_f(hidden_states)
      hidden_states = tf.reshape(hidden_states, output_shape)

      # Add last hidden state
      if self.output_hidden_states:
        all_hidden_states = all_hidden_states + (hidden_states,)

      outputs = (hidden_states, presents)

      if self.output_hidden_states:
        outputs = outputs + (all_hidden_states,)
      if self.output_attentions:
        # let the number of heads free (-1) so we can extract attention even after head pruning
        attention_output_shape = input_shape[:-1] + [-1] + shape_list(all_attentions[0])[-2:]
        all_attentions = tuple(tf.reshape(t, attention_output_shape) for t in all_attentions)
        outputs = outputs + (all_attentions,)
      if self.output_embeddings:
          outputs = outputs
      return outputs  # last hidden state, presents, (all hidden_states), (attentions), input_embedding

    return _call(input_embeddings, input_shape, padding_mask, past, attention_mask,
           training)

  def call(self, inputs, past=None, attention_mask=None, token_type_ids=None, position_ids=None,
           training=False):

    @tf.function(experimental_relax_shapes=True)
    def _call(inputs, past, attention_mask, token_type_ids, position_ids,
           training):

      if past is None:
        past_length = 0
        past = [None] * len(self.h)
      else:
        past_length = shape_list(past[0][0])[-2]
      if position_ids is None:
        position_ids = tf.range(past_length, shape_list(inputs)[-1] + past_length, dtype=tf.int32)[tf.newaxis, :]


      if attention_mask is not None:
        attention_mask = attention_mask[:, tf.newaxis, tf.newaxis, :]
        attention_mask = tf.cast(attention_mask, tf.float32)
        attention_mask = (1.0 - attention_mask) * -10000.0

      padding_mask = tf.cast(tf.not_equal(inputs, tf.zeros_like(inputs))[:,tf.newaxis,:,tf.newaxis],
                             dtype=tf.float32)

      if attention_mask is None:
        attention_mask = padding_mask
      else:
        attention_mask = attention_mask*padding_mask

      input_shape = shape_list(inputs)

      input_ids = tf.reshape(inputs, [-1, input_shape[-1]])
      position_ids = tf.reshape(position_ids, [-1, shape_list(position_ids)[-1]])

      inputs_embeds = self.wte(input_ids, mode='embedding')
      position_embeds = self.wpe(position_ids)

      if token_type_ids is not None:
        token_type_ids = tf.reshape(token_type_ids, [-1, shape_list(token_type_ids)[-1]])
        token_type_embeds = self.wte(token_type_ids, mode='embedding')
      else:
        token_type_embeds = 0

      hidden_states = inputs_embeds + position_embeds + token_type_embeds
      hidden_states = self.drop(hidden_states, training=training)

      output_shape = input_shape + [shape_list(hidden_states)[-1]]

      presents = ()
      all_attentions = []
      all_hidden_states = ()
      for i, (block, layer_past) in enumerate(zip(self.h, past)):
        if self.output_hidden_states:
          all_hidden_states = all_hidden_states + (tf.reshape(hidden_states, output_shape),)

        outputs = block([hidden_states, layer_past, attention_mask], training=training)

        hidden_states, present = outputs[:2]
        presents = presents + (present,)

        if self.output_attentions:
          all_attentions.append(outputs[2])

      hidden_states = self.ln_f(hidden_states)
      hidden_states = tf.reshape(hidden_states, output_shape)

      # Add last hidden state
      if self.output_hidden_states:
        all_hidden_states = all_hidden_states + (hidden_states,)

      outputs = (hidden_states, presents)

      if self.output_hidden_states:
        outputs = outputs + (all_hidden_states,)
      if self.output_attentions:
        # let the number of heads free (-1) so we can extract attention even after head pruning
        attention_output_shape = input_shape[:-1] + [-1] + shape_list(all_attentions[0])[-2:]
        all_attentions = tuple(tf.reshape(t, attention_output_shape) for t in all_attentions)
        outputs = outputs + (all_attentions,)
      if self.output_embeddings:
          outputs = outputs + (inputs_embeds,)
      return outputs  # last hidden state, presents, (all hidden_states), (attentions), input_embedding

    return _call(inputs, past, attention_mask, token_type_ids, position_ids,
           training)

class BertSharedWeights(Bert):
  def __init__(self, hparams, *inputs, **kwargs):
    super(BertSharedWeights, self).__init__(hparams, *inputs, **kwargs)

    self.output_hidden_states = hparams.output_hidden_states
    self.output_attentions = hparams.output_attentions
    self.output_embeddings = hparams.output_embeddings

    self.num_hidden_layers = hparams.depth
    self.vocab_size = hparams.vocab_size
    self.embedding_dim = hparams.embedding_dim
    self.regularizer = tf.keras.regularizers.l1_l2(l1=0.00,
                                                   l2=0.0001)

    self.create_vars(hparams)


  @tf.function
  def create_vars(self, hparams):
    self.wte = SharedEmbeddings(self.vocab_size,
                                hparams.hidden_size,
                                initializer_range=hparams.initializer_range,
                                regularizer=self.regularizer,
                                name='wte')
    self.wpe = tf.keras.layers.Embedding(hparams.n_positions,
                                         hparams.embedding_dim,
                                         embeddings_initializer=get_initializer(hparams.initializer_range),
                                         embeddings_regularizer=self.regularizer,
                                         name='wpe')
    self.drop = tf.keras.layers.Dropout(hparams.embd_pdrop)
    attention_block = Block(hparams.n_ctx,
                      hparams,
                      regularizer=self.regularizer,
                      scale=True,
                      casual_masking=False,
                      name='h')
    self.h = [attention_block for i in range(hparams.depth)]
    self.ln_f = tf.keras.layers.LayerNormalization(epsilon=hparams.layer_norm_epsilon, name='ln_f')
