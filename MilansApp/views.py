from django.shortcuts import render,HttpResponseRedirect,HttpResponse,redirect
import MySQLdb
import datetime
from django.http import HttpResponse
from django.core.files.storage import FileSystemStorage
#from django.contrib import messages
# from requests import request
import simplejson as json
from datetime import date
from datetime import datetime
import datetime
import webbrowser
import math, random 
from vaderSentiment.vaderSentiment import SentimentIntensityAnalyzer
import nltk

import re
from nltk.corpus import stopwords
import pyttsx3
nltk.download('stopwords')
set(stopwords.words('english'))

def my_form(request):
    engine = pyttsx3.init()
    engine.say('Hello, Welcome to the feedback section.')
    engine.runAndWait()
    return render(request,'form.html')
 

def my_post(request):
        if request.method == 'POST':
                stop_words = stopwords.words('english')
                # my contribution
                stop_words.remove('very')
                stop_words.remove('not')
                
                #convert to lowercase
                text1 = request.POST['text1'].lower()
                
                # my contribution
                text_final = ''.join(i for i in text1 if not i.isdigit())
                net_txt=re.sub('[^a-zA-Z0-9\n]', ' ',text_final)
                
                #remove stopwords    
                processed_doc1 = ' '.join([i for i in net_txt.split() if i not in stop_words])

                sa = SentimentIntensityAnalyzer()
                dd = sa.polarity_scores(text=processed_doc1)
                compound = round((1 + dd['compound'])/2, 2)
                final=compound*100
                
                if "enough" in text1 or "sufficient" in text1 or "ample" in text1 or "abudant" in text1:
                   engine = pyttsx3.init()
                   engine.say('You liked us by'+str(final)+'% Thank you for your valuable response')
                   engine.runAndWait()
                   
                   return render(request,'form.html',{'final': final,'text1':net_txt})
                   
                elif final == 50:
                   engine = pyttsx3.init()
                   engine.say('Please enter an adequate resposnse, Thank You')
                   engine.runAndWait()
                   return render(request,'form.html',{'final': final,'text1':net_txt})
                else:
                   engine = pyttsx3.init()
                   engine.say('You liked us by'+str(final)+'% Thank you for your valuable response')
                   engine.runAndWait()
                   if final > 50:
                     
                      return render(request,'form.html',{'final': final,'text1':net_txt})
                   elif final < 50:
                     
                      return render(request,'form.html',{'final': final,'text1':net_txt})
                   else:
                       
                       return render(request,'form.html',{'final': final,'text1':net_txt})
        else:
           return redirect('my_form')


def sendsms(ph,msg):
    sendToPhoneNumber= "+91"+ph
    userid = "2000022557"
    passwd = "54321@lcc"
    url = "http://enterprise.smsgupshup.com/GatewayAPI/rest?method=sendMessage&send_to=" + sendToPhoneNumber + "&msg=" + msg + "&userid=" + userid + "&password=" + passwd + "&v=1.1&msg_type=TEXT&auth_scheme=PLAIN"
    # contents = urllib.request.urlopen(url)
    webbrowser.open(url)

def generateOTP() :   
    # Declare a digits variable   
    # which stores all digits  
    digits = "0123456789"
    OTP = "" 
   # length of password can be chaged 
   # by changing value in range 
    for i in range(4) : 
        OTP += digits[math.floor(random.random() * 10)] 
        print(i)
    return OTP 

# Create your views here.

db = MySQLdb.connect('localhost','root','','Milans')
c = db.cursor()

def AdminHome(request):
    name=request.session['NAME']
    c.execute("select * from product where uname='Admin' and qty<=0")
    datas=c.fetchall()
    c.execute("select count(*) from cust_reg")
    custcount=c.fetchone()
    c.execute("select count(*) from product where uname='Admin'")
    productcount=c.fetchone()
    c.execute("select count(*) from staff_reg")
    staffcount=c.fetchone()
    return render(request,'AdminHome.html',{"custcount":custcount,"productcount":productcount,"staffcount": staffcount,"datas":datas,"name":name}) 

def billingaddress(request):
    name=request.session['NAME']
    cid=request.session["cid"]
    c.execute("select * from cust_reg where cid='"+str(cid)+"'")
    data=c.fetchone()
    print(data)
    if request.POST:

        return HttpResponseRedirect("/payment1")
    return render(request,"billingaddress.html",{"data":data,"name":name})

def CommonHome(request):
    return render(request,'CommonHome.html')

def CustomerHome(request):
    name=request.session['NAME']
    cid=request.session["cid"]
    # s="select * from subcategory where status='Active'"
    # c.execute(s)
    # data2=c.fetchall()
    s="select * from product p join myorderview1 m on p.pid=m.pid order by m.qty desc"
    c.execute(s)
    data=c.fetchall()
    t="select * from categories where status='Active'"
    c.execute(t)
    data1=c.fetchall()
    t="select count(*) from cart where cid = '"+str(cid)+"'"
    c.execute(t)
    dataa=c.fetchone()
    return render(request,'CustomerHome.html',{"data":data,"data1":data1,"name":name,"dataa":dataa[0]})



# s="select * from products p join myview m on p.pid=m.pid order by m.tqty desc"
def CustomerSalesprediction(Request):
    name=Request.session['NAME']
    cid= Request.session["cid"]
    s="select * from product p join myorderview1 m on p.pid=m.pid order by m.qty desc"
    c.execute(s)
    data=c.fetchall()
    t="select * from categories where status='Active'"
    c.execute(t)
    data1=c.fetchall()
    s="select * from subcategory"
    c.execute(s)
    data2=c.fetchall()
    t="select count(*) from cart where cid = '"+str(cid)+"'"
    c.execute(t)
    dataa=c.fetchone()
    return render(Request,'CustomerSalesprediction.html',{"name":name,"data":data,"data1":data1,"data2":data2,"dataa":dataa[0]})

