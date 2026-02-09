from reportlab.lib.pagesizes import letter
from reportlab.lib import colors
from reportlab.lib.units import inch
from reportlab.platypus import SimpleDocTemplate, Table, TableStyle, Paragraph, Spacer, Image
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from datetime import datetime
import os

class ReceiptGenerator:
    def __init__(self, app):
        self.app = app
        self.business_name = app.config['BUSINESS_NAME']
        self.business_email = app.config['BUSINESS_EMAIL']
        self.receipts_folder = 'receipts'
        os.makedirs(self.receipts_folder, exist_ok=True)
    
    def generate_receipt(self, order):
        """Generate a PDF receipt for an order"""
        filename = f"{self.receipts_folder}/receipt_{order.order_number}.pdf"
        
        # Create PDF
        doc = SimpleDocTemplate(filename, pagesize=letter)
        story = []
        styles = getSampleStyleSheet()
        
        # Custom styles
        title_style = ParagraphStyle(
            'CustomTitle',
            parent=styles['Heading1'],
            fontSize=24,
            textColor=colors.HexColor('#006994'),
            spaceAfter=30,
            alignment=1  # Center
        )
        
        heading_style = ParagraphStyle(
            'CustomHeading',
            parent=styles['Heading2'],
            fontSize=14,
            textColor=colors.HexColor('#006994'),
            spaceAfter=12
        )
        
        # Header
        story.append(Paragraph(self.business_name, title_style))
        story.append(Paragraph(f"Email: {self.business_email}", styles['Normal']))
        story.append(Spacer(1, 0.3 * inch))
        
        # Receipt Title
        story.append(Paragraph("RECEIPT", heading_style))
        story.append(Spacer(1, 0.2 * inch))
        
        # Order Information
        info_data = [
            ['Order Number:', order.order_number],
            ['Date:', order.created_at.strftime('%B %d, %Y')],
            ['Customer:', order.customer_name],
            ['Email:', order.customer_email],
        ]
        
        info_table = Table(info_data, colWidths=[2*inch, 4*inch])
        info_table.setStyle(TableStyle([
            ('FONTNAME', (0, 0), (0, -1), 'Helvetica-Bold'),
            ('FONTNAME', (1, 0), (1, -1), 'Helvetica'),
            ('FONTSIZE', (0, 0), (-1, -1), 10),
            ('BOTTOMPADDING', (0, 0), (-1, -1), 6),
        ]))
        story.append(info_table)
        story.append(Spacer(1, 0.3 * inch))
        
        # Shipping Address
        story.append(Paragraph("Shipping Address:", heading_style))
        address_text = f"{order.shipping_address}<br/>{order.shipping_city}, {order.shipping_state} {order.shipping_zip}"
        story.append(Paragraph(address_text, styles['Normal']))
        story.append(Spacer(1, 0.3 * inch))
        
        # Items Table
        story.append(Paragraph("Items Ordered:", heading_style))
        
        items_data = [['Item', 'Size', 'Qty', 'Price', 'Total']]
        for item in order.items:
            items_data.append([
                item['name'],
                item.get('size', 'N/A'),
                str(item['quantity']),
                f"${item['price']:.2f}",
                f"${item['price'] * item['quantity']:.2f}"
            ])
        
        items_table = Table(items_data, colWidths=[2.5*inch, 1*inch, 0.7*inch, 1*inch, 1*inch])
        items_table.setStyle(TableStyle([
            ('BACKGROUND', (0, 0), (-1, 0), colors.HexColor('#006994')),
            ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
            ('ALIGN', (0, 0), (-1, -1), 'LEFT'),
            ('ALIGN', (2, 0), (-1, -1), 'RIGHT'),
            ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
            ('FONTSIZE', (0, 0), (-1, 0), 12),
            ('BOTTOMPADDING', (0, 0), (-1, 0), 12),
            ('BACKGROUND', (0, 1), (-1, -1), colors.beige),
            ('GRID', (0, 0), (-1, -1), 1, colors.grey),
            ('FONTNAME', (0, 1), (-1, -1), 'Helvetica'),
            ('FONTSIZE', (0, 1), (-1, -1), 10),
        ]))
        story.append(items_table)
        story.append(Spacer(1, 0.3 * inch))
        
        # Totals
        totals_data = [
            ['Subtotal:', f"${order.subtotal:.2f}"],
            ['Shipping:', f"${order.shipping_cost:.2f}"],
            ['Tax:', f"${order.tax:.2f}"],
            ['', ''],
            ['TOTAL:', f"${order.total:.2f}"]
        ]
        
        totals_table = Table(totals_data, colWidths=[5*inch, 1.5*inch])
        totals_table.setStyle(TableStyle([
            ('ALIGN', (0, 0), (-1, -1), 'RIGHT'),
            ('FONTNAME', (0, 0), (0, 2), 'Helvetica'),
            ('FONTNAME', (1, 0), (1, 2), 'Helvetica'),
            ('FONTNAME', (0, 4), (-1, 4), 'Helvetica-Bold'),
            ('FONTSIZE', (0, 0), (-1, 3), 10),
            ('FONTSIZE', (0, 4), (-1, 4), 14),
            ('LINEABOVE', (0, 4), (-1, 4), 2, colors.HexColor('#006994')),
            ('TEXTCOLOR', (0, 4), (-1, 4), colors.HexColor('#006994')),
        ]))
        story.append(totals_table)
        story.append(Spacer(1, 0.5 * inch))
        
        # Footer
        footer_text = """
        <para align=center>
        <b>Thank you for your purchase!</b><br/>
        Each bikini is handcrafted with love.<br/>
        Questions? Contact us at """ + self.business_email + """
        </para>
        """
        story.append(Paragraph(footer_text, styles['Normal']))
        
        # Build PDF
        doc.build(story)
        
        return filename
    
    def generate_invoice(self, order, invoice_number=None):
        """Generate an invoice (similar to receipt but with invoice formatting)"""
        if not invoice_number:
            invoice_number = f"INV-{order.order_number}"
        
        filename = f"invoices/invoice_{invoice_number}.pdf"
        os.makedirs('invoices', exist_ok=True)
        
        # Similar to receipt but with "INVOICE" heading and due date info
        doc = SimpleDocTemplate(filename, pagesize=letter)
        story = []
        styles = getSampleStyleSheet()
        
        # ... (Similar structure to receipt with invoice-specific modifications)
        
        doc.build(story)
        return filename
