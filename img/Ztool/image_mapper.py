import os
import json
import argparse

def generate_image_mapping(input_dir, output_file, base_url):
    image_extensions = {'.jpg', '.jpeg', '.png', '.gif'}
    image_data = {}

    # 遍历所有目录和子目录
    for root, _, files in os.walk(input_dir):
        for file in files:
            # 获取文件扩展名并转换为小写
            file_ext = os.path.splitext(file)[1].lower()
            if file_ext in image_extensions:
                # 分割文件名和扩展名
                filename = os.path.splitext(file)[0]
                # 生成JSON键和URL
                json_key = f"Celeste_{filename}"
                image_url = f"{base_url.rstrip('/')}/{filename}{file_ext}"
                image_data[json_key] = image_url

    # 写入JSON文件
    with open(output_file, 'w') as f:
        json.dump(image_data, f, indent=4)

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="生成图片文件JSON映射")
    parser.add_argument("--input", required=True, help="输入目录路径")
    parser.add_argument("--output", default="output.json", help="输出JSON文件路径")
    parser.add_argument("--url", default="https://cdn.jsdelivr.net/gh/NiHiLine/CDN/img/C", 
                      help="CDN基础URL地址")

    args = parser.parse_args()

    generate_image_mapping(
        input_dir=args.input,
        output_file=args.output,
        base_url=args.url
    )