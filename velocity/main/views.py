from django.shortcuts import get_object_or_404, render, redirect
from .forms import LeadForm
import os
from dotenv import find_dotenv, load_dotenv
from .models import *
from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView
from .utils import parse_data, get_current_year, addVisit
from django.http import JsonResponse, HttpResponse
from .services import make_lead
from django.views.decorators.http import require_GET


dotenv_path = find_dotenv()
load_dotenv(dotenv_path)
# Create your views here.


@require_GET
def robots_txt(request):
    return HttpResponse(robots_txt_content, content_type="text/plain", status=200)

@require_GET
def txt_file(request):
    content = ""
    return HttpResponse(content, content_type="text/plain", status=200)

robots_txt_content = """\
User-Agent: *
Disallow: /admin/

User-agent: GPTBot
Disallow: /

Sitemap: forward-velocity.com/sitemap.xml
"""

def index(request):
    addVisit()
    hero = Hero.objects.latest('id')
    services = Service.objects.all()
    from_email = os.getenv("EMAIL_HOST_USER")
    template = 'main/emails/email.html'
    form = LeadForm()

    context = {
        'form': form,
        'message': 'Thank you for contacting us!',
        'services': services,
        'hero': hero,
        'about': About.objects.first(),
        'images': Image.objects.all(),
        'year': get_current_year()
    }
    return render(request, 'main/index.html', context)

def contact(request): 
    form = LeadForm()
    context =  {
        'form': form,
        'year': get_current_year()
    }
    return render(request, 'main/contact.html', context)

def email(request):
    return render(request, 'main/emails/email.html')

class EditPage(APIView):
    def put(self, request):
        # print(request.data)
        data = request.data
        print(data)
        update_hero, update_about = parse_data(data)

        hero = Hero.objects.get(id=update_hero['hero_id'])
        about = About.objects.get(id=update_about['about_id'])
        
        hero.title = update_hero['title']
        hero.description = update_hero['description']
        hero.button_text = update_hero['button_text']
        hero.save()

        about.title = update_about['title']
        about.description = update_about['description']
        about.highlight_text = update_about['highlight_text']
        about.year = update_about['year']
        about.mission_text = update_about['mission_text']
        about.vision_text = update_about['vision_text']
        about.values_text = update_about['values_text']
        about.save()

        return Response(status=status.HTTP_200_OK)
    

def post_lead(request):
    if request.method == 'POST':
        data = request.POST
        print(data)
        name = data['name']
        email = data['email']
        service = data['service']
        message = data['message']
        make_lead(name, email, service, message)
        first_name = name.split(' ')[0]
        return render(request, 'main/thankyou.html', {'name': first_name})
    return JsonResponse({'message': 'Error'}, status=400)

def blog_list(request):
    blogs = Blog.objects.all()
    form = LeadForm()
    context = {
        'blogs': blogs,
        'year': get_current_year(),
        'form': form,
    }
    return render(request, 'main/blog/blog_list.html', context)

def blog_detail(request, slug):
    form = LeadForm()
    blog = get_object_or_404(Blog, slug=slug)
    category = blog.category.name
    context = {
        'blog': blog,
        'category': category,
        'form': form,
        'year': get_current_year(),
        'og_title': blog.title,
        'og_desc': blog.intro,
        'og_image': blog.image.url,
        'og_url': request.build_absolute_uri(),
        'og_type': 'article'
    }
    return render(request, 'main/blog/blog_detail.html', context)

def affiliate_redirect(request, code):
    print(code)
    try:
        affiliate = Affiliate.objects.get(code=code)
        affiliate.clicks += 1
        affiliate.save()
    except Affiliate.DoesNotExist:
        return HttpResponse(status=404)
    return redirect('index')
