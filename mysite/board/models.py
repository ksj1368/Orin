from django.db import models
from common.models import User

class Category(models.Model):
    name = models.CharField(max_length=12, unique=True, primary_key= True)
    def __str__(self): 
        return self.name
    
class Question(models.Model):
    postname = models.CharField(max_length=30)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    category = models.ForeignKey("Category",related_name="category_id", on_delete=models.CASCADE, db_column="category", default='') 
    image = models.ImageField(upload_to = "", blank=True, null=True)
    contents = models.TextField()
    created_at = models.DateTimeField(auto_now_add= True)
    updated_at = models.DateTimeField(auto_now = True)   
    
    def __int__(self):
        return self.postname
    
class Answer(models.Model):
    created_at = models.DateTimeField(auto_now_add= True)
    updated_at = models.DateTimeField(auto_now = True)    
    question = models.ForeignKey("Question",related_name="question_id", on_delete=models.CASCADE, db_column="question") 
    content = models.TextField()
    user = models.ForeignKey(User, on_delete=models.CASCADE)

