from paypalrestsdk import Payment, configure
import json

class PaymentService:
    def __init__(self, app):
        self.app = app
        configure({
            "mode": app.config.get('PAYPAL_MODE', 'sandbox'),  # sandbox or live
            "client_id": app.config.get('PAYPAL_CLIENT_ID'),
            "client_secret": app.config.get('PAYPAL_CLIENT_SECRET')
        })
    
    def create_payment(self, amount, order_id, customer_email, return_url, cancel_url):
        """Create a PayPal payment"""
        try:
            payment = Payment({
                "intent": "sale",
                "payer": {
                    "payment_method": "paypal"
                },
                "redirect_urls": {
                    "return_url": return_url,
                    "cancel_url": cancel_url
                },
                "transactions": [{
                    "amount": {
                        "total": f"{amount:.2f}",
                        "currency": "USD"
                    },
                    "description": f"Bikinis By Telly - Order #{order_id}",
                    "custom": str(order_id),
                    "invoice_number": str(order_id)
                }]
            })
            
            if payment.create():
                return payment
            else:
                self.app.logger.error(f"PayPal error: {payment.error}")
                raise Exception(payment.error)
        except Exception as e:
            self.app.logger.error(f"PayPal error: {str(e)}")
            raise
    
    def execute_payment(self, payment_id, payer_id):
        """Execute PayPal payment after user approval"""
        try:
            payment = Payment.find(payment_id)
            if payment.execute({"payer_id": payer_id}):
                return payment
            else:
                self.app.logger.error(f"PayPal execution error: {payment.error}")
                raise Exception(payment.error)
        except Exception as e:
            self.app.logger.error(f"PayPal execution error: {str(e)}")
            raise
    
    def create_refund(self, sale_id, amount=None):
        """Create a refund for a payment"""
        try:
            from paypalrestsdk import Sale
            sale = Sale.find(sale_id)
            
            refund_request = {}
            if amount:
                refund_request = {
                    "amount": {
                        "total": f"{amount:.2f}",
                        "currency": "USD"
                    }
                }
            
            refund = sale.refund(refund_request)
            if refund.success():
                return refund
            else:
                self.app.logger.error(f"Refund error: {refund.error}")
                raise Exception(refund.error)
        except Exception as e:
            self.app.logger.error(f"Refund error: {str(e)}")
            raise

