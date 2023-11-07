from fastapi import APIRouter
# from dotenv import dotenv_values
from fastapi.responses import RedirectResponse
import stripe#, json
 
# env = dotenv_values('.env')
# stripe_config=json.loads(env['STRIPE_CONFIG'])
 
router = APIRouter(
    prefix='/stripe',
    tags=['Stripe']
)
 
YOUR_DOMAIN='http://localhost'
stripe.api_key='sk_test_51O51sFLyUJ8npuVNBuKRFJQOwNH8vK6Nz2m9cIeI9ZvYOZ1bqdoSsB0NnSuFI68VxoWQ9c71QRkmjxnSa9SfzhRM00GXWTQ3RX'
 
@router.get('/checkout')
async def get_checkout():
    checkout_session = stripe.checkout.Session.create(
        success_url = YOUR_DOMAIN+'/success.html',
        cancel_url = YOUR_DOMAIN+'/cancel.html',
        line_items=[
            {
                "price": 'price_1O51ynLyUJ8npuVNARZmr63A',
                "quantity": 1,
            }
        ],
        mode="subscription",
        payment_method_types = ['card'],
    )
    return RedirectResponse(checkout_session['url'])
 
# @router.get('/webhook')
# async def retreive_webhook():
#     return