def AdminViewProductreport(request):
    if request.POST:
        da1=request.POST["d1"]
        da2=request.POST["d2"]
        c.execute("select p.pname,p.pdesc,sum(co.P_qty) as qty,sum(co.p_price),co.date as total from customer_order co join product p on(co.pid=p.pid) where co.date between '"+str(da1)+"' and '"+str(da2)+"'  group by p.pid order by sum(co.p_price) desc")
        print("select p.pname,p.pdesc,sum(co.P_qty) as qty,sum(co.p_price),co.date as total from customer_order co join product p on(co.pid=p.pid) where co.date between '"+str(da1)+"' and '"+str(da2)+"'  group by p.pid order by sum(co.p_price) desc")
        data=c.fetchall()
        return render(request,"AdminViewProductreport.html",{"data":data,"da1":da1,"da2":da2})

    return render(request,"AdminViewProductreport.html")

def AdminDeleteProduct(request):
    id=request.GET["id"]
    c.execute("update product set status='deactivate' where pid='"+str(id)+"'")
    db.commit()
    return HttpResponseRedirect("/AdminViewProduct")

def AdminSellerReport(request):
    data = ""
    c.execute("select p.pname,sum(co.p_price)as totalprice,sum(co.p_qty),ct.catname,sc.sname,sr.sname from product p join categories ct on(p.catid=ct.catid) join subcategory sc on(ct.catid=sc.catid) join staff_reg sr on(sr.sid=p.uname) join customer_order co on(co.pid=p.pid) group by co.pid")
    data=c.fetchall() 
    print(data)
    return render (request,"AdminSellerReport.html",{"data":data})

def SellerReport(request):
    data = ""
    c.execute("select p.pname,sum(co.p_price)as totalprice,sum(co.p_qty),ct.catname,sc.sname,sr.sname from product p join categories ct on(p.catid=ct.catid) join subcategory sc on(ct.catid=sc.catid) join staff_reg sr on(sr.sid=p.uname) join customer_order co on(co.pid=p.pid) group by co.pid")
    data=c.fetchall() 
    print(data)
    return render (request,"SellerReport.html",{"data":data})


def AdminCategoryReport(request):
    data = ""
    c.execute("select c.catname,sum(co.p_qty),sum(co.p_price) as totalprice from customer_order co inner join product p on co.pid=p.pid inner join categories c on p.catid=c.catid group by c.catname")
    data=c.fetchall() 
    print(data)
    return render (request,"AdminCategoryReport.html",{"data":data})


def AdminRestoreProduct(request):
    id=request.GET["id"]
    status=""
    c.execute("select status from product where pid='"+str(id)+"'")
    data=c.fetchall()
    if (data[0][0]=='Active'):  
        status="deactivate"
    else:
        status="Active"
    c.execute("update product set status='"+str(status)+"' where pid='"+str(id)+"'")
    db.commit()
    return HttpResponseRedirect("/AdminViewProduct")

def SellerDeleteProduct(request):
    id=request.GET["id"]
    c.execute("update product set status='deactivate' where pid='"+str(id)+"'")
    db.commit()
    return HttpResponseRedirect("/SellerViewProduct")

def SellerRestoreProduct(request):
    id=request.GET["id"]
    status=""
    c.execute("select status from product where pid='"+str(id)+"'")
    data=c.fetchall()
    if (data[0][0]=='Active'):  
        status="deactivate"
    else:
        status="Active"
    c.execute("update product set status='"+str(status)+"' where pid='"+str(id)+"'")
    db.commit()
    return HttpResponseRedirect("/SellerViewProduct")

def SubRestoreProduct(request):
    id=request.GET["id"]
    status=""
    c.execute("select status from subcategory where sid='"+str(id)+"'")
    data=c.fetchall()
    if (data[0][0]=='Active'):  
        status="deactivate"
    else:
        status="Active"
    c.execute("update subcategory set status='"+str(status)+"' where sid='"+str(id)+"'")
    db.commit()
    return HttpResponseRedirect("/AdminAddSubCategory")

def CatRestoreProduct(request):
    id=request.GET["id"]
    status=""
    c.execute("select status from categories where catid='"+str(id)+"'")
    data=c.fetchall()
    if (data[0][0]=='Active'):  
        status="deactivate"
    else:
        status="Active"
    c.execute("update categories set status='"+str(status)+"' where catid='"+str(id)+"'")
    db.commit()
    return HttpResponseRedirect("/AdminAddCategory")

def SignIn(request):  
    request.session['username']=""
    request.session['NAME']=""
    request.session['cid']=""
    msg=""
    if request.POST:
        email = request.POST.get("email")
        password = request.POST.get("password")
        c.execute("select * from login where uname='"+ email +"' and pass='"+ password +"'")
        print("select * from login where uname='"+ email +"' and pass='"+ password +"'")
        ds = c.fetchone()
        request.session['username']=email
        if ds is not None:
            if ds[2] == 'Admin':
                return HttpResponseRedirect('/AdminHome/')
            elif ds[2] == 'Customer':
                c.execute("select * from cust_reg where email='"+email+"' and password='"+password+"' and status='Active'")
                ds = c.fetchone()
                
                if(ds):
                    request.session['cid'] = ds[0]
                    request.session['NAME'] = ds[1]
                    return HttpResponseRedirect('/CustomerHome/')
                else:
                    msg="Your account had deactivated"

            elif ds[2] == 'Seller':
                c.execute("select * from staff_reg where email='"+email+"' and password='"+password+"' and status='Active'")
                ds = c.fetchone()
                if(ds):
                    request.session['cid'] = ds[0]
                    request.session['NAME'] = ds[1]
                    return HttpResponseRedirect('/SellerHome/')
                else:
                    msg="Your account has deactivated"
            
        
    return render(request,'Signin.html',{"msg":msg}) 

def MyProfile(request):
    name=request.session['NAME']
    cid = request.session['cid']
    t1="select count(*) from cart where cid = '"+str(cid)+"'"
    c.execute(t1)
    dataa=c.fetchone()
    t="select * from categories where status='Active'"
    c.execute(t)
    data1=c.fetchall()
    email=request.session['username']
    
    if request.POST:
        cname = request.POST.get("uname")
        address = request.POST.get("uaddress")
        cntry = request.POST.get("udistrict")
        state = request.POST.get("uloc")
        fon = request.POST.get("umob")
        email = request.POST.get("uemail")
        password = request.POST.get("upass")
        type= "Customer"
        qry1="update cust_reg set cname='"+str(cname)+"', address = '"+str(address)+"', district = '"+str(cntry)+"', location ='"+str(state)+"' , mobile = '"+str(fon)+"' , password='"+str(password)+"' where email='"+str(email)+"' "
        c.execute(qry1)
        db.commit()
    qry="select * from cust_reg where email='"+str(email)+"' "
    c.execute(qry)
    data=c.fetchone()
    return render(request,'MyProfile.html',{"data":data,"dataa":dataa[0],"name":name,"data1":data1})
    

