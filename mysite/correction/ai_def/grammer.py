from .py_hanspell_master.hanspell import spell_checker
import re

# 1. 특수기호 제거 및 띄어쓰기 전처리
def preprocessing(text):
    # text = re.sub(r"\n+", "", text)
    text = re.sub(r" +", " ", text).strip()
    return text


# 2. 맞춤법 검사
def grammer(preprocessed_text):        
    result = spell_checker.check(preprocessed_text)
    return result


# 3. 전체
def cat_grammer(text):
    preprocessed_text = preprocessing(text)
    sentence_list = preprocessed_text.split('.')

    max_length = 500
    
    result = ''
    for sentence in sentence_list:
        while len(sentence) > max_length:   # 한 문장이 500자 이상일 경우 자름
            part, sentence = sentence[:max_length], sentence[max_length:]
            result+=grammer(part)

        result += grammer(sentence) + str('.')

    return result[:-1]
