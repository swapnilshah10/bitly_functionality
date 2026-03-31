from django.shortcuts import render, redirect, get_object_or_404
from django.urls import reverse
from django.views import View
from .forms import UrlForm
from .models import Url,Ip
from rest_framework.response import Response
from rest_framework import status
from rest_framework.decorators import api_view
import requests


def getinfo(ip):
    response = requests.get(f'https://ipapi.co/{ip}/json')
    result = response.json()
    return (result)


def get_client_ip(request):
    x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
    if x_forwarded_for:
        ip = x_forwarded_for.split(',')[0]
    else:
        ip = request.META.get('REMOTE_ADDR')
    return ip

class HomeView(View):
    def get(self, request):
        ipp =  Ip.objects.get_or_create(ip = str(get_client_ip(request)))
        form = UrlForm()
        context = {'form': form}
        return render(request, 'shortner/home.html', context)

    def post(self, request):
        ipp =  Ip.objects.get_or_create(ip = str(get_client_ip(request)))

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
        ipp =  Ip.objects.get_or_create(ip = str(get_client_ip(request)))
        url_obj = get_object_or_404(Url, short_url=short_url)
        url_obj.clicks += 1
        url_obj.save()
        return redirect(url_obj.long_url)


@api_view(['GET', 'POST'])
def get_url(request, short_url):
    if request.method == 'GET':
        ip = str(get_client_ip(request))
        info = getinfo(ip)
        if info:
            try:
                latitude = info['latitude']
                longitude = info['longitude']
                city = info['city']
                ipp =  Ip.objects.get_or_create(ip = ip , latitude = latitude ,longitude = longitude , city = city)
            except:
                pass
        url_obj = get_object_or_404(Url, short_url=short_url)
        url_obj.clicks += 1
        url_obj.save()
        return Response({"url": url_obj.long_url}, status=status.HTTP_200_OK)
    elif request.method == 'POST':
        ip = str(get_client_ip(request))
        info = getinfo(ip)
        if info:
            try:
                latitude = info['latitude']
                longitude = info['longitude']
                city = info['city']
                ipp =  Ip.objects.get_or_create(ip = ip , latitude = latitude ,longitude = longitude , city = city)
            except:
                pass
        form = (request.data)
        if form['long_url']:
            long_url = form['long_url']
            if 'short_url' in form.keys():
                short_url = form['short_url']
                if Url.objects.filter(short_url=short_url).exists():
                    url_obj = Url.objects.get(short_url=short_url)
                    url_obj.long_url = long_url
                    url_obj.ip =  str(get_client_ip(request))
                    url_obj.save()
                    return Response({"url": url_obj.short_url}, status=status.HTTP_200_OK)
                else:
                    url_obj, created = Url.objects.get_or_create(
                        long_url=long_url, short_url=short_url , ip =  str(get_client_ip(request)))
                    if created:
                        url_obj.save()
                        return Response({"url": url_obj.short_url}, status=status.HTTP_200_OK)
                    else:
                        return Response(status=status.HTTP_400_BAD_REQUEST)

            url_obj, created = Url.objects.get_or_create(long_url=long_url)
            if created:
                # url_obj.short_url = Url.objects.create_short_url()
                url_obj.ip = str(get_client_ip(request))
                url_obj.save()
            short_url = request.build_absolute_uri(
                reverse('url_redirect', kwargs={'short_url': url_obj.short_url}))
            return Response({"url":url_obj.short_url}, status=status.HTTP_200_OK)
        else:
            return Response(form, status=status.HTTP_400_BAD_REQUEST)

