from django.shortcuts import render, redirect
from django.http import HttpResponseRedirect, Http404
from django.contrib.auth.models import User
from django.contrib import auth
from django.urls import reverse

from django.utils.decorators import method_decorator
from django.utils import timezone
from .decorators import *
from .models import User
from django.views.generic import View
from django.contrib import messages

from django.core.exceptions import PermissionDenied
from .forms import CsRegisterForm
from django.views.generic import CreateView

from .forms import LoginForm
from django.contrib.auth import login, authenticate
from django.views.generic import FormView
from django.conf import settings
from django.contrib.auth import logout
from .forms import RecoveryIdForm
from django.views.generic import View
from .forms import RecoveryPwForm, CustomSetPasswordForm, CustomPasswordChangeForm, CustomCsUserChangeForm
from .forms import CheckPasswordForm
from .helper import email_auth_num
from django.contrib.auth import update_session_auth_hash

# SMTP 관련 인증
from django.contrib.sites.shortcuts import get_current_site
from django.template.loader import render_to_string
from django.utils.http import urlsafe_base64_encode,urlsafe_base64_decode
from django.core.mail import EmailMessage
from django.utils.encoding import force_bytes, force_str
from django.contrib.auth.tokens import default_token_generator
from .helper import send_mail
 
def register_success(request):
    if not request.session.get('register_auth', False):
        raise PermissionDenied
    request.session['register_auth'] = False

    return render(request, 'common/register_success.html')

class RegisterView(CreateView):
    model = User
    template_name = 'common/signup.html'
    form_class = CsRegisterForm

    def get_success_url(self):
        # messages.success(self.request, "회원가입 성공.")
        self.request.session['register_auth'] = True
        messages.success(self.request, '회원님의 입력한 Email 주소로 인증 메일이 발송되었습니다. 인증 후 로그인이 가능합니다.')
        # return settings.LOGIN_URL
        return reverse('common:register_success')

    def form_valid(self, form):
        self.object = form.save()

        send_mail(
            '{}님의 회원가입 인증메일 입니다.'.format(self.object.user_id),
            [self.object.email],
            html=render_to_string('common/register_email.html', {
                'user': self.object,
                'uid': urlsafe_base64_encode(force_bytes(self.object.pk)).encode().decode(),
                'domain': self.request.META['HTTP_HOST'],
                'token': default_token_generator.make_token(self.object),
            }),
        )
        return redirect(self.get_success_url())
    
def activate(request, uid64, token):
    try:
        uid = force_str(urlsafe_base64_decode(uid64))
        current_user = User.objects.get(pk=uid)
    except (TypeError, ValueError, OverflowError, User.DoesNotExist, ValidationError):
        messages.error(request, '메일 인증에 실패했습니다.')
        return redirect('common:login')

    if default_token_generator.check_token(current_user, token):
        current_user.is_active = True
        current_user.save()

        messages.info(request, '메일 인증이 완료 되었습니다. 회원가입을 축하드립니다!')
        return redirect('common:login')

    messages.error(request, '메일 인증에 실패했습니다.')
    return redirect('common:login') 

@method_decorator(logout_message_required, name='dispatch')
class LoginView(FormView):
    template_name = 'common/login.html'
    form_class = LoginForm
    success_url = '/orin/'

    def form_valid(self, form):
        user_id = form.cleaned_data.get("user_id")
        password = form.cleaned_data.get("password")
        user = authenticate(self.request, username=user_id, password=password)
        
        if user is not None:
            self.request.session['user_id'] = user_id
            login(self.request, user, backend='django.contrib.auth.backends.ModelBackend')
            remember_session = self.request.POST.get('remember_session', False)
            if remember_session:
                settings.SESSION_EXPIRE_AT_BROWSER_CLOSE = False

        return super().form_valid(form)


def logout_view(request):
    logout(request)
    return redirect('/') 

@method_decorator(logout_message_required, name='dispatch')
class RecoveryIdView(View):
    template_name = 'common/recovery_id.html'
    recovery_id = RecoveryIdForm

    def get(self, request):
        if request.method=='GET':
            form_id = self.recovery_id(None)
        return render(request, self.template_name, { 'form_id':form_id, })
    
import json
from django.core.serializers.json import DjangoJSONEncoder

def ajax_find_id_view(request):
    name = request.POST.get('name')
    email = request.POST.get('email')
    result_id = User.objects.get(name=name, email=email)
       
    return HttpResponse(json.dumps({"result_id": result_id.user_id}, cls=DjangoJSONEncoder), content_type = "application/json")

@method_decorator(logout_message_required, name='dispatch')
class RecoveryPwView(View):
    template_name = 'common/recovery_pw.html'
    recovery_pw = RecoveryPwForm

    def get(self, request):
        if request.method=='GET':
            form_pw = self.recovery_pw(None)
            return render(request, self.template_name, { 'form_pw':form_pw, })

def ajax_find_pw_view(request):
    user_id = request.POST.get("user_id")
    name = request.POST.get("name")
    email = request.POST.get("email")
    result_pw = User.objects.get(user_id=user_id, name=name, email=email)

    if result_pw:
        auth_num = email_auth_num()
        result_pw.auth = auth_num 
        result_pw.save()

        send_mail(
            '비밀번호 찾기 인증메일입니다.',
            [email],
            html=render_to_string('common/recovery_email.html', {
                'auth_num': auth_num,
            }),
        )
    return HttpResponse(json.dumps({"result": result_pw.user_id}, cls=DjangoJSONEncoder), content_type = "application/json")

