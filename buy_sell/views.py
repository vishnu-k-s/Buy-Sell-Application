
from django.http import request
from django.http.response import HttpResponse
from django.shortcuts import redirect, render
from django.contrib import messages
from django.core.mail import  send_mail
from django.views.generic.base import View, TemplateView
from .models import NewUser, Product, Category,  MyPurchases
from .forms import PostForm

import re
import random
import string

#Declaring some global variables
email=''


#For rendering index page
class Index(View):   
     def get(self,request):      
        products = None
        categories = Category.objects.all()
        categoryID = request.GET.get('category')

        if categoryID:
            #products = Product.get_all_products_by_categoryid(categoryID)
            if categoryID :
                products = Product.objects.filter(category = categoryID)
            else:
                products =Product.Product.objects.all()
        else:
            products = Product.objects.all()

        #Getting data from Post model in which users are creating
        #posts =Post.objects.all()

        #creating directory and adding details yo it
        data = {}
        data['categories'] = categories
        data['products'] = products
        #data['posts'] = posts

       
        return render(request,'buy_sell/index.html',data)


#For rendering registration page
class RegisterPage(TemplateView):
    template_name = 'buy_sell/registration.html'


#Registration
class Registration(View):
    def post(self,request):
        username = request.POST['username']
        name = request.POST['name']
        email = request.POST['email']
        phone = request.POST['phone']
        password = request.POST['password']
        confirmpassword = request.POST['confirmpassword']

        #Dictionary to temporarly store entered values
        values ={
            'username' : username,
            'name' : name,
            'email' : email,
            'phone' : phone,  
            'password' : password, 
            'confirmpassword' : confirmpassword,        
        }

        try:
            #Username validation
            if(len(username)<4):
                messages.error(request,"Minimum 4 characters required for username")
                return render(request,'buy_sell/registration.html',values)
            
            #Name validation
            if(len(name)>=1):
                for char in name:
                    if  not (("A" <= char and char <= "Z") or ("a" <= char and char <= "z") or (char == " ")):
                        messages.error(request,"Entered name is not valid")
                        return render(request,'buy_sell/registration.html',values)
        
            #Phone number validation
            if(len(phone)==10):
                def isValid(s):           
                    # 1) Then contains 6 or 7 or 8 or 9.
                    # 2) Then contains 9 digits
                    Pattern = re.compile("[6-9][0-9]{9}")
                    return Pattern.match(s)
            
                if (isValid(phone)):
                    pass  
                else:
                    messages.error(request,"Entered phone number is not valid")
                    return render(request,'buy_sell/registration.html',values)
            else:
                messages.error(request,"Entered phone number is not valid")
                return render(request,'buy_sell/registration.html',values)

            #Password validation
            if(password==confirmpassword):
                if(len(password)<4):
                    messages.error(request,"Minimum 4 characters required for password ")
                    return render(request,'buy_sell/registration.html',values)
        
            else:
                messages.error(request,"Password is invalid")
                return render(request,'buy_sell/registration.html',values)
            
            #Email validation
            if  NewUser.objects.filter(email=email).exists():
                messages.error(request,"Email is already taken please try another one")
                return render(request,'buy_sell/registration.html',values)
            else:
                send_mail('CONFIRMATION CODE ',
                'Hi ' + name + ' Your Confirmation code is: ' +code,
                'vishnusajeevks@gmail.com',[email],fail_silently=False)
                        
                return render(request,'buy_sell/confirmregistration.html',values)

        except:
            messages.error(request,"Unable to create an account please try again")
            return render(request,'buy_sell/registration.html',values)
        

#Create random strings for email verification
def randomString(stringlength=4):
    letters = string.ascii_letters
    return ''.join(random.choice(letters) for i in range(stringlength))

#Storing randomly generated string
code = randomString()
      
#For confirming the registration
class ConfirmRegistration(View):
    def post(self,request):
        username = request.POST['username']
        name = request.POST['name']
        email = request.POST['email']
        phone = request.POST['phone']
        password = request.POST['password']
        confirmcode = request.POST['code']

        #Dictionary to temporarly store entered values
        values ={
            'username' : username,
            'name' : name,
            'email' : email,
            'phone' : phone,  
            'password' : password, 
                  
        }
       
        #Checking confirmation code
        if code == confirmcode:
            NewUser(username=username,name=name,email=email,phonenumber=phone,password=password).save()
            messages.success(request,"Account created successfully please login ")    
            return redirect('loginpage')
            
        else:
            messages.error(request, 'Invalid Confirmation Code')
            return render(request, 'buy_sell/confirmregistration.html', values)
 

#For rendering login page
class LoginPage(TemplateView):
    template_name = 'buy_sell/login.html'