def CustomerSignUp(request):
    msg = ""
    if request.POST:
        cname = request.POST.get("cname")
        address = request.POST.get("address")
        cntry = request.POST.get("district")
        state = request.POST.get("location")
        fon = request.POST.get("mobile")
        email = request.POST.get("Email")
        password = request.POST.get("Password")
        type= "Customer"
        qry1="select count(*) from login where uname='"+str(email)+"' "
        c.execute(qry1)
        dataaa=c.fetchone()
        if(int(dataaa[0])==0):
            qry="insert into cust_reg(cname,address,district,location,mobile,email,password) values('"+ str(cname) +"','"+ str(address) +"','"+ str(cntry) +"','"+ str(state) +"','"+ str(fon) +"','"+ str(email) +"','"+ str(password) +"')"
            qr ="insert into login values('"+ str(email) +"','"+ str(password) +"','"+ str(type) +"')"
            c.execute(qry)
            c.execute(qr)
            db.commit()
            msg = "Registartion Completed Successfully."
            print(msg)
            # return HttpResponseRedirect("/")
        else:
            msg="this email already exist"
            print(msg)
    return render(request,'CustomerSignUp.html',{"msg":msg})

def SellerSignUp(request):
    msg = ""
    if request.POST:
        cname = request.POST.get("cname")
        address = request.POST.get("address")
        cntry = request.POST.get("district")
        state = request.POST.get("location")
        fon = request.POST.get("mobile")
        email = request.POST.get("Email")
        password = request.POST.get("Password")
        if request.FILES.get("file"):
            myfile=request.FILES.get("file")
            fs=FileSystemStorage()
            filename=fs.save(myfile.name , myfile)
            uploaded_file_url = fs.url(filename)
            uploaded_file_url="static"+uploaded_file_url
            type= "Seller"
            c.execute("select count(*) from login where uname='"+str(email)+"'")
            data=c.fetchone()
            
            if(data[0]==0):
                qry="insert into staff_reg(sname,address,district,location,mobile,email,Password,proof) values('"+ str(cname) +"','"+ str(address) +"','"+ str(cntry) +"','"+ str(state) +"','"+ str(fon) +"','"+ str(email) +"','"+ str(password) +"','"+str(uploaded_file_url)+"')"
                qr ="insert into login values('"+ str(email) +"','"+ str(password) +"','"+ str(type) +"')"
                c.execute(qry)
                c.execute(qr)
                db.commit()
                msg = "Registartion Completed Successfully."
            else:
                msg="username already exist"
    print(msg)
    return render(request,'SellerSignUp.html',{"msg":msg})


def SellerHome(request):
    sid=request.session['cid']
    c.execute("select count(*) from cust_reg")
    custcount=c.fetchone()
    c.execute("select count(*) from product where uname='"+str(sid)+"'")
    productcount=c.fetchone()
    c.execute("select count(*) from staff_reg")
    staffcount=c.fetchone()
    c.execute("select * from product where uname='"+str(sid)+"' and qty<=0")
    datas=c.fetchall()
    return render(request,'SellerHome.html',{"datas":datas,"custcount":custcount,"productcount":productcount,"staffcount": staffcount}) 



def SellerViewCustomers(request):
    data = ""
    c.execute("select * from cust_reg")
    data=c.fetchall() 
    return render (request,"SellerViewCustomers.html",{"data":data})

def Adminactiveseller(request):
    pid = request.GET.get('id')
    status=""
    c.execute("select status from staff_reg where sid='"+str(pid)+"'")
    data=c.fetchall()
    if (data[0][0]=='Active'):  
        status="deactive"
    else:
        status="Active"
    c.execute("update staff_reg set status='"+str(status)+"' where sid = '"+str(pid)+"'")
    db.commit()
    return HttpResponseRedirect("/AdminViewSeller/")



def Admindeleteseller(request):
    pid = request.GET.get('id')
    c.execute("update staff_reg set status='deactive' where sid = '"+str(pid)+"'")
    db.commit()
    return HttpResponseRedirect("/AdminViewSeller/")


def AdminViewProduct(request):
    st="Active"
    c.execute("select * from product where uname='Admin' and qty<=0")
    datas=c.fetchall()
    c.execute("select count(*) from cust_reg")
    custcount=c.fetchone()
    c.execute("select count(*) from product")
    productcount=c.fetchone()
    c.execute("select count(*) from staff_reg")
    staffcount=c.fetchone()
    c.execute("select * from categories")
    cdata=c.fetchall()
    c.execute("select * from subcategory")
    sdata=c.fetchall()
    c.execute("select * from product where uname='Admin'")
    data = c.fetchall()
    if request.POST:
        cid=request.POST["t11"]
        sid=request.POST["t12"]
        c.execute("select  * from product where catid='"+str(cid)+"' or subid='"+str(sid)+"'")
        data=c.fetchall()
    if request.GET:
        st = request.GET.get('st')
        pid = request.GET.get('id')
        if st == 'Accept':
            return HttpResponseRedirect("/AdminUpdateProduct/")
        else:
            c.execute("delete from product where pid = '"+str(pid)+"'")
            db.commit()
    return render(request,"AdminViewProduct.html",{"data":data,"cdata":cdata,"sdata":sdata,"st":st,"custcount":custcount,"datas":datas,"staffcount":staffcount,"productcount":productcount})

