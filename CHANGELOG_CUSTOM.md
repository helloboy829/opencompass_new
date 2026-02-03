# OpenCompass 项目修改记录

## 修改日期：2026-02-03

### 📋 修改目的
修复配置文件导入路径错误，解决评测配置无法正确加载模型和数据集配置的问题。

---

## 📝 修改文件

### 1. 评测配置文件路径调整
- **文件**: `configs/eval_qwen3_32b_supergpqa_custom.py`
- **问题**: 使用相对导入 `from .models.qwen3.qwen3_32b_api` 时，在 `configs/` 目录下找不到 `models/` 子目录
- **原因**: `configs/` 目录下没有 `models/` 和 `datasets/` 子目录，这些目录实际在 `opencompass/configs/` 下
- **解决方案**: 将配置文件复制到 `opencompass/configs/` 目录下，使相对导入能够正确工作

### 2. 配置文件位置变更
- **原位置**: `configs/eval_qwen3_32b_supergpqa_custom.py`
- **新位置**: `opencompass/configs/eval_qwen3_32b_supergpqa_custom.py`
- **修改内容**: 文件内容保持不变，仅调整存放位置
- **导入路径**:
  ```python
  from .models.qwen3.qwen3_32b_api import models
  from .datasets.supergpqa.supergpqa_custom_500 import supergpqa_custom_datasets
  ```

---

## 🔧 配置变更

### 运行命令更新
- **旧命令**: `python run.py configs/eval_qwen3_32b_supergpqa_custom.py`
- **新命令**: `python run.py opencompass/configs/eval_qwen3_32b_supergpqa_custom.py`

---

## 🚀 使用方法变更

### 正确的文件组织结构
```
opencompass/
├── configs/
│   ├── eval_qwen3_32b_supergpqa_custom.py    [评测配置应放在这里]
│   ├── models/qwen3/
│   │   └── qwen3_32b_api.py                  [模型配置]
│   └── datasets/supergpqa/
│       └── supergpqa_custom_500.py           [数据集配置]
```

### 评测运行步骤
1. 确保配置文件在 `opencompass/configs/` 目录下
2. 运行命令：`python run.py opencompass/configs/eval_qwen3_32b_supergpqa_custom.py`
3. 查看结果：`outputs/default/[时间戳]/summary/`

---

## 📖 文档更新

### 需要更新的文档
- `README_QUICKSTART.md`: 更新运行命令中的配置文件路径
- `docs/custom_supergpqa_guide.md`: 更新配置文件位置说明

---

## 🐛 问题排查记录

### 问题 1: ConfigParsingError
- **错误信息**: `configs\models/qwen3/qwen3_32b_api.py not found!`
- **原因**: `configs/` 目录下没有 `models/` 子目录
- **解决**: 将配置文件移至 `opencompass/configs/` 目录

### 问题 2: 路径拼写错误
- **错误**: 用户输入 `opencompass/config/` (少了 s)
- **正确**: `opencompass/configs/` (有 s)

---

## 💡 经验总结

1. **配置文件位置**: OpenCompass 的评测配置文件应放在 `opencompass/configs/` 目录下，而不是项目根目录的 `configs/` 下
2. **相对导入机制**: `read_base()` 的相对导入会从配置文件所在目录开始查找
3. **目录结构**: 保持与官方示例一致的目录结构，避免路径问题

---

**修改完成时间**: 2026-02-03 10:30
**修改人**: Claude (AI Assistant)
**版本**: v1.1

---

## 修改日期：2026-02-02

### 📋 修改目的
为 OpenCompass 项目添加自定义 SuperGPQA 数据集（500 条样本）的评测支持，使用本地部署的 Qwen3-32B API 进行评测。

---

## 🆕 新增文件

### 1. 数据文件
- **文件**: `data/supergpqa_500_samples.jsonl`
- **说明**: 示例数据文件（5 条），需要替换为用户的 500 条实际数据
- **格式**: JSONL（每行一个 JSON 对象）
- **必需字段**: question, options, answer_letter, discipline, field, subfield, difficulty

### 2. 自定义数据集加载器
- **文件**: `opencompass/datasets/supergpqa/supergpqa_custom.py`
- **说明**: 支持从本地 JSONL 文件加载 SuperGPQA 数据集
- **功能**:
  - 读取 JSONL 格式数据
  - 支持按学科/领域/子领域过滤
  - 应用提示模板（zero-shot 或 five-shot）

