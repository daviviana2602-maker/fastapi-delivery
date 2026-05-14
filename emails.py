import resend

from config import RESEND_API_KEY, FRONT_URL
resend.api_key = RESEND_API_KEY



def reset_email(to_email: str, token: str):

    reset_link = f"{FRONT_URL}/pages/reset-senha.html?token={token}"

    resend.Emails.send({
        "from": "Vossodelivery <no-reply@vossodelivery.com.br>",
        "to": [to_email],
        "subject": "Recuperação de senha",
        "html": f"""
            <h1>Recuperação de senha</h1>
            <a href="{reset_link}">
                Redefinir senha
            </a>
        """
    })
    
    
    
def verification_email(to_email: str, token: str):
 
    verify_link = f"{FRONT_URL}/pages/verify-email.html?token={token}"

    resend.Emails.send({
        "from": "Vossodelivery <no-reply@vossodelivery.com.br>",
        "to": [to_email],
        "subject": "Confirme seu email",
        "html": f"""
            <h1>Confirme sua conta</h1>
            <a href="{verify_link}">
                Ativar conta
            </a>
        """
    })