def SellerViewProduct(request):
    st="Active"
    sid=request.session['cid']
    c.execute("select * from product where uname='"+str(sid)+"' and qty<=0")
    datas=c.fetchall()
    c.execute("select count(*) from cust_reg")
    custcount=c.fetchone()
    c.execute("select count(*) from product where uname='"+str(sid)+"'")
    productcount=c.fetchone()
    c.execute("select count(*) from staff_reg")
    staffcount=c.fetchone()
    c.execute("select * from categories")
    cdata=c.fetchall()
    c.execute("select * from subcategory")
    sdata=c.fetchall()
    sid=request.session['cid']
    c.execute("select * from product where uname='"+str(sid)+"'")
    data = c.fetchall()
    if request.POST:
        cid=request.POST["t11"]
        sid=request.POST["t12"]
        c.execute("select  * from product where catid='"+str(cid)+"' or subid='"+str(sid)+"'")
        data=c.fetchall()
    if request.GET:
        st = request.GET.get('st')
        pid = request.GET.get('id')
        if st == 'Accept':
            return HttpResponseRedirect("/SellerUpdateProduct/")
        else:
            c.execute("delete from product where pid = '"+str(pid)+"'")
            db.commit()
    return render(request,"SellerViewProduct.html",{"data":data,"cdata":cdata,"sdata":sdata,"st":st,"custcount":custcount,"datas":datas,"staffcount":staffcount,"productcount":productcount})

def SellerdeleteProduct(request):
    pid = request.GET.get('id')
    c.execute("delete  from product where pid = '"+str(pid)+"'")
    db.commit()
    return HttpResponseRedirect("/SellerViewProduct/")


def AdminAddCategory(request):
    st="Active"
    msg=""
    c.execute("select * from product where uname='Admin' and qty<=0")
    datas=c.fetchall()
    c.execute("select count(*) from cust_reg")
    custcount=c.fetchone()
    c.execute("select count(*) from product")
    productcount=c.fetchone()
    c.execute("select count(*) from staff_reg")
    staffcount=c.fetchone()
    if request.POST:
        
        na = request.POST.get("cat_name")
        c.execute("select count(*) from categories where catname='"+str(na)+"'")
        data = c.fetchone()
        if(data[0]==0): 
            qry="insert into categories(catname) values('"+ na +"')"
            c.execute(qry)
            db.commit()
            msg = "Category Added Successfully..."
        else:
            msg="Categories already exist...!"
    c.execute("select * from categories")
    data=c.fetchall() 
    if request.GET:
        a = request.GET.get('id')
        c.execute("delete from categories where catid = '"+str(a)+"'")
        db.commit()
        return HttpResponseRedirect("/AdminAddCategory/")
    return render(request,'AdminAddCategory.html',{"data":data,"msg":msg,"st":st,"datas":datas,"staffcount":staffcount,"productcount":productcount,"custcount":custcount})


def AdminAddSubCategory(request):
    st="Active"
    msg=""
    c.execute("select * from product where uname='Admin' and qty<=0")
    datas=c.fetchall()
    c.execute("select count(*) from cust_reg")
    custcount=c.fetchone()
    c.execute("select count(*) from product")
    productcount=c.fetchone()
    c.execute("select * from subcategory")
    sdata=c.fetchall()
    c.execute("select * from categories")
    cdata=c.fetchall()
    c.execute("select count(*) from staff_reg")
    staffcount=c.fetchone()
    

    if "ADD" in request.POST:
        ca = request.POST.get("cat_title")
        sc = request.POST.get("cat_name")
        c.execute("select count(*) from subcategory where sname='"+str(sc)+"'")
        data=c.fetchone()
        print("select count(*) from subcategory where sname='"+str(sc)+"'")
        qry="insert into subcategory(catid,sname) values('"+ ca +"','"+sc+"')"
        c.execute(qry)
        db.commit()
        msg = "Subcategory Added Successfully."

    c.execute("select * from categories")
    data=c.fetchall() 
    c.execute("select * from subcategory join categories on(subcategory.catid=categories.catid)")
    sdata=c.fetchall()

    if "sub_Submit" in request.POST:
        ca = request.POST.get("cat_title")
        c.execute("select * from subcategory s,categories c  where s.catid=c.catid and s.catid= '"+str(ca)+"'")
        sdata=c.fetchall()
        
    if request.GET:
        a = request.GET.get('id')
        c.execute("delete from subcategory where sid = '"+str(a)+"'")
        db.commit()
        return HttpResponseRedirect("/AdminAddSubCategory/")
         
    return render(request,'AdminAddSubCategory.html',{"data":data,"msg":msg,"st":st,"sdata":sdata,"staffcount":staffcount,"productcount":productcount,"custcount":custcount,"cdata":cdata})
    

def AdminViewMyBooking(request):
    cid=request.session["cid"]
    c.execute("select * from customer_order inner join product on customer_order.pid = product.pid join cust_reg cr on (cr.cid=customer_order.cid)")
    data = c.fetchall()
    return render(request,"AdminViewMyBooking.html",{"data":data})

def AdminAddEvents(request):
    msg=""
    c.execute("select * from product where uname='Admin' and qty<=0")
    datas=c.fetchall()
    c.execute("select count(*) from cust_reg")
    custcount=c.fetchone()
    c.execute("select count(*) from product")
    productcount=c.fetchone()
    c.execute("select count(*) from staff_reg")
    staffcount=c.fetchone()
    if request.POST:
        na = request.POST.get("cat_name")
        qry="insert into events(events) values('"+ na +"')"
        c.execute(qry)
        db.commit()
        msg = "Events Added Successfully."
    c.execute("select * from events")
    data=c.fetchall() 
    if request.GET:
        a = request.GET.get('id')
        c.execute("delete from events where eid = '"+str(a)+"'")
        db.commit()
        return HttpResponseRedirect("/AdminAddEvents/")
    return render(request,'AdminAddEvents.html',{"data":data,"msg":msg,"datas":datas,"staffcount":staffcount,"productcount":productcount,"custcount":custcount})

def AdminAddEventProduct(request):
    # c.execute("select * from categories")
    # data=c.fetchall()
    c.execute("select * from events")
    edata=c.fetchall()
    msg=""  
    if request.POST:
        # a=request.POST.get("cat")
        # b=request.POST.get("subcategory")
        # c.execute("select sid from subcategory where sname = '"+b+"'")
        # sub = c.fetchone()
        # subid = sub[0]
        c1=request.POST.get("event")   
        d=request.POST.get('product_title')
        e=request.POST.get("des")
        f=request.POST.get("price")   
        size=request.POST.get("size")   
        qty = request.POST.get("qty")
        if request.FILES.get("file"):
            myfile=request.FILES.get("file")
            fs=FileSystemStorage()
            filename=fs.save(myfile.name , myfile)
            uploaded_file_url = fs.url(filename)
            c.execute("insert into event_pro(evid,pname,pdesc,pimage,pamount,qty,size) values('"+ str(c1) +"','"+str(d)+"','"+str(e)+"','"+ uploaded_file_url +"','"+ str(f) +"','"+qty+"','"+size+"')")
            db.commit()       
            msg = "product Added Successfully."
    return render(request,"AdminAddProduct.html",{"cat":data,"msg":msg,"edata":edata})

