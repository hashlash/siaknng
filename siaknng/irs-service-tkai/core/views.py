from django.shortcuts import render
from django.http import HttpResponse, JsonResponse
from .models import *
from django.views.decorators.csrf import csrf_exempt
import requests
import json
import datetime

def index(request):
    return HttpResponse("Hello, world. You're at the core index.")

def cek_tanggal(start_irs, end_irs):
    datetime_now = datetime.datetime.now()
    if(datetime_now >= start_irs and datetime_now<=end_irs):
        return True
    return False

@csrf_exempt
def setMatkul(request):
    if((request.method == 'POST') and ('Authorization' in request.headers)):
        token_acquired = request.headers['Authorization']
        # request ke /account/ dengan token untuk mendapatkan obj user
        response_account = requests.get(
            # works
            'http://www.mocky.io/v2/5de66c953700004f00092366',
            
            # fakultas not found
            # 'http://www.mocky.io/v2/5de66cd13700005d00092369',

            # matakuliah 0
            # 'http://www.mocky.io/v2/5de66e4a3700005d00092376',
            headers={'Authorization': token_acquired}
        )
        
        # Melakukan pemanggilan service pembayaran dan service kalender
        response_pembayaran = requests.get(
            # 'http://www.mocky.io/v2/5deb48072f00000e0007e1d1', 
            'http://165.22.108.118:8001/api/pembayaran-siak/',
            headers={'Authorization': token_acquired}
        )

        response_kalender = requests.get(
            # 'http://www.mocky.io/v2/5deb48902f0000750007e1d8',
            'http://165.22.108.118:8000/api/jadwal-siak/', 
            headers={'Authorization': token_acquired}
        )
        
        # Mengambil response dari service pembayaran dan service kalender
        pembayaran_available = response_pembayaran.json()['status_pembayaran']
        jadwal_available = response_kalender.json()['status_jadwal']
        if(jadwal_available and pembayaran_available):
            # Get Faculty ID untuk konfirmasi tanggal pelaksanaan irs
            faculty_id = int(response_account.json()['faculty_id'])
            try:
                Fakultas.objects.get(id=faculty_id)
            except:
                return JsonResponse({'error':'Fakultas not found'})
            fakultas_ = Fakultas.objects.get(id=faculty_id)
            
            try:
                out = request.POST['list_matkul']
                hasil = {
                    'status':'tersimpan',
                    'mata_kuliah':json.loads(out)
                }
            except KeyError:
                hasil = {
                    'status':'gagal menyimpan',
                    'mata_kuliah': None
                }
    
            return JsonResponse(hasil, safe=False)
        return JsonResponse('IRS tidak dapat diisi pada tanggal ini', safe=False)

def getMatkul(request):
    # nerima token
    if 'Authorization' in request.headers:
        token_acquired = request.headers['Authorization']
        # request ke /account/ dengan token
        response_account = requests.get(
            # works
            'http://www.mocky.io/v2/5de66c953700004f00092366',
            
            # fakultas not found
            # 'http://www.mocky.io/v2/5de66cd13700005d00092369',

            # matakuliah 0
            # 'http://www.mocky.io/v2/5de66e4a3700005d00092376',
            headers={'Authorization': token_acquired}
        )
        faculty_id = int(response_account.json()['faculty_id'])

        try:
            Fakultas.objects.get(id=faculty_id)
        except:
            return JsonResponse({'error':'Fakultas not found'})
        fakultas_ = Fakultas.objects.get(id=faculty_id)

        matkul = list(MataKuliah.objects.all().filter(fakultas=fakultas_).values())
        return JsonResponse(matkul, safe=False)