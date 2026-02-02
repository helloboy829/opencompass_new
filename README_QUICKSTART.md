# OpenCompass 评测 Qwen3-32B 快速参考

## 🚀 三步开始评测

### 1️⃣ 准备数据
将你的 500 条数据放到：`data/supergpqa_500_samples.jsonl`

格式：
```jsonl
{"question": "问题", "options": ["A", "B", "C", "D"], "answer_letter": "B", "discipline": "学科", "field": "领域", "subfield": "子领域", "difficulty": "easy"}
```

### 2️⃣ 配置 API
编辑：`opencompass/configs/models/qwen3/qwen3_32b_api.py`
```python
openai_api_base='http://你的地址:端口/v1'
path='你的模型名称'
```

### 3️⃣ 运行评测
```bash
python run.py configs/eval_qwen3_32b_supergpqa_custom.py
```

---

## 📂 关键文件

| 文件 | 用途 | 是否需要修改 |
|------|------|-------------|
| `data/supergpqa_500_samples.jsonl` | 你的评测数据 | ✅ 必须 |
| `opencompass/configs/models/qwen3/qwen3_32b_api.py` | API 配置 | ✅ 必须 |
| `configs/eval_qwen3_32b_supergpqa_custom.py` | 评测配置 | ❌ 不需要 |
| `opencompass/configs/datasets/supergpqa/supergpqa_custom_500.py` | 数据集配置 | ⚙️ 可选 |

---

## 🔧 常用配置

### 调整性能
```python
# 在 qwen3_32b_api.py 中
batch_size=16,          # 批处理大小（4-32）
query_per_second=5,     # QPS（1-10）
```

### 过滤学科
```python
# 在 supergpqa_custom_500.py 中
discipline='Mathematics',  # 只评测数学
```

### Few-shot 模式
```python
# 在 supergpqa_custom_500.py 中
prompt_mode='five-shot',  # 提供 5 个示例
```

---

## 📊 结果位置

```
outputs/default/[时间戳]/
├── summary/summary_[时间戳].txt    # 📈 汇总结果
├── predictions/supergpqa_500/      # 📝 详细预测
└── logs/                           # 📋 日志文件
```

---

## 🛠️ 辅助工具

### 数据转换
```bash
# CSV → JSONL
python tools/convert_supergpqa_to_jsonl.py -i data/your.csv -o data/supergpqa_500_samples.jsonl

# JSON → JSONL
python tools/convert_supergpqa_to_jsonl.py -i data/your.json -o data/supergpqa_500_samples.jsonl
```

### 数据验证
```bash
python tools/validate_supergpqa_data.py data/supergpqa_500_samples.jsonl
```

---

## ❓ 常见问题速查

| 问题 | 解决方案 |
|------|---------|
| 找不到数据文件 | 确保路径是 `data/supergpqa_500_samples.jsonl` |
| API 连接失败 | 检查 `openai_api_base` 和服务是否运行 |
| 评测太慢 | 增加 `batch_size` 和 `query_per_second` |
| 内存不足 | 减小 `batch_size` 到 4 或 2 |
| 字段缺失 | 确保包含所有必需字段（见数据格式） |

---

## 📖 详细文档

查看完整指南：`docs/custom_supergpqa_guide.md`

---

## ✅ 检查清单

- [ ] 数据文件已放置在 `data/supergpqa_500_samples.jsonl`
- [ ] 数据格式正确（包含所有必需字段）
- [ ] API 地址已配置在 `qwen3_32b_api.py`
- [ ] API 服务正常运行
- [ ] 准备好查看 `outputs/` 目录中的结果

---

**准备好了？运行评测：**
```bash
python run.py configs/eval_qwen3_32b_supergpqa_custom.py
```
