# AI Affiliate Hub

## Overview

AI Affiliate Hub is a Flask-based web application that generates comprehensive affiliate marketing content using artificial intelligence. The platform allows administrators to add product sections and individual products with affiliate links, then automatically generates detailed product reviews, descriptions, pros/cons lists, and SEO-optimized metadata using OpenAI's GPT-4o model. The application features a clean, responsive frontend built with Bootstrap 5 and provides both public-facing product pages and an administrative interface for content management.

## User Preferences

Preferred communication style: Simple, everyday language.

## Recent Changes (August 2025)

- **Enhanced Design**: Implemented minimalistic aesthetic with modern blue color scheme
- **Advanced Security**: Dual-layer admin protection with IP whitelisting + HTTP Basic Authentication
- **GitHub AI Integration**: Switched from OpenAI to GitHub AI models for content generation
- **Responsive Layout**: Improved mobile and desktop experience with clean typography
- **IP Restriction**: Admin panel only accessible from whitelisted IP addresses
- **Stealth Security**: Unauthorized access attempts see 404 errors instead of login prompts

## System Architecture

### Frontend Architecture
- **Template Engine**: Jinja2 templates with Flask for server-side rendering
- **CSS Framework**: Bootstrap 5 for responsive design and UI components
- **JavaScript**: Vanilla JavaScript for interactive features including search functionality, form validation, and lazy loading
- **Icons**: Feather Icons for consistent iconography throughout the application
- **Layout Structure**: Base template with block inheritance for consistent navigation and styling

### Backend Architecture
- **Web Framework**: Flask (Python) with modular route organization
- **Database ORM**: SQLAlchemy with declarative base model approach
- **Application Structure**: Factory pattern with separate modules for models, routes, and AI services
- **URL Routing**: RESTful URLs with slug-based product and section identification
- **Session Management**: Flask sessions with configurable secret key

### Data Storage Solutions
- **Primary Database**: SQLite for development with PostgreSQL support via environment configuration
- **Connection Pooling**: SQLAlchemy connection pool with automatic reconnection
- **Schema Design**: Two main entities - Sections (categories) and Products with one-to-many relationship
- **Content Storage**: AI-generated content stored as text fields with JSON serialization for lists
- **Search Implementation**: Basic text search across product names, descriptions, and reviews

### Authentication and Authorization
- **Admin Protection**: HTTP Basic Authentication + IP whitelisting protecting all admin routes
- **Environment Variables**: ADMIN_USERNAME, ADMIN_PASSWORD, and ADMIN_ALLOWED_IPS for secure access control
- **IP Restriction**: Only specified IP addresses can access admin panel (returns 404 for unauthorized IPs)
- **Protected Routes**: /admin, /admin/section/add, /admin/product/add, /admin/product/delete, /admin/section/delete
- **Security Features**: Dual-layer security (IP + credentials), session management, secure logout
- **Stealth Mode**: Unauthorized IPs see "Page Not Found" instead of login prompt (hides admin existence)

## External Dependencies

### AI Services
- **GitHub AI Models**: Integration with GitHub's AI inference API at https://models.github.ai/inference
- **Model**: GPT-4o-mini for content generation
- **Content Types**: Product descriptions, reviews, pros/cons lists, SEO titles and meta descriptions
- **API Configuration**: GitHub token-based authentication via OPENAI_API_KEY environment variable

### Frontend Libraries
- **Bootstrap 5**: CSS framework via CDN for responsive design
- **Feather Icons**: Icon library via CDN for consistent UI elements
- **No bundler**: Direct CDN integration for simplicity and faster development

### Backend Dependencies
- **Flask**: Core web framework
- **SQLAlchemy**: Database ORM and connection management
- **Werkzeug**: WSGI utilities including ProxyFix for deployment
- **OpenAI Python SDK**: Official client library for AI API integration

### Development Environment
- **Replit Platform**: Cloud-based development and hosting
- **Environment Variables**: Configuration via environment for API keys and database URLs
- **Debug Mode**: Flask development server with hot reload capability
- **Logging**: Python logging module with debug level configuration