#!/usr/bin/env bash

conda activate indist

cd ~/Codes/InDist

export PYTHONPATH=$PYTHONPATH:/home/dehghani/Codes/InDist


CUDA_VISIBLE_DEVICES=0 python mnist_trainer.py \
--model=cl_vcnn \
--task=svhn \
--model_config=vcnn_svhn1 \
--train_config=crs_fst \
--batch_size=128 \
--exp_name=v16 > run4 &

CUDA_VISIBLE_DEVICES=1 python mnist_trainer.py \
--model=cl_vcnn \
--task=svhn \
--model_config=vcnn_svhn1 \
--train_config=crs_fst_v2 \
--batch_size=128 \
--exp_name=v13 > run2 &

CUDA_VISIBLE_DEVICES=2 python mnist_trainer.py \
--model=cl_vcnn \
--task=svhn \
--model_config=vcnn_svhn1 \
--train_config=adam_mid \
--batch_size=128 \
--exp_name=v14 > run3 &

CUDA_VISIBLE_DEVICES=3 python mnist_trainer.py \
--model=cl_vcnn \
--task=svhn \
--model_config=vcnn_svhn1 \
--train_config=crs_slw_v2 \
--batch_size=128 \
--exp_name=v15 > run4 &

CUDA_VISIBLE_DEVICES=4 python mnist_trainer.py \
--model=cl_vcnn \
--task=svhn \
--model_config=vcnn_svhn3 \
--train_config=adam_slw \
--batch_size=128 \
--exp_name=v9 > run5 &

CUDA_VISIBLE_DEVICES=5 python mnist_trainer.py \
--model=cl_vcnn \
--task=svhn \
--model_config=vcnn_svhn3 \
--train_config=adam_mid \
--batch_size=128 \
--exp_name=v10 > run6 &

CUDA_VISIBLE_DEVICES=6 python mnist_trainer.py \
--model=cl_vcnn \
--task=svhn \
--model_config=vcnn_svhn3 \
--train_config=crs_fst \
--batch_size=128 \
--exp_name=v11 > run7 &

CUDA_VISIBLE_DEVICES=7 python mnist_trainer.py \
--model=cl_vcnn \
--task=svhn \
--model_config=vcnn_svhn3 \
--train_config=crs_slw \
--batch_size=128 \
--exp_name=v12 > run8 &

wait