# def AdminAddProduct(request):
#     c.execute("select * from categories")
#     data=c.fetchall()
#     c.execute("select * from events")
#     edata=c.fetchall()
#     msg=""  
#     if request.POST:
#         a=request.POST.get("cat")
#         b=request.POST.get("subcategory")
#         c.execute("select sid from subcategory where sname = '"+b+"'")
#         sub = c.fetchone()
#         subid = sub[0]
#         c1=request.POST.get("event")   
#         d=request.POST.get('product_title')
#         e=request.POST.get("des")
#         f=request.POST.get("price")   
#         qty = request.POST.get("qty")
#         if request.FILES.get("file"):
#             myfile=request.FILES.get("file")
#             fs=FileSystemStorage()
#             filename=fs.save(myfile.name , myfile)
#             uploaded_file_url = fs.url(filename)
#             c.execute("insert into product(catid,subid,evid,pname,pdesc,pimage,pamount,qty) values('"+ str(a) +"','"+ str(subid) +"','"+ str(c1) +"','"+str(d)+"','"+str(e)+"','"+ uploaded_file_url +"','"+ str(f) +"','"+qty+"')")
#             db.commit()       
#             msg = "product Added Successfully."
#     return render(request,"AdminAddProduct.html",{"cat":data,"msg":msg,"edata":edata})
def AdminViewprediction(request):
    if request.POST:
        month=request.POST["t1"]
        c.execute("select s.sname,max(p.qty) from subcategory s join  product p on s.sid=p.subid join customer_order co on co.pid=p.pid  where month(co.date)='"+str(month)+"' group by s.sname")
        data=c.fetchall()
        return render(request,"AdminViewprediction.html",{"data":data})

    return render(request,"AdminViewprediction.html")

def AdminAddProduct(request):
    c.execute("select * from categories")
    data=c.fetchall()
    # c.execute("select * from events")
    # edata=c.fetchall()
    cdate=date.today()
    msg="" 
    c.execute("select * from product where uname='Admin' and qty<=0")
    datas=c.fetchall()
    c.execute("select count(*) from cust_reg")
    custcount=c.fetchone()
    c.execute("select count(*) from product")
    productcount=c.fetchone()
    c.execute("select count(*) from staff_reg")
    staffcount=c.fetchone()
    if request.POST:
        cdate=date.today()
        a=request.POST.get("cat")
        b=request.POST.get("subcategory")
        c.execute("select sid from subcategory where sname  = '"+b+"' and catid= '"+a+"'")
        sub = c.fetchone()
        subid = sub[0]
        c1=request.POST.get("event")   
        d=request.POST.get('Product_title')
        e=request.POST.get("des")
        f=request.POST.get("price")   
        qty = request.POST.get("qty")
        size=request.POST.get("size") 
        if request.FILES.get("file"):
            myfile=request.FILES.get("file")
            fs=FileSystemStorage()
            filename=fs.save(myfile.name , myfile)
            uploaded_file_url = fs.url(filename)
            c.execute("insert into product(catid,subid,pname,pdesc,pimage,pamount,qty,size,date) values('"+ str(a) +"','"+ str(subid) +"','"+str(d)+"','"+str(e)+"','"+ uploaded_file_url +"','"+ str(f) +"','"+qty+"','"+size+"','"+str(cdate)+"')")
            db.commit()       
            msg = "product Added Successfully."
    return render(request,"AdminAddProduct.html",{"cat":data,"msg":msg,"cdate":cdate,"datas":datas,"staffcount":staffcount,"productcount":productcount,"custcount":custcount})      

def SellerAddProduct(request):
    sid=request.session['cid']
    c.execute("select count(*) from cust_reg")
    custcount=c.fetchone()
    c.execute("select count(*) from product where uname='"+str(sid)+"'")
    productcount=c.fetchone()
    c.execute("select * from product where uname='"+str(sid)+"' and qty<=0")
    datas=c.fetchall()
    c.execute("select count(*) from staff_reg")
    staffcount=c.fetchone()
    c.execute("select * from categories")
    data=c.fetchall()
    # c.execute("select * from events")
    # edata=c.fetchall()
    msg="" 
    cdate=date.today() 
    if request.POST:
        a=request.POST.get("cat")
        b=request.POST.get("subcategory")
        c.execute("select sid from subcategory where sname = '"+b+"'")
        sub = c.fetchone()
        subid = sub[0]
        c1=request.POST.get("event")   
        d=request.POST.get('Product_title')
        e=request.POST.get("des")
        f=request.POST.get("price")   
        qty = request.POST.get("qty")
        size=request.POST.get("size")
        if request.FILES.get("file"):
            myfile=request.FILES.get("file")
            fs=FileSystemStorage()
            filename=fs.save(myfile.name , myfile)
            uploaded_file_url = fs.url(filename)
            uname=request.session['cid']
            c.execute("insert into product(catid,subid,pname,pdesc,pimage,pamount,qty,size,uname,date) values('"+ str(a) +"','"+ str(subid) +"','"+str(d)+"','"+str(e)+"','"+ uploaded_file_url +"','"+ str(f) +"','"+qty+"','"+size+"','"+str(uname)+"','"+str(cdate)+"')")
            db.commit()       
            msg = "product Added Successfully."
    return render(request,"SellerAddProduct.html",{"cat":data,"msg":msg,"datas":datas,"custcount":custcount,"productcount":productcount,"cdate":cdate,"staffcount":staffcount})


def statistics(request):
    c.execute("select qty,pname from product")
    data=c.fetchall()
    return render(request,"statistics.html",{"data":data})


 
