import json
import re

def repair_notebook(input_path, output_path):
    with open(input_path, 'r', encoding='utf-8', errors='ignore') as f:
        content = f.read()

    # Remove control characters that are invalid in JSON strings
    content_clean = re.sub(r'[\x00-\x1f\x7f]', '', content)

    try:
        notebook_json = json.loads(content_clean)
    except json.JSONDecodeError as e:
        print(f"JSON decode error: {e}")
        # Try to fix truncated JSON by removing incomplete last line
        lines = content_clean.splitlines()
        while lines:
            try:
                notebook_json = json.loads('\n'.join(lines))
                break
            except json.JSONDecodeError:
                lines.pop()
        else:
            print("Failed to repair the notebook JSON.")
            return False

    with open(output_path, 'w', encoding='utf-8') as f:
        json.dump(notebook_json, f, indent=2)

    print(f"Repaired notebook saved to {output_path}")
    return True

if __name__ == "__main__":
    input_file = "D4/007a_REGR_SalaryLevel.ipynb"
    output_file = "D4/007a_REGR_SalaryLevel_repaired.ipynb"
    repair_notebook(input_file, output_file)
