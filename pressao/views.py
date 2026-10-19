from django.contrib import messages
from django.contrib.auth import login
from django.contrib.auth.decorators import login_required
from django.db.models import Avg
from django.shortcuts import get_object_or_404, redirect, render
from django.utils import timezone

from .forms import CadastroForm, MedicaoForm
from .models import Medicao


def cadastro(request):
    if request.user.is_authenticated:
        return redirect("lista")
    form = CadastroForm(request.POST or None)
    if request.method == "POST" and form.is_valid():
        user = form.save()
        login(request, user)
        messages.success(request, "Conta criada com sucesso!")
        return redirect("lista")
    return render(request, "registration/cadastro.html", {"form": form})


# READ (lista)
@login_required
def lista(request):
    medicoes = Medicao.objects.filter(usuario=request.user)
    medias = medicoes.aggregate(s=Avg("sistolica"), d=Avg("diastolica"), p=Avg("pulso"))
    ctx = {
        "medicoes": medicoes,
        "total": medicoes.count(),
        "media_s": round(medias["s"]) if medias["s"] else None,
        "media_d": round(medias["d"]) if medias["d"] else None,
        "media_p": round(medias["p"]) if medias["p"] else None,
        "ultima": medicoes.first(),
    }
    return render(request, "pressao/lista.html", ctx)


# CREATE
@login_required
def criar(request):
    inicial = {"data_hora": timezone.localtime().strftime("%Y-%m-%dT%H:%M")}
    form = MedicaoForm(request.POST or None, initial=inicial)
    if request.method == "POST" and form.is_valid():
        medicao = form.save(commit=False)
        medicao.usuario = request.user
        medicao.save()
        messages.success(request, "Medição registrada!")
        return redirect("lista")
    return render(request, "pressao/form.html", {"form": form, "titulo": "Nova medição"})


# UPDATE
@login_required
def editar(request, pk):
    medicao = get_object_or_404(Medicao, pk=pk, usuario=request.user)
    form = MedicaoForm(request.POST or None, instance=medicao)
    if request.method == "POST" and form.is_valid():
        form.save()
        messages.success(request, "Medição atualizada!")
        return redirect("lista")
    return render(request, "pressao/form.html", {"form": form, "titulo": "Editar medição"})


# DELETE
@login_required
def excluir(request, pk):
    medicao = get_object_or_404(Medicao, pk=pk, usuario=request.user)
    if request.method == "POST":
        medicao.delete()
        messages.success(request, "Medição excluída.")
        return redirect("lista")
    return render(request, "pressao/confirmar_exclusao.html", {"medicao": medicao})
