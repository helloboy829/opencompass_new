# 使用自定义 SuperGPQA 数据集评测 Qwen3-32B 指南

## 📋 快速开始

### 步骤 1：准备你的 500 条数据

将你的数据保存为 JSONL 格式，放在：
```
data/supergpqa_500_samples.jsonl
```

**数据格式**（每行一个 JSON 对象）：
```jsonl
{"question": "What is the capital of France?", "options": ["London", "Berlin", "Paris", "Madrid"], "answer_letter": "C", "discipline": "Geography", "field": "World Geography", "subfield": "European Geography", "difficulty": "easy"}
{"question": "What is 2+2?", "options": ["3", "4", "5", "6"], "answer_letter": "B", "discipline": "Mathematics", "field": "Arithmetic", "subfield": "Basic Operations", "difficulty": "middle"}
```

**必需字段说明**：
- `question`: 问题文本
- `options`: 选项列表（数组格式）
- `answer_letter`: 正确答案（A/B/C/D/E...）
- `discipline`: 学科名称
- `field`: 领域名称
- `subfield`: 子领域名称
- `difficulty`: 难度等级（`easy` / `middle` / `hard`）

### 步骤 2：配置 API 地址

编辑文件：`opencompass/configs/models/qwen3/qwen3_32b_api.py`

修改以下参数：
```python
models = [
    dict(
        type=OpenAI,
        abbr='qwen3-32b-api',
        path='qwen3-32b',                          # 改为你的模型名称
        key='EMPTY',                               # 如果需要 API Key，改为你的 key
        openai_api_base='http://localhost:8000/v1', # 改为你的 API 地址
        query_per_second=2,                        # 根据服务器性能调整
        max_out_len=2048,
        max_seq_len=8192,
        batch_size=8,                              # 根据服务器性能调整
        retry=3,
    )
]
```

**参数说明**：
- `path`: 你的模型名称（与 API 中的模型名称一致）
- `openai_api_base`: 你的 API 服务地址
- `key`: API 密钥（如果不需要认证，保持 `'EMPTY'`）
- `query_per_second`: 每秒请求数限制（QPS）
- `batch_size`: 批处理大小（建议 4-16）

### 步骤 3：运行评测

在项目根目录下运行：
```bash
python run.py configs/eval_qwen3_32b_supergpqa_custom.py
```

### 步骤 4：查看结果

评测完成后，结果保存在：
```
outputs/default/[时间戳]/
├── summary/
│   └── summary_[时间戳].txt          # 汇总结果（准确率、各学科得分等）
├── predictions/
│   └── supergpqa_500/                # 每道题的预测结果
└── logs/                             # 详细日志
```

---

## 🔧 数据格式转换（可选）

如果你的数据是 CSV 或 JSON 格式，可以使用转换工具：

### 从 CSV 转换
```bash
python tools/convert_supergpqa_to_jsonl.py --input data/your_data.csv --output data/supergpqa_500_samples.jsonl
```

**CSV 格式示例**：
```csv
question,options,answer_letter,discipline,field,subfield,difficulty
"What is the capital of France?","[""London"", ""Berlin"", ""Paris"", ""Madrid""]",C,Geography,World Geography,European Geography,easy
```

### 从 JSON 转换
```bash
python tools/convert_supergpqa_to_jsonl.py --input data/your_data.json --output data/supergpqa_500_samples.jsonl
```

**JSON 格式示例**：
```json
{
  "data": [
    {
      "question": "What is the capital of France?",
      "options": ["London", "Berlin", "Paris", "Madrid"],
      "answer_letter": "C",
      "discipline": "Geography",
      "field": "World Geography",
      "subfield": "European Geography",
      "difficulty": "easy"
    }
  ]
}
```

---

## ⚙️ 高级配置

### 1. 过滤特定学科

如果只想评测特定学科，编辑文件：`opencompass/configs/datasets/supergpqa/supergpqa_custom_500.py`

修改数据集配置：

```python
supergpqa_custom_dataset = dict(
    type=SuperGPQACustomDataset,
    abbr='supergpqa_500_math',
    path='data/supergpqa_500_samples.jsonl',
    prompt_mode='zero-shot',
    discipline='Mathematics',  # 只评测数学题
    # field='Algebra',         # 可选：进一步过滤到特定领域
    # subfield='Linear Algebra', # 可选：进一步过滤到特定子领域
    reader_cfg=reader_cfg,
    infer_cfg=infer_cfg,
    eval_cfg=eval_cfg,
)
```

### 2. 使用 Few-shot 提示

编辑文件：`opencompass/configs/datasets/supergpqa/supergpqa_custom_500.py`

修改 `prompt_mode` 为 `'five-shot'`：

```python
supergpqa_custom_dataset = dict(
    type=SuperGPQACustomDataset,
    abbr='supergpqa_500',
    path='data/supergpqa_500_samples.jsonl',
    prompt_mode='five-shot',  # 改为 five-shot（提供 5 个示例）
    reader_cfg=reader_cfg,
    infer_cfg=infer_cfg,
    eval_cfg=eval_cfg,
)
```

