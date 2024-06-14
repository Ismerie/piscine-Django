from django.shortcuts import render, redirect, reverse
from django.http import HttpResponse
from .models import Article, UserFavouriteArticle
from django.views.generic.base import RedirectView, TemplateView
from django.views.generic.edit import FormView
from django import forms
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.forms import AuthenticationForm
from django.http import HttpResponseRedirect
from django.http.request import HttpRequest
from django.views.generic import DetailView
from .forms import RegisterForm, PublishForm, FavouriteForm, LoginForm
from django.urls import reverse_lazy
from django.contrib import messages
from django.db import DatabaseError
from django.views.generic.list import ListView

class Articles(TemplateView):
    template_name = 'articles.html'
    queryset = Article.objects.filter().order_by('-created')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['latest_articles'] = Article.objects.filter().order_by('-created')
        return context

class Home(RedirectView):
    pattern_name = 'articles'

class LoginPage(FormView):

    template_name = 'login.html'
    form_class = LoginForm
    success_url = 'home'
    initial = {'key': 'value'}

    def get(self, request, *args, **kwargs):
        # form = LoginForm()
        form = self.form_class(initial=self.initial)
        context = {'form': form}
        return render(request, self.template_name, context)

    def post(self, request, *args, **kwargs):
        form = LoginForm(request.POST)
        if form.is_valid():
            name = form.cleaned_data.get("name")
            print(name)
            password = form.cleaned_data.get("password")
            print(password)
            user = authenticate(username=name, password=password)
            print(user)
            if user is not None:
                print(user)
                login(request, user=user)
                return HttpResponseRedirect(reverse('home'))
            else:
                form.add_error(None, "Invalid username or password")
                return self.form_invalid(form)
        return render(request, self.template_name, {'form' :form})

class Publications(TemplateView):
    template_name = 'publications.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        print(self.request.user)
        if self.request.user.is_authenticated:
            context['latest_articles'] = Article.objects.filter(author=self.request.user)
            return context
        else:
            context['latest_articles'] = None
            return context
    


class Detail(DetailView, FormView):
    model = Article
    template_name = 'article_details.html'
    form_class = FavouriteForm
    success_url = reverse_lazy('articles')


    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['favouriteForm'] = self.get_form()
        article_id = self.kwargs.get('pk')
        context["content"] = Article.objects.filter(pk=article_id)
        return context
    
    def form_valid(self, form):
        article_id = self.object.pk  # Get the current article ID from the DetailView
        try:
            favourite, created = UserFavouriteArticle.objects.get_or_create(
                article_id=article_id, user=self.request.user)
            if not created:
                favourite.delete()
                messages.success(self.request, "Successfully removed from favourites.")
            else:
                messages.success(self.request, "Successfully added to favourites.")
        except Exception as e:
            messages.error(self.request, "There was an error updating your favourites.")
        return HttpResponseRedirect(self.request.path_info)

    def form_invalid(self, form):
        print("Form errors:", form.errors)  # Debugging statement
        messages.error(self.request, "Unsuccessful add to favourite. Invalid information.")
        return HttpResponseRedirect(self.request.path_info)
    
    def get_form(self, form_class=None):
        if form_class is None:
            form_class = self.get_form_class()
        return form_class(None, **self.get_form_kwargs())
    
    def post(self, request, *args, **kwargs):
        self.object = self.get_object()  # Get the object before processing the form
        form = self.get_form()
        form.data = form.data.copy()  # Make form data mutable
        form.data['article'] = self.object.pk  # Set the article ID in the form data
        if form.is_valid():
            return self.form_valid(form)
        else:
            return self.form_invalid(form)


class Logout(RedirectView):
    template_name = 'articles.html'

    def get(self, request):
        logout(request)
        return HttpResponseRedirect(reverse('home'))


class Favourites(ListView):
    template_name = 'favourites.html'
    model = UserFavouriteArticle

    def get_queryset(self):
        if self.request.user.is_authenticated:
            return UserFavouriteArticle.objects.filter(user=self.request.user)
        else:
            return UserFavouriteArticle.objects.none()

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['user'] = self.request.user
        return context


class Register(FormView):
    template_name = "register.html"
    form_class = RegisterForm
    success_url = reverse_lazy('home')

    def get(self, request: HttpRequest, *args: str, **kwargs: any):
        if self.request.user.is_authenticated:
            messages.error(self.request, 'You already logined!')
            return redirect('home')
        return super().get(request, *args, **kwargs)

    def form_valid(self, form: RegisterForm):
        user = form.save()
        login(self.request, user)
        messages.success(self.request, "Registration successful.")
        return super().form_valid(form)

    def form_invalid(self, form):
        messages.error(
            self.request, "Unsuccessful registration. Invalid information.")
        return super().form_invalid(form)

class Publish(FormView):
    template_name = "publish.html"
    form_class = PublishForm
    success_url = reverse_lazy('home')
    login_url = reverse_lazy('home')

    def get(self, request: HttpRequest, *args: str, **kwargs: any):
        if not self.request.user.is_authenticated:
            messages.error(self.request, 'You must be logged in to publish')
            return redirect('home')
        return super().get(request, *args, **kwargs)

    def form_valid(self, form: PublishForm):
        title = form.cleaned_data['title']
        synopsis = form.cleaned_data['synopsis']
        content = form.cleaned_data['content']
        try:
            Article.objects.create(
                title=title,
                author=self.request.user,
                synopsis=synopsis,
                content=content
            )
            messages.success(self.request, "Successful publish.")
        except DatabaseError as e:
            messages.success(
                self.request, "Unsuccessful publish. DatabaseError")
            return redirect('home')
        return super().form_valid(form)

    def form_invalid(self, form):
        messages.error(
            self.request, "Unsuccessful publish. Invalid information.")
        return super().form_invalid(form)

# Create your views here.

# from django.contrib.auth.models import User
#  # Créez des utilisateurs avec les IDs spécifiés dans le fichier JSON
#  user1 = User.objects.create_user('user1', 'user1@example.com', 'password123')
#  user2 = User.objects.create_user('user2', 'user2@example.com', 'password123')
#  user3 = User.objects.create_user('user3', 'user3@example.com', 'password123')
#  user1.save()
#  user2.save()
#  user3.save()