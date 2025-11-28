# from django.test import TestCase

# # Create your tests here.
# from django.test import TestCase
# from django.contrib.auth import get_user_model
# from django.utils import timezone
# from django.contrib.auth import login
# from django.test.client import RequestFactory
# from accounts.models import Subscription

# class SubscriptionSignalTest(TestCase):
#     def setUp(self):
#         self.user = get_user_model().objects.create_user(
#             username='testuser',
#             password='testpass'
#         )
#         self.subscription = Subscription.objects.create(
#             user=self.user,
#             expiry_date=timezone.now().date() - timezone.timedelta(days=1)
#         )
#         self.factory = RequestFactory()

#     def test_signal_triggered_on_login(self):
#         request = self.factory.post('/login/')
#         request.user = self.user

#         with self.assertLogs('accounts.signals', level='INFO') as cm:
#             login(request, self.user)
#             self.assertIn('User logged in', cm.output[0])
#             self.assertFalse(Subscription.objects.filter(id=self.subscription.id).exists())