def auth_confirm_view(request):
    user_id = request.POST.get('user_id')
    input_auth_num = request.POST.get('input_auth_num')
    user = User.objects.get(user_id=user_id, auth=input_auth_num)
    user.auth = ""
    user.save()
    request.session['auth'] = user.user_id  
    
    return HttpResponse(json.dumps({"result": user.user_id}, cls=DjangoJSONEncoder), content_type = "application/json")
    
@logout_message_required
def auth_pw_reset_view(request):
    if request.method == 'GET':
        if not request.session.get('auth', False):
            raise PermissionDenied

    if request.method == 'POST':
        session_user = request.session['auth']
        current_user = User.objects.get(user_id=session_user)
        login(request, current_user, backend='django.contrib.auth.backends.ModelBackend')

        reset_password_form = CustomSetPasswordForm(request.user, request.POST)
        
        if reset_password_form.is_valid():
            user = reset_password_form.save()
            messages.success(request, "비밀번호 변경완료! 변경된 비밀번호로 로그인하세요.")
            logout(request)
            return redirect('common:login')
        else:
            logout(request)
            request.session['auth'] = session_user
    else:
        reset_password_form = CustomSetPasswordForm(request.user)

    return render(request, 'common/password_reset.html', {'form':reset_password_form})

@login_message_required
def password_edit_view(request):
    if request.method == 'POST':
        password_change_form = CustomPasswordChangeForm(request.user, request.POST)
        if password_change_form.is_valid():
            user = password_change_form.save()
            update_session_auth_hash(request, user)
            messages.success(request, "비밀번호를 성공적으로 변경하였습니다.")
            return redirect('common:my_profile')
    else:
        password_change_form = CustomPasswordChangeForm(request.user)

    return render(request, 'common/my_profile_password.html', {'password_change_form':password_change_form})


@login_message_required
def my_profile_view(request):
    if request.method == 'GET':
        password_form = CheckPasswordForm(request.user, request.POST)
        render(request,  'common/my_profile.html', {'password_form':password_form})
    
    elif request.method == 'POST':
        password_form = CheckPasswordForm(request.user, request.POST)
        
        if password_form.is_valid():
            request.user.delete()
            logout(request)
            messages.success(request, "회원탈퇴가 완료되었습니다.")
            return redirect('/common/login/')
        else:
            messages.error(request, "비밀번호가 틀렸습니다.")
            return render(request,  'common/my_profile.html', {'password_form':password_form})
    else:
        password_form = CheckPasswordForm(request.user)

    return render(request,  'common/my_profile.html', {'password_form':password_form})
    
def my_profile_update_view(request):
    if request.method == 'POST':
        user_change_form = CustomCsUserChangeForm(request.POST, instance=request.user)
        
        if user_change_form.is_valid():
            user_change_form.save()
            messages.success(request, '회원정보가 수정되었습니다.')
            return render(request, 'common/my_profile.html')
        else:
            messages.error(request, '전화번호를 다시 확인해주세요.')  # 에러 메시지 추가
    else:
        user_change_form = CustomCsUserChangeForm(instance = request.user)
        
    return render(request, 'common/my_profile_update.html', {'user_change_form':user_change_form})
    
@login_message_required
def my_profile_delete_view(request):
    if request.method == 'POST':
        password_form = CheckPasswordForm(request.user, request.POST)
        
        if password_form.is_valid():
            request.user.delete()
            logout(request)
            messages.success(request, "회원탈퇴가 완료되었습니다.")
            return redirect('/common/login/')
    else:
        password_form = CheckPasswordForm(request.user)

    return render(request, 'common/my_profile_delete.html', {'password_form':password_form})

@login_message_required
def my_profile_delete_social_view(request):
    if request.method == 'POST':
        password_form = CheckPasswordForm(request.user, request.POST)
        
        if password_form.is_valid():
            request.user.delete()
            logout(request)
            messages.success(request, "회원탈퇴가 완료되었습니다.")
            return redirect('/common/login/')
    else:
        password_form = CheckPasswordForm(request.user)

    return render(request, 'common/my_profile_delete.html', {'password_form':password_form})

@unsubscribe_message_required
def subscribe_view(request):
    if request.method == 'POST':
        user_id = request.POST.get('user_id')
        user_profile = User.objects.get(user_id=user_id)
        user_profile.subscribe = 1
        user_profile.subscribe_joined = timezone.now()
        user_profile.save()
        return redirect('common:my_profile')  # 버튼 클릭 후 리디렉션할 페이지 설정

    return render(request, 'common/subscribe.html')

@subscribe_message_required
def unsubscribe_view(request):
    if request.method == 'POST':
        user_id = request.POST.get('user_id')
        user_profile = User.objects.get(user_id=user_id)
        user_profile.subscribe = 0
        user_profile.subscribe_joined = None
        user_profile.save()
        return redirect('common:my_profile')  # 버튼 클릭 후 리디렉션할 페이지 설정

    return render(request, 'common/unsubscribe.html')