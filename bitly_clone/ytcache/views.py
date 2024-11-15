import requests
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
import json
from datetime import date 
from datetime import datetime

json_data = None
updated_at = date.today()


with open('./keys.json', 'r') as file:
    # Load the JSON data
    json_data = json.load(file)

def parse_timestamp(timestamp):
    # Replace 'Z' with '+00:00' and parse the timestamp
    return datetime.strptime(timestamp.replace("Z", "+00:00"), "%Y-%m-%dT%H:%M:%S%z")

def Caching():
        # data = requests.get(json_data["url"].replace("paylist" ,json_data["all"] )).json()
        print("Caching")
        def helper(urldata):
            data = {"snippet" :[]}
            for idd in json_data[urldata]:
                url = json_data["url"].replace("paylist" , idd)
                data1 = requests.get(url).json()
                while True:
                    for i in data1["items"]:
                        data["snippet"].append(i["snippet"])
                    if "nextPageToken" in data1:
                        data1 = requests.get(url+"&pageToken="+data1["nextPageToken"]).json()
                    else:
                        break
            file_path = f'./{urldata}.json' 
            data["snippet"].sort(key= lambda x : parse_timestamp(x["publishedAt"]) , reverse=True)
            json_string = json.dumps(data, indent=2)
            with open(file_path, 'w') as json_file:
                    json_file.write(json_string)
            return data
        helper("all")
        helper("shorts")
        helper("tdm")
        helper("drills")
        helper("chess")
        # Return a JSON response
        # return Response(len(data["snippet"]), status=status.HTTP_200_OK)

# Caching()

class Allvideos(APIView):
    def get(self, request):
        # Your logic to fetch data goes here
        global updated_at
        if (date.today() - updated_at).days > 0:
            Caching()
            updated_at = date.today()
        file_path = f'./all.json'
        with open(file_path, 'r') as file:
            # Load the JSON data
           data = json.load(file)
        # Return a JSON response
        return Response(data, status=status.HTTP_200_OK)

class Shorts(APIView):
    def get(self, request):
        # Your logic to fetch data goes here
        global updated_at
        if (date.today() - updated_at).days > 0:
            Caching()
            updated_at = date.today()
        file_path = f'./shorts.json'
        with open(file_path, 'r') as file:
            # Load the JSON data
           data = json.load(file)
        # Return a JSON response
        return Response(data, status=status.HTTP_200_OK)

class Tdm(APIView):
    def get(self, request):
        # Your logic to fetch data goes here
        global updated_at
        if (date.today() - updated_at).days > 0:
            Caching()
            updated_at = date.today()
        file_path = f'./tdm.json'
        with open(file_path, 'r') as file:
            # Load the JSON data
           data = json.load(file)
        # Return a JSON response
        return Response(data, status=status.HTTP_200_OK)

class Drills(APIView):
    def get(self, request):
        # Your logic to fetch data goes here
        global updated_at
        if (date.today() - updated_at).days > 0:
            Caching()
            updated_at = date.today()
        file_path = f'./drills.json'
        with open(file_path, 'r') as file:
            # Load the JSON data
           data = json.load(file)
        # Return a JSON response
        return Response(data, status=status.HTTP_200_OK)

class Chess(APIView):
    def get(self, request):
        # Your logic to fetch data goes here
        global updated_at
        if (date.today() - updated_at).days > 0:
            Caching()
            updated_at = date.today()
        file_path = f'./chess.json'
        with open(file_path, 'r') as file:
            # Load the JSON data
           data = json.load(file)
        # Return a JSON response
        return Response(data, status=status.HTTP_200_OK)