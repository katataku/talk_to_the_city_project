
import subprocess
import json
import os
# def visualization(config):
#     output_dir = config['output_dir']
#     with open(f"outputs/{output_dir}/result.json") as f:
#         result = f.read()

#     cwd = "../next-app"
#     command = f"REPORT={output_dir} npm run build"

#     try:
#         process = subprocess.Popen(command, shell=True, cwd=cwd, stdout=subprocess.PIPE,
#                                    stderr=subprocess.PIPE, universal_newlines=True)
#         while True:
#             output_line = process.stdout.readline()
#             if output_line == '' and process.poll() is not None:
#                 break
#             if output_line:
#                 print(output_line.strip())
#         process.wait()
#         errors = process.stderr.read()
#         if errors:
#             print("Errors:")
#             print(errors)
#     except subprocess.CalledProcessError as e:
#         print("Error: ", e)

def visualization(config):
    output_dir = config['output_dir']
    
    try:
        # 1. 读取数据
        with open(f"outputs/{output_dir}/result.json") as f:
            result = json.load(f)
        
        # 2. 处理数据（如果需要的话）
        visualization_data = process_for_visualization(result)
        
        # 3. 保存处理后的数据
        output_path = f"outputs/{output_dir}"
        
        with open(f"{output_path}/visualization.json", 'w') as f:
            json.dump(visualization_data, f, indent=2)
            
    except Exception as e:
        print(f"Error in visualization: {e}")
        raise

def process_for_visualization(data):
    """处理数据为可视化所需的格式"""
    # 在这里添加任何必要的数据转换逻辑
    return data