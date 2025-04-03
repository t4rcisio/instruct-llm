from django.shortcuts import render
from rest_framework.response import Response
from rest_framework.decorators import api_view
import traceback
import os

@api_view(['GET'])
def server_status(request):
    
    #return Response({"oi":"oi"})
    if os.path.exists('pages/templates/home.html'):
        return render(request, 'pages/home.html')
    return Response({"file":"not exists"})

    return render(request, )
