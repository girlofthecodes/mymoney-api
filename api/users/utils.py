from django.core.mail import EmailMessage, BadHeaderError
from django.conf import settings


class Util:
    @staticmethod
    def send_email(data):
        try: 
            
            email = EmailMessage(
                subject=data['email_subject'], 
                body=data['email_body'], 
                to=[data['to_email']], 
                from_email=settings.DEFAULT_FROM_EMAIL
            )
            
            email.send()
            return True #Indica que el envo fue exitoso   
        except BadHeaderError: 
            return False 
        except Exception as e:
            print(f"Ocurrió un error al enviar el correo: {e}")
            return False #Maneja cualquier otro error 