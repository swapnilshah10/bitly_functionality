from django.shortcuts import render, redirect, get_object_or_404
from django.urls import reverse
from django.views import View
from .forms import UrlForm
from .models import FeatureToggle, Url,Ip , UniqueIp
from rest_framework.response import Response
from rest_framework import status
from rest_framework.decorators import api_view
from datetime import datetime
# import requests
from django.utils import timezone
from rest_framework.views import APIView
import requests
from datetime import date
from django.http import JsonResponse

# def getinfo(ip):
#     response = requests.get(f'https://ipapi.co/{ip}/json')
#     result = response.json()
#     return (result)


def get_client_ip(request):
    x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
    ip = ""
    if x_forwarded_for:
        ip = x_forwarded_for.split(',')[0]
    else:
        ip = request.META.get('REMOTE_ADDR')
    return ip

class HomeView(View):
    def get(self, request):
        ipp =  Ip.objects.get_or_create(ip = str(get_client_ip(request)) , time = timezone.now())
        form = UrlForm()
        context = {'form': form}
        return render(request, 'shortner/home.html', context)

    def post(self, request):
        form = UrlForm(request.POST)
        if form.is_valid():
            long_url = form.cleaned_data['long_url']
            ipp =  Ip.objects.get_or_create(ip = str(get_client_ip(request)) , method = "post" , page = long_url ,time = timezone.now())
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
        ipp =  Ip.objects.get_or_create(ip = str(get_client_ip(request)) , method = "get" , page = short_url , time = timezone.now())
        url_obj = get_object_or_404(Url, short_url=short_url)
        url_obj.clicks += 1
        url_obj.save()
        return redirect(url_obj.long_url)


@api_view(['GET', 'POST'])
def get_url(request, short_url):
    if request.method == 'GET':
        ip = str(get_client_ip(request))
        ipp =  Ip.objects.get_or_create(ip = ip ,method = "get" , page = short_url , time = timezone.now())
        #     except:
        #         pass
        url_obj = get_object_or_404(Url, short_url=short_url)
        # url_obj.clicks += 1
        # url_obj.save()
        formatted_date = url_obj.created_at.strftime("%Y-%m-%d %H:%M")
        response = {"url": url_obj.long_url , "created_at":formatted_date , "created_by_ip" : url_obj.ip , "created_by" : url_obj.name}
        return Response(response, status=status.HTTP_200_OK)
    elif request.method == 'POST':
        ip = str(get_client_ip(request))
        ipp =  Ip.objects.get_or_create(ip = ip ,method = "post" ,  time = timezone.now())
        form = (request.data)
        short_url = ""
        url_obj = None
        if form['long_url']:
            long_url = form['long_url']
            if 'short_url' in form.keys():
                short_url = form['short_url']
                url_obj, created = Url.objects.get_or_create(short_url=short_url)


            else:
                url_obj = Url.objects.create()
            url_obj.long_url = long_url
            url_obj.ip = str(get_client_ip(request))
            url_obj.name = form.get("created_by", "")
            url_obj.created_at = timezone.now()
            url_obj.save()

            # short_url = request.build_absolute_uri(
            #     reverse('url_redirect', kwargs={'short_url': url_obj.short_url}))
            return Response({"url":url_obj.short_url}, status=status.HTTP_200_OK)
        else:
            return Response(form, status=status.HTTP_400_BAD_REQUEST)



@api_view(['GET'])
def save_ip(request):
    ip = str(get_client_ip(request))

    ipp =  Ip.objects.get_or_create(ip = ip ,method = "get" ,page = "Homepage"  ,time = timezone.now())
    return Response( status=status.HTTP_200_OK)


@api_view(['GET'])
def copy_ip(request):
    ip_list = Url.objects.all()
    for ip in ip_list:
        c = UniqueIp.objects.get_or_create(ip=ip.ip)
        ip.ip2 = c[0]
        ip.save()
    return Response( status=status.HTTP_200_OK)


class IPChecker(APIView):

    def get(self, request):
        ip = get_client_ip(request)
        response = requests.get(f"http://ip-api.com/json/{ip}")
        data = response.json()
        data['date'] = str(date.today())
        data['ip'] = str(ip)
        data['data'] = response.json()
        return Response(data, status=status.HTTP_200_OK)



def check_feature_status(request, feature_name):
    try:
        feature = FeatureToggle.objects.get(name=feature_name)
        return JsonResponse({'feature': feature_name, 'is_enabled': feature.is_enabled})
    except FeatureToggle.DoesNotExist:
        return JsonResponse({'error': 'Feature not found'}, status=404)