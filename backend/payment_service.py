import stripe

class PaymentService:
    def __init__(self, app):
        self.app = app
        stripe.api_key = app.config['STRIPE_SECRET_KEY']
        self.webhook_secret = app.config.get('STRIPE_WEBHOOK_SECRET', '')
    
    def create_payment_intent(self, amount, order_id, customer_email):
        """Create a Stripe payment intent"""
        try:
            intent = stripe.PaymentIntent.create(
                amount=amount,  # Amount in cents
                currency='usd',
                receipt_email=customer_email,
                metadata={
                    'order_id': order_id,
                    'business': 'Bikinis By Telly'
                },
                description=f'Order payment for Bikinis By Telly'
            )
            return intent
        except stripe.error.StripeError as e:
            self.app.logger.error(f"Stripe error: {str(e)}")
            raise
    
    def handle_webhook(self, payload, sig_header):
        """Handle Stripe webhook events"""
        try:
            if self.webhook_secret:
                event = stripe.Webhook.construct_event(
                    payload, sig_header, self.webhook_secret
                )
            else:
                # For development without webhook secret
                import json
                event = json.loads(payload)
            
            return event
        except ValueError as e:
            # Invalid payload
            self.app.logger.error(f"Invalid webhook payload: {str(e)}")
            raise
        except stripe.error.SignatureVerificationError as e:
            # Invalid signature
            self.app.logger.error(f"Invalid webhook signature: {str(e)}")
            raise
    
    def create_refund(self, payment_intent_id, amount=None):
        """Create a refund for a payment"""
        try:
            refund = stripe.Refund.create(
                payment_intent=payment_intent_id,
                amount=amount  # Optional: partial refund amount in cents
            )
            return refund
        except stripe.error.StripeError as e:
            self.app.logger.error(f"Refund error: {str(e)}")
            raise
