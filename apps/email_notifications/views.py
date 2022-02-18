from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from apps.contacts.models import Email
from apps.email_notifications.render_template import render_order_to_admin, render_order_to_buyer
from unine_engine.globals import EMAIL_HOST, EMAIL_HOST_PASSWORD, EMAIL_PORT, EMAIL_HOST_USER, SITE_NAME


def notify_admin_about_order(_order, request):
    try:
        html = render_order_to_admin(_order, request)
        send_html_mail('Новый заказ', html)
        return {'success': True}
    except Exception as e:
        print(str(e))
        return {'success': False, 'error': str(e)}


def notify_buyer_about_order(_order, request):
    try:
        html = render_order_to_buyer(_order, request)
        send_html_mail(f'Заказ от {_order.date}', html, _order.email)
        return {'success': True}
    except Exception as e:
        print(str(e))
        return {'success': False, 'error': str(e)}


def send_html_mail(subject, html, recipient=None):
    import smtplib
    if recipient is None:
        try:
            recipient = Email.objects.get(keyword='checkout').email
        except Exception as e:
            print('No *checkout* email found')
            return False
    else:
        try:
            text = ""
            msg = MIMEMultipart('alternative')
            part1 = MIMEText(text, 'plain')
            part2 = MIMEText(html, 'html')
            msg.attach(part1)
            msg.attach(part2)
            msg['Subject'] = subject

            smtpserver = smtplib.SMTP(EMAIL_HOST, EMAIL_PORT)
            smtpserver.ehlo()
            smtpserver.starttls()
            smtpserver.login(EMAIL_HOST_USER, EMAIL_HOST_PASSWORD)
            smtpserver.sendmail(SITE_NAME, recipient, msg.as_string())
            smtpserver.quit()
        except Exception as e:
            print(str(e))
    return True
