from django import forms
from .models import Draft


class DraftForm(forms.ModelForm):
    question = forms.CharField(label='* 질문',
                               widget=forms.TextInput(
                                attrs={'placeholder': ' ex)  지원동기는 무엇인가요?'}))
    office = forms.CharField(label='* 회사',
                               widget=forms.TextInput(
                                attrs={'placeholder': ' ex)  Orin'}))
    position = forms.CharField(label='* 포지션',
                               widget=forms.TextInput(
                                attrs={'placeholder': ' ex)  백엔드 개발자'}))
    num = forms.CharField(label='* 글자 수',
                               widget=forms.TextInput(
                                attrs={'placeholder': ' ex)  500'}))
    experience = forms.CharField(label='* 경험 1',
                                widget=forms.TextInput(
                                attrs={'placeholder': '경험 1'}))
    experience2 = forms.CharField(label='경험 2   ',
                                  required=False,
                                widget=forms.TextInput(
                                attrs={'placeholder': '경험 2 (선택)'}))
    experience3 = forms.CharField(label='경험 3   ',
                                  required=False,
                                widget=forms.TextInput(
                                attrs={'placeholder': '경험 3 (선택)'}))
    

    class Meta:
        model = Draft
        fields = ('question', 'office', 'position', 'num', 'experience', 'experience2', 'experience3')