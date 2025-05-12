# WhatsApp Scheduler Pro

A powerful Python-based automation tool for scheduling WhatsApp messages, reminders, and broadcasts. Built with Flask and Twilio API, it offers a user-friendly web interface for managing your WhatsApp communications.

## Features

- Schedule one-time and recurring messages
- Upload contacts via CSV
- Real-time message status tracking
- User authentication
- Responsive web interface
- Message templates
- End-to-end encryption

## Prerequisites

- Python 3.8 or higher
- Twilio account with WhatsApp API access
- SQLite (included with Python)

## Installation

1. Clone the repository:
```bash
git clone https://github.com/Kratos3213/whatsapp-scheduler-pro.git
cd whatsapp-scheduler-pro
```

2. Create a virtual environment and activate it:
```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

3. Install the required packages:
```bash
pip install -r requirements.txt
```

4. Create a `.env` file in the project root with your Twilio credentials:
```
TWILIO_ACCOUNT_SID=your_account_sid
TWILIO_AUTH_TOKEN=your_auth_token
TWILIO_WHATSAPP_NUMBER=your_twilio_whatsapp_number
SECRET_KEY=your_flask_secret_key
```

## Running the Application

1. Initialize the database:
```bash
flask db init
flask db migrate
flask db upgrade
```

2. Start the Flask development server:
```bash
python app.py
```

3. Open your browser and navigate to `http://localhost:5000`

## Usage

1. Register a new account or log in
2. Navigate to the dashboard
3. Schedule a new message:
   - Enter recipient's phone number
   - Compose your message
   - Set the delivery time
   - Choose between one-time or recurring message
4. Upload contacts via CSV for bulk messaging
5. Monitor message status in the dashboard

## CSV Format for Contact Upload

The CSV file should have the following columns:
- phone_number (required): Recipient's phone number with country code
- name (optional): Recipient's name
- group (optional): Contact group/category

Example:
```csv
phone_number,name,group
+1234567890,John Doe,Family
+1987654321,Jane Smith,Friends
```

## Contributing

1. Fork the repository
2. Create a new branch
3. Make your changes
4. Submit a pull request

## License

This project is licensed under the MIT License - see the LICENSE file for details.

## Security

- All messages are encrypted end-to-end
- User authentication required for all operations
- Secure storage of credentials
- Regular security updates

## Support

For support, please open an issue in the GitHub repository or contact the maintainers. 