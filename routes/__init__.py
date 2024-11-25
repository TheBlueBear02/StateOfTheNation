from .index import index_bp
from .offices import offices_bp
from .demography import demography_bp
from .economy import economy_bp
from .parliament import parliament_bp

# Export blueprints for app.py
__all__ = ['index_bp', 'offices_bp', 'demography_bp', 'economy_bp', 'parliament_bp']
