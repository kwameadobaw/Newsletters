"""
Configuration file for Byte-Sized Brilliance Newsletter Website
"""

import os
from datetime import datetime

# Flask Configuration
class Config:
    # Basic Flask settings
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'your-secret-key-change-this-in-production'
    DEBUG = os.environ.get('FLASK_DEBUG', 'True').lower() == 'true'
    
    # File upload settings
    UPLOAD_FOLDER = 'newsletters'
    MAX_CONTENT_LENGTH = 16 * 1024 * 1024  # 16MB max file size
    ALLOWED_EXTENSIONS = {'pdf'}
    
    # Admin settings
    ADMIN_USERNAME = os.environ.get('ADMIN_USERNAME') or 'Brilliance'
    ADMIN_PASSWORD = os.environ.get('ADMIN_PASSWORD') or 'Heisenb3rg@1'
    
    # Website settings
    SITE_NAME = 'Byte-Sized Brilliance'
    SITE_TAGLINE = 'Your Monthly Tech Navigator'
    SITE_DESCRIPTION = 'Stay ahead of the curve with our monthly tech insights, trends, and actionable knowledge.'
    
    # Social media links (update these with your actual links)
    SOCIAL_LINKS = {
        'linkedin': '#',
        'x_twitter': '#',
        'github': '#',
        'email': 'mailto:contact@bytesizedbrilliance.com'
    }
    
    # Newsletter settings
    ITEMS_PER_PAGE = 6
    DEFAULT_DATE = datetime.now().strftime('%Y-%m-%d')
    
    # Theme colors (CSS variables)
    THEME_COLORS = {
        'primary': '#6366f1',
        'primary_hover': '#4f46e5',
        'secondary': '#8b5cf6',
        'accent': '#06b6d4',
        'bg_dark': '#0f0f23',
        'bg_darker': '#0a0a1a',
        'bg_card': '#1a1a2e',
        'bg_card_hover': '#252545',
        'text_primary': '#ffffff',
        'text_secondary': '#a1a1aa',
        'text_muted': '#71717a',
        'border_color': '#2d2d4a',
        'success': '#10b981',
        'warning': '#f59e0b',
        'danger': '#ef4444'
    }

# Development configuration
class DevelopmentConfig(Config):
    DEBUG = True
    TESTING = False

# Production configuration
class ProductionConfig(Config):
    DEBUG = False
    TESTING = False
    # In production, use environment variables for sensitive data
    SECRET_KEY = os.environ.get('SECRET_KEY')
    ADMIN_USERNAME = os.environ.get('ADMIN_USERNAME')
    ADMIN_PASSWORD = os.environ.get('ADMIN_PASSWORD')

# Testing configuration
class TestingConfig(Config):
    TESTING = True
    DEBUG = True
    WTF_CSRF_ENABLED = False

# Configuration dictionary
config = {
    'development': DevelopmentConfig,
    'production': ProductionConfig,
    'testing': TestingConfig,
    'default': DevelopmentConfig
}

def get_config():
    """Get configuration based on environment"""
    env = os.environ.get('FLASK_ENV', 'development')
    return config.get(env, config['default'])

# Utility functions
def allowed_file(filename):
    """Check if file extension is allowed"""
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in Config.ALLOWED_EXTENSIONS

def get_file_size_mb(file_size_bytes):
    """Convert bytes to MB"""
    return round(file_size_bytes / (1024 * 1024), 2)

def format_date(date_string):
    """Format date string for display"""
    try:
        date_obj = datetime.strptime(date_string, '%Y-%m-%d')
        return date_obj.strftime('%B %Y')
    except:
        return date_string

def get_social_links():
    """Get social media links"""
    return Config.SOCIAL_LINKS

def get_theme_colors():
    """Get theme colors"""
    return Config.THEME_COLORS 