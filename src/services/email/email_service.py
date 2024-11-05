import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText

from starlette.background import BackgroundTasks

from core.logger import logger
from core.settings import settings


class EmailService:
    def __init__(
            self,
            smtp_server: str,
            smtp_port: int,
            smtp_user: str,
            smtp_password: str,
    ) -> None:
        self.smtp_server = smtp_server
        self.smtp_port = smtp_port
        self.smtp_user = smtp_user
        self.smtp_password = smtp_password
        self.background_tasks = BackgroundTasks()

    async def _start_tasks(self) -> None:
        logger.info("[EmailService]: Starting background tasks...")
        await self.background_tasks()

    @staticmethod
    def render_template(name: str, context: dict) -> str:
        return settings.templates.get_template(name=name).render(**context)

    @staticmethod
    def build_email(
            to_email: str,
            from_email: str,
            subject: str,
            html_content: str,
            text_content: str | None = None
    ) -> MIMEMultipart:
        msg = MIMEMultipart()
        msg["From"] = from_email
        msg["To"] = to_email
        msg["Subject"] = subject

        if text_content:
            msg.attach(MIMEText(text_content, "plain"))
        msg.attach(MIMEText(html_content, "html"))
        return msg

    async def send_confirmation_email(
            self,
            to_email: str,
            from_email: str,
            subject: str,
            code: str,
    ) -> None:
        html_content = self.render_template(
            "mail_confirmation.html",
            {
                "code": code
            }
        )
        msg = self.build_email(
            to_email,
            from_email,
            subject,
            html_content
        )
        self.background_tasks.add_task(self._send_email, msg=msg)
        await self._start_tasks()

    def _send_email(self, msg: MIMEMultipart) -> None:
        try:
            with smtplib.SMTP(self.smtp_server, self.smtp_port) as server:
                server.starttls()
                server.login(self.smtp_user, self.smtp_password)
                server.send_message(msg)
                logger.info("[EmailService]: Email sent successfully!")
        except Exception as e:
            logger.error(f"[EmailService]: Failed to send email: {e}")
