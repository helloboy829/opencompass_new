from opencompass.models import OpenAI

models = [
    dict(
        type=OpenAI,
        abbr='qwen3-32b-api',
        path='qwen3-32b',  # 你的模型名称，根据实际 API 调整
        key='EMPTY',  # 如果不需要 key 就用 'EMPTY'，或者用 'ENV' 从环境变量 $OPENAI_API_KEY 读取
        openai_api_base='http://localhost:8000/v1',  # 替换为你的 API 地址
        query_per_second=2,  # 根据你的服务器性能调整 QPS
        max_out_len=2048,
        max_seq_len=8192,
        batch_size=8,
        retry=3,
    )
]
