from django.shortcuts import render, redirect, get_object_or_404
from django.urls import reverse
from django.views import View
from .forms import UrlForm
from .models import Url

class HomeView(View):
    def get(self, request):
        form = UrlForm()
        context = {'form': form}
        return render(request, 'shortner/home.html', context)

    def post(self, request):
        form = UrlForm(request.POST)
        if form.is_valid():
            long_url = form.cleaned_data['long_url']
            url_obj, created = Url.objects.get_or_create(long_url=long_url)
            if created:
                # url_obj.short_url = Url.objects.create_short_url()
                url_obj.save()
            short_url = request.build_absolute_uri(reverse('url_redirect', kwargs={'short_url': url_obj.short_url}))
            context = {'form': form, 'short_url': short_url}
            return render(request, 'shortner/home.html', context)
        else:
            context = {'form': form}
            return render(request, 'shortner/base.html', context)

class UrlRedirectView(View):
    def get(self, request, short_url):
        url_obj = get_object_or_404(Url, short_url=short_url)
        url_obj.clicks += 1
        url_obj.save()
        return redirect(url_obj.long_url)
