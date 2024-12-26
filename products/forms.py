from django import forms
from .models import Product, HashTag

class ProductForm(forms.ModelForm):
    hashtags_str = forms.CharField(required=False)

    # 폼 초기화 시 사용자 정보를 전달받음
    def __init__(self, *args, **kwargs):
        self.user = kwargs.pop('user', None)
        super().__init__(*args, **kwargs)

    class Meta:
        model = Product
        fields = ['title', 'description', 'image', 'hashtags_str']

    def save(self, commit=True):
        # 부모 클래스의 save 메서드 호출 (commit=False로 저장)
        product = super().save(commit=False)

        # 현재 로그인한 사용자 설정
        if self.user:
            product.user = self.user

        if commit:
            product.save()  # DB에 저장하여 ID 생성

        # 해시태그 처리
        hashtags_input = self.cleaned_data.get('hashtags_str', '')
        hashtag_list = [h.strip() for h in hashtags_input.replace(',', ' ').split() if h]  # 쉼표와 공백으로 구분
        new_hashtags = []
        for ht in hashtag_list:
            ht_obj, created = HashTag.objects.get_or_create(name=ht)
            new_hashtags.append(ht_obj)

        # Many-to-Many 관계 설정
        product.save()  # 다시 저장 (ID 생성 후에 Many-to-Many 관계 설정 가능)
        product.hashtags.set(new_hashtags)

        return product


