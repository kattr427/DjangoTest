from django.core.files.storage import FileSystemStorage
from django.http import HttpRequest, HttpResponse
from django.shortcuts import render, reverse, redirect

from request_app.forms import UserForm, UploadFileForm

MAX_FILE_SIZE = 10 * 1024

def process_get(request: HttpRequest) -> HttpResponse:
    a = request.GET.get('a', '')
    b = request.GET.get('b', '')
    result = a + b
    context={
        'a': a,
        'b': b,
        'result': result,
    }
    return render(request, 'request_app/request_query_params.html',context=context)


def user_form(request: HttpRequest) -> HttpResponse:

    context = {
        'form': UserForm(),
    }

    return render(request, 'request_app/user-form.html', context=context)

def upload_file(request: HttpRequest):
    if request.method == "POST":
        form = UploadFileForm(request.POST, request.FILES)
        if form.is_valid():

            # myfile = request.FILES['myfile']
            myfile = form.cleaned_data['file']

            if myfile.size > MAX_FILE_SIZE:
                print(f'Файл слишком большой! Максимальный размер { MAX_FILE_SIZE // 1024}KB')

                url = reverse('request_app:file-upload')

                return redirect(url)

            fs = FileSystemStorage()
            try:
                filename = fs.save(myfile.name, myfile)
                print(f'сохранили файл: {filename}')
            except Exception as e:
                print(f'Ошибка загрузки файла {e}')
    else:
        form = UploadFileForm()

    context = {
        'form': form,
    }

    return render(request, 'request_app/file-upload.html', context=context)
