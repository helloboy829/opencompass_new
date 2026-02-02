import json
import os
from datasets import Dataset

from opencompass.datasets.supergpqa.supergpqa import SuperGPQADataset
from opencompass.datasets.supergpqa.supergpqa_utils import load_yaml
from opencompass.registry import LOAD_DATASET


def _parse(item, template, prompt_mode):
    """解析数据项，生成推理提示"""
    prompt_format = [
        item['question'] + '\n' + '\n'.join([
            f'{chr(65+i)}) {option}'
            for i, option in enumerate(item['options'])
        ])
    ]
    item['infer_prompt'] = template['prompt_format'][0].format(*prompt_format)
    item['prompt_mode'] = prompt_mode
    return item


@LOAD_DATASET.register_module()
class SuperGPQACustomDataset(SuperGPQADataset):
    """自定义 SuperGPQA 数据集加载器，支持本地 JSONL 文件"""

    @staticmethod
    def load(path: str,
             prompt_mode: str = 'zero-shot',
             discipline: str = None,
             field: str = None,
             subfield: str = None,
             **kwargs):
        """
        从本地 JSONL 文件加载数据集

        Args:
            path: JSONL 文件路径
            prompt_mode: 提示模式 ('zero-shot' 或 'five-shot')
            discipline: 过滤特定学科（可选）
            field: 过滤特定领域（可选）
            subfield: 过滤特定子领域（可选）
        """
        # 读取 JSONL 文件
        data_list = []
        with open(path, 'r', encoding='utf-8') as f:
            for line in f:
                if line.strip():
                    data_list.append(json.loads(line))

        # 创建 Dataset
        dataset = Dataset.from_list(data_list)

        # 过滤数据（如果指定了过滤条件）
        if discipline is not None:
            dataset = dataset.filter(lambda x: x['discipline'] == discipline)
        if field is not None:
            dataset = dataset.filter(lambda x: x['field'] == field)
        if subfield is not None:
            dataset = dataset.filter(lambda x: x['subfield'] == subfield)

        # 加载提示模板
        template_path = None
        if prompt_mode == 'zero-shot':
            template_path = os.path.join(
                os.path.dirname(__file__),
                'supergpqa_dataset_config/prompt/zero-shot.yaml',
            )
        elif prompt_mode == 'five-shot':
            template_path = os.path.join(
                os.path.dirname(__file__),
                'supergpqa_dataset_config/prompt/five-shot.yaml',
            )

        try:
            template = load_yaml(template_path)
        except FileNotFoundError:
            print(f'[ERROR] Missing prompt template: {template_path}')
            return Dataset.from_list([])

        # 应用提示模板
        dataset = dataset.map(lambda item: _parse(item, template, prompt_mode))

        return dataset
