from flask_mail import Message
from datetime import datetime

class EmailService:
    def __init__(self, app, mail):
        self.app = app
        self.mail = mail
        self.business_email = app.config['BUSINESS_EMAIL']
        self.business_name = app.config['BUSINESS_NAME']
    
    def send_email(self, to, subject, html_body, attachments=None):
        """Send an email"""
        msg = Message(
            subject=subject,
            sender=self.business_email,
            recipients=[to] if isinstance(to, str) else to
        )
        msg.html = html_body
        
        if attachments:
            for attachment in attachments:
                with open(attachment, 'rb') as f:
                    msg.attach(
                        filename=attachment.split('/')[-1],
                        content_type='application/pdf',
                        data=f.read()
                    )
        
        self.mail.send(msg)
    
    def send_order_confirmation(self, order, receipt_path=None):
        """Send order confirmation email with receipt"""
        subject = f"Order Confirmation - {order.order_number}"
        
        items_html = ''.join([
            f"<li>{item['name']} (Size: {item['size']}) x {item['quantity']} - ${item['price'] * item['quantity']:.2f}</li>"
            for item in order.items
        ])
        
        html = f"""
        <html>
        <body style="font-family: Arial, sans-serif; color: #2C3E50;">
            <div style="max-width: 600px; margin: 0 auto; padding: 20px;">
                <h1 style="color: #006994;">Thank You for Your Order!</h1>
                <p>Hi {order.customer_name},</p>
                <p>Your order has been confirmed! We're excited to start handcrafting your beautiful bikini.</p>
                
                <div style="background: #F5E6D3; padding: 20px; border-radius: 8px; margin: 20px 0;">
                    <h2 style="color: #006994;">Order Details</h2>
                    <p><strong>Order Number:</strong> {order.order_number}</p>
                    <p><strong>Order Date:</strong> {order.created_at.strftime('%B %d, %Y')}</p>
                    
                    <h3 style="color: #006994;">Items:</h3>
                    <ul>
                        {items_html}
                    </ul>
                    
                    <p><strong>Subtotal:</strong> ${order.subtotal:.2f}</p>
                    <p><strong>Shipping:</strong> ${order.shipping_cost:.2f}</p>
                    <p><strong>Tax:</strong> ${order.tax:.2f}</p>
                    <p><strong style="font-size: 1.2em; color: #006994;">Total:</strong> ${order.total:.2f}</p>
                </div>
                
                <div style="background: #E3F2FD; padding: 15px; border-radius: 8px; margin: 20px 0;">
                    <h3 style="color: #006994;">What's Next?</h3>
                    <p>🎨 Your bikini will be handcrafted over the next 2-3 weeks</p>
                    <p>📧 You'll receive updates as your order progresses</p>
                    <p>📦 Shipping notification when it's on the way</p>
                </div>
                
                <p>Questions? Reply to this email or contact us at {self.business_email}</p>
                
                <p style="margin-top: 30px;">With love,<br>
                <strong>Bikinis By Telly</strong></p>
            </div>
        </body>
        </html>
        """
        
        attachments = [receipt_path] if receipt_path else None
        self.send_email(order.customer_email, subject, html, attachments)
        
        # Also notify admin
        admin_subject = f"New Order Received - {order.order_number}"
        admin_html = f"""
        <html>
        <body>
            <h2>New Order Alert</h2>
            <p><strong>Order Number:</strong> {order.order_number}</p>
            <p><strong>Customer:</strong> {order.customer_name}</p>
            <p><strong>Email:</strong> {order.customer_email}</p>
            <p><strong>Total:</strong> ${order.total:.2f}</p>
            <p><strong>Items:</strong></p>
            <ul>{items_html}</ul>
        </body>
        </html>
        """
        self.send_email(self.business_email, admin_subject, admin_html)
    
    def send_custom_order_confirmation(self, custom_order):
        """Send custom order confirmation"""
        subject = f"Custom Order Request Received - {custom_order.order_number}"
        
        html = f"""
        <html>
        <body style="font-family: Arial, sans-serif; color: #2C3E50;">
            <div style="max-width: 600px; margin: 0 auto; padding: 20px;">
                <h1 style="color: #006994;">Custom Order Request Received!</h1>
                <p>Hi {custom_order.customer_name},</p>
                <p>Thank you for your custom bikini request! We've received your specifications and will review them shortly.</p>
                
                <div style="background: #F5E6D3; padding: 20px; border-radius: 8px; margin: 20px 0;">
                    <h2 style="color: #006994;">Your Request</h2>
                    <p><strong>Request Number:</strong> {custom_order.order_number}</p>
                    <p><strong>Style:</strong> {custom_order.style}</p>
                    <p><strong>Primary Color:</strong> {custom_order.primary_color}</p>
                    {f"<p><strong>Secondary Color:</strong> {custom_order.secondary_color}</p>" if custom_order.secondary_color else ""}
                    <p><strong>Pattern:</strong> {custom_order.pattern}</p>
                    <p><strong>Budget Range:</strong> {custom_order.budget}</p>
                </div>
                
                <div style="background: #E3F2FD; padding: 15px; border-radius: 8px; margin: 20px 0;">
                    <h3 style="color: #006994;">Next Steps</h3>
                    <p>📋 We'll review your specifications within 24 hours</p>
                    <p>💰 You'll receive a quote and timeline estimate</p>
                    <p>✅ Once approved, we'll start crafting your unique piece</p>
                </div>
                
                <p>We'll be in touch soon!</p>
                
                <p style="margin-top: 30px;">With love,<br>
                <strong>Bikinis By Telly</strong><br>
                {self.business_email}</p>
            </div>
        </body>
        </html>
        """
        
        self.send_email(custom_order.customer_email, subject, html)
        
        # Notify admin
        admin_subject = f"New Custom Order Request - {custom_order.order_number}"
        admin_html = f"""
        <html>
        <body>
            <h2>New Custom Order Request</h2>
            <p><strong>Request Number:</strong> {custom_order.order_number}</p>
            <p><strong>Customer:</strong> {custom_order.customer_name}</p>
            <p><strong>Email:</strong> {custom_order.customer_email}</p>
            <p><strong>Phone:</strong> {custom_order.customer_phone}</p>
            <p><strong>Style:</strong> {custom_order.style}</p>
            <p><strong>Colors:</strong> {custom_order.primary_color} / {custom_order.secondary_color}</p>
            <p><strong>Budget:</strong> {custom_order.budget}</p>
            <p><strong>Special Requests:</strong> {custom_order.special_requests}</p>
            <p><strong>Measurements:</strong> {custom_order.measurements}</p>
        </body>
        </html>
        """
        self.send_email(self.business_email, admin_subject, admin_html)
    
    def send_shipping_notification(self, order, tracking_number=None):
        """Send shipping notification"""
        subject = f"Your Order Has Shipped - {order.order_number}"
        
        tracking_info = f"<p><strong>Tracking Number:</strong> {tracking_number}</p>" if tracking_number else ""
        
        html = f"""
        <html>
        <body style="font-family: Arial, sans-serif; color: #2C3E50;">
            <div style="max-width: 600px; margin: 0 auto; padding: 20px;">
                <h1 style="color: #006994;">Your Bikini is On Its Way! 📦</h1>
                <p>Hi {order.customer_name},</p>
                <p>Great news! Your handmade bikini has been shipped and is heading your way.</p>
                
                <div style="background: #F5E6D3; padding: 20px; border-radius: 8px; margin: 20px 0;">
                    <p><strong>Order Number:</strong> {order.order_number}</p>
                    {tracking_info}
                    <p><strong>Shipping Address:</strong><br>{order.shipping_address}</p>
                </div>
                
                <p>Enjoy your beautiful new bikini! Don't forget to follow our care instructions to keep it looking amazing.</p>
                
                <p style="margin-top: 30px;">With love,<br>
                <strong>Bikinis By Telly</strong></p>
            </div>
        </body>
        </html>
        """
        
        self.send_email(order.customer_email, subject, html)
    
    def send_contact_confirmation(self, contact):
        """Send contact form confirmation"""
        subject = "We Received Your Message"
        
        html = f"""
        <html>
        <body style="font-family: Arial, sans-serif; color: #2C3E50;">
            <div style="max-width: 600px; margin: 0 auto; padding: 20px;">
                <h1 style="color: #006994;">Thank You for Contacting Us!</h1>
                <p>Hi {contact.name},</p>
                <p>We've received your message and will get back to you within 24 hours.</p>
                
                <div style="background: #F5E6D3; padding: 20px; border-radius: 8px; margin: 20px 0;">
                    <p><strong>Your Message:</strong></p>
                    <p>{contact.message}</p>
                </div>
                
                <p>Talk soon!<br>
                <strong>Bikinis By Telly</strong></p>
            </div>
        </body>
        </html>
        """
        
        self.send_email(contact.email, subject, html)
        
        # Notify admin
        admin_subject = f"New Contact Message - {contact.subject}"
        admin_html = f"""
        <html>
        <body>
            <h2>New Contact Form Submission</h2>
            <p><strong>From:</strong> {contact.name} ({contact.email})</p>
            <p><strong>Subject:</strong> {contact.subject}</p>
            <p><strong>Message:</strong></p>
            <p>{contact.message}</p>
        </body>
        </html>
        """
        self.send_email(self.business_email, admin_subject, admin_html)
    
    def send_newsletter_welcome(self, email):
        """Send newsletter welcome email"""
        subject = "Welcome to Bikinis By Telly!"
        
        html = f"""
        <html>
        <body style="font-family: Arial, sans-serif; color: #2C3E50;">
            <div style="max-width: 600px; margin: 0 auto; padding: 20px;">
                <h1 style="color: #006994;">Welcome! 🌊</h1>
                <p>Thanks for joining our newsletter!</p>
                <p>You'll be the first to know about:</p>
                <ul>
                    <li>New bikini designs</li>
                    <li>Special promotions</li>
                    <li>Behind-the-scenes content</li>
                    <li>Exclusive offers</li>
                </ul>
                <p>Stay tuned for beautiful handmade bikinis!</p>
                <p style="margin-top: 30px;">With love,<br>
                <strong>Bikinis By Telly</strong></p>
            </div>
        </body>
        </html>
        """
        
        self.send_email(email, subject, html)
    
    def send_new_review_notification(self, review):
        """Notify admin of new review"""
        subject = f"New Review Submitted - Product #{review.product_id}"
        
        html = f"""
        <html>
        <body>
            <h2>New Review Awaiting Approval</h2>
            <p><strong>Product ID:</strong> {review.product_id}</p>
            <p><strong>From:</strong> {review.name}</p>
            <p><strong>Rating:</strong> {'★' * review.rating}{'☆' * (5 - review.rating)}</p>
            <p><strong>Review:</strong></p>
            <p>{review.review}</p>
            <p>Log in to the admin panel to approve or reject this review.</p>
        </body>
        </html>
        """
        
        self.send_email(self.business_email, subject, html)
