import requests
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
import json
from datetime import date
from datetime import datetime

# Global memory cache for storing JSON data
cache = {
    "all": None,
    "shorts": None,
    "tdm": None,
    "drills": None,
    "chess": None,
}

updated_at = date.today()


with open('./keys.json', 'r') as file:
    # Load the JSON data
    json_data = json.load(file)

def parse_timestamp(timestamp):
    # Replace 'Z' with '+00:00' and parse the timestamp
    return datetime.strptime(timestamp.replace("Z", "+00:00"), "%Y-%m-%dT%H:%M:%S%z")

def Caching():
    print("Caching")

    def helper(urldata):
        data = {"snippet": []}
        for idd in json_data[urldata]:
            url = json_data["url"].replace("paylist", idd)
            data1 = requests.get(url).json()
            while True:
                for i in data1["items"]:
                    data["snippet"].append(i["snippet"])
                if "nextPageToken" in data1:
                    data1 = requests.get(url + "&pageToken=" + data1["nextPageToken"]).json()
                else:
                    break
        data["snippet"].sort(key=lambda x: parse_timestamp(x["publishedAt"]), reverse=True)
        cache[urldata] = data  # Cache the data in memory
        return data

    # Cache all data categories in memory
    helper("all")
    helper("shorts")
    helper("tdm")
    helper("drills")
    helper("chess")


Caching()

class Allvideos(APIView):
    def get(self, request):
        global updated_at
        if (date.today() - updated_at).days > 0:
            Caching()
            updated_at = date.today()
        # Serve from in-memory cache
        data = cache.get("all")
        return Response(data, status=status.HTTP_200_OK)


class Shorts(APIView):
    def get(self, request):
        global updated_at
        if (date.today() - updated_at).days > 0:
            Caching()
            updated_at = date.today()
        # Serve from in-memory cache
        data = cache.get("shorts")
        return Response(data, status=status.HTTP_200_OK)


class Tdm(APIView):
    def get(self, request):
        global updated_at
        if (date.today() - updated_at).days > 0:
            Caching()
            updated_at = date.today()
        # Serve from in-memory cache
        data = cache.get("tdm")
        return Response(data, status=status.HTTP_200_OK)


class Drills(APIView):
    def get(self, request):
        global updated_at
        if (date.today() - updated_at).days > 0:
            Caching()
            updated_at = date.today()
        # Serve from in-memory cache
        data = cache.get("drills")
        return Response(data, status=status.HTTP_200_OK)


class Chess(APIView):
    def get(self, request):
        global updated_at
        if (date.today() - updated_at).days > 0:
            Caching()
            updated_at = date.today()
        # Serve from in-memory cache
        data = cache.get("chess")
        return Response(data, status=status.HTTP_200_OK)
