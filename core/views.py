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

    current_user = request.user

    try:
        if WaterKeep.objects.filter(user=current_user).exists():
            water_keeper = WaterKeep.objects.get(user=current_user)
            s_count = water_keeper.pair_count
        else:
            WaterKeep.objects.create(user=current_user)
    finally:
        water_keeper = WaterKeep.objects.get(user=current_user)
        s_count = water_keeper.pair_count

    context = {
        "kvartira": current_user.kvartira,
        "name": current_user.last_name,
        "s_count": s_count
    }

    if request.method == "POST":
        if request.POST.get("l_email"):
            l_text = str(request.POST.get("l_textarea"))
            l_email = request.POST.get("l_email")
            new_letter = Letter.objects.create(kvartira=current_user.kvartira, email=l_email, text=l_text)
            return render(request, "profile.html", context)


        if request.POST.get("hot_water_value"):
            hot1_value = request.POST.get("hot_water_value")
            cold1_value = request.POST.get("cold_water_value")
            hot2_value = request.POST.get("hot_water2_value")
            cold2_value = request.POST.get("cold_water2_value")
            hot3_value = request.POST.get("hot_water3_value")
            cold3_value = request.POST.get("cold_water3_value")
            hot4_value = request.POST.get("hot_water4_value")
            cold4_value = request.POST.get("cold_water4_value")
            hot5_value = request.POST.get("hot_water5_value")
            cold5_value = request.POST.get("cold_water5_value")
            water_date = request.POST.get("w_date")
            values = {
                "hot1":hot1_value, "cold1":cold1_value, 
            'hot2':hot2_value, 'cold2':cold2_value, "hot3":hot3_value, 'cold3':cold3_value,
            'hot4':hot4_value, 'cold4':cold4_value, 'hot5':hot5_value, 'cold5':cold5_value
            }
            new_water = Water.objects.create(kvartira=current_user.kvartira,  hot1 = hot1_value,  cold1 = cold1_value, 
             hot2 = hot2_value,  cold2 = cold2_value,  hot3 = hot3_value,  cold3 = cold3_value,
             hot4 = hot4_value,  cold4 = cold4_value,  hot5 = hot5_value,  cold5 = cold5_value,
             date=water_date)
            
            return render(request, "profile.html", context)


        if request.POST.get("hot_water_number"):
            pairs = 0
            hot1_number = request.POST.get("hot_water_number")
            cold1_number = request.POST.get("cold_water_number")
            hot2_number = request.POST.get("hot_water2_number")
            cold2_number = request.POST.get("cold_water2_number")
            hot3_number = request.POST.get("hot_wate3r_number")
            cold3_number = request.POST.get("cold_water3_number")
            hot4_number = request.POST.get("hot_water4_number")
            cold4_number = request.POST.get("cold_water4_number")
            hot5_number = request.POST.get("hot_water5_number")
            cold5_number = request.POST.get("cold_water5_number")
            numbers = [hot1_number, hot2_number, hot3_number, hot4_number, hot5_number]

            for number in numbers:
                if number != None:
                    pairs += 1

            values_for_update = {
                "user":current_user, "pair_count": pairs, "hot1":hot1_number, "cold1":cold1_number, 
            'hot2':hot2_number, 'cold2':cold2_number, "hot3":hot3_number, 'cold3':cold3_number,
            'hot4':hot4_number, 'cold4':cold4_number, 'hot5':hot5_number, 'cold5':cold5_number
            }
            
            new_waterkepper, created = WaterKeep.objects.update_or_create(user=current_user, defaults = values_for_update)
            return render(request, "profile.html", context)


    else:
        pass
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





    
    
    

    
    
    
    
    
    
