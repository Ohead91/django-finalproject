from wsgiref.util import request_uri
from shortener.forms import RegisterForm
from shortener.models import Users
from django.shortcuts import redirect, render
from django.contrib.auth import login, authenticate, logout
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator


from django.views.decorators.csrf import csrf_exempt
from django.http import JsonResponse

# Create your views here.
def index(request):
    
    user = Users.objects.filter(username="admin").first()
    email = user.email if user else "Anonymous User"
    print("Logged in?", request.user.is_authenticated)
    # print(request.user.)

    if request.user.is_authenticated is False:
        email = "Anonymous User"
    print(email)
    return render(request, "index.html", {"welcome_msg": f"Hello {email} Daeho!", "hello":"world" })
 
@csrf_exempt
def get_user(request, user_id):
    print(user_id)
    if request.method == "GET":
        abc = request.GET.get("abc")
        xyz = request.GET.get("xyz")
        user = Users.objects.filter(pk=user_id).first()
        return render(request, "base.html", {"user": user, "params": [abc, xyz] })
    elif request.method == "POST":
        username = request.GET.get("username")
        if username:
            user = Users.objects.filter(pk=user_id).update(username=username)

            return JsonResponse(dict(msg="You Just reached with Post Method!"))

def register(request):
    if request.method == "POST":
        form = RegisterForm(request.POST)
        msg = "올바르지 않은 데이터입니다."
        if form.is_valid():
            form.save()
            username = form.cleaned_data.get("username")
            raw_password = form.cleaned_data.get("password1")
            user = authenticate(username=username, password=raw_password)
            login(request, user)
            msg = "회원가입 완료"
        return render(request, "register.html", {"form":form, "msg":msg})
    else:
        form = RegisterForm()
        return render(request, "register.html", {"form":form})

def login_view(request):
    if request.method == "POST":
        form = AuthenticationForm(request, request.POST)
        msg = "가입되어 있지 않거나 로그인 정보가 잘못되었습니다"
        if form.is_valid():
            username = form.cleaned_data.get("username")
            raw_password = form.cleaned_data.get("password")
            user = authenticate(username=username, password=raw_password)
            if user is not None:
                msg = "로그인 성공"
                login(request, user)
                return redirect("index")
        return render(request, "login.html", {"form":form, "msg":msg})
    else:
        form = AuthenticationForm()
        return render(request, "login.html", {"form":form})

def logout_view(request):
    logout(request)
    return redirect("index")

@login_required
def list_view(request):
    page = int(request.GET.get("p", 1))
    users = Users.objects.all().order_by("id")
    paginator = Paginator(users, 3)
    user = paginator.get_page(page)

    return render(request, "boards.html", {"users":users})
    