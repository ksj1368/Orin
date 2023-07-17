from django.urls import path

from . import views
from django.conf.urls.static import static
from django.conf import settings

app_name='board'

urlpatterns = [
    path('qna/', views.qna_list, name='qna'),
    path('qna/<int:pk>/',views.question, name="question2"),
    path('qna/create_question/', views.create_question, name = "create_question"),
    path('qna/modify_question/<int:pk>/', views.modify_question, name='modify_question'),
    path('create_answer/<int:pk>/', views.create_answer, name = "create_answer"),
    path('my_qna/', views.my_qna, name = "my_qna"),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT) 
