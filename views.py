import os
from django.template import Context
from django.http import HttpResponse
from django.shortcuts import get_object_or_404
from django.utils.html import mark_safe
from mezzanine.core.views import direct_to_template

import pprint

from urlparse import urlparse, urlunparse

from mezzanine.blog.models import BlogPost
from mezzanine.blog.templatetags.blog_tags import blog_recent_posts
from mezzanine.galleries.models import Gallery
from mezzanine.pages.models import Page
from mezzanine.conf import settings

from mezzanine.utils.views import render

from ckeditor.views import upload, get_upload_filename, get_thumb_filename
from PIL import Image, ImageOps
from datetime import datetime
from django.views.decorators.csrf import csrf_exempt
from django.core.files.base import ContentFile
from django.core.files.storage import default_storage

from django.contrib.sites.models import get_current_site

def blog_homepage(request):
    """ 
    Display the homepage
    """
    current_site = get_current_site(request).domain

#    if current_site == "gracebreedlove.com": 
#        page = get_object_or_404(Page, slug="grace-breedlove-photography")
#        content = mark_safe(page.richtextpage.content)
#        context = { 'page' : page, 'content' : content  }
#        return render(request, "photo_index.html", context)

    if current_site == "solarpoweredyogi.com":
        settings.use_editable()
        blog_posts = BlogPost.objects.published(for_user=request.user)

        slider_posts = blog_posts[:4]
        section_posts = blog_posts[0:15]

        context = { "slider_posts" : slider_posts, "section_posts": section_posts }

        return render(request, "index.html", context)

    settings.use_editable()
    blog_posts = BlogPost.objects.published(for_user=request.user)

    slider_posts = blog_posts[:4]
    section_posts = blog_posts[0:15]

    context = { "slider_posts" : slider_posts, "section_posts": section_posts }

    return render(request, "index.html", context)


THUMBNAIL_SIZE = ( 425, 300 )
@csrf_exempt
def ckupload(request):
    """ 
    run normal upload for ckeditor, 
    move the file over to storage,
    then delete it.
    """

    #callback = upload(request)
    #return callback
    # Get the uploaded file from request.
    upload = request.FILES['upload']
    upload_ext = os.path.splitext(upload.name)[1]

    # If CKEDITOR_RESTRICT_BY_USER is True upload file to user specific path.
    if getattr(settings, 'CKEDITOR_RESTRICT_BY_USER', False):
        user_path = user.username
    else:
        user_path = ''

    # Generate date based path to put uploaded file.
    date_path = datetime.now().strftime('%Y/%m/%d')

    # Complete upload path (upload_path + date_path).
    upload_path = os.path.join(settings.CKEDITOR_UPLOAD_PATH, user_path, \
            date_path)

    # Open output file in which to store upload.
    saved_path = default_storage.save(upload_path + '/' + upload.name, ContentFile(upload.read()))





    ###make thumbnail###
    tmp_filename = 'tmp' + os.path.splitext(upload.name)[1]
    out = open(tmp_filename, 'wb+')

    # Iterate through chunks and write to destination.
    for chunk in upload.chunks():
        out.write(chunk)
    out.close()

    image = Image.open(tmp_filename)

    if image.mode not in ('L', 'RGB'):
        image = image.convert('RGB')
    # scale and crop to thumbnail
    imagefit = ImageOps.fit(image, THUMBNAIL_SIZE, Image.ANTIALIAS)
    default_storage.save(upload_path + '/' + get_thumb_filename(upload.name), ContentFile(imagefit))

    # Respond with Javascript sending ckeditor upload url.
    #url = get_media_url(upload_filename)
    url = settings.MEDIA_URL + saved_path
    return HttpResponse("""
    <script type='text/javascript'>
        window.parent.CKEDITOR.tools.callFunction(%s, '%s');
    </script>""" % (request.GET['CKEditorFuncNum'], url))

def portfolio_homepage(request):
    """ display the portfolio homepage
    """
    galleries = Gallery.objects.published(for_user=request.user)

    page = get_object_or_404(Page, slug="portfolio")

    context = { "galleries" : galleries, "page": page }

    return render(request, "portfolio_home.html", context )
