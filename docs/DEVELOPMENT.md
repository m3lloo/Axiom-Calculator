# Development Guide

## Setup for Development

### Prerequisites
- Python 3.9+
- Git
- Virtual environment support

### Initial Setup

```bash
# Clone repository
cd "Calculator App"

# Create virtual environment
python -m venv venv

# Activate (Windows)
venv\Scripts\activate

# Activate (macOS/Linux)
source venv/bin/activate

# Install development dependencies
pip install -r requirements-dev.txt
```

## Code Style & Standards

### Formatting
```bash
# Format all Python files
black app.py config.py test_app.py

# Check formatting without changes
black --check app.py
```

### Linting
```bash
# Run flake8
flake8 app.py config.py test_app.py

# Run pylint for detailed analysis
pylint app.py
```

### Type Hints
- Add type hints to all function signatures
- Use `typing` module for complex types
- Example:
  ```python
  def calculate(expression: str) -> Dict[str, str]:
      """Docstring"""
      pass
  ```

## Testing

### Running Tests
```bash
# Run all tests
pytest

# Run with coverage
pytest --cov=. --cov-report=html

# Run specific file
pytest test_app.py -v

# Run specific test
pytest test_app.py::TestCalculator::test_simple_calculation -v
```

### Writing Tests
1. Create test functions prefixed with `test_`
2. Use fixtures for setup
3. Use descriptive assertion messages
4. Test both success and failure cases

Example:
```python
def test_valid_calculation(client):
    """Test that valid calculations return correct results"""
    response = client.post('/calculate',
        json={'expression': '2+2'},
        content_type='application/json'
    )
    assert response.status_code == 200
    data = json.loads(response.data)
    assert data['result'] == '4'
```

## Git Workflow

### Commit Messages
Format: `[TYPE] Brief description`

Types:
- `feat:` New feature
- `fix:` Bug fix
- `refactor:` Code refactoring
- `test:` Test additions/changes
- `docs:` Documentation
- `style:` Code style (no logic change)
- `perf:` Performance improvement

Example:
```
feat: add localStorage persistence for history
fix: handle edge case in division by zero
test: add comprehensive test suite
```

### Branching
- `main` - Production ready code
- `develop` - Development branch
- `feature/description` - Feature branches
- `bugfix/description` - Bug fix branches

## Frontend Development

### CSS Changes
- Update `static/css/style.css`
- Keep neon aesthetic consistent
- Test responsive design (mobile, tablet, desktop)
- Maintain accessibility contrast ratios

### JavaScript Changes
- Update `static/js/main.js`
- Keep functions focused and pure where possible
- Add JSDoc comments for complex logic
- Test keyboard events and browser compatibility

### HTML Changes
- Update `templates/index.html`
- Maintain semantic HTML structure
- Keep accessibility features (ARIA labels)
- Update corresponding JavaScript selectors

## Backend Development

### Adding Routes
1. Follow existing error handling patterns
2. Validate all inputs
3. Add logging
4. Include type hints
5. Write tests

Example:
```python
@app.route('/new-endpoint', methods=['POST'])
def new_endpoint() -> Any:
    """Description of what endpoint does"""
    try:
        data = request.get_json()
        # Validate input
        if not data:
            return jsonify({'error': 'Invalid JSON'}), 400
        # Process
        result = process(data)
        logger.info(f"Result: {result}")
        return jsonify({'result': result}), 200
    except Exception as e:
        logger.error(f"Error: {e}")
        return jsonify({'error': 'Server error'}), 500
```

### Adding Functions
1. Add type hints
2. Add docstring
3. Add logging for important operations
4. Write corresponding tests

Example:
```python
def validate_input(value: str) -> Optional[str]:
    """Validate user input and return error message if invalid.
    
    Args:
        value: User input to validate
        
    Returns:
        Error message if invalid, None if valid
    """
    if not value:
        return "Value cannot be empty"
    if len(value) > 500:
        return "Value too long"
    return None
```

## Docker Development

### Building Local Image
```bash
docker build -t axiom-calc:dev .
```

### Running with docker-compose
```bash
# Development mode
docker-compose -f docker-compose.yml up

# Rebuild image
docker-compose build --no-cache

# Run with shell
docker-compose exec axiom-calc /bin/bash
```

## Database/Storage (Future)

Currently uses browser localStorage. For future database integration:
1. Consider SQLite for development
2. Use PostgreSQL for production
3. Implement ORM (SQLAlchemy) for database abstraction
4. Add database migrations (Alembic)

## Debugging

### Flask Debug Mode
Already enabled in development. Access at `http://localhost:5000`

### Python Debugging
```python
# Add breakpoint in code
import pdb; pdb.set_trace()

# Or use Python 3.7+
breakpoint()
```

### Browser DevTools
- F12 to open DevTools
- Console tab for JavaScript errors
- Network tab to inspect API calls
- Application tab to view localStorage

### Logging
Adjust logging level in `app.py`:
```python
logging.basicConfig(level=logging.DEBUG)  # Show all messages
logging.basicConfig(level=logging.WARNING)  # Show warnings only
```

## Performance Optimization

### Frontend
- Profile with Chrome DevTools
- Monitor localStorage usage
- Check CSS/JS bundle sizes (future minification)

### Backend
- Profile with `cProfile`:
  ```bash
  python -m cProfile -s cumulative app.py
  ```
- Monitor response times
- Check database queries (if applicable)

## Security Considerations

1. **Input Validation**: Always validate and sanitize
2. **Environment Variables**: Never commit secrets to git
3. **Dependencies**: Keep updated with `pip check`
4. **Logging**: Don't log sensitive information
5. **HTTPS**: Use in production with valid certificates

## Documentation

### Updating Docs
1. Keep README.md current
2. Add docstrings to functions
3. Document breaking changes
4. Update this file for new processes

### Docstring Format
```python
def function_name(param1: type1, param2: type2) -> ReturnType:
    """Brief description.
    
    Longer description if needed.
    
    Args:
        param1: Description of param1
        param2: Description of param2
        
    Returns:
        Description of return value
        
    Raises:
        ValueError: When input is invalid
        
    Example:
        >>> function_name("test", 42)
        result
    """
```

## Troubleshooting

### Import Errors
```bash
# Ensure virtual environment is activated
# Reinstall dependencies
pip install -r requirements-dev.txt
```

### Port in Use
```bash
# Find process using port 5000
lsof -i :5000

# Kill process (macOS/Linux)
kill -9 <PID>

# Or change port in .env
```

### Test Failures
1. Check if all dependencies installed
2. Run `pytest --tb=short` for detailed errors
3. Check database/file permissions
4. Clear pytest cache: `pytest --cache-clear`

## Release Process

1. Update version in `pyproject.toml`
2. Update CHANGELOG (if created)
3. Create git tag: `git tag v2.4.0`
4. Push changes and tag
5. Create GitHub release with notes

## Useful Commands Reference

```bash
# Activate environment
source venv/bin/activate  # macOS/Linux
venv\Scripts\activate     # Windows

# Install dependencies
pip install -r requirements-dev.txt

# Format code
black app.py config.py test_app.py

# Lint code
flake8 app.py

# Run tests
pytest -v

# Run tests with coverage
pytest --cov=. --cov-report=html

# Run app
python app.py

# Run with gunicorn
gunicorn -w 4 -b 0.0.0.0:5000 app:app

# Docker
docker-compose up -d
docker-compose down
docker-compose logs -f
```

---

For questions or issues during development, check the main README.md or create an issue.
