from django.contrib.auth.signals import user_logged_in
from django.dispatch import receiver
from django.conf import settings
from warehouse_man.models import Warehouse
from .models import Subscription
from .models import Plan
from django.utils.timezone import now

@receiver(user_logged_in)
def check_subscription_status_every_logged_in(sender,request,user,**kwargs):
    print("Django signals")
    if user.user_plan:
        print("Django signals222")
        subscription = Subscription.objects.filter(sub_user = user).first()
        if subscription and subscription.sub_end_date < now():
            default_plan = Plan.objects.filter(is_default=True).first()
            if default_plan:
                user.user_plan = default_plan
                user.save()
                subscription.delete()
        deactivate_warehouses(user)
        activate_warehouses(user)

def deactivate_warehouses(user):
    if user.user_plan.plan_type == 'infinite':
        print('deactiveinfinite')
        warehouses = Warehouse.objects.filter(user=user)
        if warehouses.count() > 1:
            #warehouses[1:].update(is_active=False)
            
            extra_warehouses = warehouses[1:]
            for warehouse in extra_warehouses:
                warehouse.is_active = False
                warehouse.save()

def activate_warehouses(user):
    if user.user_plan.plan_type in ['monthly','annual']:
        print('deactivemonth')
        max_warehouses = 2
        warehouses = Warehouse.objects.filter(user=user, is_active=False)[:max_warehouses]
        #warehouses.update(is_active=True)
        
        for warehouse in warehouses:
            warehouse.is_active = True
            warehouse.save()

def get_active_warehouses(user):
    warehouses = Warehouse.objects.filter(user=user, is_active=True)
    return warehouses
