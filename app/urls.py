from django.urls import path, re_path
from django.contrib.auth.views import (
    LoginView, 
    LogoutView, 
    PasswordChangeDoneView, 
    PasswordChangeView
)

from app.views import (
    main, product, order, report
)

urlpatterns = [

    # products
    path('products-by-category', product.ProductListByCategoryView.as_view()),
    path('products-by-title', product.ProductListByTitleView.as_view()),
    path('categories', product.CategoryListView.as_view()),

    # order
    path('create-order', order.CreateOrder.as_view()),

    # report

    path('reconciliation-act', report.ReconciliationActView.as_view()),

]
