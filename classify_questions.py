import pandas as pd
import json
from openai import OpenAI
from config import API_KEY

# 读取标签
with open("标签.txt", "r", encoding="utf-8") as f:
    labels = [line.strip() for line in f.readlines()]

# 初始化deepseek客户端
client = OpenAI(api_key=API_KEY, base_url="https://api.deepseek.com")

def classify_question(question, options):
    """使用deepseek API对题目进行分类"""
    prompt = f"""
    请根据以下题目和选项内容，从以下标签中选择最合适的分类：
    标签列表：{", ".join(labels)}
    
    题目：{question}
    选项：{options}
    
    请返回以下格式的JSON：
    {{
        "label": "最合适的标签"
    }}
    """
    
    try:
        response = client.chat.completions.create(
            model="deepseek-chat",
            messages=[
                {"role": "system", "content": "你是一个专业的题目分类助手"},
                {"role": "user", "content": prompt}
            ],
            response_format={"type": "json_object"},
            temperature=0.2,
            timeout=30  # 增加超时时间
        )
        if response.choices and response.choices[0].message.content:
            result = json.loads(response.choices[0].message.content)
            return result["label"]
        else:
            raise ValueError("API返回结果为空")
    except Exception as e:
        print(f"分类失败: {str(e)}")
        return "未知"

def main():
    # 读取试题
    df = pd.read_excel("试题.xlsx")
    
    # 添加分类结果列
    df["分类"] = ""
    
    # 对每个题目进行分类
    for i, row in df.iterrows():
        print(f"正在处理第 {i+1}/{len(df)} 题")
        label = classify_question(row["题目"], row["选项"])
        df.at[i, "分类"] = label
    
    # 保存结果
    df.to_excel("试题_分类结果.xlsx", index=False)
    print("分类完成，结果已保存到 试题_分类结果.xlsx")

if __name__ == "__main__":
    main()
