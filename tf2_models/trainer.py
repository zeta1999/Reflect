import tensorflow as tf
import os
from tf2_models.keras_callbacks import CheckpointCallback, SummaryCallback
from tf2_models.train_utils import RectifiedAdam, ExponentialDecayWithWarmpUp

OPTIMIZER_DIC = {'adam': tf.keras.optimizers.Adam,
                 'radam': RectifiedAdam,
                 }
class Trainer(object):

  def __init__(self, hparams, strategy, model, task, train_params, log_dir, ckpt_dir):
    self.hparams = hparams
    self.model = model
    self.task = task
    self.train_params = train_params
    self.strategy = strategy

    lr_schedule = self.get_lr_schedule()

    self.optimizer = OPTIMIZER_DIC[self.train_params.optimizer](learning_rate=lr_schedule, epsilon=1e-08, clipnorm=1.0)

    self.ckpt = tf.train.Checkpoint(step=tf.Variable(1, name='checkpoint_step'), optimizer=self.optimizer, net=self.model)
    self.manager = tf.train.CheckpointManager(self.ckpt, ckpt_dir,
                                                keep_checkpoint_every_n_hours=self.hparams.keep_checkpoint_every_n_hours,
                                                max_to_keep=2)

    with self.strategy.scope():
      x, y = iter(self.task.valid_dataset).next()
      model(x)
      model.summary()
      model.compile(
        optimizer=self.optimizer,
        loss=self.task.get_loss_fn(),
        metrics=self.task.metrics())#[self.task.get_loss_fn()])
      #tf.keras.losses.SparseCategoricalCrossentropy(from_logits=True),)


      summary_dir = os.path.join(log_dir, 'summaries')
      tf.io.gfile.makedirs(log_dir)
      self.summary_writer = tf.compat.v2.summary.create_file_writer(os.path.join(summary_dir, 'train'))
      tf.compat.v2.summary.experimental.set_step(self.optimizer.iterations)

      ckpt_callback = CheckpointCallback(manager=self.manager, ckpt=self.ckpt)
      summary_callback = SummaryCallback(summary_writer=self.summary_writer)

      self.callbacks = [ckpt_callback, summary_callback]

  def get_lr_schedule(self):
    if 'crs' in self.train_params.schedule:
      initial_learning_rate = self.train_params.learning_rate
      lr_schedule = (
        tf.keras.experimental.CosineDecayRestarts(
          initial_learning_rate,
          self.train_params.decay_steps,
          t_mul=2.0,
          m_mul=0.9,
          alpha=0.001,
        ))
    elif self.train_params.optimizer == 'radam':
      initial_learning_rate = self.train_params.learning_rate
      lr_schedule = ExponentialDecayWithWarmpUp(
        initial_learning_rate=initial_learning_rate,
        decay_steps=self.train_params.decay_steps,
        hold_base_rate_steps=self.train_params.hold_base_rate_steps,
        decay_rate=0.96,
        warmup_steps=0.0)
    else:
      initial_learning_rate = self.train_params.learning_rate
      lr_schedule = ExponentialDecayWithWarmpUp(
        initial_learning_rate=initial_learning_rate,
        decay_steps=self.train_params.decay_steps,
        decay_rate=0.96,
        hold_base_rate_steps=self.train_params.hold_base_rate_steps,
        warmup_steps=self.train_params.warmup_steps)
    return lr_schedule

  def restore(self):
    with self.strategy.scope():
      self.ckpt.restore(self.manager.latest_checkpoint)
      if self.manager.latest_checkpoint:
        print("Restored from {}".format(self.manager.latest_checkpoint))
      else:
        print("Initializing from scratch.")

  def train(self):
    with self.strategy.scope():
      with self.summary_writer.as_default():
        print("initial learning rate:", self.model.optimizer.learning_rate(self.model.optimizer.iterations))
        self.model.fit(self.task.train_dataset,
                  epochs=self.train_params.num_train_epochs,
                  steps_per_epoch=self.task.n_train_batches,
                  validation_steps=self.task.n_valid_batches,
                  callbacks=self.callbacks,
                  validation_data=self.task.valid_dataset,
                  verbose=2
                  )
