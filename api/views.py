from django.http import JsonResponse
from django.shortcuts import render
from rest_framework.views import APIView


class ExampleView(APIView):
    def get(self):
        return JsonResponse({'blah': 'asd'})
