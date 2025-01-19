# Create your views here.
from datetime import date, timedelta
from django.core.mail import send_mail
from django.utils import timezone
from django.shortcuts import render, get_object_or_404, redirect
from django.urls import reverse_lazy
from django.views.generic import ListView, CreateView, UpdateView, DeleteView
# from .models import Store,StoreItem,Barcode,Item,ItemImage,Unit,GroupsItem,Currency,Station,Supplier,Beneficiary,CustomUser, IncomingProcess,IncomingItem,OutgoingProcess,OutgoingItem,ModifyProcess,IncomingReturn,ReturnedItem,DamagedItem,DamageProcess,Transaction,InventoryCount,InventoryCountItem,AuditLog,Notification,AutomaticOrder,SupplierPerformance,Quotation, QuotationItem,ScheduledTask,Chat,Branch,CustomPermission
# from .forms import StoreForm,ExcelUploadForm,BranchForm,StoreItemForm,CustomUserCreationForm,ItemForm,ItemImageFormSet,UnitForm,GroupsItemForm,CurrencyForm,StationForm,SupplierForm,BeneficiaryForm,CustomUserForm,IncomingProcessForm,IncomingItemForm,OutgoingProcessForm,OutgoingItemForm,ModifyProcessForm,ReturnedItemForm,ReturnedOutgoingItemForm,OutgoingReturnForm,DamagedItemForm,DamageProcessForm,TransferredItemForm,StockTransferForm,InventoryCountForm,InventoryCountItemForm,InventoryCountFilterForm,QuotationForm, QuotationItemForm,PaymentVoucherForm,DisbursementVoucherForm,ExpenseForm,SalaryAdvanceForm,CustomUserCreationForm, CustomUserLoginForm,CustomPermissionForm
from django.views import View
from django.contrib import messages
from django.core.paginator import Paginator
from django.forms import modelformset_factory
from django.utils.dateparse import parse_date
from django.db import transaction
from django.db.models import F
from django.http import HttpResponse, HttpResponseForbidden
from django.http import JsonResponse
from django.contrib.auth.views import LoginView
from django.contrib.auth import login, authenticate,logout
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.contrib.sessions.models import Session
from django.forms import inlineformset_factory

from django.contrib.auth.decorators import user_passes_test
from django.core.exceptions import PermissionDenied
from django.dispatch import receiver
import json
from django.contrib.auth.models import Permission,User
import os
from io import BytesIO
from django.core.files.base import ContentFile
import random
import string
from django.views.decorators.csrf import csrf_exempt
from django.template.loader import render_to_string

# Create your views here.




def get_income_data(request):
    today = date.now()
    year_start = today.replace(month=1, day=1, hour=0, minute=0, second=0, microsecond=0)
    
    # حساب الدخل لليوم والسنة
    income_today = 1000  # استبدل هذه القيمة بحسابك الفعلي
    income_this_year = 50000  # استبدل هذه القيمة بحسابك الفعلي

    data = {
        'income_today': income_today,
        'income_this_year': income_this_year,
    }
    return JsonResponse(data)



















##################################### صفحة لوحة التحكم  ##################################################################
# class IndexView(ListView):
#     template_name = 'base.html'
#     def get_queryset(self):
#          return Branch.objects.all()
    
#     def get_context_data(self, **kwargs):
#         context = super().get_context_data(**kwargs)
#         context['branches'] = self.get_queryset()  
#         return context
##################################### صفحة لوحة التحكم  ##################################################################