from .ai_def.grammer import cat_grammer
from .ai_def.synonym_word import synonym_noun
from .ai_def.coaching import coaching
from .ai_def.bad_thing_gpt import bad_thing
## 맞춤법 교정 
def cat_grammar_final(text):
    output = cat_grammer(text)
    return output

## 유의어 크롤링 및 반환
def synonym_word_final(word): 
    output = synonym_noun(word)
    return output

## 단어 좋은 점,아쉬운 점 코칭
def coaching_final(text):
    output = coaching(text)
    return output

## 문맥 아쉬운 점 코칭 GPT
def bad_thing_final(text):
    output = bad_thing(text)
    return output