#Login view
class Login(View):
    def post(self,request):
        email = request.POST['email']
        password = request.POST['password']

        try:
            #Checking email&password exists or not
            if NewUser.objects.filter(email=email,password=password).exists():          
                userdetails = NewUser.objects.get(email=email,password=password)
                
                #Creating sessions for future purposes
                request.session['username'] = userdetails.username
                request.session['name'] = userdetails.name
                request.session['phonenumber'] = userdetails.phonenumber
                request.session['email'] = userdetails.email
                request.session['password'] = userdetails.password

                #Changing value of global variable
                email = request.session['email']
                
                return redirect('home')

            else:
                messages.error(request, 'Email/Password is invalid')
                return render(request, 'buy_sell/login.html') 

        except:
            messages.error(request, 'Email/Password is invalid')
            return render(request, 'buy_sell/login.html')


#Logout view
def logout(request):
    request.session.clear()
    return redirect('home')      

    
#For rendering forgotpassword page
class ForgotpasswordPage(TemplateView):
    template_name = 'buy_sell/forgotpassword.html'


#Sending password mail to user
class Forgotpassword(View):
    def post(self,request):
        email = request.POST['email']

        try:
            #Checking email exists or not
            if NewUser.objects.filter(email=email).exists():
                userdetails = NewUser.objects.get(email=email)        
                name = userdetails.name
                password = userdetails.password           

                #Sending password through mail
                send_mail('YOUR PASSWORD IS...',
                'Hi ' + name + ' your password is : ' + password,
                'vishnusajeevks@gmail.com',[email],fail_silently=False)
                
                messages.success(request,"your password has been sent to your mail ")           
                return render(request,'buy_sell/forgotpassword.html')

            else:
                messages.success(request,"please enter a valid registered email")
                return render(request, 'buy_sell/forgotpassword.html')

        except:  
            messages.success(request,"please enter a valid registered email")
            return render(request, 'buy_sell/forgotpassword.html')

   
#User profile 
#For rendering editprofile page
class EditProfile(View):
    def get(self, request):
        return render(request, 'user/editprofile.html')
        
#For rendering viewprofile page
class ViewProfile(View):
    def get(self,request):
        userdetails = { 
            'singleuserdetails' : NewUser.objects.get(email = request.session['email'])
        }
        return render(request, 'user/viewprofile.html', userdetails)


# Change password    
class ChangePassword(View):
    def post(self,request):
        try:
            oldpassword = request.POST['oldpassword']
            newpassword = request.POST['newpassword']
            confirmpasswor = request.POST['confirmpassword']

            if(newpassword  == confirmpasswor):    
            #if(newpassword):
                changepassword = NewUser.objects.get(password = oldpassword) 
                changepassword.password = newpassword 
                changepassword.save()

                #Changing password session with new value
                request.session['password'] = newpassword

                messages.success(request,"your password has been changed sucessfully ")           
                return render(request, 'user/changepassword.html')
            else:
                messages.success(request,"something went wrong check entered details and try again")           
                return render(request, 'user/changepassword.html')
        except:
            messages.success(request,"something went wrong check entered details and try again")           
            return render(request, 'user/changepassword.html')
    def get(self, request):
        return render(request, 'user/changepassword.html')

#Change username
class ChangeUsername(View):
    def post(self,request):
        oldusername = request.POST['oldusername']
        newusername = request.POST['newusername']
        confirmusername = request.POST['confirmusername']
       
        try:
            if(newusername  == confirmusername):
                changeusername = NewUser.objects.get(username = oldusername) 
                changeusername.username = newusername
                changeusername.save()

                #Changing username session with new value
                request.session['username'] = newusername

                messages.success(request,"your username has been changed sucessfully...! ")           

                return render(request, 'user/changeusername.html')
            else:
                messages.success(request,"something went wrong check entered details and try again...! ")           
                return render(request, 'user/changeusername.html')
        except:
            messages.success(request,"something went wrong check entered details and try again...! ")           
            return render(request, 'user/changeusername.html')

    def get(self, request):
        return render(request, 'user/changeusername.html')


#Create post
class CreatePost(View):
    def post(self, request):
        form = PostForm(request.POST, request.FILES)
        
        if form.is_valid():
            form.save()
            messages.success(request,"your post has been added sucessfully ")           
            return render(request, 'user/createpost.html', {'form' : form})

        else:
            messages.error(request,"something went wrong check entered details and try again...! ")           
            return render(request, 'user/createpost.html', {'form' : form})

    def get(self, request):
        form = PostForm()
        
        return render(request, 'user/createpost.html', {'form' : form})


#Viewing own posts
class MyPosts(View):
    def get(self,request):      
        posts = Product.objects.filter(ownerusername=request.session['username'])

        #creating directory and adding details yo it
        data = {}
        data['posts'] = posts
       
        return render(request,'user/myposts.html',data)


