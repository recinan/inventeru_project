from django.shortcuts import render
from .models import Plan
# Create your views here.

def plan_page(request):
    plans = Plan.objects.all()
    context = {
        'plans':plans
    }
    return render(request,'accounts_plans/plans.html',context)