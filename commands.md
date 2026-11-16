python train.py \
  --config config/train/chatgpt-bladder.yml \
  --strategy single \
  --train-sizes 5 10 20 40 \
  --num-tests-per-set 5 \
  --max-depth 3 \
    --tau 0.35 \

  python train.py `
  --config config/train/chatgpt-bladder-multiple.yml `
  --strategy llmt_forest `
  --train-sizes 10 20 `
  --num-tests-per-set 5 `
  --num-trees 10 `
  --max-depth 3

  python train.py \
  --config config/train/chatgpt-bladder-multiple.yml \
  --exp-name chatgpt-bladder-forest-d5-tau35 \
  --strategy llmt_forest \
  --train-sizes 5 10 20 40 \
  --num-tests-per-set 5 \
  --num-trees 10 \
  --max-depth 5 \
  --tau 0.35 \
  --openai-api-base https://api.openai.com/v1 \
  --model-name gpt-4o-mini