import datetime
from django.http import HttpResponseRedirect
from django.urls import reverse
from django.shortcuts import render
from wishlist.models import BarangWishlist
from django.http import HttpResponse
from django.core import serializers
from django.shortcuts import redirect
from django.contrib.auth.forms import UserCreationForm
from django.contrib import messages
from django.contrib.auth import authenticate, login
from django.contrib.auth import logout
from django.contrib.auth.decorators import login_required
from .forms import BarangForm

@login_required(login_url='/wishlist/login/')
def show_wishlist(request):
    data_barang_wishlist = BarangWishlist.objects.all()
    context = {
    'list_barang': data_barang_wishlist,
    'nama': request.user,
    'last_login': request.COOKIES['last_login'],
}
    return render(request, "wishlist.html", context)

def show_wishlist_ajax(request):
    if request.method == 'POST':
        form = BarangForm(request.POST)  
   
        if form.is_valid():
            nama_barang = form.cleaned_data["nama_barang"]
            harga_barang = form.cleaned_data["harga_barang"]
            deskripsi = form.cleaned_data["deskripsi"]
            task_temp = tambah_barang(nama_barang, harga_barang, deskripsi)
            task_temp.save()
        return HttpResponseRedirect("/wishlist/ajax" )
    else:
        form = BarangForm()
    data_barang_wishlist = BarangWishlist.objects.all()
    context = {
    'list_barang': data_barang_wishlist,
    'nama': request.user,
    'last_login': request.COOKIES['last_login'],
    'form' : form
    }
    return render(request, "wishlist_ajax.html", context)

def show_xml(request):
    data = BarangWishlist.objects.all()
    return HttpResponse(serializers.serialize("xml", data), content_type="application/xml")

def show_json(request):
    data = BarangWishlist.objects.all()
    return HttpResponse(serializers.serialize("json", data), content_type="application/json")

def show_json_by_id(request, id):
    data = BarangWishlist.objects.filter(pk=id)
    if id == 1:
        return HttpResponse(serializers.serialize("json", data), content_type="application/json")
    else:
        return HttpResponse(serializers.serialize("xml", data), content_type="application/xml")

def register(request):
    form = UserCreationForm()

    if request.method == "POST":
        form = UserCreationForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'Akun telah berhasil dibuat!')
            return redirect('wishlist:login')
    
    context = {'form':form}
    return render(request, 'register.html', context)

def login_user(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            response = HttpResponseRedirect(reverse("wishlist:show_wishlist")) # membuat response
            response.set_cookie('last_login', str(datetime.datetime.now())) # membuat cookie last_login dan menambahkannya ke dalam response
            return response
        else:
            messages.info(request, 'Username atau Password salah!')
    context = {}
    return render(request, 'login.html', context)

def logout_user(request):
    logout(request)
    response = HttpResponseRedirect(reverse('wishlist:login'))
    response.delete_cookie('last_login')
    return response

def show_css(request):
    return render(request, 'CSSTutorial.html')

def tambah_barang(nama_barang, harga_barang, deskripsi):
    return BarangWishlist.objects.create(nama_barang = nama_barang, harga_barang = harga_barang, deskripsi = deskripsi)