### 3. 调整性能参数

如果你的 API 服务器性能较好，可以提高并发。

编辑文件：`opencompass/configs/models/qwen3/qwen3_32b_api.py`

```python
models = [
    dict(
        type=OpenAI,
        abbr='qwen3-32b-api',
        path='qwen3-32b',
        key='EMPTY',
        openai_api_base='http://localhost:8000/v1',
        batch_size=16,         # 增加批处理大小（默认 8）
        query_per_second=5,    # 增加 QPS（默认 2）
        max_out_len=2048,
        max_seq_len=8192,
        retry=3,
    )
]
```

### 4. 自定义数据集路径

如果你的数据文件在其他位置，编辑文件：`opencompass/configs/datasets/supergpqa/supergpqa_custom_500.py`

修改 `path` 参数：

```python
supergpqa_custom_dataset = dict(
    type=SuperGPQACustomDataset,
    abbr='supergpqa_500',
    path='path/to/your/custom_data.jsonl',  # 修改为你的数据文件路径
    prompt_mode='zero-shot',
    reader_cfg=reader_cfg,
    infer_cfg=infer_cfg,
    eval_cfg=eval_cfg,
)
```

---

## 📊 结果解读

评测完成后，`summary_[时间戳].txt` 文件包含：

```
Overall Accuracy: 85.2%

Discipline Breakdown:
- Mathematics: 90.5% (42/50)
- Physics: 82.3% (28/34)
- Biology: 88.1% (37/42)
- Computer Science: 91.2% (31/34)
...

Difficulty Breakdown:
- Easy: 92.5% (148/160)
- Middle: 85.3% (145/170)
- Hard: 72.9% (124/170)
```

---

## ❓ 常见问题

### Q1: 数据文件路径错误
**A**: 确保 `data/supergpqa_500_samples.jsonl` 文件存在，路径相对于项目根目录 `opencompass/`。

### Q2: API 连接失败
**A**: 检查：
- API 服务是否正常运行
- `openai_api_base` 地址是否正确
- 网络连接是否正常
- 防火墙是否阻止连接

### Q3: 字段缺失错误
**A**: 确保每条数据都包含所有必需字段。可以使用验证脚本检查：
```bash
python tools/validate_supergpqa_data.py data/supergpqa_500_samples.jsonl
```

### Q4: 选项格式错误
**A**: `options` 必须是数组格式，例如：
```json
"options": ["Option A", "Option B", "Option C", "Option D"]
```
不能是字符串：`"options": "A,B,C,D"`

### Q5: 评测速度太慢
**A**: 可以尝试：
- 增加 `batch_size`（如 16 或 32）
- 增加 `query_per_second`
- 检查 API 服务器性能
- 使用更快的推理后端（如 vLLM）

### Q6: 内存不足
**A**: 减小 `batch_size`，例如改为 4 或 2。

---

## 📁 项目文件结构

```
opencompass/
├── data/
│   └── supergpqa_500_samples.jsonl           # 你的 500 条数据
│
├── configs/
│   ├── eval_qwen3_32b_supergpqa_custom.py    # 评测配置（组合模型和数据集）
│   ├── models/qwen3/
│   │   └── qwen3_32b_api.py                  # 模型配置（需要修改 API 地址）
│   └── datasets/supergpqa/
│       └── supergpqa_custom_500.py           # 数据集配置
│
├── opencompass/datasets/supergpqa/
│   └── supergpqa_custom.py                   # 自定义数据集加载器
│
├── tools/
│   ├── convert_supergpqa_to_jsonl.py         # 数据格式转换工具
│   └── validate_supergpqa_data.py            # 数据验证工具
│
└── outputs/                                   # 评测结果输出目录
    └── default/
        └── [时间戳]/
            ├── summary/                       # 汇总结果
            ├── predictions/                   # 详细预测
            └── logs/                          # 日志文件
```

---

## 🎯 完整工作流程

1. **准备数据** → 将 500 条数据保存为 `data/supergpqa_500_samples.jsonl`
2. **配置 API** → 修改 `opencompass/configs/models/qwen3/qwen3_32b_api.py`
3. **运行评测** → `python run.py configs/eval_qwen3_32b_supergpqa_custom.py`
4. **查看结果** → 检查 `outputs/default/[时间戳]/summary/` 目录

---

## 💡 提示

- 首次运行会自动创建必要的目录
- 评测过程中可以按 `Ctrl+C` 中断
- 建议先用少量数据（如 10 条）测试配置是否正确
- 评测结果会自动保存，不会覆盖之前的结果

---

## 📞 需要帮助？

如果遇到问题，请检查：
1. 数据格式是否正确（使用验证工具）
2. API 配置是否正确
3. API 服务是否正常运行
4. 查看 `outputs/default/[时间戳]/logs/` 中的日志文件
