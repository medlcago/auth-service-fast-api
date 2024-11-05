from services.email.email_service import EmailService


class EmailServiceProtocol:
    async def send_confirmation_email(
            self,
            to_email: str,
            from_email: str,
            subject: str,
            code: str
    ) -> None:
        ...
