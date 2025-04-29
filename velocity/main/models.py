from django.db import models
from django.urls import reverse
from django.utils import timezone
from django.contrib.auth.models import User
from django.utils.text import slugify
from ckeditor.fields import RichTextField


class BaseModel(models.Model):
    created_at = models.DateTimeField(db_index=True, default=timezone.now)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        abstract = True

class Lead(BaseModel):
    name = models.CharField(max_length=255)
    email = models.EmailField()
    service = models.CharField(max_length=40)
    message = models.TextField()

    def __str__(self):
        return self.name
    
class Service(BaseModel):
    name = models.CharField(max_length=255)
    description = models.TextField()
    icon = models.TextField()
    html_id = models.CharField(max_length=255)

    def __str__(self):
        return self.name
    
class Hero(BaseModel):
    title = models.CharField(max_length=255)
    description = models.TextField()
    # image = models.TextField()
    button_text = models.CharField(max_length=255)
    button_link = models.CharField(max_length=255)

    def __str__(self):
        return self.title

class About(BaseModel):
    title = models.CharField(max_length=255)
    description = models.TextField()
    highlight_text = models.TextField()
    year = models.IntegerField()
    mission_text = models.TextField()
    vision_text = models.TextField()
    values_text = models.TextField()

    def __str__(self):
        return self.title
    
class Image(BaseModel):
    image = models.ImageField(upload_to='static/main/assets')
    alt_text = models.CharField(max_length=255)

    def __str__(self):
        return self.alt_text

# Visit Object
class Visit(BaseModel):
    visit = models.PositiveIntegerField()
    modified_date = models.DateTimeField(auto_now=True)
    def __str__(self):
        return str(self.visit)
    
# Blog Related Models
    
class Category(BaseModel):
    name = models.CharField(max_length=100)
    slug = models.SlugField(default='', blank=True, null=True)

    def __str__(self):
        return self.name
    
    class Meta:
        verbose_name_plural = "Categories"
        ordering = ['name']

    def get_absolute_url(self):
        return '/%s/' % self.slug

class Blog(BaseModel):
    ACTIVE = 'active'
    DRAFT = 'draft'

    CHOICES_STATUS = (
        (ACTIVE, 'Active'),
        (DRAFT, 'Draft')
    )

    title = models.CharField(max_length=300)
    intro = models.TextField(null=True, blank=True)
    category = models.ForeignKey(Category, on_delete=models.CASCADE, related_name='category', null=True, blank=True)
    content = RichTextField()
    publication_date = models.DateTimeField(auto_now_add=True)
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    slug = models.SlugField(max_length=300, unique=True, null=True, blank=True)
    views = models.PositiveIntegerField(default=0)
    status = models.CharField(max_length=10, choices=CHOICES_STATUS, default=DRAFT)
    image = models.ImageField(upload_to='blog/images', null=True, blank=True)

    class Meta:
        ordering = ('-created_at',)

    def get_absolute_url(self):
        return reverse('blog_detail', args=[self.slug])
    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.title)
        super(Blog, self).save(*args, **kwargs)

    def __str__(self):
        return self.title

class Tag(BaseModel):
    name = models.CharField(max_length=50)

    def __str__(self):
        return self.name
    

class Affiliate(BaseModel):
    code = models.CharField(max_length=50, unique=True)
    clicks = models.PositiveIntegerField(default=0)

    def __str__(self):
        return f"Affilicate Code: {self.code} - Clicks: {self.clicks}"