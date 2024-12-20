from django.shortcuts import render,redirect
from .models import Plan
from django.contrib import messages
from django.urls import reverse_lazy
from .models import Subscription
from django.utils.timezone import now
from datetime import datetime,timedelta
from django.contrib.auth.signals import user_logged_in
from django.dispatch import receiver
from django.conf import settings
from warehouse_man.models import Warehouse

# Create your views here.

def plan_page(request):
    plans = Plan.objects.all()
    subscription = Subscription.objects.filter(sub_user = request.user).first()
    context = {
        'plans':plans,
        'subscription':subscription
    }
    return render(request,'accounts_plans/plans.html',context)

def upgrade_plan(request, plan_id):
    new_plan = Plan.objects.get(id=plan_id)
    request.user.user_plan = new_plan
    subscription = create_subscription(request.user, new_plan)
    request.user.save()
    messages.success(request,f"Your plan updated as {new_plan.plan_name}! It expires on {subscription.sub_end_date}")
    return redirect(reverse_lazy('profile-update',kwargs={'username':request.user.username}))


def create_subscription(sub_user, new_plan):
    subscription,created = Subscription.objects.get_or_create(sub_user=sub_user)
    subscription.sub_plan = new_plan
    subscription.sub_start_date = now()
    if new_plan.plan_type == 'infinite':
        subscription.sub_end_date = datetime.max
    if new_plan.plan_type == "monthly":
        subscription.sub_end_date = now() + timedelta(days=30)
    if new_plan.plan_type == "annual":
        subscription.sub_end_date = now() + timedelta(days=365)
    subscription.sub_is_active = True
    subscription.save()
    return subscription

