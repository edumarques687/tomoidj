from django.shortcuts import render, get_object_or_404
from jutsu.models import Jutsu, Enhancement
from django.db.models import Q
from tome.models import Tome
# import unidecode
# import regex as rx

def jutsus_page(request):
    user_tomes = False

    if request.user.is_authenticated:
        user_tomes = Tome.objects.filter(user=request.user).all().order_by('name')

    if request.method == 'GET':
        query = Q()
        query &= Q()
        chacra_filters = ['FO', 'DE', 'CO', 'IN', 'SA', 'CA']
        descriptor_filters = ['AB', 'AD', 'EM', 'AC', 'EL', 'FO', 'FR', 'VE', 'EN', 'IL', 'IN', 'NI', 'LU', 'TR', 'TT', 'VA']
        for key, value in request.GET.items():
            if value != '':
                if 'ch' in key and value != '':
                    if any(value in s for s in chacra_filters):
                        query |= Q(chacra__icontains=value)
        jutsus = Jutsu.objects.filter(query).order_by('sorting_name')
        query = Q()

        for key, value in request.GET.items():
            if value != '':
                if key == 'keyword' and value != '':
                    kw_list = value.split(';')
                    for kw in kw_list:
                        query |= Q(name__icontains=kw)
                        query |= Q(enhancement__cost__icontains=kw)
                        query |= Q(description__icontains=kw)
                        query |= Q(enhancement__effect__icontains=kw)
                    jutsus = jutsus.filter(query).distinct()
                    query = Q()

        for key, value in request.GET.items():
            if value != '':
                if 'desc' in key and value != '':
                    if any(value in s for s in descriptor_filters):
                        query |= Q(descriptor__icontains=value)
                        query |= Q(descriptor2__icontains=value)
                        query |= Q(descriptor3__icontains=value)
                        query |= Q(descriptor4__icontains=value)
                if key == 'execution' and value != '':
                    query &= Q(execution__icontains=value)
                if key == 'duration' and value != '':
                    query &= Q(duration__icontains=value)
                if key == 'range' and value != '':
                    query &= Q(range__icontains=value)
                if key == 'target_area_effect' and value != '':
                    query &= Q(target_area_effect__icontains=value)
                if key == 'resistance' and value != '':
                    query &= Q(resistance__icontains=value)
                if key == 'book_magazine' and value != '':
                    query &= Q(book_magazine__icontains=value)

        jutsus = jutsus.filter(query).order_by('sorting_name').distinct()
        origins = []
        for jutsu in jutsus:
            jutsu_origin = jutsu.book_magazine
            if jutsu_origin not in origins:
                origins.append(jutsu_origin)
        return render(request, 'jutsu/jutsus_page.html', {'jutsus': jutsus,
                                                          'grades': ['BA', 'ME', 'AV', 'SU', 'LE'],
                                                          'chacras': ['FO', 'DE', 'CO', 'IN', 'SA', 'CA'],
                                                          'user_tomes': user_tomes,
                                                          'origins': origins,
                                                          })


def jutsu_details(request, jutsu_id):
    jutsu = get_object_or_404(Jutsu, pk=jutsu_id)
    enhancements = Enhancement.objects.filter(related_jutsu=jutsu_id)
    return render(request, 'jutsu/jutsu_details.html', {'jutsu': jutsu, 'enhancements': enhancements})

"""
def remove_control_characters(str):
    return rx.sub(r'[\x02]', '', str)

def remove_strange_char(request):
    jutsus = Jutsu.objects.order_by('name').all()
    for j in jutsus:
        j.description = remove_control_characters(j.description)
        j.name = remove_control_characters(j.name)
        j.execution = remove_control_characters(j.execution)
        j.range = remove_control_characters(j.range)
        j.target_area_effect = remove_control_characters(j.target_area_effect)
        j.duration = remove_control_characters(j.duration)
        j.resistance = remove_control_characters(j.resistance)
        j.save()
        enhancements = Enhancement.objects.filter(related_jutsu=j.id)
        for en in enhancements:
            en.effect = remove_control_characters(en.effect)
            en.save()

    return render(request, 'homepage/home.html', {'response': 'DONE'})

def copy_sorting_name(request):
    jutsus = Jutsu.objects.order_by('name').all()
    for jutsu in jutsus:
        jutsu.sorting_name = unidecode.unidecode(jutsu.name)
        jutsu.save()
    return render(request, 'homepage/home.html', {'response': 'sorting names copied'})

def complete_fields(request):
    jutsus = Jutsu.objects.order_by('name').all()
    for j in jutsus:
        if j.execution == "m":
            j.execution = "ação de movimento"
        if j.execution == "p":
            j.execution = "ação padrão"
        if j.execution == "l":
            j.execution = "ação livre"
        if j.execution == "c":
            j.execution = "ação completa"
        if j.execution == "r":
            j.execution = "reação"
        if j.range == "p":
            j.range = "pessoal"
        if j.range == "cc":
            j.range = "corpo-a-corpo"
        if j.range == "c":
            j.range = "curto"
        if j.range == "l":
            j.range = "longo"
        if j.range == "i":
            j.range = "ilimitado"
        if j.target_area_effect == "v":
            j.target_area_effect = "você"
        if j.target_area_effect == "1":
            j.target_area_effect = "1 criatura"
        if j.duration == "c":
            j.duration = "cena"
        if j.duration == "i":
            j.duration = "instantânea"
        if j.duration == "p":
            j.duration = "permanente"
        if j.duration == "vv":
            j.duration = "veja texto"
        if j.resistance == "vv":
            j.resistance = "veja texto"
        j.save()

    return render(request, 'homepage/home.html', {'response': 'DONE'})

def remove_blank_space(str):
    new = rx.sub(r'^ ', '', str)
    new = rx.sub(r' $', '', new)
    return new

def trim(request):
    jutsus = Jutsu.objects.order_by('name').all()
    for j in jutsus:
        j.description = remove_blank_space(j.description)
        j.name = remove_blank_space(j.name)
        j.execution = remove_blank_space(j.execution)
        j.range = remove_blank_space(j.range)
        j.target_area_effect = remove_blank_space(j.target_area_effect)
        j.duration = remove_blank_space(j.duration)
        j.resistance = remove_blank_space(j.resistance)
        j.save()
        enhancements = Enhancement.objects.filter(related_jutsu=j.id)
        for en in enhancements:
            en.effect = remove_blank_space(en.effect)
            en.save()

    return render(request, 'homepage/home.html', {'response': 'DONE'})
"""