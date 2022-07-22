export SAVE_DIR=./output
export DATA="GAD"
export SPLIT="1"
export DATA_DIR=../datasets/RE/${DATA}/${SPLIT}
export ENTITY=${DATA}-${SPLIT}

export MAX_LENGTH=128
export BATCH_SIZE=32
export NUM_EPOCHS=3
export SAVE_STEPS=1000
export SEED=1


python ./scripts/re_eval.py --output_path=${SAVE_DIR}/${ENTITY}/test_results.txt --answer_path=${DATA_DIR}/test_original.tsv
