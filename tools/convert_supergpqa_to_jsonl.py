"""
将 SuperGPQA 数据转换为 JSONL 格式的脚本

使用方法：
1. 如果你的数据是 CSV 格式：
   python tools/convert_supergpqa_to_jsonl.py --input data/supergpqa_500.csv --output data/supergpqa_500_samples.jsonl

2. 如果你的数据是 JSON 格式：
   python tools/convert_supergpqa_to_jsonl.py --input data/supergpqa_500.json --output data/supergpqa_500_samples.jsonl
"""

import json
import argparse
import csv
from pathlib import Path


def convert_csv_to_jsonl(input_file, output_file):
    """将 CSV 格式转换为 JSONL"""
    with open(input_file, 'r', encoding='utf-8') as f_in, \
         open(output_file, 'w', encoding='utf-8') as f_out:

        reader = csv.DictReader(f_in)
        for row in reader:
            # 处理 options（假设是逗号分隔或已经是列表）
            if isinstance(row.get('options'), str):
                # 如果 options 是字符串，尝试解析
                try:
                    options = json.loads(row['options'])
                except:
                    # 如果不是 JSON，假设是逗号分隔
                    options = [opt.strip() for opt in row['options'].split(',')]
            else:
                options = row.get('options', [])

            data = {
                'question': row['question'],
                'options': options,
                'answer_letter': row['answer_letter'],
                'discipline': row.get('discipline', 'unknown'),
                'field': row.get('field', 'unknown'),
                'subfield': row.get('subfield', 'unknown'),
                'difficulty': row.get('difficulty', 'middle'),
            }
            f_out.write(json.dumps(data, ensure_ascii=False) + '\n')

    print(f"✅ 转换完成：{input_file} -> {output_file}")


def convert_json_to_jsonl(input_file, output_file):
    """将 JSON 格式转换为 JSONL"""
    with open(input_file, 'r', encoding='utf-8') as f_in, \
         open(output_file, 'w', encoding='utf-8') as f_out:

        data = json.load(f_in)

        # 如果是列表
        if isinstance(data, list):
            items = data
        # 如果是字典，尝试找到数据列表
        elif isinstance(data, dict):
            # 常见的键名
            for key in ['data', 'examples', 'items', 'questions']:
                if key in data:
                    items = data[key]
                    break
            else:
                items = [data]  # 单个对象
        else:
            items = [data]

        for item in items:
            # 确保必需字段存在
            data_item = {
                'question': item['question'],
                'options': item['options'],
                'answer_letter': item['answer_letter'],
                'discipline': item.get('discipline', 'unknown'),
                'field': item.get('field', 'unknown'),
                'subfield': item.get('subfield', 'unknown'),
                'difficulty': item.get('difficulty', 'middle'),
            }
            f_out.write(json.dumps(data_item, ensure_ascii=False) + '\n')

    print(f"✅ 转换完成：{input_file} -> {output_file}")


def main():
    parser = argparse.ArgumentParser(description='将 SuperGPQA 数据转换为 JSONL 格式')
    parser.add_argument('--input', '-i', required=True, help='输入文件路径')
    parser.add_argument('--output', '-o', required=True, help='输出文件路径')
    args = parser.parse_args()

    input_path = Path(args.input)
    output_path = Path(args.output)

    # 确保输出目录存在
    output_path.parent.mkdir(parents=True, exist_ok=True)

    # 根据输入文件类型选择转换方法
    if input_path.suffix.lower() == '.csv':
        convert_csv_to_jsonl(args.input, args.output)
    elif input_path.suffix.lower() == '.json':
        convert_json_to_jsonl(args.input, args.output)
    elif input_path.suffix.lower() == '.jsonl':
        print(f"⚠️  输入文件已经是 JSONL 格式，无需转换")
    else:
        print(f"❌ 不支持的文件格式：{input_path.suffix}")
        print("支持的格式：.csv, .json, .jsonl")


if __name__ == '__main__':
    main()
