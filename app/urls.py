from django.urls import path, re_path
from django.contrib.auth.views import (
    LoginView,
    LogoutView,
    PasswordChangeDoneView,
    PasswordChangeView
)

from app.views import (
    main, product, order, report, favorites, feedback
)

urlpatterns = [

    # products
    path('products-by-category', product.ProductListByCategoryView.as_view()),
    path('products-by-title', product.ProductListByTitleView.as_view()),
    path('categories', product.CategoryListView.as_view()),

    # order
    path('create-order', order.CreateOrder.as_view()),
    path('get-shipping-date', order.GetShippingDate.as_view()),
    path('orders-list-by-client', order.OrdersListByClient.as_view()),
    path('get-min-order-amount', order.GetMinOrderAmount.as_view()),

    # report
    path('reconciliation-act', report.ReconciliationActView.as_view()),

    # favorites
    path('create-favorites', favorites.CreateFavorites.as_view()),
    path('delete-favorites', favorites.DeleteFavorites.as_view()),
    path('favorites-list-by-client', favorites.FavoritesListByClient.as_view()),

    # feedback
    path('feedback-create', feedback.FeedbackCreateView.as_view()),


]
