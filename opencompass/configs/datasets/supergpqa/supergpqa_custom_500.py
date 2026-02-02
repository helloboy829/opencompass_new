from opencompass.datasets.supergpqa.supergpqa_custom import SuperGPQACustomDataset
from opencompass.datasets.supergpqa.supergpqa import SuperGPQAEvaluator
from opencompass.openicl.icl_inferencer import GenInferencer
from opencompass.openicl.icl_prompt_template import PromptTemplate
from opencompass.openicl.icl_retriever import ZeroRetriever


# Reader 配置
reader_cfg = dict(
    input_columns=[
        'question',
        'options',
        'discipline',
        'field',
        'subfield',
        'difficulty',
        'infer_prompt',
        'prompt_mode',
    ],
    output_column='answer_letter',
)

# Inference 配置
infer_cfg = dict(
    prompt_template=dict(
        type=PromptTemplate,
        template=dict(
            round=[
                dict(
                    role='HUMAN',
                    prompt='{infer_prompt}',
                ),
            ],
        ),
    ),
    retriever=dict(type=ZeroRetriever),
    inferencer=dict(type=GenInferencer),
)

# Evaluation 配置
eval_cfg = dict(
    evaluator=dict(type=SuperGPQAEvaluator),
    pred_role='BOT',
)

# 数据集配置
supergpqa_custom_dataset = dict(
    type=SuperGPQACustomDataset,
    abbr='supergpqa_500',
    path='data/supergpqa_500_samples.jsonl',  # 你的数据文件路径
    prompt_mode='zero-shot',
    reader_cfg=reader_cfg,
    infer_cfg=infer_cfg,
    eval_cfg=eval_cfg,
)

supergpqa_custom_datasets = [supergpqa_custom_dataset]
