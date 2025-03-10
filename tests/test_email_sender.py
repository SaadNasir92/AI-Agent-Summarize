# tests/test_email_sender.py
import os
import smtplib
import pytest
from email_sender import send_email


class DummySMTP:
    def __init__(self, server, port):
        self.server = server
        self.port = port
        self.logged_in = False
        self.sent_emails = []

    def starttls(self):
        pass

    def login(self, sender_email, sender_password):
        self.logged_in = True

    def sendmail(self, sender_email, to_email, message):
        self.sent_emails.append((sender_email, to_email, message))

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        pass


@pytest.fixture(autouse=True)
def set_env(monkeypatch):
    monkeypatch.setenv("SMTP_SERVER", "dummy.smtp.com")
    monkeypatch.setenv("SMTP_PORT", "587")
    monkeypatch.setenv("SENDER_EMAIL", "dummy@example.com")
    monkeypatch.setenv("SENDER_PASSWORD", "dummy_password")


def test_send_email(monkeypatch):
    dummy_smtp = DummySMTP("dummy.smtp.com", 587)
    monkeypatch.setattr(smtplib, "SMTP", lambda server, port: dummy_smtp)
    send_email("recipient@example.com", "Test Subject", "Test Body")
    # Check that login was performed.
    assert dummy_smtp.logged_in is True
    # Check that an email was sent.
    assert len(dummy_smtp.sent_emails) == 1
    sender, recipient, message = dummy_smtp.sent_emails[0]
    assert sender == "dummy@example.com"
    assert recipient == "recipient@example.com"
    assert "Test Subject" in message