#Displaying items individually using detail view 
# pass id attribute from urls
def productdetails(request,id):
    # dictionary for initial data with 
    # field names as keys
    context ={}
    try :
        #Checks wheather user is loged in or not 
        if request.session['email']:
            context['userdetails'] = NewUser.objects.get(email=request.session['email'])
        else:
            pass

        if request.method == "GET":
            # add the dictionary during initialization
            productdetails = Product.objects.get(id =id) 
            context['data'] = productdetails

            #Creating sessions for sending mails during chat/buy now
            request.session['to_address'] = productdetails.owneremail 
            request.session['item_name'] = productdetails.name
            request.session['item_prize'] = productdetails.price
           
            return render(request,"buy_sell/productdetails.html", context)

    except:
        if request.method == "GET":
            
            # add the dictionary during initialization
            context['data'] = Product.objects.get(id =id) 
        
            
            #context['username'] = request.session['username']        
            
            #context["data"] = Post.objects.get(id =id)           
            return render(request,"buy_sell/productdetails.html", context)


#Deleting a post
def delete_view(request,id):
    if request.method =="POST":
        return HttpResponse('post')
    else:
        product = Product.objects.filter(id=id)
        product.delete()
        return redirect('myposts')   
  


   
#Search
class Search(View):
    def post(self, request):
        search = request.POST.get('search')

        data = {} 
        categories = Category.objects.all()
        data['categories'] = categories

        if search.lower() in ['mobiles','phone','samsung','nokia','redmi']:
            products = Product.objects.filter(category =1)    
            data['products'] = products
            return render(request,'buy_sell/index.html',data)
        elif search.lower() in ['cars','contessa']:
            products = Product.objects.filter(category =2)
            data['products'] = products
            return render(request,'buy_sell/index.html',data)
        elif search.lower() in ['sports','cricket','footbal']:
            products = Product.objects.filter(category =3)
            data['products'] = products
            return render(request,'buy_sell/index.html',data)
        elif search.lower() in ['books','novels']:
            products = Product.objects.filter(category =4)
            data['products'] = products
            return render(request,'buy_sell/index.html',data)
        elif search.lower() in ['bikes','rx','duke']:
            products = Product.objects.filter(category =5)                 
            data['products'] = products
            return render(request,'buy_sell/index.html',data)
        elif search.lower() in ['electronics','fridge']:
            products = Product.objects.filter(category =6)                 
            data['products'] = products
            return render(request,'buy_sell/index.html',data)
        else:
            products = Product.objects.all()                 
            data['products'] = products
            return render(request,'buy_sell/index.html',data)

    def get(self, request):
        return render(request, 'buy_sell/index.html')
   


class BuyProduct(View):
    def get(self, request):
        return render(request, 'buy_sell/buyproduct.html')
    

class BuyProductNow(View):     
    def get(self, request):
        try:
            #Message for buyer
            send_mail('Congratulations You have sucessfully bought the item...',
                'your purchase for item: ' + request.session['item_name'] + ' for the prize: ' + str(request.session['item_prize']) + ' is successful ',
                'vishnusajeevks@gmail.com',
                [request.session['email']],fail_silently=False)
            #Changing status of item
            productdetails = Product.objects.get(name=request.session['item_name'])
            productdetails.status='sold'
            productdetails.save()

            print(request.session['email'],productdetails.name,productdetails.price,productdetails.image)
            #Adding product details to mypurchases model
            #obj =MyPurchases(customeremail=request.session['email'], name=productdetails.name, price=productdetails.price, Category=productdetails.category, description=productdetails.description, image=productdetails.image)
            obj =MyPurchases(customeremail=request.session['email'], name=productdetails.name, price=productdetails.price,image=productdetails.image)
            obj.save()           
            print('saved to database')
            
            #Message for seller
            send_mail('Congratulations Your item has been sold out...',
                'your item: '+ request.session['item_name'] + ' has been bought by \n' + request.session['name'] +' for the prize of: ' + str(request.session['item_prize']) ,
                'vishnusajeevks@gmail.com',
                [request.session['to_address']],fail_silently=False)

            return render(request, 'buy_sell/buyproduct.html')  
        except:
            return render(request, 'buy_sell/buyproduct.html')  
            
    def post(self, request):
        return render(request, 'buy_sell/buyproduct.html')

#Chat with user
class Chat(View):
    def get(self, request):
        return render(request, 'buy_sell/chat.html')
    def post(self, request):
        try:
            message = request.POST['message']
            from_address = request.session['email']
            send_mail('Someone wants to buy your product...',
                message + ' \n you can reach me on \n phone : {0} or \n email : {1}'.format(request.session['phonenumber'], request.session['email']) ,
                from_address,
                [request.session['to_address']],fail_silently=False)
                
            messages.success(request,"message sent successfully ")              
            return render(request, 'buy_sell/chat.html')

        except:
            messages.success(request,"unable to send message please try again ")               
            return render(request, 'buy_sell/chat.html')


#Purchased product details
class Purchases(View):
    def get(self, request):
        context={}
        context['products'] = MyPurchases.objects.filter(customeremail=request.session['email'])
        return render(request, 'buy_sell/mypurchases.html', context)


#Clear history
class ClearHistory(View):
    def get(self, request):
        try:
            productdetails = MyPurchases.objects.filter(customeremail=request.session['email'])
            productdetails.delete()
            
            return redirect('mypurchases')
        except:
            return HttpResponse('error')


#Error page
class Error(TemplateView):
    template_name = 'buy_sell/error.html'