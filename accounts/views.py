from django.http import HttpResponse, JsonResponse
from django.shortcuts import get_object_or_404, render, redirect
from django.contrib.auth import login as auth_login
from django.contrib.auth import logout as auth_logout
from django.contrib.auth.forms import AuthenticationForm
from django.utils import timezone
from .forms import RegisterForm
from .forms import UploadFileForm
from django.core.files.storage import FileSystemStorage
from .models import UploadedFile
from django.contrib.auth.decorators import login_required

import pandas as pd

def register(request):
    if request.method == 'POST':
        form = RegisterForm(request.POST)
        if form.is_valid():
            user = form.save()
            auth_login(request, user)
            user.last_login = timezone.now()
            user.save()
            return redirect('upload_and_list_files')
    else:
        form = RegisterForm()
    return render(request, 'accounts/register.html', {'form': form})

def login(request):
    if request.method == 'POST':
        form = AuthenticationForm(request, data=request.POST)
        if form.is_valid():
            user = form.get_user()
            auth_login(request, user)
            user.last_login = timezone.now()
            user.save()
            return redirect('upload_and_list_files')
    else:
        form = AuthenticationForm()
    return render(request, 'accounts/login.html', {'form': form})

def logout(request):
    auth_logout(request)
    return redirect('login')


@login_required
def upload_and_list_files(request):
    if request.method == 'POST':
        form = UploadFileForm(request.POST, request.FILES)
        if form.is_valid():
            file = request.FILES['file']
            
            uploadFile = UploadedFile.objects.create(user=request.user, file=file)
            try:
                file_path = uploadFile.file.path
                df = pd.read_excel(file_path)
                
            except Exception as e:
                uploadFile.delete()  # 删除失败上传记录
                return render(request, 'accounts/upload_and_list.html', {
                    'form': form,
                    'files': UploadedFile.objects.filter(user=request.user).order_by('-upload_time'),
                    'last_login': request.user.last_login,
                    'username': request.user.username,
                    'error': f'读取文件时出错，请上传格式正确的文件'
                })
            return redirect('upload_and_list_files')
    else:
        form = UploadFileForm()

    files = UploadedFile.objects.filter(user=request.user).order_by('-upload_time')
    last_login = request.user.last_login
    username = request.user.username
    return render(request, 'accounts/upload_and_list.html', {'form': form, 'files': files,
                                                             'last_login': last_login, 'username': username})
@login_required
def delete_file(request, file_id):
    file = get_object_or_404(UploadedFile, id=file_id, user=request.user)
    if request.method == 'POST':
        file.delete()
        return redirect('upload_and_list_files')
    return redirect('upload_and_list_files')

@login_required
def visualize(request, file_id):
    file = get_object_or_404(UploadedFile, id=file_id, user=request.user)
    file_path = file.file.path
    df = pd.read_excel(file_path)

    stock_codes = df['股票代码'].unique().tolist()
    avg_open_prices = df.groupby('股票代码')['开盘价'].mean().tolist()
    avg_close_prices = df.groupby('股票代码')['收盘价'].mean().tolist()
    max_prices = df.groupby('股票代码')['最高价'].max().tolist()
    min_prices = df.groupby('股票代码')['最低价'].min().tolist()
    total_volume = df.groupby('股票代码')['交易量'].sum().tolist()

    df['日期'] = pd.to_datetime(df['日期'])
    start_price = df.groupby('股票代码').apply(lambda x: x.loc[x['日期'].idxmin()]['收盘价'])
    end_price = df.groupby('股票代码').apply(lambda x: x.loc[x['日期'].idxmax()]['收盘价'])
    changes = ((end_price - start_price) / start_price) * 100
    changes = changes.tolist()

    avg_amplitude = df.groupby('股票代码')['振幅'].mean().tolist()
    avg_turnover = df.groupby('股票代码')['换手率'].mean().tolist()

    stock_datas = {}
    for code in stock_codes:
        stock_df = df[df['股票代码'] == code]
        stock_df['收盘价'].fillna(0, inplace=True)  
        stock_df['振幅'].fillna(0, inplace=True)  
        stock_df['换手率'].fillna(0, inplace=True)  

        open_prices = stock_df['开盘价'].tolist()
        close_prices = stock_df['收盘价'].tolist()
        high_prices = stock_df['最高价'].tolist()
        low_prices = stock_df['最低价'].tolist()

        ochl = [list(t) for t in zip(open_prices, close_prices, high_prices, low_prices)]

        stock_datas[code] = {
            'dates': stock_df['日期'].dt.strftime('%Y-%m-%d').tolist(),
            'open_prices': stock_df['开盘价'].tolist(),
            'close_prices': stock_df['收盘价'].tolist(),
            'high_prices': stock_df['最高价'].tolist(),
            'low_prices': stock_df['最低价'].tolist(),
            'ochl': ochl,
            'volumes': stock_df['交易量'].tolist(),
            'amplitude': stock_df['振幅'].tolist(),
            'turnover': stock_df['换手率'].tolist(),
            'change_rate': stock_df['涨跌幅'].tolist(),
            'sma_5': [x if pd.notnull(x) else None for x in stock_df['收盘价'].rolling(window=5).mean().tolist()],
            'sma_10': [x if pd.notnull(x) else None for x in stock_df['收盘价'].rolling(window=10).mean().tolist()],
            'sma_30': [x if pd.notnull(x) else None for x in stock_df['收盘价'].rolling(window=30).mean().tolist()]
        }

    data = {
        'stock_codes': stock_codes,
        'avg_open_prices': avg_open_prices,
        'avg_close_prices': avg_close_prices,
        'max_prices': max_prices,
        'min_prices': min_prices,
        'total_volume': total_volume,
        'changes': changes,
        'avg_amplitude': avg_amplitude,
        'avg_turnover': avg_turnover,
        'stock_datas': stock_datas
    }

    return render(request, 'accounts/visualize.html', {'data': data})