### 3. 数据集配置文件
- **文件**: `opencompass/configs/datasets/supergpqa/supergpqa_custom_500.py`
- **说明**: 自定义 SuperGPQA 数据集的配置
- **配置内容**:
  - Reader 配置（输入输出列）
  - Inference 配置（提示模板、推理器）
  - Evaluation 配置（评估器）
  - 数据集路径和参数

### 4. 模型配置文件
- **文件**: `opencompass/configs/models/qwen3/qwen3_32b_api.py`
- **说明**: Qwen3-32B API 模型配置
- **配置内容**:
  - 模型类型：OpenAI 兼容 API
  - API 地址：需要用户配置
  - 批处理大小：8
  - QPS 限制：2

### 5. 评测配置文件
- **文件**: `configs/eval_qwen3_32b_supergpqa_custom.py`
- **说明**: 组合模型和数据集的评测配置
- **功能**: 导入模型配置和数据集配置，启动评测

### 6. 数据转换工具
- **文件**: `tools/convert_supergpqa_to_jsonl.py`
- **说明**: 将 CSV/JSON 格式转换为 JSONL 格式
- **支持格式**: CSV, JSON → JSONL

### 7. 数据验证工具
- **文件**: `tools/validate_supergpqa_data.py`
- **说明**: 验证 JSONL 数据格式是否正确
- **功能**:
  - 检查必需字段
  - 验证数据格式
  - 统计学科和难度分布

### 8. 使用文档
- **文件**: `docs/custom_supergpqa_guide.md`
- **说明**: 完整的使用指南
- **内容**:
  - 快速开始步骤
  - 数据格式说明
  - 配置方法
  - 高级功能
  - 常见问题解答

### 9. 快速参考文档
- **文件**: `README_QUICKSTART.md`
- **说明**: 快速参考卡片
- **内容**:
  - 三步开始
  - 关键文件速查
  - 常用配置
  - 常见问题速查表

---

## 📝 修改文件

### 1. 评测配置（原有文件更新）
- **文件**: `configs/eval_qwen3_32b_supergpqa.py`
- **修改内容**:
  - 添加数据集缓存路径配置
  - 设置为项目内部 `data/` 目录
  - 使用 `os.path.join` 动态计算路径

---

## 📂 目录结构变化

```
opencompass/
├── data/                                         [新增目录]
│   └── supergpqa_500_samples.jsonl              [新增文件]
│
├── configs/
│   ├── eval_qwen3_32b_supergpqa.py              [修改]
│   ├── eval_qwen3_32b_supergpqa_custom.py       [新增文件]
│   ├── models/qwen3/
│   │   └── qwen3_32b_api.py                     [新增文件]
│   └── datasets/supergpqa/
│       └── supergpqa_custom_500.py              [新增文件]
│
├── opencompass/datasets/supergpqa/
│   └── supergpqa_custom.py                      [新增文件]
│
├── tools/
│   ├── convert_supergpqa_to_jsonl.py            [新增文件]
│   └── validate_supergpqa_data.py               [新增文件]
│
├── docs/
│   └── custom_supergpqa_guide.md                [新增文件]
│
└── README_QUICKSTART.md                          [新增文件]
```

---

## 🔧 配置说明

### 需要用户配置的文件

#### 1. API 配置（必须）
**文件**: `opencompass/configs/models/qwen3/qwen3_32b_api.py`

需要修改的参数：
```python
path='qwen3-32b',                          # 改为实际模型名称
openai_api_base='http://localhost:8000/v1', # 改为实际 API 地址
key='EMPTY',                               # 如需认证，改为实际 API Key
```

#### 2. 数据文件（必须）
**文件**: `data/supergpqa_500_samples.jsonl`

需要替换为用户的 500 条实际数据。

#### 3. 数据集配置（可选）
**文件**: `opencompass/configs/datasets/supergpqa/supergpqa_custom_500.py`

可选修改：
- `path`: 数据文件路径
- `discipline`: 过滤特定学科
- `field`: 过滤特定领域
- `prompt_mode`: 'zero-shot' 或 'five-shot'

---

## 🚀 使用方法

### 基本使用
```bash
# 1. 准备数据
# 将 500 条数据放到 data/supergpqa_500_samples.jsonl

# 2. 配置 API
# 编辑 opencompass/configs/models/qwen3/qwen3_32b_api.py

# 3. 运行评测
python run.py configs/eval_qwen3_32b_supergpqa_custom.py

# 4. 查看结果
# outputs/default/[时间戳]/summary/summary_[时间戳].txt
```

### 数据转换
```bash
# CSV 转 JSONL
python tools/convert_supergpqa_to_jsonl.py -i data/your.csv -o data/supergpqa_500_samples.jsonl

# JSON 转 JSONL
python tools/convert_supergpqa_to_jsonl.py -i data/your.json -o data/supergpqa_500_samples.jsonl
```

