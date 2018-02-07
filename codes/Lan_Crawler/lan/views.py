from django.http import HttpResponse
from django.http import Http404
from django.shortcuts import render
from django.template import loader
from . models import Metadata

def index(request):
    all_files = Metadata.objects.all()
    # templet = loader.get_template('lan/index.html')

    context = {'all_files':all_files}
    return render(request,'lan/index.html',context)
    # html = ''
    # for files in all_files :
    #     url = files.Path
    #     html +='<a target="_blank" href=" '+ url + '">'+ files.Name +'</a><br>'
    #return HttpResponse(html)
    # return HttpResponse(templet.render(context,request))


def search_result(request, Name):
    try:
        # return HttpResponse("<h2>u requested for :" + Name + "</h2>")
        file = Metadata.objects.get(pk=Name)
    except Metadata.DoesNotExist:
        raise Http404("file might be delete try after some time")
        return render(request, 'lan/default.html', {'file':file})
