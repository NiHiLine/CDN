import os
import json
import argparse
from pathlib import Path

UNSAFE_PATHS = [
    "/", "/etc", "/bin", "/usr", 
    "C:\\Windows", "C:\\Program Files",
    str(Path.home() / "Desktop")
]

def is_safe_directory(path):
    abs_path = str(Path(path).resolve())
    return not any(abs_path.startswith(p) for p in UNSAFE_PATHS)

def validate_file_overwrite(file_path):
    if Path(file_path).exists():
        confirm = input(f"文件 {file_path} 已存在，是否覆盖？[y/N] ")
        if confirm.lower() != 'y':
            print("操作已取消")
            exit(0)

def generate_image_mapping(args):
    image_extensions = {'.jpg', '.jpeg', '.png', '.gif'}
    image_data = {}

    for root, _, files in os.walk(args.input):
        for file in files:
            filename, file_ext = os.path.splitext(file)
            if file_ext.lower() in image_extensions:
                # 保留原始文件名（含中文）
                raw_filename = f"{filename}{file_ext}"
                
                # 构建URL路径（直接使用中文）
                base_url = args.url.rstrip('/')
                url_path = args.url_path.strip('/')
                full_url = f"{base_url}/{url_path}/{raw_filename}" if url_path else f"{base_url}/{raw_filename}"
                
                # 生成JSON键名（保留中文）
                json_key = f"{args.prefix}_{filename}"
                image_data[json_key] = full_url

    # 返回生成的数据
    return image_data

if __name__ == "__main__":
    parser = argparse.ArgumentParser(
        description="图片文件映射生成器",
        formatter_class=argparse.ArgumentDefaultsHelpFormatter
    )
    
    parser.add_argument("-i", "--input", 
                      required=True,
                      type=lambda p: str(Path(p).resolve()),
                      help="输入目录路径")
    parser.add_argument("-o", "--output",
                      default="output.json",
                      type=Path,
                      help="输出JSON文件路径")
    parser.add_argument("-u", "--url",
                      default="https://cdn.jsdelivr.net/gh/NiHiLine/CDN/img",
                      help="CDN基础URL地址")
    parser.add_argument("-p", "--prefix",
                      default="Celeste",
                      help="JSON键名前缀")
    parser.add_argument("-up", "--url-path",
                      default="C",
                      help="URL路径段")

    args = parser.parse_args()

    # 安全检查
    if not is_safe_directory(args.input):
        print(f"错误：禁止扫描危险目录 {args.input}")
        exit(1)
    
    if not Path(args.input).is_dir():
        print(f"错误：输入路径 {args.input} 不是有效目录")
        exit(1)

    validate_file_overwrite(args.output)

    # 获取生成的数据
    result_data = generate_image_mapping(args)

    # 写入文件（UTF-8编码）
    with open(args.output, 'w', encoding='utf-8') as f:
        json.dump(result_data, f, indent=4, ensure_ascii=False)

    # 修正后的打印语句
    print(f"成功生成 {len(result_data)} 条记录到 {args.output}")