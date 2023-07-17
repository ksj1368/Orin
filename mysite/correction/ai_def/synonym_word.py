import requests, re
from bs4 import BeautifulSoup
from mecab import MeCab
from concurrent.futures import ThreadPoolExecutor

## 1. 명사, 부사 추출
def token_noun(text):
    mecab = MeCab()
    tagged_text = mecab.pos(text)
    # 일반명사, 고유명사, 대명사, 일반 부사, 접속 부사 추출
    nouns = [word for word, pos in tagged_text if pos in ['NNG', 'NNP', 'NP','MAJ','MAG']]     
    return nouns

## 2. 네이버 사전 유의어 크롤링
def synonym_word(word): 
    url = f"https://dict.naver.com/search.dict?dicQuery={word}&query={word}&target=dic&ie=utf8&query_utf=&isOnlyViewEE="
    response = requests.get(url)
    soup = BeautifulSoup(response.content, "html.parser")

    result = []
    try:
        soup = soup.select_one('#content > div.kr_dic_section.search_result.dic_kr_entry > ul > li:nth-child(1)')
        a_soup = soup.find_all('a', {'class':'syno'})
        for a in a_soup:
            word = re.sub(r'\d+', '', str(a.get_text()))
            result.append(word)  
    except:
        return []
    return result


## 3. 유의어 추출
def synonym_noun(text):
    noun_list = token_noun(text)
    noun_synonym_list = []

    with ThreadPoolExecutor() as executor:
        futures = [executor.submit(synonym_word, noun) for noun in noun_list]
        for future, noun in zip(futures, noun_list):
            result = future.result()
            if result:
                noun_synonym_list.append([noun, result])
            if len(noun_synonym_list) >= 3:
                return noun_synonym_list
    return noun_synonym_list