def AdminAddModels(request):
    c.execute("select * from categories")
    data=c.fetchall()
    c.execute("select * from events")
    edata=c.fetchall()
    msg=""  
    if request.POST:
        a=request.POST.get("cat")
        b=request.POST.get("subcategory")
        c.execute("select sid from subcategory where sname = '"+b+"'")
        sub = c.fetchone()
        subid = sub[0]
        # c1=request.POST.get("event")   
        d=request.POST.get('product_title')
        e=request.POST.get("des")
        f=request.POST.get("price")   
        # qty = request.POST.get("qty")
        if request.FILES.get("file"):
            myfile=request.FILES.get("file")
            fs=FileSystemStorage()
            filename=fs.save(myfile.name , myfile)
            uploaded_file_url = fs.url(filename)
            c.execute("insert into model(catid,subid,mname,mdesc,mimage,mamount) values('"+ str(a) +"','"+ str(subid) +"','"+str(d)+"','"+str(e)+"','"+ uploaded_file_url +"','"+ str(f) +"')")
            db.commit()       
            msg = "product Added Successfully."
    return render(request,"AdminAddModels.html",{"cat":data,"msg":msg,"edata":edata})

def AdminViewCustomers(request):
    st="Active"
    c.execute("select * from product where uname='Admin' and qty<=0")
    datas=c.fetchall()
    c.execute("select count(*) from cust_reg")
    custcount=c.fetchone()
    c.execute("select count(*) from product")
    productcount=c.fetchone()
    c.execute("select count(*) from staff_reg")
    staffcount=c.fetchone()
    data = ""
    c.execute("select * from cust_reg")
    data=c.fetchall() 
    return render (request,"AdminViewCustomers.html",{"data":data,"custcount":custcount,"datas":datas,"staffcount":staffcount,"productcount":productcount,"st":st})

def AdminViewSeller(request):
    st="Active"
    data = ""
    c.execute("select * from product where uname='Admin' and qty<=0")
    datas=c.fetchall()
    c.execute("select count(*) from cust_reg")
    custcount=c.fetchone()
    c.execute("select count(*) from product")
    productcount=c.fetchone()
    c.execute("select count(*) from staff_reg")
    staffcount=c.fetchone()
    c.execute("select * from staff_reg")
    data=c.fetchall() 
    return render (request,"AdminViewSeller.html",{"data":data,"custcount":custcount,"datas":datas,"staffcount":staffcount,"productcount":productcount,"st":st})

def AdminViewFeedback(request):
    c.execute("select count(*) from cust_reg")
    custcount=c.fetchone()
    c.execute("select count(*) from product")
    productcount=c.fetchone()
    c.execute("select * from product where uname='Admin' and qty<=0")
    datas=c.fetchall()
    c.execute("select count(*) from staff_reg")
    staffcount=c.fetchone()
    data = ""
    c.execute("select * from cust_reg inner join feedback on cust_reg.cid = feedback.cid")
    data=c.fetchall() 
    return render (request,"AdminViewFeedback.html",{"data":data,"custcount":custcount,"productcount":productcount,"datas":datas,"staffcount":staffcount})
def SellerUpdateProduct(request):
    pid = request.GET.get('id')
    c.execute("select * from product where pid = '"+str(pid)+"'")
    data = c.fetchall()
    cdate=date.today()
    if request.POST:
        if request.FILES.get("file"):
            myfile=request.FILES.get("file")
            fs=FileSystemStorage()
            filename=fs.save(myfile.name , myfile)
            uploaded_file_url = fs.url(filename)
            uploaded_file_url=uploaded_file_url
            price=request.POST.get("price")
            qty=request.POST.get("qty") 
            c.execute("update product set pamount = '"+str(price)+"', qty = '"+str(qty)+"',pimage='"+str(uploaded_file_url)+"' where pid = '"+str(pid)+"'")
            db.commit()
            return HttpResponseRedirect("/SellerViewProduct/")
        else:
            
            price=request.POST.get("price")
            qty=request.POST.get("qty") 
            c.execute("update product set pamount = '"+str(price)+"', qty = '"+str(qty)+"', date='"+str(cdate)+"' where pid = '"+str(pid)+"'")
            db.commit()
            return HttpResponseRedirect("/SellerViewProduct/")
    return render(request,"SellerUpdateProduct.html",{"data":data,"cdate":cdate})

def AdminUpdateProduct(request):
    pid = request.GET.get('id')
    c.execute("select * from product where pid = '"+str(pid)+"'")
    data = c.fetchall()
    cdate=date.today()
    if request.POST:
        if request.FILES.get("file"):
            myfile=request.FILES.get("file")
            fs=FileSystemStorage()
            filename=fs.save(myfile.name , myfile)
            uploaded_file_url = fs.url(filename)
            uploaded_file_url=uploaded_file_url
            price=request.POST.get("price")
            qty=request.POST.get("qty") 
            c.execute("update product set pamount = '"+str(price)+"', qty = '"+str(qty)+"',pimage='"+str(uploaded_file_url)+"' where pid = '"+str(pid)+"'")
            db.commit()
            return HttpResponseRedirect("/AdminViewProduct/")
        else:
            price=request.POST.get("price")
            qty=request.POST.get("qty") 
            c.execute("update product set pamount = '"+str(price)+"', qty = '"+str(qty)+"', date='"+str(cdate)+"' where pid = '"+str(pid)+"'")
            db.commit()
            return HttpResponseRedirect("/AdminViewProduct/")
    return render(request,"AdminUpdateProduct.html",{"data":data,"cdate":cdate})

# def AdminDeletProduct(request):
#     pid = request.GET.get('id')
#     c.execute("delete from product where pid = '"+str(pid)+"'")
#     db.commit()
#     return HttpResponseRedirect("/AdminViewProduct/")
#     return render(request,"AdminViewProduct.html")

def custdeactivate(request):
    id=request.GET["id"]
    c.execute("update cust_reg set status='deactive' where cid='"+str(id)+"'")
    db.commit()
    return HttpResponseRedirect("/AdminViewCustomers")

def custactivate(request):
    id=request.GET["id"]
    status=""
    c.execute("select status from cust_reg where cid='"+str(id)+"'")
    data=c.fetchall()
    if (data[0][0]=='Active'):  
        status="deactive"
    else:
        status="Active"
    c.execute("update cust_reg set status='"+str(status)+"' where cid='"+str(id)+"'")
    db.commit()
    return HttpResponseRedirect("/AdminViewCustomers")

