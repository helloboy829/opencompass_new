from mmengine.config import read_base

with read_base():
    # 导入模型配置
    from .models.qwen3.qwen3_32b_api import models

    # 导入数据集配置（根据需要选择）
    from .datasets.mmlu.mmlu_ppl_ac766d import mmlu_datasets
    from .datasets.ceval.ceval_ppl_578f8d import ceval_datasets
    from .datasets.gsm8k.gsm8k_gen_1d7fe4 import gsm8k_datasets
    from .datasets.humaneval.humaneval_gen_8e312c import humaneval_datasets
    from .datasets.mbpp.mbpp_gen_1e1056 import mbpp_datasets

# 组合所有数据集
datasets = [*mmlu_datasets, *ceval_datasets, *gsm8k_datasets, *humaneval_datasets, *mbpp_datasets]
