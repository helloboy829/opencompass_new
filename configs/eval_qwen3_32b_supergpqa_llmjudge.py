from mmengine.config import read_base

with read_base():
    # 导入模型配置
    from .models.qwen3.qwen3_32b_api import models

    # 导入 SuperGPQA 数据集配置（使用 LLM 评判）
    from .datasets.supergpqa.supergpqa_llmjudge_gen_12b8bc import supergpqa_datasets

# 配置评判模型（使用你的 Qwen3-32B 作为评判器）
judge_model = dict(
    type='opencompass.models.OpenAI',
    path='qwen3-32b',  # 评判模型，可以和被测模型相同或不同
    key='EMPTY',
    openai_api_base='http://localhost:8000/v1',
    query_per_second=2,
    max_out_len=2048,
    max_seq_len=8192,
    batch_size=8,
    retry=3,
)

# 将评判模型配置应用到数据集
for dataset in supergpqa_datasets:
    dataset['eval_cfg']['evaluator']['judge_cfg'] = judge_model

datasets = supergpqa_datasets
