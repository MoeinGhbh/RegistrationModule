from Auth.sendEmail import SendEmail
import pytest

class TestClass:

    @pytest.fixture
    def smtp_connection(self):
        import smtplib
        return smtplib.SMTP("smtp.gmail.com", 587, timeout=5)

    def test_sendEmail(self,smtp_connection):
        pass
