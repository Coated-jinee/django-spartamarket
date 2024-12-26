from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from .forms import ProductForm
from .models import Product
from django.db.models import Q, Count

def product_list_view(request):
    # GET 요청에서 검색어와 정렬 기준 가져오기
    query = request.GET.get('query', '')  # 검색어 가져오기
    sort_by = request.GET.get('sort', 'created_at')  # 정렬 기준 가져오기 (기본값: 최신순)

    # 기본 QuerySet
    products = Product.objects.all()

    # 검색어가 있으면 필터링
    if query:
        products = products.filter(
            Q(title__icontains=query) |  # 제목에 검색어 포함
            Q(description__icontains=query) |  # 설명에 검색어 포함
            Q(user__username__icontains=query) |  # 작성자 이름에 검색어 포함
            Q(hashtags__name__icontains=query)  # 해시태그 이름에 검색어 포함
        ).distinct()  # 중복 제거

    # 정렬 옵션 적용
    products = products.annotate(like_count=Count('likes'))  # 모든 정렬에서 like_count 포함

    if sort_by == 'likes':  # 인기순 정렬
        products = products.order_by('-like_count', '-created_at')
    elif sort_by == 'views':  # 조회수순 정렬
        products = products.order_by('-views', '-created_at')
    else:  # 최신순 정렬
        products = products.order_by('-created_at')

    return render(request, 'products/product_list.html', {'products': products, 'query': query})


@login_required
def product_create_view(request):
    if request.method == 'POST':
        form = ProductForm(request.POST, request.FILES, user=request.user)
        if form.is_valid():
            form.save()
            return redirect('products:product_list')
    else:
        form = ProductForm(user=request.user)

    return render(request, 'products/product_form.html', {'form': form})

@login_required
def product_edit_view(request, pk):
    product = get_object_or_404(Product, pk=pk)

    # 작성자만 수정 가능
    if product.user != request.user:
        return redirect('products:product_detail', pk=pk)

    if request.method == 'POST':
        form = ProductForm(request.POST, request.FILES, instance=product)
        if form.is_valid():
            form.save()
            return redirect('products:product_detail', pk=pk)
    else:
        form = ProductForm(instance=product)

    return render(request, 'products/product_form.html', {'form': form})

@login_required
def product_delete_view(request, pk):
    # 삭제할 상품 가져오기
    product = get_object_or_404(Product, pk=pk)
    
    # POST 요청일 때만 삭제 수행
    if request.method == 'POST':
        product.delete()
        return redirect('products:product_list')  # 삭제 후 목록으로 이동

    # GET 요청일 경우 삭제 확인 페이지 렌더링
    return render(request, 'products/product_confirm_delete.html', {'product': product})

# 상품 상세 보기: 조회수 증가 포함
def product_detail_view(request, pk):
    product = get_object_or_404(Product, pk=pk)
    
    # 조회수 증가
    product.views += 1
    product.save()
    
    # 찜수 계산
    like_count = product.likes.count()
    
    return render(request, 'products/product_detail.html', {
        'product': product,
        'like_count': like_count,
    })

# 찜하기(좋아요) 처리
def product_like_view(request, pk):
    product = get_object_or_404(Product, pk=pk)
    if request.user in product.likes.all():
        product.likes.remove(request.user)  # 찜 취소
    else:
        product.likes.add(request.user)  # 찜하기 추가
    return redirect('products:product_detail', pk=pk)  # 상세 페이지로 리디렉션