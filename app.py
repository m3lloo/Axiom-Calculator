from flask import Flask, render_template, request, jsonify
import math
import re
import logging
from typing import Dict, Tuple, Any, Optional
from config import config

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

app = Flask(__name__)
app.config.from_object(config)

# Unit conversion definitions
UNIT_CONVERSIONS: Dict[str, Tuple[str, callable]] = {
    # Length
    "km_to_mi": ("Kilometers → Miles", lambda x: x * 0.621371),
    "mi_to_km": ("Miles → Kilometers", lambda x: x * 1.60934),
    "m_to_ft": ("Meters → Feet", lambda x: x * 3.28084),
    "ft_to_m": ("Feet → Meters", lambda x: x * 0.3048),
    "cm_to_in": ("Centimeters → Inches", lambda x: x * 0.393701),
    "in_to_cm": ("Inches → Centimeters", lambda x: x * 2.54),
    # Weight
    "kg_to_lb": ("Kilograms → Pounds", lambda x: x * 2.20462),
    "lb_to_kg": ("Pounds → Kilograms", lambda x: x * 0.453592),
    "g_to_oz": ("Grams → Ounces", lambda x: x * 0.035274),
    "oz_to_g": ("Ounces → Grams", lambda x: x * 28.3495),
    # Temperature
    "c_to_f": ("Celsius → Fahrenheit", lambda x: x * 9/5 + 32),
    "f_to_c": ("Fahrenheit → Celsius", lambda x: (x - 32) * 5/9),
    "c_to_k": ("Celsius → Kelvin", lambda x: x + 273.15),
    "k_to_c": ("Kelvin → Celsius", lambda x: x - 273.15),
    # Speed
    "kmh_to_mph": ("km/h → mph", lambda x: x * 0.621371),
    "mph_to_kmh": ("mph → km/h", lambda x: x * 1.60934),
    "ms_to_kmh": ("m/s → km/h", lambda x: x * 3.6),
    "kmh_to_ms": ("km/h → m/s", lambda x: x / 3.6),
    # Area
    "sqm_to_sqft": ("m² → ft²", lambda x: x * 10.7639),
    "sqft_to_sqm": ("ft² → m²", lambda x: x * 0.0929),
    # Data
    "mb_to_gb": ("MB → GB", lambda x: x / 1024),
    "gb_to_tb": ("GB → TB", lambda x: x / 1024),
    "kb_to_mb": ("KB → MB", lambda x: x / 1024),
}


@app.after_request
def add_security_headers(response: Any) -> Any:
    """Add security headers to all responses"""
    response.headers['X-Content-Type-Options'] = 'nosniff'
    response.headers['X-Frame-Options'] = 'SAMEORIGIN'
    response.headers['X-XSS-Protection'] = '1; mode=block'
    return response


@app.route('/')
def index() -> Any:
    """Render the main calculator page"""
    try:
        conversions = {k: v[0] for k, v in UNIT_CONVERSIONS.items()}
        return render_template('index.html', conversions=conversions)
    except Exception as e:
        logger.error(f"Error rendering index: {e}")
        return jsonify({'error': 'Failed to load calculator'}), 500


def validate_expression(expression: str) -> Optional[str]:
    """Validate expression for safety and format"""
    if not expression or not isinstance(expression, str):
        return "Invalid expression"

    if len(expression) > 500:
        return "Expression too long (max 500 characters)"

    # Check for potentially dangerous patterns
    dangerous_patterns = [
        r'__',  # double underscore
        r'import',
        r'exec',
        r'open',
        r'system',
    ]

    for pattern in dangerous_patterns:
        if re.search(pattern, expression, re.IGNORECASE):
            return "Invalid expression: prohibited pattern"

    return None


