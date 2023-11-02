from django.http import HttpResponse
from django.shortcuts import render, get_object_or_404
from django.views.generic import TemplateView,ListView
from .models import News, Category
from .forms import ContactForm

def news_list(request):
    news_list = News.objects.filter(status=News.Status.Published)

    context = {
        'news_list':news_list,

    }
    return render(request, 'news_list.html', context=context)

def news_detail(request, news):
    news = get_object_or_404(News, slug=news, status=News.Status.Published)
    context = {
        'news':news
    }
    return render(request, 'detail.html', context=context)

def homePageView(request):
    categories = Category.objects.all()
    news_list = News.objects.all().order_by('-publish_time')[:5]
    local_one = News.objects.filter(category__name = 'Mahalliy').order_by("-publish_time")[:1]
    local_news = News.objects.all().filter(category__name = 'Mahalliy').order_by("publish_time")[:6]
    sport_one =News.objects.all().filter(category__name='Sport').order_by("-publish_time")[:1]
    sport_news = News.objects.all().filter(category__name='Sport').order_by("publish_time")[:6]
    tech_one=News.objects.all().filter(category__name='Texnologiya').order_by("-publish_time")[:1]
    tech_news = News.objects.all().filter(category__name='Texnologiya').order_by("publish_time")[:6]
    context = {
        'news_list':news_list,
        'categories':categories,
        'local_one':local_one,
        'local_news': local_news,
        'sport_one':sport_one,
        'sport_news': sport_news,
        'tech_one':tech_one,
        'tech_news': tech_news,
    }
    return render(request, 'home.html', context)

class HomePageView(ListView):
    model = News
    template_name = 'home.html'
    context_object_name = 'news'

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        context['categories'] =Category.objects.all()
        context['news_list'] = News.objects.all().order_by('-publish_time')[:5]
        context['local_one'] = News.objects.filter(category__name = 'Mahalliy').order_by("-publish_time")[:1]
        context['mahalliy_xabarlar'] = News.objects.all().filter(category__name = 'Mahalliy').order_by("-publish_time")[:6]
        context['sport_xabarlari'] = News.objects.all().filter(category__name='Sport').order_by("-publish_time")[:6]
        context['xorij_xabarlari'] = News.objects.all().filter(category__name='Xorij').order_by("-publish_time")[:6]
        context['texnologiya_xabarlari'] = News.objects.all().filter(category__name='Texnologiya').order_by("-publish_time")[:6]
        return context



class ContactPageView(TemplateView):
    template_name = 'contact.html'

    def get(self, request, *args, **kwargs):
        form = ContactForm()
        context = {
            'form':form
        }
        return render(request, 'contact.html', context)
    def post(self, request, *args, **kwargs):
        form = ContactForm(request.POST)
        if request.method == 'POST' and form.is_valid():
            form.save()
            return HttpResponse("<h2>Biz bilan bog'langaniz uchun tashakkur</h2>")
        context = {
            'form':form
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

