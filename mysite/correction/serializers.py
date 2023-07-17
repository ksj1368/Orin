from rest_framework import serializers
from .models import J_Category, Jasoseo

#질문 - image 제외
class JasoseoSerializer(serializers.ModelSerializer):
    class Meta:
        model = Jasoseo
        fields = ['title', 'content', 'jasoseo_length', 'category', 'created_at','user']
    
    def create(self, validated_data):
        request = self.context.get('request')  # context에서 request 가져오기
        category_name = request.data.get('category')
        user = request.user
        category, _ = J_Category.objects.get_or_create(category_name=category_name, user=user)[0]
        # validated_data를 업데이트하여 필요한 정보 추가
        validated_data.update({
            'jasoseo_length': len(validated_data.get('content')),
            'category': category,
            'user': user
        })
        return super().create(validated_data)

