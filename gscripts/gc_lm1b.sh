#!/usr/bin/env bash

conda activate indist

cd ~/Codes/InDist

export PYTHONPATH=$PYTHONPATH:/home/dehghani/Codes/InDist


CUDA_VISIBLE_DEVICES=0,1,2,3 python keras_trainer.py \
--model=lm_lstm_shared_emb \
--task=lm1b \
--model_config=lstm_drop31_v2 \
--train_config=radam_slw \
--batch_size=32 \
--exp_name=offlineteacher_v1 > lm1b_run1 &


CUDA_VISIBLE_DEVICES=4,5,6,7 python keras_trainer.py \
--model=lm_lstm_shared_emb \
--task=lm1b \
--model_config=lstm_drop31_v2 \
--train_config=radam_fst \
--batch_size=32 \
--exp_name=offlineteacher_v2 > lm1b_run2 &

wait