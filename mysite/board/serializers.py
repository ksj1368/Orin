from rest_framework import serializers
from .models import Question,Answer

#질문 - image 제외
class BaseQuestionSerializer(serializers.ModelSerializer):
    userId = serializers.CharField(source='user.user_id')   # view에 반드시 select_related 해줘야함
    class Meta:
        model = Question
        fields = ['id','postname', 'contents', 'created_at', 'updated_at','category', 'userId'] 

#질문 - image 포함
class ImageQuestionSerializer(BaseQuestionSerializer):
    class Meta(BaseQuestionSerializer.Meta):
        fields = BaseQuestionSerializer.Meta.fields + ['image']

#답변
class AnswerSerializer(serializers.ModelSerializer):
    userId = serializers.CharField(source='user.user_id')

    class Meta:
        model = Answer
        fields = ['id','created_at', 'updated_at','content', 'question', 'userId']