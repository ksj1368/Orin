from django.db import models
from common.models import User
    
    
class J_Category(models.Model):
    category_name = models.CharField(max_length=20)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    def __str__(self):
        return self.category_name
        
class Jasoseo(models.Model):
    title = models.CharField(max_length=45)
    content = models.TextField(max_length=3000)
    jasoseo_length = models.IntegerField()
    created_at = models.DateTimeField(auto_now_add=True)
    category = models.ForeignKey("J_Category",db_column="category_id", on_delete = models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    
    def __str__(self):
        return self.title
