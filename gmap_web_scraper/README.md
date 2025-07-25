# Google Maps Web Scraper

A Django-based web application that scrapes Google Maps search results for businesses and locations, providing detailed information including ratings, reviews, contact details, and distance calculations from a specified starting point.

## 🚀 Features

- **Google Maps Scraping**: Automatically scrapes business listings from Google Maps
- **Detailed Information Extraction**: Collects business name, rating, review count, category, address, phone number, and operating status
- **Distance Calculation**: Calculates driving distance and time from a specified starting point
- **Interactive Web Interface**: User-friendly web interface with dark/light theme toggle
- **Data Export**: Results can be exported to CSV and Excel formats
- **Database Storage**: All scraped data is stored in a PostgreSQL database
- **Responsive Design**: Modern, mobile-friendly interface

## 📋 Prerequisites

- Python 3.8+
- PostgreSQL database
- Google Chrome browser (for web scraping)
- Git

## 🛠️ Installation

### 1. Clone the Repository
```bash
git clone https://github.com/noufanvp/GScrapper.git
cd GScrapper
```

### 2. Create Virtual Environment
```bash
python -m venv gscraper_env
source gscraper_env/bin/activate  # On Windows: gscraper_env\Scripts\activate
```

### 3. Install Dependencies
```bash
pip install -r requirements.txt
```

### 4. Database Setup

#### PostgreSQL Installation (Ubuntu/Debian)
```bash
sudo apt update
sudo apt install postgresql postgresql-contrib
```

#### Create Database and User
```bash
sudo -u postgres psql
CREATE DATABASE gscraper_db;
CREATE USER your_username WITH PASSWORD 'your_password';
ALTER ROLE your_username SET client_encoding TO 'utf8';
ALTER ROLE your_username SET default_transaction_isolation TO 'read committed';
ALTER ROLE your_username SET timezone TO 'UTC';
GRANT ALL PRIVILEGES ON DATABASE gscraper_db TO your_username;
\q
```

### 5. Environment Configuration

Create a `.env` file in the project root (copy from `.env.example`):
```bash
cp .env.example .env
```

Then edit the `.env` file with your actual values:
```bash
SECRET_KEY=your-actual-secret-key-here
DEBUG=True
DB_NAME=gscraper_db
DB_USER=your_username
DB_PASSWORD=your_password
DB_HOST=localhost
DB_PORT=5432
```

### 6. Run Migrations
```bash
python manage.py makemigrations
python manage.py migrate
```

### 7. Create Superuser (Optional)
```bash
python manage.py createsuperuser
```

### 8. Run the Development Server
```bash
python manage.py runserver
```

Visit `http://127.0.0.1:8000/` to access the application.

## 🎯 Usage

1. **Access the Web Interface**: Open your browser and navigate to the application URL
2. **Enter Search Parameters**:
   - **Search Keyword**: Enter what you're looking for (e.g., "restaurants near calicut")
   - **Starting Point**: Enter your starting location for distance calculations
3. **Start Scraping**: Click the "Start Scraping" button
4. **View Results**: The results will be displayed in a sortable table with all extracted information
5. **Export Data**: Use the export buttons to download results in CSV or Excel format

## 📊 Data Collected

For each business/location, the scraper collects:

- Business Name
- Rating (1-5 stars)
- Number of Reviews
- Business Category
- Full Address
- Phone Number
- Operating Status (Open/Closed)
- Distance from Starting Point
- Estimated Travel Time
- Google Maps URL

## 🏗️ Project Structure

```
gmap_web_scraper/
├── manage.py
├── requirements.txt
├── .gitignore
├── gmap_web_scraper/
│   ├── __init__.py
│   ├── settings.py
│   ├── urls.py
│   ├── wsgi.py
│   └── asgi.py
└── gscraper/
    ├── __init__.py
    ├── admin.py
    ├── apps.py
    ├── models.py
    ├── views.py
    ├── urls.py
    ├── forms.py
    ├── scraper_logic.py
    ├── migrations/
    ├── static/
    │   ├── css/
    │   └── js/
    └── templates/
```

## 🔧 Configuration

### Chrome Driver
The application uses `undetected-chromedriver` which automatically handles Chrome driver management. Ensure you have Google Chrome installed on your system.

### Database Configuration
The application is configured to use PostgreSQL. You can modify the database settings in `settings.py` if you prefer a different database.

### Scraping Parameters
You can adjust scraping parameters in `gscraper/scraper_logic.py`:
- Maximum scroll attempts
- Wait times between actions
- Element selectors (if Google Maps changes its structure)

## ⚠️ Important Notes

- **Rate Limiting**: Be respectful of Google's servers. The scraper includes delays between requests
- **Terms of Service**: Ensure your usage complies with Google's Terms of Service
- **Chrome Updates**: Google Maps structure may change; the scraper might need updates accordingly
- **Headless Mode**: You can enable headless mode in `scraper_logic.py` for production use

## 🚨 Troubleshooting

### Common Issues

1. **Chrome Driver Issues**:
   ```bash
   pip install --upgrade undetected-chromedriver
   ```

2. **Database Connection Errors**:
   - Verify PostgreSQL is running
   - Check database credentials
   - Ensure database exists

3. **Selenium Timeouts**:
   - Increase wait times in `scraper_logic.py`
   - Check internet connection
   - Verify Google Maps accessibility

4. **Missing Dependencies**:
   ```bash
   pip install -r requirements.txt --upgrade
   ```

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/AmazingFeature`)
3. Commit your changes (`git commit -m 'Add some AmazingFeature'`)
4. Push to the branch (`git push origin feature/AmazingFeature`)
5. Open a Pull Request

## 📄 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## ⚖️ Legal Disclaimer

This tool is for educational and research purposes only. Users are responsible for ensuring their usage complies with Google's Terms of Service and applicable laws. The developers are not responsible for any misuse of this tool.

## 📞 Support

If you encounter any issues or have questions, please:
1. Check the troubleshooting section
2. Search existing issues on GitHub
3. Create a new issue with detailed information

## 🙏 Acknowledgments

- [Selenium](https://selenium-python.readthedocs.io/) for web automation
- [undetected-chromedriver](https://github.com/ultrafunkamsterdam/undetected-chromedriver) for Chrome driver management
- [Django](https://www.djangoproject.com/) for the web framework
- [pandas](https://pandas.pydata.org/) for data processing

---

**⭐ Star this repository if you find it helpful!**
