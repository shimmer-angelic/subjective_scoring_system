import re
import os
import pandas as pd
import logging

def extract_info(file_path: str) -> list[dict]:
    """从DOC文件提取考生信息"""
    with open(file_path, 'r', encoding='utf-8') as f:
        content = f.read()
    
    # 更安全的文件名解析
    try:
        filename = os.path.basename(file_path)
        name_part = filename.split('-')[-1]  # 分割文件名获取姓名部分
        name = name_part.split('.')[0]  # 去除扩展名
        if not name.isprintable():
            raise ValueError("包含不可打印字符")
    except (IndexError, ValueError) as e:
        logging.warning(f"文件名解析失败: {filename} - {str(e)}")
        name = "未知"
    
    with open(file_path, 'r', encoding='utf-8') as f:
        content = f.read()
    
    # 提取姓名
    name = re.search(r'(\d+)-([\u4e00-\u9fa5]+)\.doc', file_path).group(2)
    
    # 提取作答和得分
    answers = re.findall(r'<span>考生作答:</span> <span>(.*?)</span>', content)
    scores = re.findall(r'<span>考生得分:</span> <span>(.*?)</span>', content)
    
    results = []
    for i, (answer, score) in enumerate(zip(answers, scores)):
        results.append({
            '姓名': name,
            '试题序号': i+1,
            '作答': answer,
            '得分': float(score)
        })
    
    return results

def main():
    all_results = []
    for filename in os.listdir('test'):
        if filename.endswith('.doc'):
            file_path = os.path.join('test', filename)
            try:
                all_results.extend(extract_info(file_path))
            except Exception as e:
                print(f"Error processing {filename}: {str(e)}")
    
    df = pd.DataFrame(all_results)
    df.to_excel('scores.xlsx', index=False, columns=['姓名', '试题序号', '作答', '得分'])

if __name__ == '__main__':
    main()