def subcat(request):
    sublist=[]
    catid=request.GET.get("dataid")
    c.execute("select * from subcategory where catid='"+ str(catid)+"'")
    data2=c.fetchall()
    for d in data2:
        sublist.append(d[2])
    return HttpResponse(json.dumps(sublist),content_type="application/json")

def CustomerAddFeedback(request):
    name=request.session['NAME']
    msg=""
    cid = request.session['cid']
    t="select * from categories where status='Active'"
    c.execute(t)
    data1=c.fetchall()
    t1="select count(*) from cart where cid = '"+str(cid)+"'"
    c.execute(t1)
    dataa=c.fetchone()
    if request.POST:
        a = request.POST.get('room')
        d = date.today()
        c.execute("insert into feedback(cid,feedback,fdate) values('"+str(cid)+"','"+a+"','"+str(d)+"')")
        db.commit()
        msg = "Your feedback posted successfully"
    return render(request,'CustomerAddFeedback.html',{"msg":msg,"data1":data1,"dataa":dataa[0],"name":name})

def CustomerSearchProduct(Request):
    name=Request.session['NAME']
    cid = Request.session['cid']
    s="select * from product where status='Active';"
    c.execute(s)
    data=c.fetchall()
    t1="select count(*) from cart where cid = '"+str(cid)+"'"
    c.execute(t1)
    dataa=c.fetchone()
    t="select * from categories where status='Active'"
    c.execute(t)
    data1=c.fetchall()
    s="select * from subcategory"
    c.execute(s)
    data2=c.fetchall()
    e="select * from events"
    c.execute(e)
    data3=c.fetchall()
    if Request.POST:
        print("**************************************************************")
        pname=Request.POST["t1"]
        s="select * from product where status='Active' and pname like'%"+str(pname)+"%'"
        c.execute(s)
        data=c.fetchall()
    return render(Request,'CustomerSearchProduct.html',{"data":data,"data1":data1,"data2":data2,"data3":data3,"dataa":dataa[0],"name":name})

    
def CustomerSearchmodel(Request):
    s="select * from model"
    c.execute(s)
    data=c.fetchall()
    t="select * from categories"
    c.execute(t)
    data1=c.fetchall()
    s="select * from subcategory"
    c.execute(s)
    data2=c.fetchall()
    e="select * from events"
    c.execute(e)
    data3=c.fetchall()
    return render(Request,'CustomerSearchmodel.html',{"data":data,"data1":data1,"data2":data2,"data3":data3})

def CustomerViewProCategory(Request):
    cname=Request.GET.get("id")
    name=Request.session['NAME']
   
    s="select * from product where catid = '"+str(cname)+"'"
    c.execute(s)
    data=c.fetchall()
    t="select * from categories"
    c.execute(t)
    data1=c.fetchall()
    s="select * from subcategory"
    c.execute(s)
    data2=c.fetchall()
    
    return render(Request,'CustomerSearchProduct.html',{"data":data,"data1":data1,"data2":data2,"name":name})

def CustomerViewProSubCategory(Request):
    name=Request.session['NAME']
    sid=Request.GET.get("id")
    c_id=Request.GET.get("c_id")
    s="select * from product where subid = '"+str(sid)+"' and catid  = '"+str(c_id)+"'"
    c.execute(s)
    data=c.fetchall()
    t="select * from categories"
    c.execute(t)
    data1=c.fetchall()
    s="select * from subcategory"
    c.execute(s)
    data2=c.fetchall()
   
    return render(Request,'CustomerSearchProduct.html',{"data":data,"data1":data1,"data2":data2,"name":name})

def CustomerViewProEvents(Request):
    sid=Request.GET.get("id")
    s="select * from event_pro "
    c.execute(s)
    data=c.fetchall()
    
    e="select * from events"
    c.execute(e)
    data3=c.fetchall()
    return render(Request,'CustomerSearchProduct.html',{"data":data,"data3":data3})

def CustomerViewProductDetails(Request):
    name=Request.session['NAME']
    pid=Request.GET.get("id")
    msg=""
    cid = Request.session['cid']  
    t1="select count(*) from cart where cid = '"+str(cid)+"'"
    c.execute(t1)
    dataa=c.fetchone()
    s="select * from product where pid = '"+str(pid)+"' and status='Active' or qty<0 "
    c.execute(s)
    data=c.fetchall()
    t="select * from categories"
    c.execute(t)
    data1=c.fetchall()
    s="select * from subcategory"
    c.execute(s)
    data2=c.fetchall()
    # e="select * from events"
    # c.execute(e)
    # data3=c.fetchall()
    if "cart" in Request.POST:
        price = data[0][6]
        qty = Request.POST.get("qty")
        if(qty=="") :
            msg= "Enter qty"
        else : 
            nqty= int(qty)
            c.execute("select qty from product where pid = '"+str(pid)+"' and status='Active'")
            q = c.fetchone()
            cq = q[0]
            if int(nqty) > cq:
                msg = "Invalid Stock"
            else:
                am = int(qty) * int(price)
                c.execute("insert into cart (cid,pid,qty,price)values('"+str(cid)+"','"+str(pid)+"','"+str(qty)+"','"+str(am)+"')")
                db.commit()
                msg = "Product added to cart"
    if "review" in Request.POST:
        review= Request.POST["Message"]
        c.execute("insert into review (pid,review,cid)values('"+str(pid)+"','"+str(review)+"','"+str(cid)+"')")
        db.commit()
    c.execute("select * from review join cust_reg on (review.cid=cust_reg.cid) where pid = '"+str(pid)+"' ")
    review=c.fetchall()
    return render(Request,'CustomerViewProductDetails.html',{"data":data,"data1":data1,"msg":msg,"data2":data2,"review":review,"name":name,"dataa":dataa[0]})
    

def CustomerOrderProduct(Request):
    pid=Request.GET.get("id")
    s="select * from product where pid = '"+str(pid)+"'"
    c.execute(s)
    data=c.fetchall()
    cid = Request.session["uid"]
    merid = data[0][8] 
    price = data[0][6]
    c.execute("insert into cart (cid,fid,pid,amount,qty)values('"+str(cid)+"','"+str(merid)+"','"+str(pid)+"','"+str(price)+"','1')")
    db.commit()
    t="select * from categories"
    c.execute(t)
    data1=c.fetchall()
    u="select * from brands"
    c.execute(u)
    data2=c.fetchall()
    return render(Request,'CustomerViewProDetails.html',{"data":data,"data1":data1,"data2":data2})

