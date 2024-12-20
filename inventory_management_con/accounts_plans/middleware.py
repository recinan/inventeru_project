from django.utils.timezone import now
from .models import Subscription, Plan
from warehouse_man.models import Warehouse
from django.contrib import messages

class CheckSubscriptionAndManageWarehousesMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        user = request.user
        if user.is_authenticated:
            if user.user_plan:
                subscription = Subscription.objects.filter(sub_user=user).first()
                if subscription and subscription.sub_end_date < now():
                    default_plan = Plan.objects.filter(is_default=True).first()
                    if default_plan:
                        user.user_plan = default_plan
                        user.save()
                        subscription.delete()

                # Deactivate and activate warehouses
                deactivate_warehouses(user)
                activate_warehouses(user)
        
        # Proceed with the request
        response = self.get_response(request)
        return response

def deactivate_warehouses(user):
    if user.user_plan.plan_type == 'infinite':
        print('deactiveinfinite')
        warehouses = Warehouse.objects.filter(user=user)
        if warehouses.count() > 1:
            extra_warehouses = warehouses[1:]
            for warehouse in extra_warehouses:
                warehouse.is_active = False
                warehouse.save()

def activate_warehouses(user):
    if user.user_plan.plan_type in ['monthly', 'annual']:
        print('deactivemonth')
        max_warehouses = 2
        warehouses = Warehouse.objects.filter(user=user, is_active=False)[:max_warehouses]
        for warehouse in warehouses:
            warehouse.is_active = True
            warehouse.save()
