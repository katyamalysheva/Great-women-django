
from django.http import HttpResponse, HttpResponseNotFound, Http404
from django.shortcuts import render, redirect ,get_object_or_404
from django.views.generic import ListView, DetailView, CreateView
from .forms import AddPostForm, RegisterUserForm
from django.urls import reverse_lazy
from .models import *
from .utils import *
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator


class WomenHome(DataMixin, ListView):
    
    model = Women
    template_name = 'women/index.html'
    context_object_name = 'posts'
    paginate_by = 2

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        c_def = self.get_user_context(title = 'Главная страница')
        return dict(list(context.items()) + list(c_def.items() ))

    def get_queryset(self):
        return Women.objects.filter(is_published=True)
    
'''def index(request): #HttpRequest
    posts = Women.objects.all()
    #cats = Category.objects.all()
    context = {
        'title': 'Главная страница',  
        'posts': posts ,
        'cat_selected': 0, 
    }
    return render(request, 'women/index.html', context = context)
'''

#@login_required 
def about(request): #HttpRequest
    contact_list= Women.objects.all()
    paginator = Paginator(contact_list, 3)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    
    return render(request, 'women/about.html', {'page_obj':page_obj, 'menu': menu, 'title': 'О странице'})


class AddPage( LoginRequiredMixin, DataMixin, CreateView):
    form_class = AddPostForm
    template_name = 'women/addpage.html'
    success_url = reverse_lazy('home')
    login_url = reverse_lazy('home')
    raise_exception = True

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        c_def = self.get_user_context(title = 'Главная страница')
        return dict(list(context.items()) + list(c_def.items() ))
    
'''def addpage(request):
    if request.method == 'POST':
        form = AddPostForm(request.POST, request.FILES)
        if form.is_valid():
            #print(form.cleaned_data)
            form.save()
            return redirect('home')
    else:
        form = AddPostForm()
    return render(request, 'women/addpage.html', {'form': form,  'title': 'Добавление статьи'})'''

def contact(request):
    return HttpResponse("Обратная связь")

def login(request):
    return HttpResponse("Авторизация")

class ShowPost(DataMixin, DetailView):
    model = Women
    template_name = 'women/post.html'
    slug_url_kwarg = 'post_slug'
    context_object_name = 'post'

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        c_def = self.get_user_context(title = 'Главная страница')
        return dict(list(context.items()) + list(c_def.items() ))
    
'''def show_post(request, post_slug):
    post = get_object_or_404(Women, slug = post_slug)
    context = {
        'post': post, 
        'title': post.title,  
        'cat_selected': post.cat_id, 
    }
    return render(request, 'women/post.html', context=context)
'''
class WomenCategory(DataMixin, ListView):
    model = Women
    template_name = 'women/index.html'
    context_object_name = 'posts'
    allow_empty = False

    def get_queryset(self):
        return Women.objects.filter(cat__slug=self.kwargs['cat_slug'], is_published=True)

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        c_def = self.get_user_context(
            title = 'Категория - ' + str(context['posts'][0].cat), 
            cat_selected = context['posts'][0].cat_id
            )
        return dict(list(context.items()) + list(c_def.items() ))
       

'''def show_category(request, cat_slug):

    posts = Women.objects.filter(cat = Category.objects.get(slug = cat_slug))
    #cats = Category.objects.all()
    if len(posts) == 0:
        raise Http404()
    
    context = {
        'title': 'Отображение по рубрикам', 
        'posts': posts ,
        'cat_selected': cat_slug, 
    }
    return render(request, 'women/index.html', context = context)'''

'''def categories(request, catid):
    if request.POST:
        print(request.POST)

    return HttpResponse(f"<h1>Статьи по категориям</h1><p>{catid}</p>")

def archive(request, year):
    if int(year) > 2020:
        return redirect('home', permanent=False)

    return HttpResponse(f"<h1>Архив по годам</h1><p>{year}</p>")'''

def pageNotFound(request, exception):
    return HttpResponseNotFound('<h1>Страница не найдена</h1>')

class RegisterUser(DataMixin, CreateView):
    form_class = RegisterUserForm
    template_name = 'women/register.html'
    success_url = reverse_lazy('login')
    
    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        c_def = self.get_user_context(title = 'Регистрация')
        return dict(list(context.items()) + list(c_def.items() ))
    