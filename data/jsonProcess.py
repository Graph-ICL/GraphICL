import json

def modify_json(input_filepath, output_filepath):
    # 打开并逐行读取 JSON 文件
    with open(input_filepath, 'r') as infile:
        data_list = []
        for line in infile:
            try:
                # 逐行解析每个 JSON 对象
                data = json.loads(line)
                
                # 删除指定的键（"edges" 和 "removed_edge"）
                if "edges" in data:
                    del data["edges"]
                if "removed_edge" in data:
                    del data["removed_edge"]
                
                # 将修改后的数据添加到列表
                data_list.append(data)
            except json.JSONDecodeError as e:
                print(f"Error decoding JSON: {e}")
                continue

    # 将修改后的数据作为单行 JSON 写入新的文件
    with open(output_filepath, 'w') as outfile:
        for data in data_list:
            # 每个数据对象单独一行写入
            json.dump(data, outfile, separators=(',', ':'))
            outfile.write("\n")  # 确保每个 JSON 对象在一行

# 示例用法
input_filepath = "/home/zch/Code/NLGraph/data/dataset2.json"  # 替换为你文件的路径和文件名
output_filepath = "/home/zch/Code/NLGraph/data/newdataset2.json"  # 新文件的路径和文件名

modify_json(input_filepath, output_filepath)
