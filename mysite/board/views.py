from django.shortcuts import render, get_object_or_404, redirect
from django.utils import timezone
from django.urls import reverse
from .models import Question, Answer, Category
from common.models import User
import os
from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator
from .decorators import *
from django.http import JsonResponse
from django.forms.models import model_to_dict
from .decorators import *

# 인덱스 페이지
def index(request):
    return render(request,'board/index.html')

## 모든 질문 목록
@login_message_required
def qna_list(request):
    question_list = Question.objects.all().order_by("-pk")
    context = display_paginated(request, question_list)
    return render(request, 'board/qna_page.html', {'context': context})

# 페이지 내부 페이지 번호 구현
def display_paginated(request, data_query):
    max_list_cnt = 10
    max_page_cnt = 10
    
    page = request.GET.get('page', "1")  # 페이지
    paginator = Paginator(data_query, max_list_cnt)  # 페이지당 10개씩 보여주기
    page_obj = paginator.get_page(page)
    
    last_page_num = 0

    for last_page in paginator.page_range:
        last_page_num = last_page_num + 1

    current_block = ((int(page)-1) / max_page_cnt) + 1
    current_block = int(current_block)
    
    page_start_number = ((current_block -1 ) *max_page_cnt) +1
    
    page_end_number = page_start_number + max_page_cnt -1
    
    context = {
        'memo_list' : page_obj,
        'last_page_num' : last_page_num,
        'page_start_number' : page_start_number,
        'page_end_number' : page_end_number,
    }
    return context

## 질문 세부사항 확인하기
@login_required
def question2(request, pk):
    post = Question.objects.filter(pk=pk)
    user_level = request.user.level
    post_dict = model_to_dict(post)
    if post.image:
        post_dict['image'] = post.image.url  
    post_dict['user'] = post.user_id
    post_dict['category'] = post.category.name 
    
    # 질문 답변이 있을 경우
    if Answer.objects.filter(question=pk).exists():
        answer_list = Answer.objects.filter(question=pk)
        answer_list_dict = []
        
        for answer in answer_list:
            answer_dict = model_to_dict(answer)
            answer_dict['user'] = answer.user.user_id 
            answer_dict['question'] = answer.question.id  
            answer_list_dict.append(answer_dict)

        return JsonResponse({
            'question': post_dict,
            'answer_list': answer_list_dict,
            'user_level': user_level
        }, safe=False)
    # 질문 답변이 없을 경우
    else:
        return JsonResponse({
            'question': post_dict,
            'user_level': user_level
        }, safe=False)

# 문의 하기 내용
@login_required
def question(request, pk):
    post = Question.objects.get(pk=pk)
    user_level = request.user.level
    if Answer.objects.filter(question = pk) is not None:
        answer_list = Answer.objects.filter(question = pk)
        return render(request, 'board/question_page.html', {'question':post, "answer_list" : answer_list, "user_level" : user_level})
    else:
        return JsonResponse({'question':post, "user_level" : user_level},safe=False)
        
# 내 질문 목록
@login_required
def my_qna(request):
    my_question_list = Question.objects.filter(user_id = request.user.id).order_by("-pk")
    context = display_paginated(request, my_question_list)
    return render(request, 'board/my_qna_page.html', {'context':context})

# 답변 생성
@admin_required
def create_answer(request, pk): 
    question = Question.objects.get(pk = pk)
    if request.method == "POST":
        comment = Answer.objects.create(
        content = request.POST['content'],
        user = User.objects.get(pk= request.user.id),
        question = Question.objects.get(pk=pk), 
        created_at = timezone.now(),
        )
        comment.save()
        return redirect(reverse('board:question2', kwargs={'pk': str(pk)}))
    return render(request, 'board/create_answer_page.html', {"question" : question})

# 질문 생성
@login_required
def create_question(request):
    category_list = Category.objects.all()
    if request.method == 'POST':
        # 첨부 파일 이미지가 있을 경우
        if request.FILES.get('image'):
            new_question = Question.objects.create(
                postname = request.POST['postname'],
                user = User.objects.get(pk= request.user.id),
                contents = request.POST['contents'],
                
                category = Category.objects.get(name = request.POST['category']),
                image = request.FILES.get('image'),
                created_at = timezone.now(),
            )
        # 첨부 파일이 없을 경우
        else:
            new_question = Question.objects.create(
                postname = request.POST['postname'],
                user = User.objects.get(pk= request.user.id),
                contents = request.POST['contents'],
                category = Category.objects.get(name = request.POST['category']),
                image = "",
                created_at = timezone.now(),
            )
        new_question.save()
        return redirect('board:qna')
    return render(request, 'board/create_question_page.html',{'category_list':category_list})


# 질문 수정
@login_required
def modify_question(request, pk):
    category_list = Category.objects.all()
    mod_question = get_object_or_404(Question, id=pk)

    # 유저 id가 다를 경우 수정을 못하게 함
    if mod_question.user_id != request.user.id:
        return redirect(reverse('board:question2', kwargs={'pk': str(pk)}))

    if request.method == 'POST':
        postname = request.POST['postname']
        contents = request.POST['contents']
        category_name = request.POST['category']
        
        mod_question.postname = postname
        mod_question.contents = contents
        mod_question.category = Category.objects.get(name=category_name)
        
        # 수정한 내용에 이미지를 수정했을 경우
        if request.FILES.get('image'):
            image = request.FILES.get('image')
            mod_question.image = image
    
        mod_question.save()

        return redirect(reverse('board:question2', kwargs={'pk': str(pk)}))

    return render(request, 'board/modify_question_page.html', {'post': mod_question, 'category_list': category_list})

