# your_app/context_processors.py

from django.utils import timezone
from accounts.models import Users,Subscription
from dealer.models import DealerBitCounts
from django.shortcuts import redirect
from django.urls import reverse

def bits_context_processor(request):
    user_id = request.session.get('user_id')

    # Check if user_id is available in the session
    if not user_id:
        return {}

    try:
            user = Users.objects.get(id=user_id)

            if user.role != 'Dealer':
                return {}
            context={}
            current_date = timezone.now().date()
            subscriptions = Subscription.objects.filter(user=user, expiry_date__gte=current_date)

            total_bits_allowed = 0
            unlimited = False

            for subscription in subscriptions:
                if subscription.planname == 'free':
                    total_bits_allowed += 1
                elif subscription.planname == 'basic':
                    total_bits_allowed += 4
                elif subscription.planname == 'standard':
                    total_bits_allowed += 10
                elif subscription.planname == 'premium':
                    unlimited = True
                    break

            if unlimited:
                total_bits_allowed = float('inf')

            dealer_bit_count, created = DealerBitCounts.objects.get_or_create(user=user)

            remaining_bits = max(total_bits_allowed - dealer_bit_count.current_bid_count, 0)

            context['total_bits_allowed'] = total_bits_allowed
            context['remaining_bits'] = remaining_bits
            print('context',context)
            return context
    except Users.DoesNotExist:
        # If user does not exist, redirect to the home page
        return redirect(reverse('/'))

    return {}