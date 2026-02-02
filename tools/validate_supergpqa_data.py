"""
验证 SuperGPQA JSONL 数据格式的脚本

使用方法：
    python tools/validate_supergpqa_data.py data/supergpqa_500_samples.jsonl
"""

import json
import argparse
from pathlib import Path


def validate_jsonl(file_path):
    """验证 JSONL 文件格式"""
    print(f"Validating file: {file_path}\n")

    required_fields = ['question', 'options', 'answer_letter', 'discipline', 'field', 'subfield', 'difficulty']
    valid_difficulties = ['easy', 'middle', 'hard']

    errors = []
    warnings = []
    total_lines = 0
    valid_lines = 0

    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            for line_num, line in enumerate(f, 1):
                total_lines += 1
                line = line.strip()

                if not line:
                    warnings.append(f"Line {line_num}: Empty line")
                    continue

                try:
                    data = json.loads(line)
                except json.JSONDecodeError as e:
                    errors.append(f"Line {line_num}: JSON parse error - {e}")
                    continue

                # Check required fields
                missing_fields = [field for field in required_fields if field not in data]
                if missing_fields:
                    errors.append(f"Line {line_num}: Missing fields {missing_fields}")
                    continue

                # Check if options is a list
                if not isinstance(data['options'], list):
                    errors.append(f"Line {line_num}: 'options' must be a list, current type: {type(data['options'])}")
                    continue

                # Check number of options
                if len(data['options']) < 2:
                    errors.append(f"Line {line_num}: 'options' needs at least 2 choices, current: {len(data['options'])}")
                    continue

                # Check if answer_letter is valid
                max_option_letter = chr(65 + len(data['options']) - 1)
                if data['answer_letter'] not in [chr(65 + i) for i in range(len(data['options']))]:
                    errors.append(f"Line {line_num}: 'answer_letter' must be between A-{max_option_letter}, current: {data['answer_letter']}")
                    continue

                # Check difficulty
                if data['difficulty'] not in valid_difficulties:
                    warnings.append(f"Line {line_num}: 'difficulty' should be one of {valid_difficulties}, current: {data['difficulty']}")

                # Check for empty fields
                for field in required_fields:
                    if not data[field]:
                        warnings.append(f"Line {line_num}: Field '{field}' is empty")

                valid_lines += 1

    except FileNotFoundError:
        print(f"ERROR: File not found: {file_path}")
        return False
    except Exception as e:
        print(f"ERROR: Error reading file: {e}")
        return False

    # Output results
    print("=" * 60)
    print("Validation Results:")
    print("=" * 60)
    print(f"Total lines: {total_lines}")
    print(f"Valid data: {valid_lines}")
    print(f"Errors: {len(errors)}")
    print(f"Warnings: {len(warnings)}")
    print("=" * 60 + "\n")

    if errors:
        print("ERRORS found:\n")
        for error in errors[:10]:
            print(f"  - {error}")
        if len(errors) > 10:
            print(f"  ... and {len(errors) - 10} more errors")
        print()

    if warnings:
        print("WARNINGS:\n")
        for warning in warnings[:10]:
            print(f"  - {warning}")
        if len(warnings) > 10:
            print(f"  ... and {len(warnings) - 10} more warnings")
        print()

    if not errors:
        print("SUCCESS: Data format validation passed!\n")
        print("Data Statistics:")

        # Statistics
        disciplines = {}
        difficulties = {'easy': 0, 'middle': 0, 'hard': 0}

        with open(file_path, 'r', encoding='utf-8') as f:
            for line in f:
                if line.strip():
                    data = json.loads(line)
                    discipline = data.get('discipline', 'unknown')
                    disciplines[discipline] = disciplines.get(discipline, 0) + 1
                    difficulty = data.get('difficulty', 'unknown')
                    if difficulty in difficulties:
                        difficulties[difficulty] += 1

        print("\nDiscipline distribution:")
        for discipline, count in sorted(disciplines.items(), key=lambda x: x[1], reverse=True):
            print(f"  - {discipline}: {count}")

        print("\nDifficulty distribution:")
        for difficulty, count in difficulties.items():
            print(f"  - {difficulty}: {count}")

        return True
    else:
        print("FAILED: Data format validation failed. Please fix the errors above.")
        return False


def main():
    parser = argparse.ArgumentParser(description='Validate SuperGPQA JSONL data format')
    parser.add_argument('file', help='JSONL file path')
    args = parser.parse_args()

    file_path = Path(args.file)

    if validate_jsonl(file_path):
        print(f"\nSUCCESS: Ready to start evaluation!")
        print(f"Run command: python run.py configs/eval_qwen3_32b_supergpqa_custom.py")
    else:
        exit(1)


if __name__ == '__main__':
    main()