### 数据验证
```bash
python tools/validate_supergpqa_data.py data/supergpqa_500_samples.jsonl
```

---

## 📊 数据格式

### JSONL 格式示例
```jsonl
{"question": "What is the capital of France?", "options": ["London", "Berlin", "Paris", "Madrid"], "answer_letter": "C", "discipline": "Geography", "field": "World Geography", "subfield": "European Geography", "difficulty": "easy"}
```

### 必需字段
- `question`: 问题文本（字符串）
- `options`: 选项列表（数组）
- `answer_letter`: 正确答案（A/B/C/D/E...）
- `discipline`: 学科名称（字符串）
- `field`: 领域名称（字符串）
- `subfield`: 子领域名称（字符串）
- `difficulty`: 难度等级（easy/middle/hard）

---

## ⚙️ 技术细节

### 数据加载流程
1. `SuperGPQACustomDataset.load()` 读取 JSONL 文件
2. 根据过滤条件筛选数据
3. 加载提示模板（zero-shot.yaml 或 five-shot.yaml）
4. 应用模板生成推理提示
5. 返回 HuggingFace Dataset 对象

### 评估流程
1. 模型生成预测结果
2. `SuperGPQAEvaluator` 提取答案选项
3. 与标准答案比对
4. 统计准确率（总体、按学科、按难度）
5. 生成详细报告

### API 调用
- 使用 OpenAI 兼容接口
- 支持批处理（batch_size）
- QPS 限制（query_per_second）
- 自动重试机制（retry）

---

## 🔍 关键代码位置

### 数据加载
- **类**: `SuperGPQACustomDataset`
- **文件**: `opencompass/datasets/supergpqa/supergpqa_custom.py`
- **方法**: `load(path, prompt_mode, discipline, field, subfield)`

### 评估器
- **类**: `SuperGPQAEvaluator`
- **文件**: `opencompass/datasets/supergpqa/supergpqa.py`（复用原有）
- **方法**: `score(predictions, references, test_set)`

### 模型接口
- **类**: `OpenAI`
- **文件**: `opencompass/models/openai_api.py`（系统自带）
- **方法**: `generate(inputs, max_out_len)`

---

## 📖 文档位置

- **完整指南**: `docs/custom_supergpqa_guide.md`
- **快速参考**: `README_QUICKSTART.md`
- **修改记录**: `CHANGELOG_CUSTOM.md`（本文件）

---

## ✅ 测试状态

- [x] 数据加载器创建完成
- [x] 配置文件创建完成
- [x] 示例数据创建完成
- [x] 转换工具创建完成
- [x] 验证工具创建完成
- [x] 文档编写完成
- [ ] 实际数据准备（待用户完成）
- [ ] API 配置（待用户完成）
- [ ] 评测运行测试（待用户完成）

---

## 🔄 后续维护

### 如需修改数据集
1. 更新 `data/supergpqa_500_samples.jsonl`
2. 运行验证工具检查格式
3. 重新运行评测

### 如需修改模型
1. 编辑 `opencompass/configs/models/qwen3/qwen3_32b_api.py`
2. 或创建新的模型配置文件
3. 更新评测配置文件中的导入

### 如需添加新数据集
1. 参考 `supergpqa_custom.py` 创建新的加载器
2. 在 `configs/datasets/` 下创建配置文件
3. 创建新的评测配置文件

---

## 📝 注意事项

1. **数据格式**: 必须严格遵循 JSONL 格式，每行一个完整的 JSON 对象
2. **API 地址**: 确保 API 服务正常运行且地址正确
3. **路径配置**: 所有路径相对于项目根目录 `opencompass/`
4. **编码问题**: Windows 系统注意文件编码为 UTF-8
5. **性能调优**: 根据服务器性能调整 `batch_size` 和 `query_per_second`

---

## 🐛 已知问题

1. **Windows 编码**: 验证工具在 Windows 下可能有中文显示问题（已修复为英文输出）
2. **路径分隔符**: Windows 使用反斜杠，配置中统一使用正斜杠或 `os.path.join`

---

## 📞 支持

如遇问题，请检查：
1. 数据格式是否正确（使用验证工具）
2. API 配置是否正确
3. API 服务是否正常运行
4. 查看日志文件：`outputs/default/[时间戳]/logs/`

---

**修改完成时间**: 2026-02-02 23:30
**修改人**: Claude (AI Assistant)
**版本**: v1.0
