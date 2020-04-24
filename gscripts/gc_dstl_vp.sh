#!/usr/bin/env bash

conda activate indist

cd ~/Codes/InDist

export PYTHONPATH=$PYTHONPATH:/home/dehghani/Codes/InDist


CUDA_VISIBLE_DEVICES=0 python distill/distill_main.py  \
--task=word_sv_agreement_vp \
--teacher_model=cl_bert \
--student_model=cl_lstm \
--student_exp_name=gc_o_std100 \
--teacher_exp_name=gc_o_tchr100 \
--teacher_config=small_gpt_v9 \
--student_config=small_lstm_v4 \
--distill_mode=online \
--distill_config=pure_dstl_4_crs_slw > run0 &

CUDA_VISIBLE_DEVICES=1 python distill/distill_main.py  \
--task=word_sv_agreement_vp \
--teacher_model=cl_bert \
--student_model=cl_lstm \
--student_exp_name=gc_o_std101 \
--teacher_exp_name=gc_o_tchr101 \
--teacher_config=small_gpt_v9 \
--student_config=small_lstm_v4 \
--distill_mode=online \
--distill_config=pure_dstl_4_crs_slw > run1 &

CUDA_VISIBLE_DEVICES=2 python distill/distill_main.py \
--task=word_sv_agreement_vp \
--teacher_model=cl_bert \
--student_model=cl_lstm \
--student_exp_name=gc_o_std102 \
--teacher_exp_name=gc_o_tchr102 \
--teacher_config=small_gpt_v9 \
--student_config=small_lstm_v4 \
--distill_mode=online \
--distill_config=pure_dstl_4_crs_slw > run2 &


CUDA_VISIBLE_DEVICES=3 python distill/distill_main.py  \
--task=word_sv_agreement_vp \
--teacher_model=cl_bert \
--student_model=cl_lstm \
--student_exp_name=gc_o_std103 \
--teacher_exp_name=gc_o_tchr103 \
--teacher_config=small_gpt_v9 \
--student_config=small_lstm_v4 \
--distill_mode=online \
--distill_config=pure_dstl_4_crs_slw > run3 &


CUDA_VISIBLE_DEVICES=4 python distill/distill_main.py  \
--task=word_sv_agreement_vp \
--teacher_model=cl_bert \
--student_model=cl_gpt2_shared \
--student_exp_name=gc_o_std104 \
--teacher_exp_name=gc_o_tchr104 \
--teacher_config=small_gpt_v9 \
--student_config=small_gpt_v9 \
--distill_mode=online \
--distill_config=pure_dstl5_4_crs_slw > run4 &

CUDA_VISIBLE_DEVICES=5 python distill/distill_main.py  \
--task=word_sv_agreement_vp \
--teacher_model=cl_bert \
--student_model=cl_gpt2_shared \
--student_exp_name=gc_o_std105 \
--teacher_exp_name=gc_o_tchr105 \
--teacher_config=small_gpt_v9 \
--student_config=small_gpt_v9 \
--distill_mode=online \
--distill_config=pure_dstl_4_crs_slw > run5 &

CUDA_VISIBLE_DEVICES=6 python distill/distill_main.py \
--task=word_sv_agreement_vp \
--teacher_model=cl_bert \
--student_model=cl_gpt2_shared \
--student_exp_name=gc_o_std106 \
--teacher_exp_name=gc_o_tchr106 \
--teacher_config=small_gpt_v9 \
--student_config=small_gpt_v9 \
--distill_mode=online \
--distill_config=pure_dstl_4_crs_slw > run6 &


CUDA_VISIBLE_DEVICES=7 python distill/distill_main.py  \
--task=word_sv_agreement_vp \
--teacher_model=cl_bert \
--student_model=cl_gpt2_shared \
--student_exp_name=gc_o_std107 \
--teacher_exp_name=gc_o_tchr107 \
--teacher_config=small_gpt_v9 \
--student_config=small_gpt_v9 \
--distill_mode=online \
--distill_config=pure_dstl_4_crs_slw > run7 &