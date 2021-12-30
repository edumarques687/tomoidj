from django.shortcuts import render, get_object_or_404, redirect
from jutsu.models import Jutsu
from .models import Tome
from .forms import TomeForm
from django.views.decorators.csrf import csrf_protect
import time

# Create your views here.

@csrf_protect
def tome_list(request):
    if not request.user.is_authenticated:
        return redirect('loginuser')
    message = ''
    if request.method == "POST":
        if request.POST['name'] == '':
            message = 'Defina um nome para seu tomo de jutsus ;)'
        elif len(request.POST['name']) > 100:
            message = 'O nome informado é grande demais ;)'
        else:
            form = TomeForm(request.POST)
            new_tome = form.save(commit=False)
            new_tome.user = request.user
            new_tome.save()
            message = 'Grimório criado com sucesso!'
    if request.user.is_authenticated:
        user_tomes = Tome.objects.filter(user=request.user).all().order_by('name')
        if user_tomes is not None:
            return render(request, 'tome/tome_list.html', {
                'user_tomes': user_tomes, 'message': message})
    return render(request, 'homepage/loginuser.html')


@csrf_protect
def delete_tome(request):
    if request.method == 'POST':
        if request.user.is_authenticated:
            tome = get_object_or_404(Tome, pk=request.POST['tome_id'])
            tome.delete()
            user_tomes = Tome.objects.filter(user=request.user).all().order_by('name')
            return render(request, 'tome/tome_list.html', {
                'user_tomes': user_tomes, 'message': 'Grimório {} excluído com sucesso!'.format(tome.name)})
        return render(request, 'homepage/loginuser.html')

@csrf_protect
def tome_page(request):
    if not request.user.is_authenticated:
        return redirect('loginuser')
    if request.method == 'POST':
        if request.POST['action'] == 'Excluir':
            return delete_tome(request)

        tome = get_object_or_404(Tome, pk=request.POST['tome_id'])
        jutsu_list = [val for val in Jutsu.objects.all().order_by('name') if val in tome.jutsus.all()]
        return render(request, 'tome/tome_page.html', {
            'tome': tome,
            'jutsu_list': jutsu_list,
            'grades': ['BA', 'ME', 'AV', 'SU', 'LE'],
            'chacras': ['FO', 'DE', 'CO', 'IN', 'SA', 'CA'],
            'count': len(jutsu_list)})


@csrf_protect
def add_jutsus(request):
    if request.method == 'POST':
        tome = get_object_or_404(Tome, pk=request.POST['tome_id'])
        for value in request.POST:
            if 'jutsu' in value:
                jutsu_id = value.replace('jutsu', '')
                sp = Jutsu.objects.get(id=jutsu_id)
                tome.jutsus.add(sp.id)

        jutsu_list = [val for val in Jutsu.objects.all().order_by('name') if val in tome.jutsus.all()]
        return render(request, 'tome/tome_page.html', {
            'tome': tome, 'jutsu_list': jutsu_list,
            'grades': ['BA', 'ME', 'AV', 'SU', 'LE'],
            'chacras': ['FO', 'DE', 'CO', 'IN', 'SA', 'CA'],
            'count': len(jutsu_list)})

@csrf_protect
def remove_jutsu(request):
    if request.method == 'POST':
        tome = get_object_or_404(Tome, pk=request.POST['tome_id'])
        value = request.POST['jutsu']
        jutsu_id = value.replace('jutsu', '')
        sp = Jutsu.objects.get(id=jutsu_id)
        tome.jutsus.remove(sp.id)

        jutsu_list = [val for val in Jutsu.objects.all().order_by('name') if val in tome.jutsus.all()]
        print("Removing jutsu {} in tome {}".format(jutsu_id, tome.id))
        return render(request, 'tome/tome_page.html', {
            'tome': tome,
            'jutsu_list': jutsu_list,
            'grades': ['BA', 'ME', 'AV', 'SU', 'LE'],
            'chacras': ['FO', 'DE', 'CO', 'IN', 'SA', 'CA'],
            })
