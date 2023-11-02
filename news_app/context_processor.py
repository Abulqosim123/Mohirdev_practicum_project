from .models import News,Category

def latest_news(request):
    latest_news = News.objects.all().order_by("-publish_time")[:10]
    categories = Category.objects.all()

    context = {

        'latest_news':latest_news
    }
    return context