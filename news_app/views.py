from django.contrib.auth.decorators import login_required, user_passes_test
from django.contrib.auth.models import User
from django.db.models import Q
from django.http import HttpResponse
from django.shortcuts import render, get_object_or_404, redirect
from django.views.generic import TemplateView, ListView, UpdateView, DeleteView, CreateView
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.urls import reverse_lazy
from hitcount.utils import get_hitcount_model
from .models import News, Category
from hitcount.views import HitCountDetailView, HitCountMixin
from .forms import ContactForm, CommentForm
from DjangoApp.custom_permissions import OnlyloggedSuperUser
from django.views.decorators.http import require_POST


def news_list(request):
    news_list = News.objects.filter(status=News.Status.Published)

    context = {
        'news_list': news_list,

    }
    return render(request, 'news_list.html', context=context)


def news_detail(request, news):
    news = get_object_or_404(News, slug=news, status=News.Status.Published)
    context = {}
    hit_count = get_hitcount_model().objects.get_for_object(news)
    hits = hit_count.hits
    context['hitcount'] = {'pk': hit_count.pk}
    hit_count_response = HitCountMixin.hit_count(request, hit_count)
    if hit_count_response.hit_counted:
        hits = hits + 1
        context['hit_count'] = hit_count_response.hit_counted
        context['hit_message'] = hit_count_response.hit_message
        context['total_hits'] = hits

    comments = news.comments.filter(active=True)
    comment_count = comments.count()
    new_comment = None
    if request.method == 'POST':
        comment_form = CommentForm(data=request.POST)
        if comment_form.is_valid():
            new_comment = comment_form.save(commit=False)
            new_comment.news = news
            new_comment.user = request.user
            new_comment.save()
            return redirect(news.get_absolute_url())


    else:
        comment_form = CommentForm()

    context = {
        'news': news,
        'comments': comments,
        'comment_count': comment_count,
        'new_comment': new_comment,
        'comment_form': comment_form,
    }
    return render(request, 'detail.html', context=context)


def homePageView(request):
    categories = Category.objects.all()
    news_list = News.objects.all().order_by('-publish_time')[:5]
    local_one = News.objects.filter(category__name='Mahalliy').order_by("-publish_time")[:1]
    local_news = News.objects.all().filter(category__name='Mahalliy').order_by("publish_time")[:6]
    sport_one = News.objects.all().filter(category__name='Sport').order_by("-publish_time")[:1]
    sport_news = News.objects.all().filter(category__name='Sport').order_by("publish_time")[:6]
    tech_one = News.objects.all().filter(category__name='Texnologiya').order_by("-publish_time")[:1]
    tech_news = News.objects.all().filter(category__name='Texnologiya').order_by("publish_time")[:6]
    context = {
        'news_list': news_list,
        'categories': categories,
        'local_one': local_one,
        'local_news': local_news,
        'sport_one': sport_one,
        'sport_news': sport_news,
        'tech_one': tech_one,
        'tech_news': tech_news,
    }
    return render(request, 'home.html', context)


class HomePageView(ListView):
    model = News
    template_name = 'home.html'
    context_object_name = 'news'

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        context['categories'] = Category.objects.all()
        context['news_list'] = News.objects.all().order_by('-publish_time')[:4]
        context['local_one'] = News.objects.filter(category__name='Mahalliy').order_by("-publish_time")[:1]
        context['mahalliy_xabarlar'] = News.objects.all().filter(category__name='Mahalliy').order_by("-publish_time")[
                                       :6]
        context['sport_xabarlari'] = News.objects.all().filter(category__name='Sport').order_by("-publish_time")[:6]
        context['xorij_xabarlari'] = News.objects.all().filter(category__name='Xorij').order_by("-publish_time")[:6]
        context['texnologiya_xabarlari'] = News.objects.all().filter(category__name='Texnologiya').order_by(
            "-publish_time")[:6]
        return context


class ContactPageView(TemplateView):
    template_name = 'contact.html'

    def get(self, request, *args, **kwargs):
        form = ContactForm()
        context = {
            'form': form
        }
        return render(request, 'contact.html', context)

    def post(self, request, *args, **kwargs):
        form = ContactForm(request.POST)
        if request.method == 'POST' and form.is_valid():
            form.save()
            return HttpResponse("<h2>Biz bilan bog'langaniz uchun tashakkur</h2>")
        context = {
            'form': form
        }

        return render(request, 'contact.html', context)


class LocalNewsView(ListView):
    model = News
    template_name = 'mahalliy.html'
    context_object_name = 'mahalliy_yangiliklar'

    def get_queryset(self):
        news = self.model.objects.all().filter(category__name='Mahalliy')
        return news


class ForeignNewsView(ListView):
    model = News
    template_name = 'xorij.html'
    context_object_name = 'xorij_yangiliklar'

    def get_queryset(self):
        news = self.model.objects.all().filter(category__name='Xorij')
        return news


class SportNewsView(ListView):
    model = News
    template_name = 'sport.html'
    context_object_name = 'sport_yangiliklar'

    def get_queryset(self):
        news = self.model.objects.all().filter(category__name='Sport')
        return news


class TechnologyNewsView(ListView):
    model = News
    template_name = 'texnologiya.html'
    context_object_name = 'texnologik_yangiliklar'

    def get_queryset(self):
        news = self.model.objects.all().filter(category__name='Texnologiya')
        return news


class NewsUpdateView(OnlyloggedSuperUser, UpdateView):
    model = News
    fields = ('title', 'body', 'image', 'category', 'status')
    template_name = 'news_edit.html'
    success_url = reverse_lazy('home_page')


class NewsDeleteView(OnlyloggedSuperUser, DeleteView):
    model = News
    template_name = 'news_delete.html'
    success_url = reverse_lazy('home_page')


class NewsCreateView(OnlyloggedSuperUser, CreateView):
    model = News
    template_name = 'news_create.html'
    fields = ('title', 'title_uz', 'title_en', 'title_ru', 'slug',  'body','body_uz', 'body_en', 'body_ru','image', 'category', 'status')
    success_url = reverse_lazy('home_page')


@login_required
@user_passes_test(lambda u: u.is_superuser)
def admin_page_view(request):
    admin_users = User.objects.filter(is_superuser=True)

    context = {
        'admin_users': admin_users
    }
    return render(request, 'admin_page.html', context)


class SearchResultList(ListView):
    model = News
    template_name = 'search_result.html'
    context_object_name = 'barcha_yangiliklar'

    def get_queryset(self):
        query = self.request.GET.get('q')
        return News.objects.filter(
            Q(title__icontains=query) | Q(body__icontains=query)

        )



