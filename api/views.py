from django.http import JsonResponse
from rest_framework.views import APIView

from api.helpers.parser import MtgaLogParser


class BoardView(APIView):
    def get(self, request):
        parser = MtgaLogParser('UTC_Log - 03-15-2020 20.19.00.log')
        parser.fetch_infos()
        print(parser.games)
        return JsonResponse({'blah': 'asd'})
