# email.py

import logging
from django.core.mail import send_mail, get_connection
from django.template.loader import render_to_string
from django.utils.http import urlsafe_base64_encode
from django.utils.encoding import force_bytes
from django.contrib.auth.tokens import default_token_generator
from django.conf import settings

logger = logging.getLogger(__name__)

def send_confirmation_email(user):
    try:
        token = default_token_generator.make_token(user)
        uid = urlsafe_base64_encode(force_bytes(user.pk))
        confirm_url = f"{settings.BASE_URL}/api/confirm/{uid}/{token}/"
        
        subject = 'Confirm Your Email'
        message = render_to_string('confirmation_email.html', {
            'user': user,
            'confirm_url': confirm_url,
        })
        
        # Use custom connection with unverified SSL context
        connection = get_connection()
        connection.ssl_context = settings.EMAIL_SSL_CONTEXT
        
        send_mail(subject, message, settings.DEFAULT_FROM_EMAIL, [user.email], connection=connection)
        logger.info(f'Confirmation email sent to {user.email}')
    except Exception as e:
        logger.error(f'Error sending confirmation email: {e}')
