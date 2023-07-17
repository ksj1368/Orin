from django.contrib import admin
from . import models
# Register your models here.
class JasoseoAdmin(admin.ModelAdmin):
    list_display = ['get_title','get_user','get_category_name','created_at']    #list_display는 모델의 필드명 or 모델 어드민에서 정의된 메소드명만을 받음
    
    def get_title(self, obj):
        return obj.title
    get_title.short_description = '제목'
    
    def get_user(self, obj):
        return obj.user
    get_user.short_description = '사용자'
    
    def get_category_name(self, obj):
        return obj.category.category_name
    get_category_name.short_description = '카테고리'


class J_CategoryAdmin(admin.ModelAdmin):
    list_display = ['get_category_name', 'get_user']
    
    def get_user(self, obj):
        return obj.user
    get_user.short_description = '사용자'
    
    def get_category_name(self, obj):
        return obj.category_name
    get_category_name.short_description = '카테고리'

admin.site.register(models.Jasoseo,JasoseoAdmin)
admin.site.register(models.J_Category,J_CategoryAdmin)