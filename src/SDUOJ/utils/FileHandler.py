import json
import os

def read_json_file(file_path):
    with open(file_path, "r") as f:
        return json.load(f)

def write_json_file(file_path, data):
    # write the data to the json file
    with open(file_path, "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=4)

def create_file(pIdx, title, description):
    pIdx = int(pIdx)
    if not os.path.exists(f"{pIdx + 1}_{title}.md"):
        file = f"{pIdx + 1}_{title}.md"
        with open(file, "w", encoding="utf-8") as f:
            f.write(description)
        print(f"create file {file}")
    else:
        print(f"file already exist")

def debugprint(func):
    def wrapper(*args, **kwargs):
        ret = func(*args, **kwargs)
        file_name = func.__name__ + ".txt"
        with open(file_name, "w", encoding='utf-8') as f:
            if isinstance(ret, dict):
                f.write(json.dumps(ret, indent=4, ensure_ascii=False))
            else:
                f.write(str(ret))
        return ret
    return wrapper