#!/usr/bin/env bash

conda activate indist

cd ~/Codes/InDist

export PYTHONPATH=$PYTHONPATH:/home/dehghani/Codes/InDist


CUDA_VISIBLE_DEVICES=0 python distill/distill_main.py  \
--task=word_sv_agreement_vp \
--teacher_model=cl_lstm \
--student_model=cl_gpt2_shared \
--student_exp_name=gc_o_std4005 \
--teacher_exp_name=gc_o_tchr4005 \
--teacher_config=small_lstm_v4 \
--student_config=small_gpt_v9 \
--distill_mode=online \
--distill_config=pure_dstl_4_crs_slw_hld30 > run0 &


CUDA_VISIBLE_DEVICES=1 python distill/distill_main.py  \
--task=word_sv_agreement_vp \
--teacher_model=cl_lstm \
--student_model=cl_gpt2 \
--student_exp_name=gc_o_std4015 \
--teacher_exp_name=gc_o_tchr4015 \
--teacher_config=small_lstm_v4 \
--student_config=small_gpt_v9 \
--distill_mode=online \
--distill_config=pure_dstl_4_crs_slw_hld30 > run0 &


CUDA_VISIBLE_DEVICES=2 python distill/distill_main.py  \
--task=word_sv_agreement_vp \
--teacher_model=cl_bert \
--student_model=cl_gpt2_shared \
--student_exp_name=gc_fo_std4025 \
--teacher_exp_name=gc_o_tchr4025 \
--teacher_config=small_gpt_v9 \
--student_config=small_gpt_v9 \
--distill_mode=online \
--distill_config=pure_dstl_4_crs_slw_hld30 > run0 &

CUDA_VISIBLE_DEVICES=3 python distill/distill_main.py  \
--task=word_sv_agreement_vp \
--teacher_model=cl_bert \
--student_model=cl_gpt2 \
--student_exp_name=gc_o_std4035 \
--teacher_exp_name=gc_o_tchr4035 \
--teacher_config=small_gpt_v9 \
--student_config=small_gpt_v9 \
--distill_mode=online \
--distill_config=pure_dstl_4_crs_slw_hld30 > run0 &


CUDA_VISIBLE_DEVICES=4 python distill/distill_main.py  \
--task=word_sv_agreement_vp \
--teacher_model=cl_gpt2_shared \
--student_model=cl_gpt2_shared \
--student_exp_name=gc_o_std4045 \
--teacher_exp_name=gc_o_tchr4045 \
--teacher_config=small_gpt_v9 \
--student_config=small_gpt_v9 \
--distill_mode=online \
--distill_config=pure_dstl_4_crs_slw_hld30 > run0 &

CUDA_VISIBLE_DEVICES=5 python distill/distill_main.py  \
--task=word_sv_agreement_vp \
--teacher_model=cl_gpt2_shared \
--student_model=cl_gpt2 \
--student_exp_name=gc_o_std4055 \
--teacher_exp_name=gc_o_tchr4055 \
--teacher_config=small_gpt_v9 \
--student_config=small_gpt_v9 \
--distill_mode=online \
--distill_config=pure_dstl_4_crs_slw_hld30 > run0 &


CUDA_VISIBLE_DEVICES=6 python distill/distill_main.py  \
--task=word_sv_agreement_vp \
--teacher_model=cl_gpt2 \
--student_model=cl_gpt2_shared \
--student_exp_name=gc_o_std4065 \
--teacher_exp_name=gc_o_tchr4065 \
--teacher_config=small_gpt_v9 \
--student_config=small_gpt_v9 \
--distill_mode=online \
--distill_config=pure_dstl_4_crs_slw_hld30 > run0 &

CUDA_VISIBLE_DEVICES=7 python distill/distill_main.py  \
--task=word_sv_agreement_vp \
--teacher_model=cl_gpt2 \
--student_model=cl_gpt2 \
--student_exp_name=gc_o_std4075 \
--teacher_exp_name=gc_o_tchr4075 \
--teacher_config=small_gpt_v9 \
--student_config=small_gpt_v9 \
--distill_mode=online \
--distill_config=pure_dstl_4_crs_slw_hld30 > run0 &

wait