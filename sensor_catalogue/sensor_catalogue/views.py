from django.shortcuts import redirect


def redirect_howe_to_catalogue_view(request):
    return redirect('/catalogue/')
