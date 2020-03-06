from django.http import JsonResponse
from django.shortcuts import render
from rest_framework.views import APIView


class BoardView(APIView):
    def get(self, request):
        return JsonResponse({'blah': 'asd'})
