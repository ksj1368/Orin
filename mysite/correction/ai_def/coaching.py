import re

def good_1(text):
    # 숫자 리스트
    nums = re.findall(r"\b(\d+)[^\d.'단계''대')]", text)

    if len(nums) >= 2:
        return "숫자 활용(수치 등)을 통해 자기소개서가 더 구체적, 객관적으로 느껴져요."
    return ''


def good_2(text):
    pattern = r'첫[ ]?번째로|두[ ]?번째로|첫째로|둘째로|첫[ ]?째|둘[ ]?째'
    matches = re.findall(pattern, text)

    if len(matches) >= 2:
        return '"첫째, 둘째"같은 번호가 있어서 읽기 쉬워요.' 
    return ''


def good_3(text):
    sentences = text.split('.')                 # 문장 분리
    sentences = [s + '.' for s in sentences]    # 문장별 . 추가
    sentences = [s.strip() for s in sentences]  # 문장 앞 뒤 공백 제거

    count = sum(1 for s in sentences if s.endswith('때문입니다.'))
    if count >= 1:
        return "서술한 내용의 이유가 명확해서 설득력이 있어 보여요."
    return ''



def check(text, bad_words):
    bad_list = []            # bad_words 리스트 안의 모든 단어 count 3개 이상
    bad_word_list = []       # 특정 단어 count
    cnt = 0
    for bad_word in bad_words:
        bad_word_cnt = text.count(bad_word)   # 특정 단어 개수
        cnt += bad_word_cnt         
        if bad_word_cnt > 0:                  # 특정 단어가 1번 이상
            bad_word_list.append(bad_word)
        if cnt >= 3:                          # bad_words 리스트 안의 단어들이 3번 이상
            bad_list.extend(bad_word_list)
            bad_list = list(set(bad_list))
    return bad_list

def bad_1(text):
    bad_lists = []

    ## 2. bad_word 3번 이상
    bad_words_1 = ['이에', '이를', '그런', '이러한', '이런', '그러한', '그에']
    bad_words_2 = ['그리고', '하지만', '또', '또한']
    bad_words_3 = ['저는', '제가', '저 ', '저의']
    
    ## 1. 빈 줄을 기준으로 문단 분리
    paragraphs = text.split('\n\n')  
    for paragraph in paragraphs:
        # 문단별 bad_word 개수
        bad_lists.extend(check(paragraph, bad_words_1))
        bad_lists.extend(check(paragraph, bad_words_2))
        bad_lists.extend(check(paragraph, bad_words_3))
    
    if len(bad_lists) != 0:
        return f'글의 원활한 흐름을 위해 {list(set(bad_lists))}과(와) 같은 표현은 한 단락에 3번 이하로 작성해보세요.'
    return ''


def bad_2(text):
    bad_list = []
    paragraph_bad_word = []
    ## 1. 빈 줄을 기준으로 문단 분리
    paragraphs = text.split('\n\n')  

    ## 2. bad_word 3번 이상
    bad_words = ['다양', '꽤', '상당', '꾸준', '매우', '굉장', '엄청', '충분', '여러', '항상', '뜻깊은', '여러', '더욱', '대부분', '거의', '어느정도', '어느 정도']
    for paragraph in paragraphs:
        # 문단별 bad_word 개수
        cnt = 0
        for bad_word in bad_words:
            bad_word_cnt = paragraph.count(bad_word)
            cnt += bad_word_cnt
            if bad_word_cnt > 0:
                paragraph_bad_word.append(bad_word)
        # 문단별 bad_word 개수 1개 이상이면 출력        
        if cnt >= 1:
            bad_list.extend(paragraph_bad_word)
    if len(bad_list) != 0:
        return f'경험을 입증하거나 설명할 때는 구체적인 근거나 정확한 수치를 사용해보세요. ex) {list(set(bad_list))}'
    return ''


def bad_3(text):
    bad_list = []
    # 일상말투
    words = ['있다는 걸', '뭐든', '저에겐', '처음엔', '한테', '있는게', '좀']
    cnt = 0
    for word in words:
        bad_word_cnt = text.count(word)
        cnt += bad_word_cnt
        if bad_word_cnt > 0:
            bad_list.append(word)
    if cnt > 0:
        return f'{bad_list}과(와) 같은 일상적 말투를 문어체로 바꿔보세요.'
    return ''


def bad_4(text):
    cnt = 0
    # 한 문장에 130자 이상
    sentences = text.split('.')
    for sentence in sentences:
        if len(sentence) >= 130:
            cnt += 1
    if cnt > 0:    
        return '가독성을 높이기 위해 긴 문장은 간결하게 줄여보세요.'
    return ''


def bad_5(text):
    bad_list = []
    words = ['생각합니다', '같습니다']
    cnt = 0
    for word in words:
        bad_word_cnt = text.count(word)
        cnt += bad_word_cnt
        if bad_word_cnt > 0:
            bad_list.append(word)
    if cnt > 0:
        return f"{list(set(bad_list))}과(와) 같은 일상적 말투를 문어체로 바꿔보세요."
    return ''


def bad_6(text):
    bad_list = []
    words = ['되었습니다', '됐습니다']
    cnt = 0
    for word in words:
        bad_word_cnt = text.count(word)
        cnt += bad_word_cnt
        if bad_word_cnt > 0:
            bad_list.append(word)
    if cnt > 0:
        return f"{list(set(bad_list))}과(와) 같은 수동적인 말투를 능동적인 말투로 바꿔보세요."
    return ''


def bad_7(text):
    cnt = 0
    # 한 문단에 7문장 이상
    sentences = text.split('.')
    paragraph_sentence_len = len(sentences)
    if paragraph_sentence_len > 7:
        cnt += 1
    if cnt > 0:    
        return '가독성을 높이기 위해 7문장 내외로 문단을 구성해보세요.'
    return ''


def coaching(text):
    good_funcs = [good_1, good_2, good_3]
    bad_funcs = [bad_1, bad_2, bad_3,bad_4, bad_5, bad_6]
    
    good_list = [result for func in good_funcs if (result := func(text))] # 빈문자열 아닌 것만
    bad_list = [result for func in bad_funcs if(result := func(text))]

    return {'good': good_list, 'bad': bad_list}