import pandas as pd
import json
from openai import OpenAI, APIError, Timeout
from config import API_KEY,BASE_URL,MODEL
import logging

# 设置日志记录
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

# 读取标签
with open("标签.txt", "r", encoding="utf-8") as f:
    labels = [line.strip() for line in f.readlines()]

# 初始化deepseek客户端
client = OpenAI(api_key=API_KEY, base_url=BASE_URL)

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
        logging.info(f"开始分类题目: {question[:50]}...")
        response = client.chat.completions.create(
            model=MODEL,
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
            logging.info(f"分类结果: {result['label']}")
            return result["label"]
        else:
            raise ValueError("API返回结果为空")
    except APIError as api_err:
        logging.error(f"API错误: {str(api_err)}")
        return "未知"
    except Timeout as timeout_err:
        logging.error(f"请求超时: {str(timeout_err)}")
        return "未知"
    except ValueError as value_err:
        logging.error(f"值错误: {str(value_err)}")
        return "未知"
    except Exception as e:
        logging.error(f"分类失败: {str(e)}")
        return "未知"

def main():
    # 读取试题
    logging.info("开始读取试题文件")
    df = pd.read_excel("试题.xlsx")
    
    # 对每个题目进行分类
    logging.info("开始分类题目")
    df["分类"] = df.apply(lambda row: classify_question(row["题目"], row["选项"]), axis=1)
    
    # 保存结果
    logging.info("保存分类结果")
    df.to_excel("试题_分类结果.xlsx", index=False)
    logging.info("分类完成，结果已保存到 试题_分类结果.xlsx")

if __name__ == "__main__":
    main()
