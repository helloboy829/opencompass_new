from mmengine.config import read_base

with read_base():
    # 导入模型配置
    from .models.qwen3.qwen3_32b_api import models

    # 导入 SuperGPQA 数据集配置
    from .datasets.supergpqa.supergpqa_gen import supergpqa_datasets

# 自定义数据集缓存路径
# 数据集会下载到项目的 data/ 目录下
import os
DATASET_CACHE_DIR = os.path.join(os.path.dirname(__file__), '..', 'data')

for dataset in supergpqa_datasets:
    dataset['cache_dir'] = DATASET_CACHE_DIR

datasets = supergpqa_datasets
