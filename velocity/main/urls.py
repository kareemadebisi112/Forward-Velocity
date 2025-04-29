from django.urls import path, include
from . import views
from django.contrib.auth import views as auth_views
from django.contrib.sitemaps.views import sitemap
from .sitemaps import StaticViewSitemap
from django.conf import settings
from django.conf.urls.static import static

sitemaps = {
    'static': StaticViewSitemap,
}

urlpatterns = [
    path('', views.index, name='index'),
    path('contact/', views.contact, name='contact'),
    path('email/', views.email, name='email'),
    path('post_lead/', views.post_lead, name='post-lead'),

    # Blog
    path('blog/', views.blog_list, name='blog_list'),
    path('blog/<slug>/', views.blog_detail, name='blog_detail'),


    path('sitemap.xml', 
         sitemap, 
         {'sitemaps': sitemaps}, 
         name='django.contrib.sitemaps.views.sitemap'
         ),

    path('robots.txt', views.robots_txt, name='robots_txt'),
    path('7bb8a3b7f66b77a63016e9818c6c22a8.txt', views.txt_file, name='txt_file'),

    path('<code>', views.affiliate_redirect, name='affiliate_redirect'),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
