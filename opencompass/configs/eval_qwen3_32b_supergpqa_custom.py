from mmengine.config import read_base

with read_base():
    # 导入模型配置
    from .models.qwen3.qwen3_32b_api import models

    # 导入自定义 SuperGPQA 数据集配置（500 条样本）
    from .datasets.supergpqa.supergpqa_custom_500 import supergpqa_custom_datasets

# 使用自定义数据集
datasets = supergpqa_custom_datasets
