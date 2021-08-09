
from django.urls import path,include
from django.contrib.auth.views import LogoutView
from django.views.generic.base import TemplateView
from .views import BuyProduct, BuyProductNow, Index, RegisterPage, Registration, ConfirmRegistration 
from .views import LoginPage, Login, logout, ForgotpasswordPage, Forgotpassword
from .views import EditProfile, ViewProfile, ChangePassword, ChangeUsername
from .views import  CreatePost, MyPosts, Search
from .views import  productdetails, delete_view, BuyProduct, BuyProductNow, Chat, Purchases, ClearHistory
from .views import Error
urlpatterns = [
   path('', Index.as_view(), name='home'),
  
   path('registrationpage/',  RegisterPage.as_view(), name='registerpage'),
   path('registration/', Registration.as_view(), name='registration'),
   path('confirmregistration/', ConfirmRegistration.as_view(), name='confirmregistration'),
   path('loginpage/', LoginPage.as_view(), name='loginpage'),
   path('login/', Login.as_view(), name='login'),
   path('logout/', logout, name='logout'),
   path('forgotpassword/', ForgotpasswordPage.as_view(), name='forgotpasswordpage'),
   path('forgotpasswordpage/', Forgotpassword.as_view(), name='forgotpassword'),

   #For social login
   path('accounts/', include('allauth.urls')),
   path('logout', LogoutView.as_view(), name="sociallogout"),

   #User profile
   path('editprofile/', EditProfile.as_view(), name='editprofile'),
   path('viewprofile/', ViewProfile.as_view(), name='viewprofile'),
   path('changepassword/', ChangePassword.as_view(), name='changepassword'),
   path('changeusername/', ChangeUsername.as_view(), name='changeusername'),
   path('createpost/', CreatePost.as_view(), name='createpost'),

   path('/', Search.as_view(), name='search'),

   path('myposts/<id>/delete', delete_view, name='deletepost'),#delete post
   path('myposts/', MyPosts.as_view(), name='myposts'),
   path('myposts/<id>', productdetails),#test

   path('<id>', productdetails, name='productdetails'),   
   path('chat/', Chat.as_view(), name='chat'),
   path('buyproduct/', BuyProduct.as_view(), name='buyproduct'),
   path('buyproductnow/', BuyProductNow.as_view(), name='buyproductnow'),
   path('mypurchases/', Purchases.as_view(), name='mypurchases'),
   path('clearhistory/', ClearHistory.as_view(), name='clearhistory'),

   path('error/', Error.as_view(), name='error'),
  
]