@app.route('/calculate', methods=['POST'])
def calculate() -> Any:
    """Calculate mathematical expression"""
    try:
        data = request.get_json()
        if not data:
            return jsonify({'error': 'Invalid JSON'}), 400

        expression = str(data.get('expression', '')).strip()

        # Validate expression
        validation_error = validate_expression(expression)
        if validation_error:
            logger.warning(f"Invalid expression attempt: {expression}")
            return jsonify({'error': validation_error}), 400

        if not expression:
            return jsonify({'error': 'Empty expression'}), 400

        # Transform expression safely
        safe_expr = expression
        safe_expr = safe_expr.replace('^', '**')
        safe_expr = re.sub(r'sqrt\(', 'math.sqrt(', safe_expr)
        safe_expr = re.sub(r'sin\(', 'math.sin(math.radians(', safe_expr)
        safe_expr = re.sub(r'cos\(', 'math.cos(math.radians(', safe_expr)
        safe_expr = re.sub(r'tan\(', 'math.tan(math.radians(', safe_expr)
        safe_expr = re.sub(r'log\(', 'math.log10(', safe_expr)
        safe_expr = re.sub(r'ln\(', 'math.log(', safe_expr)
        safe_expr = re.sub(r'abs\(', 'abs(', safe_expr)
        safe_expr = re.sub(r'ceil\(', 'math.ceil(', safe_expr)
        safe_expr = re.sub(r'floor\(', 'math.floor(', safe_expr)

        # Fix closing parens for trig functions
        for fn in ['sin', 'cos', 'tan']:
            safe_expr = re.sub(
                r'math\.' + fn + r'\(math\.radians\(([^)]+)\)',
                r'math.' + fn + r'(math.radians(\1))',
                safe_expr
            )

        # Create safe namespace for eval
        allowed_names = {k: v for k, v in math.__dict__.items() if not k.startswith('_')}
        allowed_names['math'] = math
        allowed_names['abs'] = abs
        allowed_names['round'] = round

        # Evaluate
        result = eval(safe_expr, {"__builtins__": {}}, allowed_names)

        # Format result
        if isinstance(result, float):
            if result == int(result) and abs(result) < 1e15:
                result_str = str(int(result))
            else:
                result_str = f"{result:.10g}"
        else:
            result_str = str(result)

        logger.info(f"Calculation: {expression} = {result_str}")
        return jsonify({'result': result_str, 'expression': expression}), 200

    except ZeroDivisionError:
        logger.warning(f"Division by zero attempt")
        return jsonify({'error': 'Division by zero'}), 400
    except ValueError as e:
        logger.warning(f"Value error in calculation: {e}")
        return jsonify({'error': 'Invalid value in expression'}), 400
    except SyntaxError as e:
        logger.warning(f"Syntax error in expression: {e}")
        return jsonify({'error': 'Syntax error in expression'}), 400
    except Exception as e:
        logger.error(f"Calculation error: {e}")
        return jsonify({'error': 'Invalid expression'}), 400


@app.route('/convert', methods=['POST'])
def convert() -> Any:
    """Convert units"""
    try:
        data = request.get_json()
        if not data:
            return jsonify({'error': 'Invalid JSON'}), 400

        conversion_key = str(data.get('conversion', '')).strip()
        value = data.get('value', 0)

        # Validate inputs
        if not conversion_key:
            return jsonify({'error': 'Conversion type required'}), 400

        if conversion_key not in UNIT_CONVERSIONS:
            logger.warning(f"Unknown conversion attempt: {conversion_key}")
            return jsonify({'error': 'Unknown conversion'}), 400

        try:
            value = float(value)
        except (ValueError, TypeError):
            return jsonify({'error': 'Invalid value'}), 400

        try:
            label, conversion_fn = UNIT_CONVERSIONS[conversion_key]
            result = conversion_fn(value)

            # Validate result
            if not isinstance(result, (int, float)) or math.isnan(result) or math.isinf(result):
                return jsonify({'error': 'Conversion resulted in invalid value'}), 400

            # Format result
            if result == int(result) and abs(result) < 1e12:
                result_str = str(int(result))
            else:
                result_str = f"{result:.6g}"

            logger.info(f"Conversion: {conversion_key}({value}) = {result_str}")
            return jsonify({'result': result_str, 'label': label}), 200

        except Exception as e:
            logger.error(f"Conversion error: {e}")
            return jsonify({'error': 'Conversion failed'}), 400

    except Exception as e:
        logger.error(f"Unexpected error in convert: {e}")
        return jsonify({'error': 'Server error'}), 500


@app.errorhandler(404)
def not_found(error: Any) -> Tuple[Any, int]:
    """Handle 404 errors"""
    return jsonify({'error': 'Not found'}), 404


@app.errorhandler(500)
def server_error(error: Any) -> Tuple[Any, int]:
    """Handle 500 errors"""
    logger.error(f"Server error: {error}")
    return jsonify({'error': 'Internal server error'}), 500


if __name__ == '__main__':
    """Run Flask development server"""
    logger.info(f"Starting AXIOM CALC in {app.config['ENV']} mode")
    app.run(
        host='0.0.0.0',
        port=5000,
        debug=app.config['DEBUG']
    )