def CustomerViewCart(Request):
    name=Request.session['NAME']
    cid = Request.session["cid"]
    s="select * from cart inner join product on cart.pid = product.pid where cart.cid = '"+str(cid)+"'"
    c.execute(s)
    data=c.fetchall()
    t="select count(*) from cart where cid = '"+str(cid)+"'"
    c.execute(t)
    data1=c.fetchone()
    u="select sum(price) from cart where cid = '"+str(cid)+"'"
    c.execute(u)
    data2=c.fetchone()
    s="select * from subcategory"
    c.execute(s)
    data3=c.fetchall()
    totalamount = data2[0]
    tot = totalamount
    qt=""
    cqt=""
    nqt=""
    Request.session["pay"] = str(tot)
    if Request.GET:
        ci = Request.GET.get('id')
        c.execute("delete from cart where id = '"+str(ci)+"'")
        db.commit()
        return HttpResponseRedirect("/CustomerViewCart")
    if Request.POST:
        c.execute("select * from cart where cid = '"+str(cid)+"'")
        data3 = c.fetchall()
        for d3 in data3:
            custid = d3[1]
            proid = d3[2]
            amot = d3[4]
            quty = d3[3]
            carid = d3[0]
            today = datetime.datetime.today()
            c.execute("insert into customer_order (cid,pid,p_price,p_qty,date)values('"+str(custid)+"','"+str(proid)+"','"+str(amot)+"','"+str(quty)+"','"+str(today)+"')")
            db.commit()
            c.execute("select qty from product where pid = '"+str(proid)+"'")
            qt=c.fetchone()
            cqt = qt[0]
            nqt = int(cqt) - int(quty)
            c.execute("update product set qty = '"+str(nqt)+"' where pid = '"+str(proid)+"'")
            db.commit()
            c.execute("delete from cart where id = '"+str(carid)+"'")
            db.commit()
        return HttpResponseRedirect("/billingaddress")
    return render(Request,'CustomerViewCart.html',{"data":data,"data1":data1[0],"data2":data2[0],"data3":data3,"name":name})

def AdminViewsales(request):
    data = ""
    c.execute("select * from product where uname='Admin' and qty<=0")
    datas=c.fetchall()
    c.execute("select count(*) from cust_reg")
    custcount=c.fetchone()
    c.execute("select count(*) from product")
    productcount=c.fetchone()
    c.execute("select count(*) from staff_reg")
    staffcount=c.fetchone()
    c.execute("select p.pid,p.pname,p.pimage,sum(co.p_qty) as tot from product p join customer_order co on(p.pid=co.pid) group by co.pid")
    data=c.fetchall() 
    return render (request,"AdminViewsales.html",{"data":data,"custcount":custcount,"datas":datas,"staffcount":staffcount,"productcount":productcount})



def SellerViewSales(request):
    data = ""
    c.execute("select p.pid,p.pname,sum(co.p_qty) as tot from product p join customer_order co on(p.pid=co.pid) group by co.pid")
    data=c.fetchall() 
    return render (request,"SellerViewSales.html",{"data":data})


    
def Acceptorder(request):
    id=request.GET["id"]
    c.execute("update customer_order set status='Accepted' where id='"+str(id)+"'")
    db.commit()
    return HttpResponseRedirect("/AdminViewMyBooking")

def payment1(request): 
    if request.POST:
        card=request.POST.get("test")
        request.session["card"]=card
        cardno=request.POST.get("cardno")
        request.session["card_no"]=cardno
        pinno=request.POST.get("pinno")
        request.session["pinno"]=pinno
        return HttpResponseRedirect("/payment2")
    return render(request,"payment1.html")

def payment2(request):
    cno=request.session["card_no"]
    amount=request.session["pay"]
    if request.POST:
        return HttpResponseRedirect("/payment3")
    return render(request,"payment2.html",{"cno":cno,"amount":amount})

def payment3(request):
    return render(request,"payment3.html")

def payment4(request):
    return render(request,"payment4.html")

def payment5(request):
    cno=request.session["card_no"]
    today = date.today()
    name =  request.session['NAME'] 
    amount = request.session["pay"]
    return render(request,"payment5.html",{"cno":cno,"today":today,"name":name,"amount":amount})

def CustomerViewMyBooking(request):
    name=request.session['NAME']
    cid=request.session["cid"]
    t1="select count(*) from cart where cid = '"+str(cid)+"'"
    c.execute(t1)
    dataa=c.fetchone()
    c.execute("select * from customer_order inner join product on customer_order.pid = product.pid where customer_order.cid = '"+str(cid)+"'")
    data = c.fetchall()
    t="select * from categories where status='Active'"
    c.execute(t)
    data1=c.fetchall()
    return render(request,"CustomerViewMyBooking.html",{"data":data,"dataa":dataa[0],"data1":data1,"name":name})
    
def AdminViewMyBooking(request):
    cid=request.session["cid"]
    c.execute("select count(*) from cust_reg")
    custcount=c.fetchone()
    c.execute("select count(*) from product")
    productcount=c.fetchone()
    c.execute("select * from product where uname='Admin' and qty<=0")
    datas=c.fetchall()
    c.execute("select count(*) from staff_reg")
    staffcount=c.fetchone()
    c.execute("select * from customer_order inner join product on customer_order.pid = product.pid join cust_reg cr on (cr.cid=customer_order.cid)")
    data = c.fetchall()
    return render(request,"AdminViewMyBooking.html",{"data":data,"custcount":custcount,"productcount":productcount,"datas":datas,"staffcount":staffcount})
def Acceptorder(request):
    id=request.GET["id"]
    c.execute("update customer_order set status='Accepted' where id='"+str(id)+"'")
    db.commit()
    return HttpResponseRedirect("/AdminViewMyBooking")



def changepassword(request):
    if request.POST:
        uname=request.session.get('username')
        opass=request.POST.get('t1')
        npass=request.POST.get('t2')
        c.execute("update login set password=%s where username=%s and password=%s",npass,uname,opass)
        db.commit()
        return render(request,"Delivarypassword.html")