# Create your views here.
from django.http import HttpResponse
from django.shortcuts import render_to_response, redirect
from django.template import RequestContext as RC
from models import *
from django.contrib.auth.models import User
import platform
import os
from picture import *
from django.utils import simplejson
import base64

def render(template_name,request, params=None):
    return render_to_response(template_name,
        context_instance = RC(request,params)
    )


def home(request):
    cats = Category.objects.all()
    data_dict = {
        'tools': Tool.objects.all(),
        'cats': cats,
        'authors' : User.objects.all()
    }
    return render('tool list.html', request, data_dict)


def run_tool_and_get_result(request, tool, params):
    ns = {}
    function_name = tool.function_name
    real_code = tool.code
    if platform.system() == 'Linux':
        real_code = real_code.replace('\r\n','\n')

    params_str = []
    for p in params:
        p.value = request.POST.get(p.name)
        code = compile('%s = """%s"""' %(p.name, p.value), '<string>', 'exec')
        params_str.append(p.name)
        exec code in ns

    params_str = ','.join(params_str)

    code = compile(real_code, '<string>', 'exec')
    exec code in ns

    code = compile('result = %s(%s)' %(function_name, params_str), '<string>', 'exec')
    exec code in ns

    return ns['result']

def run_tool(request, tool_id):
    tool = Tool.objects.get(pk=tool_id)
    params = tool.parameter_set.all()

    if request.method == 'POST':
        result = run_tool_and_get_result(request, tool, params)
    else:
        result = ""
    data_dict = {
        'tool' : tool,
        'params': params,
        'result': result
    }
    return render('run tool.html', request, data_dict)



def get_font(font):
    return {
        'name' : font.lower(),
        'value' : font
    }

def get_fonts():
    all_fonts = os.listdir(get_font_path())
    return sorted([get_font(font[:-4]) for font in all_fonts if (font[-3:].upper() == 'TTF')])


def center_text_image(request):
    fonts = get_fonts()
    return render('draw center.html', request, { 'fonts' : fonts})

def JsonResponse(contents, status=200):
    return HttpResponse(contents, mimetype='application/json', status=status)

def create_image_view(request):
    picture_filter = request.POST.get('filter',None)
    text = request.POST.get('text','JED Utils')

    width = int(request.POST.get('width',200))
    height = int(request.POST.get('height',200))
    backColor = request.POST.get('backColor',"red")
    font = request.POST.get('font',"BOOKOSBI")
    fontSize =  int(request.POST.get('fontSize',"16"))
    fontColor = request.POST.get('fontColor', "#949494")
    img_type = request.POST.get('img_type', "JPEG")
    image = create_image(font, fontSize, fontColor, width, height, backColor, text, img_type, picture_filter)
    image_str = base64.encodestring(image)
    json_str = simplejson.dumps({'image' :image_str})
    return JsonResponse(json_str)


