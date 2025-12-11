import sys
import imaplib
import email
from email.header import decode_header
import time
from PyQt5.QtCore import Qt, QTimer
from PyQt5.QtWidgets import QApplication, QMainWindow, QWidget, QVBoxLayout, QLabel

class NewsFeedApp(QMainWindow):
    def __init__(self):
        super().__init__()

        self.init_ui()
        self.fetch_news()

    def init_ui(self):
        self.setWindowTitle("Government News Feed")
        self.setGeometry(100, 100, 800, 600)

        central_widget = QWidget(self)
        self.setCentralWidget(central_widget)

        layout = QVBoxLayout(central_widget)

        self.banner = QLabel("Government News Feed", self)
        self.banner.setAlignment(Qt.AlignCenter)
        self.banner.setStyleSheet("background-color: green; color: white; font-size: 20px; padding: 10px;")
        layout.addWidget(self.banner)

        self.news_label = QLabel("No news available.", self)
        self.news_label.setAlignment(Qt.AlignLeft)
        self.news_label.setStyleSheet("font-size: 16px; margin: 10px;")
        layout.addWidget(self.news_label)

        self.news_items = []
        self.news_index = -1

        self.timer = QTimer(self)
        self.timer.timeout.connect(self.show_next_news)
        self.timer.start(6000)  # Display each news item for 6 seconds

        self.show()

    def fetch_news(self):
        # Email account settings (update these with your own information)
        email_username = "your_email@example.com"
        email_password = "your_email_password"
        imap_server = "imap.example.com"
        imap_port = 993

        # Connect to the IMAP server
        mail = imaplib.IMAP4_SSL(imap_server, imap_port)

        # Login to the email account
        mail.login(email_username, email_password)

        # Select the mailbox you want to check (e.g., "INBOX")
        mailbox = "INBOX"
        mail.select(mailbox)

        # Calculate the date for 3 days ago
        from_date = (time.time() - 3 * 24 * 60 * 60)  # 3 days ago in seconds

        # Search for email messages with the subject containing "news" from the last 3 days
        search_criteria = '(SUBJECT "news" SINCE {0})'.format(time.strftime("%d-%b-%Y", time.gmtime(from_date)))
        status, email_ids = mail.search(None, search_criteria)

        if status == 'OK':
            email_ids = email_ids[0].split()  # Split email IDs into a list

            if email_ids:
                for email_id in email_ids:
                    status, email_data = mail.fetch(email_id, '(RFC822)')
                    if status == 'OK':
                        msg = email.message_from_bytes(email_data[0][1])
                        subject, encoding = decode_header(msg["Subject"])[0]
                        if isinstance(subject, bytes):
                            subject = subject.decode(encoding or "utf-8")
                        content = ""
                        if msg.is_multipart():
                            for part in msg.walk():
                                if part.get_content_type() == "text/plain":
                                    content = part.get_payload(decode=True).decode("utf-8")
                        else:
                            content = msg.get_payload(decode=True).decode("utf-8")

                        self.news_items.append((subject, content))

            # Logout from the email account
            mail.logout()

    def show_next_news(self):
        self.news_index = (self.news_index + 1) % len(self.news_items)
        subject, content = self.news_items[self.news_index]
        self.banner.setText(subject)
        self.news_label.setText(content)

if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = NewsFeedApp()
    sys.exit(app.exec_())
