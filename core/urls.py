from django.urls import path
from core import views


app_name = 'core'

urlpatterns = [
    path('',views.HomeView.as_view(), name='home'),
    path('product/<slug>/', views.ItemDetailView.as_view(), name='product'),
    path('checkout/',views.CheckoutView.as_view(), name='checkout'),
    path('add-to-cart/<slug>/', views.add_to_cart, name='add_to_cart'),
    path('remove_from_cart/<slug>/', views.remove_from_cart, name='remove_from_cart'),
    path('order-summary/', views.OrderSummaryView.as_view(), name='order-summary'),
    path('remove-item-from-cart/<slug>/', views.remove_single_item_from_cart,name='remove-single-item-from-cart'),
    path('order-submitted',views.OrderSubmitedView.as_view(),name='order-submitted'),
    path('search-results/',views.SearchResultsVIew.as_view(),name='search-results'),
    path('accessory-search-results/',views.SearchResultsAcc.as_view(),name='accessory-search-results'),
    path('iphone-search-results/',views.SearchResultsIphone.as_view(),name='iphone-search-results'),
    path('oppo-search-results/',views.SearchResultsOppo.as_view(),name='oppo-search-results'),
    path('nokia-search-results/',views.SearchResultsNokia.as_view(),name='nokia-search-results'),
    path('samsung-search-results/',views.SearchResultsSamsung.as_view(),name='samsung-search-results'),
    path('huawei-search-results/',views.SearchResultsHuawei.as_view(),name='huawei-search-results'),
    path('tecno-search-results/',views.SearchResultsTecno.as_view(),name='tecno-search-results'),
    path('infinix-search-results/',views.SearchResultsInfinix.as_view(),name='infinix-search-results'),
    path('htc-search-results/',views.SearchResultsHtc.as_view(),name='htc-search-results'),
    path('realme-search-results/',views.SearchResultsRealMe.as_view(),name='realme-search-results'),
    path('oneplus-search-results/',views.SearchResultsOneplus.as_view(),name='oneplus-search-results'),
    # Hot deals
    path('hotdeals-search-results/',views.SearchResultsHot.as_view(),name='hotdeals-search-results'),
    path('tablet-search-results/',views.SearchResultsTablet.as_view(),name='tablet-search-results'),
    path('vivo-search-results/',views.SearchResultsVivo.as_view(),name='vivo-search-results'),
    path('computer-search-results/',views.SearchResultsComputer.as_view(),name='computer-search-results'),
    path('redmi-search-results/',views.SearchResultsRedmi.as_view(),name='redmi-search-results'),
    path('laptop-search-results/',views.SearchResultsLaptop.as_view(),name='laptop-search-results'),





]