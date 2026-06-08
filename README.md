# AXIOM CALC - Retro-Futuristic Calculator

[![Python 3.9+](https://img.shields.io/badge/Python-3.9%2B-blue)](https://python.org)
[![Flask 2.3+](https://img.shields.io/badge/Flask-2.3%2B-green)](https://flask.palletsprojects.com)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](LICENSE)

A retro-futuristic scientific calculator web application with unit conversions, calculation history, and persistent storage.

## ✨ Features

### Calculator
- ✅ **Full Scientific Functions**: sin, cos, tan, sqrt, log, ln, absolute value, ceiling
- ✅ **Live Preview**: Real-time expression preview as you type
- ✅ **Basic & Scientific Modes**: Toggle between basic and advanced functions
- ✅ **Keyboard Support**: Full keyboard navigation and shortcuts
- ✅ **Error Handling**: Comprehensive error messages for invalid expressions

### Converter
- ✅ **Multiple Categories**: Length, Weight, Temperature, Speed, Area, Data
- ✅ **30+ Conversions**: Pre-configured common unit conversions
- ✅ **Real-time Results**: Instant conversion as you type values

### History
- ✅ **Persistent Storage**: History saved to browser localStorage
- ✅ **Recall Calculations**: Click any history item to reuse the result
- ✅ **Clear History**: Remove calculation history with confirmation
- ✅ **100 Item Limit**: Maintains last 100 calculations

### Accessibility
- ✅ **ARIA Labels**: Full semantic HTML with ARIA roles and labels
- ✅ **Keyboard Navigation**: Complete keyboard support for all functions
- ✅ **Screen Reader Support**: Friendly labels for assistive technologies
- ✅ **Color Contrast**: WCAG compliant contrast ratios

### Security
- ✅ **Input Validation**: Strict validation of all expressions and inputs
- ✅ **Sandboxed Evaluation**: Safe expression evaluation with restricted namespace
- ✅ **Security Headers**: XSS, clickjacking, and content-type protection
- ✅ **Rate Limiting Ready**: Configuration for rate limiting support

## 📁 Project Structure

```
Calculator App/
├── app.py                 # Flask backend with logging & error handling
├── config.py             # Configuration management (dev/prod/test)
├── requirements.txt      # Production dependencies
├── requirements-dev.txt  # Development dependencies
├── pyproject.toml        # Project metadata and build configuration
├── test_app.py          # Comprehensive pytest test suite
├── Dockerfile           # Docker containerization
├── docker-compose.yml   # Multi-container orchestration
├── .env.example         # Environment variables template
├── .gitignore          # Git ignore rules
├── .flake8             # Linting configuration
├── README.md           # This file
├── static/
│   ├── css/
│   │   └── style.css     # Neon UI styling (800+ lines)
│   └── js/
│       └── main.js       # Frontend logic with localStorage (400+ lines)
└── templates/
    └── index.html        # HTML template with accessibility features
```

## 🚀 Quick Start

### Local Development

1. **Clone and setup**:
   ```bash
   cd "Calculator App"
   python -m venv venv
   source venv/Scripts/activate  # Windows
   ```

2. **Install dependencies**:
   ```bash
   pip install -r requirements-dev.txt
   ```

3. **Configure environment**:
   ```bash
   cp .env.example .env
   # Edit .env if needed (optional for development)
   ```

4. **Run development server**:
   ```bash
   python app.py
   ```
   Visit http://localhost:5000

### Docker Deployment

1. **Build and run**:
   ```bash
   docker-compose up -d
   ```

2. **Access application**:
   Visit http://localhost:5000

3. **View logs**:
   ```bash
   docker-compose logs -f axiom-calc
   ```

## 📚 Usage

### Calculator Tab
- **Type numbers**: Use keyboard or buttons
- **Operations**: +, -, ×, ÷, ^, %, ()
- **Scientific**: Toggle "SCIENTIFIC" mode for advanced functions
- **Submit**: Press Enter or click =
- **Clear**: Press Esc or click AC
- **Copy**: Press C or Ctrl+C to copy result

### Converter Tab
- **Select Category**: Choose from Length, Weight, Temperature, Speed, Area, Data
- **Pick Conversion**: Click desired conversion button
- **Enter Value**: Type in left input field
- **Result Appears**: Automatically converts in real-time

### History Tab
- **View Calculations**: Scroll through past calculations
- **Recall**: Click any item to use result in calculator
- **Clear**: Click "CLEAR LOG" to remove all history

## ⌨️ Keyboard Shortcuts

| Key | Action |
|-----|--------|
| `0-9`, `.` | Input numbers |
| `+`, `-`, `*`, `/` | Operations |
| `(`, `)` | Parentheses |
| `^`, `%` | Power, percent |
| `Enter` | Calculate |
| `Backspace` | Delete last character |
| `Esc` | Clear all |
| `C` | Copy result |

## 🧪 Testing

```bash
# Run all tests
pytest

# With coverage
pytest --cov=. --cov-report=html

# Run specific test file
pytest test_app.py -v

# Run specific test class
pytest test_app.py::TestCalculator -v
```

## 📋 Code Quality

```bash
# Format code
black app.py config.py

# Lint code
flake8 app.py config.py test_app.py

# Type checking (if added)
pylint app.py
```

## 🔧 Configuration

### Environment Variables (`.env`)

```bash
# Flask
FLASK_ENV=development          # development, production, testing
FLASK_APP=app.py
SECRET_KEY=your-secret-key    # Change in production!

# Server
SERVER_HOST=0.0.0.0
SERVER_PORT=5000
```

### Config Modes

**Development** (default):
- Debug mode enabled
- Detailed error messages
- No rate limiting

**Production**:
- Debug mode disabled
- Generic error messages
- Rate limiting enabled
- Requires SECRET_KEY

**Testing**:
- Testing mode enabled
- Error suppression
- Rate limiting disabled

## 📦 Dependencies

### Production
- `flask>=2.3.0` - Web framework
- `python-dotenv>=1.0.0` - Environment variable management
- `gunicorn>=21.2.0` - Production WSGI server
- `werkzeug>=2.3.0` - WSGI toolkit

### Development
- `pytest>=7.4.0` - Testing framework
- `pytest-cov>=4.1.0` - Coverage reporting
- `black>=23.7.0` - Code formatter
- `flake8>=6.0.0` - Linter
- `pylint>=2.17.0` - Advanced linter

## 🐳 Docker

### Build Image
```bash
docker build -t axiom-calc:latest .
```

### Run Container
```bash
docker run -p 5000:5000 axiom-calc:latest
```

### With docker-compose
```bash
docker-compose up -d        # Start
docker-compose down         # Stop
docker-compose logs -f      # View logs
```

## 🔒 Security Features

- **Input Validation**: All inputs validated and sanitized
- **Expression Sandboxing**: Limited namespace for eval() execution
- **Security Headers**: X-Content-Type-Options, X-Frame-Options, X-XSS-Protection
- **Error Messages**: Generic messages in production, detailed in development
- **Logging**: All calculations and errors logged for monitoring
- **CORS Ready**: Easy to add CORS configuration

## 🎨 Frontend Features

- **Responsive Design**: Works on desktop, tablet, mobile
- **Dark Theme**: Easy on the eyes retro-futuristic interface
- **Animations**: Smooth transitions and effects
- **localStorage**: Automatic save/restore of history and mode
- **Progressive Enhancement**: Works without JavaScript

## 📊 Performance

- **Minified Assets**: Production-ready CSS/JS
- **Efficient Calculations**: Live preview without server calls
- **localStorage Caching**: Reduced server requests
- **Lazy Evaluation**: Expressions evaluated on-demand only

## 🚀 Production Deployment

### With Gunicorn
```bash
gunicorn -w 4 -b 0.0.0.0:5000 app:app
```

### With Nginx (reverse proxy)
```nginx
server {
    listen 80;
    server_name yourdomain.com;

    location / {
        proxy_pass http://127.0.0.1:5000;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
    }
}
```

### Environment Setup
```bash
export FLASK_ENV=production
export SECRET_KEY=$(python -c 'import secrets; print(secrets.token_hex(32))')
gunicorn -w 4 -b 0.0.0.0:5000 app:app
```

## 🐛 Troubleshooting

### Port Already in Use
```bash
# Change port in docker-compose.yml or .env
SERVER_PORT=8000
```

### localStorage Not Available
- Check browser privacy settings
- Ensure cookies/storage are enabled
- Clear browser cache if issues persist

### Expression Errors
- Check syntax: missing parentheses, operators
- Use live preview to debug
- Refer to keyboard shortcuts for supported operations

## 📝 Logging

Logs are output to console with the following format:
```
2024-01-15 10:30:45,123 - app - INFO - Calculation: 2+2 = 4
```

Configure logging level in `app.py` (line 11-15).

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/improvement`)
3. Make changes following code style (black, flake8)
4. Add/update tests for new functionality
5. Submit a pull request

## 📄 License

MIT License - See LICENSE file for details

## 🙏 Credits

- **Design Inspiration**: Retro-futuristic neon aesthetic
- **Framework**: Flask microframework
- **Fonts**: Google Fonts (Orbitron, Rajdhani, Share Tech Mono)

## 📞 Support

For issues, questions, or suggestions:
- Open an issue on GitHub
- Check existing documentation
- Review test cases for usage examples

---

**Version 2.4.0** - Last updated: 2024

# Axiom-Calculator
