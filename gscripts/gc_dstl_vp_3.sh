#!/usr/bin/env bash

conda activate indist

cd ~/Codes/InDist

export PYTHONPATH=$PYTHONPATH:/home/dehghani/Codes/InDist


CUDA_VISIBLE_DEVICES=0 python distill/distill_main.py  \
--task=word_sv_agreement_vp \
--teacher_model=cl_bert \
--student_model=cl_lstm \
--student_exp_name=gc_o_std9301 \
--teacher_exp_name=gc_o_tchr9301 \
--teacher_config=small_gpt_v9 \
--student_config=small_lstm_v4 \
--distill_mode=online \
--distill_config=pure_dstl_4_exp_vp9 > run0 &

CUDA_VISIBLE_DEVICES=1 python distill/distill_main.py  \
--task=word_sv_agreement_vp \
--teacher_model=cl_bert \
--student_model=cl_lstm \
--student_exp_name=gc_o_std9302 \
--teacher_exp_name=gc_o_tchr9302 \
--teacher_config=small_gpt_v9 \
--student_config=small_lstm_v4 \
--distill_mode=online \
--distill_config=pure_dstl_4_exp_vp9 > run0 &
#
CUDA_VISIBLE_DEVICES=2 python distill/distill_main.py  \
--task=word_sv_agreement_vp \
--teacher_model=cl_bert \
--student_model=cl_gpt2_shared \
--student_exp_name=gc_o_std8331 \
--teacher_exp_name=gc_o_tchr8331 \
--teacher_config=small_gpt_v9 \
--student_config=small_ugpt_v9 \
--distill_mode=online \
--distill_config=pure_dstl_4_exp_vp8 > run0 &

CUDA_VISIBLE_DEVICES=3 python distill/distill_main.py  \
--task=word_sv_agreement_vp \
--teacher_model=cl_bert \
--student_model=cl_gpt2_shared \
--student_exp_name=gc_o_std9331 \
--teacher_exp_name=gc_o_tchr9331 \
--teacher_config=small_gpt_v9 \
--student_config=small_ugpt_v9 \
--distill_mode=online \
--distill_config=pure_dstl_4_exp_vp9 > run0 &

CUDA_VISIBLE_DEVICES=4 python distill/distill_main.py  \
--task=word_sv_agreement_vp \
--teacher_model=cl_bert \
--student_model=cl_gpt2 \
--student_exp_name=gc_o_std8323 \
--teacher_exp_name=gc_o_tchr8323 \
--teacher_config=small_gpt_v9 \
--student_config=small_gpt_v9 \
--distill_mode=online \
--distill_config=pure_dstl_4_exp_vp8 > run0 &
##
CUDA_VISIBLE_DEVICES=5 python distill/distill_main.py  \
--task=word_sv_agreement_vp \
--teacher_model=cl_bert \
--student_model=cl_gpt2 \
--student_exp_name=gc_o_std8324 \
--teacher_exp_name=gc_o_tchr8324 \
--teacher_config=small_gpt_v9 \
--student_config=small_gpt_v9 \
--distill_mode=online \
--distill_config=pure_dstl_4_exp_vp8 > run0 &
#
CUDA_VISIBLE_DEVICES=6 python distill/distill_main.py  \
--task=word_sv_agreement_vp \
--teacher_model=cl_bert \
--student_model=cl_bert \
--student_exp_name=gc_o_std8311 \
--teacher_exp_name=gc_o_tchr8311 \
--teacher_config=small_gpt_v9 \
--student_config=small_gpt_v9 \
--distill_mode=online \
--distill_config=pure_dstl_4_exp_vp8 > run0 &

CUDA_VISIBLE_DEVICES=7 python distill/distill_main.py  \
--task=word_sv_agreement_vp \
--teacher_model=cl_bert \
--student_model=cl_bert \
--student_exp_name=gc_o_std8312 \
--teacher_exp_name=gc_o_tchr8312 \
--teacher_config=small_gpt_v9 \
--student_config=small_gpt_v9 \
--distill_mode=online \
--distill_config=pure_dstl_4_exp_vp8 > run0 &




wait