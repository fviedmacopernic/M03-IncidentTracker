from django.shortcuts import render
from django.contrib.auth.decorators import login_required

@login_required  # Aquesta línia protegeix la vista. Sense sessió, no passes.
def perfil_usuari(request):
    return render(request, 'perfil.html')
