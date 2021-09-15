from .models import Article

from django.views.generic import TemplateView, DetailView


class Create(TemplateView):

    template_name = 'create.html'


class View(DetailView):

    model = Article
    queryset = Article.objects.all()
    template_name = 'view.html'
