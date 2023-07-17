from django.shortcuts import render, redirect
from django.utils.decorators import method_decorator
from common.decorators import subscribe_message_required
from .forms import DraftForm
from django.contrib import messages
from django.utils.html import escape
import openai
from bardapi import Bard
from django.conf import settings

# Create your views here.
token=settings.BARD_KEY
# chatGPT에게 채팅 요청 API
def chatGPT(prompt, num):
    openai.api_key = settings.OPENAI_KEY
    model_name = 'gpt-3.5-turbo'

    modified_prompt = prompt
    # GPT 모델에 요청하여 출력 생성
    response = openai.ChatCompletion.create(
        model=model_name,
        messages=[
            {
                'role': 'system',
                'content': f'한국 인사담당자가 좋아하는 자기 소개서를 반드시 글자수 {num}자에 가깝게 끝나는 내용으로 생성'
            },
            {
                'role': 'user',
                'content': modified_prompt
            }
        ],
        max_tokens=2048,
        temperature=0.7
    )

    print(response)
    result = response.choices[0].message.content.strip()
    return result
# BARD에게 채팅 요청 API
def bard(prompt):
    bard = Bard(token=token)
    result = bard.get_answer(prompt)['content']
    return result

@subscribe_message_required
def draft_create(request):
    if request.method == 'POST':
        form = DraftForm(request.POST)
        # model = request.POST.get('model')
        if form.is_valid():
            essay_prompt = form.cleaned_data['question']
            company_name = form.cleaned_data['office']
            position = form.cleaned_data['position']
            num = form.cleaned_data['num']
            e1 = form.cleaned_data['experience']
            e2 = form.cleaned_data.get('experience2', '없습니다.')
            e2_p = e2
            e3 = form.cleaned_data.get('experience3', '없습니다.')
            e3_p = e3
            if len(e2) > 0:
                e2_p = f'내 경험2: {e2}'
            if len(e3) > 0:
                e3_p = f'내 경험3: {e3}'
            prompt1 = f"자기소개서 문항: {essay_prompt}에 대해 {num}자로 작성\n 내 경험1: {e1}\n"
            prompt2 = e2_p + "\n" + e3_p + "\n\n" + f"{company_name} 회사의 {position} 직무에 맞춰서\n 내 경험을 벗어나지 않는 자기소개서를 자연스럽게 작성.\n\n아래 4가지에 대한 내용은 언급하지 않음 \n1. 대학교 \n2. 대학원\n3. 전공\n4. 나이"

            prompt = prompt1 + prompt2
            output_chat = chatGPT(prompt, num)

            try:
                output_bard = bard(prompt)
            except Exception as e:
                if str(e) == "SNlM0e value not found in response. Check __Secure-1PSID value.":
                    
                    output_bard = "Bard Key가 만료되었습니다. 문의 바랍니다."
                else:
                    print("다른 예외가 발생했습니다:", str(e))
                    
            output_bard_safe = escape(output_bard)
            output_chat_safe = escape(output_chat)
            
            output_bard_safe = str(output_bard_safe).replace('\r\n', '<br>')
            output_bard_safe = str(output_bard_safe).replace('\n', '<br>')
            output_chat_safe = str(output_chat_safe).replace('\r\n', '<br>')
            output_chat_safe = str(output_chat_safe).replace('\n', '<br>')
            
            context = {
                'question': essay_prompt,
                'office': company_name,
                'position': position,
                'num' : num,
                'experience': e1,
                'experience2': e2,
                'experience3': e3,
                'output_chat': output_chat_safe,
                'output_bard': output_bard_safe,
            }
            
            return render(request,'draft/result.html', context)
        else:
            messages.info(request, '입력된 내용이 없습니다.')
            return redirect('draft:createdraft')
    else:
        form = DraftForm()
    return render(request, 'draft/create_draft.html', {'form': form})