from django import forms
from django.forms import Textarea
from .models import Articles, Comments, User
from django.contrib.auth.forms import AuthenticationForm, UserCreationForm



class ArticleForm(forms.ModelForm):
    class Meta:
        model = Articles
        fields = ('name','text')
    def __init__(self,*args,**kwargs):
        super().__init__(*args,**kwargs)
        for field in self.fields:
            self.fields[field].widget.attrs['class'] = 'form-control'



class AuthUserForm(AuthenticationForm, forms.ModelForm):
    class Meta:
        model = User
        fields = ('username','password')

    def __init__(self,*args,**kwargs):
        super().__init__(*args,**kwargs)
        self.fields["username"].widget.attrs["class"] = "form-control mb-3"
        self.fields["password"].widget.attrs["class"] = "form-control"



class RegistrationForm(UserCreationForm):

    email = forms.EmailField(required=True, widget=forms.EmailInput(attrs={"class": "form-control mb-2"}))
    kvartira = forms.IntegerField(required=True, label="Квартира", widget=forms.NumberInput(attrs={"class": "form-control mb-2"}))
    
    class Meta:
        model = User
        fields = (
            'username',
            'first_name',
            'last_name',
            'kvartira',
            'email',
            'password1',
            'password2'
        )

    def save(self, commit=True):
        user = super(RegistrationForm, self).save(commit=False)
        user.first_name = self.cleaned_data['first_name']
        user.last_name = self.cleaned_data['last_name']
        user.email = self.cleaned_data['email']
        user.set_password(self.cleaned_data["password1"])
        

        if commit:
            user.save()

        return user

    def __init__(self, *args, **kwargs):
        super(RegistrationForm, self).__init__(*args, **kwargs)
        self.fields["username"].widget.attrs["class"] = "form-control"
        self.fields["password1"].widget.attrs["class"] = "form-control"
        self.fields["password2"].widget.attrs["class"] = "form-control"
        self.fields["first_name"].widget.attrs["class"] = "form-control mb-2"
        self.fields["last_name"].widget.attrs["class"] = "form-control mb-2"


class RegisterUserForm(forms.ModelForm):

    kvartira = forms.IntegerField(
        label= ("Квартира"),
    )

    class Meta:
        model = User
        fields = ('username','password')

    def __init__(self,*args,**kwargs):
        super().__init__(*args,**kwargs)
        for field in self.fields:
            self.fields[field].widget.attrs['class'] = 'form-control'

    def save(self, commit=True):
        user = super().save(commit=False)
        user.set_password(self.cleaned_data["password"])
        if commit:
            user.save()
        return user
        
        
        
        
        
class CommentForm(forms.ModelForm):
    class Meta:
        model = Comments
        fields = ('text',)
    def __init__(self,*args,**kwargs):
        super().__init__(*args,**kwargs)
        for field in self.fields:
            self.fields[field].widget.attrs['class'] = 'form-control'
        self.fields['text'].widget = Textarea(attrs={'rows':5})
        

        
        
        
        
        
        
        
        
        
        
        