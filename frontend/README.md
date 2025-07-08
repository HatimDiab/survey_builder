# Survey Builder Frontend (Flask)

A modern, responsive web application for building and managing surveys, built with Flask and Tailwind CSS.

## Features

- **Modern UI**: Clean, responsive design with Tailwind CSS
- **Drag & Drop**: Intuitive question building with drag-and-drop functionality
- **Multiple Question Types**: Support for various question formats
- **Real-time Preview**: Live preview of survey as you build
- **Export Options**: Multiple export formats (PDF, HTML, JSON, CSV)
- **White-label Support**: Custom branding and colors
- **Category Management**: Organize questions into logical categories

## Technology Stack

- **Backend**: Flask (Python)
- **Frontend**: HTML, CSS (Tailwind), JavaScript (Vanilla)
- **Styling**: Tailwind CSS
- **Icons**: Font Awesome
- **HTTP Client**: Axios

## Project Structure

```
frontend/
├── app.py                 # Main Flask application
├── requirements.txt       # Python dependencies
├── Dockerfile            # Docker configuration
├── templates/            # HTML templates
│   ├── base.html         # Base template with navigation
│   ├── splash.html       # Welcome page
│   ├── white_label.html  # Branding configuration
│   ├── category.html     # Category management
│   ├── question.html     # Question builder
│   └── review.html       # Review and export
├── static/               # Static assets
│   └── css/
│       └── custom.css    # Custom styles
└── README.md            # This file
```

## Getting Started

### Prerequisites

- Python 3.8+
- uv (recommended) or pip

### Local Development

1. **Install dependencies** (using uv):
   ```bash
   uv pip install -r requirements.txt
   ```
   
   Or using pyproject.toml:
   ```bash
   uv sync
   ```

2. **Run the application**:
   ```bash
   python app.py
   ```

3. **Access the application**:
   Open your browser and navigate to `http://localhost:3000`

### Docker Development

1. **Build and run with Docker Compose**:
   ```bash
   docker-compose up frontend
   ```

2. **Or build individually**:
   ```bash
   docker build -t survey-builder-frontend .
   docker run -p 3000:3000 survey-builder-frontend
   ```

## Pages

### 1. Splash Page (`/`)
- Welcome screen with feature overview
- Call-to-action buttons to start building

### 2. White Label (`/white-label`)
- Custom branding configuration
- Color picker for primary/secondary colors
- Logo upload functionality
- Live preview of branding changes

### 3. Categories (`/category`)
- Create and manage survey categories
- Drag-and-drop category organization
- Category color coding
- Real-time preview

### 4. Questions (`/question`)
- Drag-and-drop question builder
- Multiple question types:
  - Multiple choice
  - Checkbox
  - Text input
  - Long text (textarea)
  - Rating (stars)
  - Scale (1-10)
- Question editing modal
- Live preview of questions

### 5. Review (`/review`)
- Complete survey preview
- Export options (PDF, HTML, JSON, CSV)
- Survey statistics
- Publish functionality

## API Endpoints

- `POST /api/export` - Export survey data
- `POST /api/save-progress` - Save survey progress

## Customization

### Styling
- Modify `templates/base.html` for global styling changes
- Add custom CSS in `static/css/custom.css`
- Tailwind classes are used throughout for consistent styling

### Adding New Question Types
1. Add the question type to the drag-and-drop panel in `question.html`
2. Update the `generateQuestionForm()` function
3. Add preview rendering in `generatePreviewContent()`
4. Update the question type colors and names functions

### Adding New Export Formats
1. Add export button in `review.html`
2. Create export generation function
3. Update the `exportSurvey()` function

## Development Notes

- The application uses vanilla JavaScript for interactivity
- All styling is done with Tailwind CSS classes
- Font Awesome icons are used throughout
- Axios is used for API calls
- The application is designed to be responsive and mobile-friendly

## Contributing

1. Follow the existing code structure
2. Use Tailwind CSS for styling
3. Ensure responsive design
4. Test on multiple browsers
5. Add appropriate error handling

## License

This project is part of the Survey Builder application. 