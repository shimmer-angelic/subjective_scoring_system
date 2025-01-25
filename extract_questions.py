import pandas as pd
from bs4 import BeautifulSoup

def extract_questions(html_content):
    soup = BeautifulSoup(html_content, 'html.parser')
    
    questions = []
    for topic in soup.find_all('div', class_='topic'):
        question_data = {}
        
        # 提取题号和题目
        serial_span = topic.find('span', class_='serial')
        if serial_span:
            # 提取题号
            serial = serial_span.text.strip()
            question_data['题号'] = serial.replace('.', '')
            
            # 提取题目 - 查找题目文本
            question_span = serial_span.find_next_sibling('span')
            if question_span:
                # 获取题目文本并清理
                question_text = question_span.get_text(separator=' ').strip()
                # 去除多余空白
                question_text = ' '.join(question_text.split())
                question_data['题目'] = question_text
            else:
                question_data['题目'] = ''
        else:
            question_data['题号'] = ''
            question_data['题目'] = ''
        
        # 提取选项
        options = []
        option_div = topic.find('div', class_='option')
        if option_div:
            for option in option_div.find_all('div', class_='optionitem'):
                option_text = option.text.strip()
                options.append(option_text)
        question_data['选项'] = '\n'.join(options)
        
        # 提取考生作答
        response_div = topic.find('div', class_='respondence')
        if response_div:
            response = response_div.text.strip()
            question_data['考生作答'] = response.replace('考生作答:', '').strip()
        else:
            question_data['考生作答'] = ''
        
        questions.append(question_data)
    
    return pd.DataFrame(questions)

def save_to_excel(df, output_path):
    df.to_excel(output_path, index=False)

if __name__ == '__main__':
    # 读取试卷文件
    with open('试卷.doc', 'r', encoding='utf-8') as f:
        html_content = f.read()
    
    # 提取试题
    df = extract_questions(html_content)
    
    # 保存到Excel
    save_to_excel(df, '试题.xlsx')
    print("试题已成功提取并保存到 试题.xlsx")
