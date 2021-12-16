
from django.shortcuts import render,HttpResponse,redirect,reverse
import json
from django.views.decorators.csrf import csrf_exempt
from django.http.response import JsonResponse

@csrf_exempt
def test(request):
    get_data = json.loads(request.body)
    casefile = get_data.get('casefile')
    # print(casefile)
    return redirect(reverse('test2',kwargs={'file':'file'}))

def test2(request,file):
    print(file)
    return render(request,'TestApp/testpage.html')