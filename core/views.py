from django.shortcuts import render, redirect, get_object_or_404
from django.http import HttpResponse, JsonResponse
from django.views.decorators.csrf import csrf_exempt
from .models import Paste
from django.utils import timezone
from django.conf import settings
import os
from datetime import datetime

# Home: Create new paste (text/file upload)
def home(request):
    if request.method == 'POST':
        content_type = request.POST.get('content_type')
        text_content = request.POST.get('text_content')
        file_content = request.FILES.get('file_content')
        expires_at = request.POST.get('expires_at')
        paste = Paste(content_type=content_type)
        if content_type == 'text':
            paste.text_content = text_content
        elif content_type == 'file' and file_content:
            paste.file_content = file_content
        if expires_at:
            try:
                paste.expires_at = datetime.strptime(expires_at, '%Y-%m-%dT%H:%M')
            except Exception:
                paste.expires_at = None
        paste.save()
        return redirect('display_paste', code=paste.code)
    return render(request, 'core/home.html')

# Retrieve: Enter 4-digit code to access content
def retrieve(request):
    if request.method == 'POST':
        code = request.POST.get('code')
        return redirect('display_paste', code=code)
    return render(request, 'core/retrieve.html')

# Display: Show the retrieved content
def display_paste(request, code):
    paste = get_object_or_404(Paste, code=code)
    if paste.expires_at and timezone.now() > paste.expires_at:
        return HttpResponse('This paste has expired.', status=410)
    return render(request, 'core/display.html', {'paste': paste})

# Add a new view for file download
def download_file(request, code):
    paste = get_object_or_404(Paste, code=code)
    if paste.content_type == 'file' and paste.file_content:
        file_path = paste.file_content.path
        if os.path.exists(file_path):
            with open(file_path, 'rb') as f:
                response = HttpResponse(f.read(), content_type='application/octet-stream')
                response['Content-Disposition'] = f'attachment; filename="{os.path.basename(file_path)}"'
                return response
        else:
            return HttpResponse('File not found.', status=404)
    return HttpResponse('Invalid file request.', status=400)

# API endpoint for creating pastes
@csrf_exempt
def api_create(request):
    if request.method == 'POST':
        content_type = request.POST.get('content_type')
        text_content = request.POST.get('text_content')
        file_content = request.FILES.get('file_content')
        expires_at = request.POST.get('expires_at')
        paste = Paste(content_type=content_type)
        if content_type == 'text':
            paste.text_content = text_content
        elif content_type == 'file' and file_content:
            paste.file_content = file_content
        if expires_at:
            try:
                paste.expires_at = datetime.strptime(expires_at, '%Y-%m-%dT%H:%M')
            except Exception:
                paste.expires_at = None
        paste.save()
        return JsonResponse({'code': paste.code})
    return JsonResponse({'error': 'Invalid request'}, status=400)
