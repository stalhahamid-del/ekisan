from datetime import datetime
from accounts.models import Subscription,Users
from farmer.models import Product

from django.shortcuts import redirect
from django.urls import reverse

def product_limit_info(request):
    user_id = request.session.get('user_id')

    # Check if user_id is available in the session
    if not user_id:
        return {}

    try:
        user = Users.objects.get(id=user_id)

        if user.role != 'Farmer':
            return {}

        # Calculate product limits and remaining chances
        current_date = datetime.now().date()
        max_products_allowed = 0
        user_subscriptions = Subscription.objects.filter(user=user, paid=True, expiry_date__gte=current_date)

        for subscription in user_subscriptions:
            if subscription.planname == 'free':
                max_products_allowed += 1
            elif subscription.planname == 'basic':
                max_products_allowed += 4
            elif subscription.planname == 'standard':
                max_products_allowed += 10
            elif subscription.planname == 'premium':
                max_products_allowed = float('inf')
                break

        product_count = Product.objects.filter(user=user).count()
        remaining_chances = max_products_allowed - product_count

        return {
            'max_products_allowed': max_products_allowed,
            'remaining_chances': remaining_chances,
        }
    except Users.DoesNotExist:
        # If user does not exist, redirect to the home page
        return redirect(reverse('/'))

    return {}
