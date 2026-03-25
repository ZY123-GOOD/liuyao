 CUDA_VISIBLE_DEVICES=0,1,2 vllm serve /data/zhuyao/models/Qwen3.5-35B-A3B \
    --host 0.0.0.0 \
    --port 8000 \
    --tensor-parallel-size 1 \
    --max-model-len 16384 \
    --reasoning-parser qwen3 \
    --tensor-parallel-size 2
