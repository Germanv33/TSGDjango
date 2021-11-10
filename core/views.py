from django.shortcuts import render,redirect,HttpResponse

from .models import Articles,Comments, Documents, User, Letter, Water, WaterKeep
from django.views.generic import ListView, DetailView,CreateView, UpdateView,DeleteView
from django.views.generic.edit import FormMixin
from .forms import ArticleForm, AuthUserForm, RegisterUserForm, CommentForm, RegistrationForm
from django.urls import reverse, reverse_lazy
from django.contrib import messages
from django.contrib.auth.views import LoginView,LogoutView

from django.contrib.auth import authenticate, login
from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import HttpResponseRedirect, request
from django.contrib.auth.decorators import login_required
from django.template import Context, Template, context

from django.db.models import Q

@login_required
def ProfileView(request):
    if request.method == "POST":
        if request.POST.get("water"):
            new_water = Water()

        if request.POST.get("letter"):
            new_letter = Letter()

        if request.POST.get("letter"):
            new_letter = Letter()

        if request.POST.get("letter"):
            new_letter = Letter()

        if request.POST.get("letter"):
            new_letter = Letter()


    current_user = request.user

    context = {
        "kvartira": current_user.kvartira,
        "name": current_user.last_name

    }

    return render(request, "profile.html", context)


class HomeListView(ListView):
    model = Articles
    template_name = 'index.html'
    context_object_name = 'list_articles'
    
    def get_queryset(self):
        return Articles.objects.order_by("-create_date")[:3]
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["list_count"] = Articles.objects.count
        return context


class NewsListView(ListView):

    paginate_by = 3
    model = Articles
    template_name = 'news.html'
    context_object_name = 'list_articles'
    
    def get_queryset(self):
        query = self.request.GET.get('searched')
        object_list = Articles.objects.order_by("-create_date")
        if query:
            print(query)
            
            object_list = Articles.objects.filter(
                Q(name__icontains=query)  | Q(text__icontains=query))
            return object_list
        else:
            return object_list
        
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["list_count"] = Articles.objects.count
        return context
    

class DocsListView(ListView):
    
    paginate_by = 3
    model = Documents
    template_name = 'docs.html'
    context_object_name = 'docs_list'
    
    def get_queryset(self):
        query = self.request.GET.get('searched')
        object_list = Documents.objects.order_by("-create_date")
        if query:
            print(query)
            
            object_list = Documents.objects.filter(
                Q(name__icontains=query)  | Q(text__icontains=query))
            return object_list
        else:
            return object_list
        
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["list_count"] = Articles.objects.count
        return context



class CustomSuccessMessageMixin:
    @property
    def success_msg(self):
        return False
        
    def form_valid(self,form):
        messages.success(self.request, self.success_msg)
        return super().form_valid(form)
    def get_success_url(self):
        return '%s?id=%s' % (self.success_url, self.object.id)



class HomeDetailView(CustomSuccessMessageMixin, FormMixin, DetailView):
    model = Articles
    template_name = 'detail.html'
    context_object_name = 'get_article'
    form_class = CommentForm
    success_msg = 'Комментарий успешно создан, ожидайте модерации'
    
    
    def get_success_url(self):
        return reverse_lazy('detail_page', kwargs={'pk':self.get_object().id})
    
    def post(self,request, *args, **kwargs):
        form = self.get_form()
        if form.is_valid():
            return self.form_valid(form)
        else:
            return self.form_invalid(form)
    
    def form_valid(self,form):
        self.object = form.save(commit=False)
        self.object.article = self.get_object()
        self.object.author = self.request.user
        self.object.save()
        return super().form_valid(form)


class DocsDetailView(CustomSuccessMessageMixin, FormMixin, DetailView):
    model = Documents
    template_name = 'detail1.html'
    context_object_name = 'get_docs'
    form_class = CommentForm
    success_msg = 'Комментарий успешно создан, ожидайте модерации'
    
    
    def get_success_url(self):
        return reverse_lazy('detail_doc_page', kwargs={'pk':self.get_object().id})
    
    def post(self,request, *args, **kwargs):
        form = self.get_form()
        if form.is_valid():
            return self.form_valid(form)
        else:
            return self.form_invalid(form)
    
    def form_valid(self,form):
        self.object = form.save(commit=False)
        self.object.article = self.get_object()
        self.object.author = self.request.user
        self.object.save()
        return super().form_valid(form)




def update_comment_status(request, pk, type):
    item = Comments.objects.get(pk=pk)
    if request.user != item.article.author:
        return HttpResponse('deny')
    
    if type == 'public':
        import operator
        item.status = operator.not_(item.status)
        item.save()
        template = 'comment_item.html'
        context = {'item':item, 'status_comment':'Комментарий опубликован'}
        return render(request, template, context)
        
    elif type == 'delete':
        item.delete()
        return HttpResponse('''
        <div class="alert alert-success">
        Комментарий удален
        </div>
        ''')
    
    return HttpResponse('1')



class ArticleCreateView(LoginRequiredMixin, CustomSuccessMessageMixin, CreateView):
    login_url = reverse_lazy('login_page')
    model = Articles
    template_name = 'edit_page.html'
    form_class = ArticleForm
    success_url = reverse_lazy('edit_page')
    success_msg = 'Запись создана'

    def get_context_data(self,**kwargs):
        kwargs['list_articles'] = Articles.objects.all().order_by('-id')
        return super().get_context_data(**kwargs)

    def form_valid(self,form):
        self.object = form.save(commit=False)
        self.object.author = self.request.user
        self.object.save()
        return super().form_valid(form)
    
    

class ArticleUpdateView(LoginRequiredMixin, CustomSuccessMessageMixin,UpdateView):
    model = Articles
    template_name = 'edit_page.html'
    form_class = ArticleForm
    success_url = reverse_lazy('edit_page')
    success_msg = 'Запись успешно обновлена'

    def get_context_data(self,**kwargs):
        kwargs['update'] = True
        return super().get_context_data(**kwargs)

    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        if self.request.user != kwargs['instance'].author:
            return self.handle_no_permission()
        return kwargs



class MyprojectLoginView(LoginView):
    template_name = 'login.html'
    form_class = AuthUserForm
    success_url = reverse_lazy('home')

    def get_success_url(self):
        return self.success_url


class RegisterUserView(CreateView):
    model = User
    template_name = 'register_page.html'
    form_class = RegistrationForm
    success_url = reverse_lazy('home')
    success_msg = 'Пользователь успешно создан'

    def form_valid(self,form):
        form_valid = super().form_valid(form)
        username = form.cleaned_data["username"]
        password = form.cleaned_data["password1"]
        aut_user = authenticate(username=username,password=password)
        login(self.request, aut_user)
        return form_valid


class MyProjectLogout(LogoutView):
    next_page = reverse_lazy('edit_page')

class ArticleDeleteView(LoginRequiredMixin, DeleteView):
    model = Articles
    template_name = 'edit_page.html'
    success_url = reverse_lazy('edit_page')
    success_msg = 'Запись удалена'

    def post(self,request,*args,**kwargs):
        messages.success(self.request, self.success_msg)
        return super().post(request)

    def delete(self, request, *args, **kwargs):
        self.object = self.get_object()
        if self.request.user != self.object.author:
            return self.handle_no_permission()
        success_url = self.get_success_url()
        self.object.delete()
        return HttpResponseRedirect(success_url)





    
    
    

    
    
    
    
    
    
