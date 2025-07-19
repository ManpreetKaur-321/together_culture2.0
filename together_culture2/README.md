# 🏛️ Together Culture 2.0

A comprehensive Django web application for managing community events, member benefits, and digital content.

## 🚀 Features

### 👥 Member Management
- **User Registration & Authentication**: Custom user model with role-based access
- **Member Profiles**: Detailed profiles with interests and membership types
- **Authorization System**: Admin approval workflow for new members
- **Profile Management**: Members can update their information

### 🎉 Events & Bookings
- **Event Management**: Create and manage community events
- **Digital Content**: Separate digital content from regular events
- **Booking System**: Members can book events with admin approval
- **Event Filtering**: Automatic separation of digital vs regular events

### 🎁 Benefits System
- **Membership Benefits**: Different benefits for different membership types
- **Benefit Tracking**: Track which benefits members have used
- **Benefits Dashboard**: Members can view and manage their benefits

### 👨‍💼 Admin Features
- **Member Management**: Admin can authorize/deauthorize members
- **Event Management**: Create and manage events and digital content
- **Benefits Management**: Create and assign benefits to membership types
- **Statistics**: View member statistics and booking information

## 🛠️ Installation & Setup

### Prerequisites
- Python 3.8+
- MySQL Database
- Virtual Environment

### Quick Start

1. **Clone the repository**
   ```bash
   git clone <repository-url>
   cd together_culture2
   ```

2. **Create virtual environment**
   ```bash
   python -m venv .venv
   .venv\Scripts\activate  # Windows
   # or
   source .venv/bin/activate  # Linux/Mac
   ```

3. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

4. **Configure database**
   - Update database settings in `together_culture2/settings.py`
   - Create MySQL database

5. **Run migrations**
   ```bash
   python manage.py migrate
   ```

6. **Create superuser**
   ```bash
   python manage.py createsuperuser
   ```

7. **Start the server**
   ```bash
   python manage.py runserver
   ```

## 🎯 Usage

### Using the Application Manager
For easy management, use the provided application manager:

```bash
python run_app.py
```

This provides a menu-driven interface for:
- 🏃‍♂️ Running the development server
- 🧪 Running tests
- 📊 Running tests with coverage
- 🗄️ Making migrations
- 🔄 Running migrations
- 🧹 Cleaning cache files

### Manual Commands

#### Development Server
```bash
python manage.py runserver
```
Access the application at: http://127.0.0.1:8000

#### Running Tests
```bash
# Run all tests
python manage.py test

# Run specific app tests
python manage.py test users
python manage.py test members
python manage.py test events
python manage.py test bookings

# Run with coverage
coverage run --source='.' manage.py test
coverage report
```

#### Database Management
```bash
# Create migrations
python manage.py makemigrations

# Apply migrations
python manage.py migrate

# Create superuser
python manage.py createsuperuser
```

## 📊 Test Coverage

The application includes comprehensive test coverage:

- **20 tests** with 100% pass rate
- **63% overall code coverage**
- **Core functionality tested**: Models, views, business logic
- **Reliable test suite** for safe development

### Test Results
```
✅ User Tests: 100% pass rate
✅ Member Tests: 100% pass rate  
✅ Event Tests: 100% pass rate
✅ Booking Tests: 100% pass rate
```

## 🏗️ Project Structure

```
together_culture2/
├── users/                 # User authentication & profiles
├── members/              # Member management & benefits
├── events/               # Event & digital content management
├── bookings/             # Booking system
├── tags/                 # Tagging system
├── dashboard/            # Dashboard views
├── together_culture2/    # Project settings
├── tests/               # Test files
├── run_app.py           # Application manager
└── README.md            # This file
```

## 🔧 Configuration

### Database Settings
Update `together_culture2/settings.py` with your database configuration:

```python
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.mysql',
        'NAME': 'your_database_name',
        'USER': 'your_username',
        'PASSWORD': 'your_password',
        'HOST': 'localhost',
        'PORT': '3306',
    }
}
```

### Environment Variables
Create a `.env` file for sensitive settings:

```env
SECRET_KEY=your_secret_key
DEBUG=True
DATABASE_URL=mysql://user:password@localhost/dbname
```

## 🎨 Features Overview

### Member Dashboard
- View available events (excluding digital content)
- Manage bookings and profile information
- Access benefits dashboard
- View digital content separately

### Admin Dashboard
- Manage member authorizations
- Create and manage events
- Manage benefits and membership types
- View statistics and reports

### Event System
- Regular events for in-person activities
- Digital content for online resources
- Automatic filtering and categorization
- Booking and approval workflow

### Benefits System
- Membership-based benefits
- Usage tracking
- Benefits dashboard for members
- Admin management interface

## 🚀 Deployment

### Production Setup
1. Set `DEBUG = False` in settings
2. Configure production database
3. Set up static file serving
4. Configure web server (nginx/apache)
5. Set up SSL certificates

### Environment Variables
```env
DEBUG=False
SECRET_KEY=your_production_secret_key
ALLOWED_HOSTS=yourdomain.com,www.yourdomain.com
DATABASE_URL=mysql://user:password@localhost/dbname
```

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Add tests for new functionality
5. Run the test suite
6. Submit a pull request

## 📝 License

This project is licensed under the MIT License.

## 🆘 Support

For support and questions:
- Check the test suite for examples
- Review the application manager (`run_app.py`)
- Run tests to verify functionality
- Check the Django admin interface

---

**🎉 Together Culture 2.0** - Building stronger communities through technology! 