from django.urls import path,include
from . import views

app_name = 'correction'
urlpatterns = [
    path('', views.index,name = 'index'),
    path('correct/', views.correct, name = 'correct'),
    path('correct/categories/',views.categories,name = 'categories'),
    path('category/delete/<int:pk>/',views.j_category_delete ,name = 'j_category_delete'),
    path('synonyms/', views.get_synonyms, name = 'synonyms'),
    path('correct/savejasoseo/', views.mypage_save,name = 'mypage_save'),
    path('correct/coaching/', views.get_coaching,name = 'get_coaching'),
    path('download/', views.download_docs,name = 'download_docs'),
    path('my_manage/', views.my_manage,name = 'my_manage'),
    path('my_manage/<int:pk>/', views.my_manage_detail, name = 'my_manage_detail'),
    path('my_manage/<int:pk>/delete/', views.my_jasoseo_delete, name = 'my_jasoseo_delete'),
    path('my_manage/<int:pk>/modify/', views.my_jasoseo_modify, name = 'my_jasoseo_modify'),      
    path('my_manage/create_jasoseo/', views.create_jasoseo, name = 'create_jasoseo'),    
]
