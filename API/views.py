from django.shortcuts import render
from django.views import View
from rest_framework.views import APIView


class HomeView(APIView):
    def get(self, request):
        self.dispatch(request)

