export SAVE_DIR=./output
export DATA_DIR=./datasets

export MAX_LENGTH=128
export BATCH_SIZE=32
export NUM_EPOCHS=3
export SAVE_STEPS=1000
export SEED=1

python run_re.py \
    --task_name SST-2 \
    --config_name bert-base-cased \
    --data_dir ${DATA_DIR} \
    --model_name_or_path dmis-lab/biobert-base-cased-v1.1 \
    --max_seq_length ${MAX_LENGTH} \
    --num_train_epochs ${NUM_EPOCHS} \
    --per_device_train_batch_size ${BATCH_SIZE} \
    --save_steps ${SAVE_STEPS} \
    --seed ${SEED} \
    --do_predict \
    --learning_rate 5e-5 \
    --output_dir ${SAVE_DIR} \
    --overwrite_output_dir


