# AI News Aggregator

A smart news aggregation system that helps business leaders stay informed about practical AI implementations through curated news and podcast insights.

## Overview

This system aggregates AI-related news and uses engagement metrics from an associated podcast to determine story relevance. It features a daily email digest of the most interesting stories and provides insights for podcast content strategy.

Planned integration of podcast listener data will further improve story scoring and suggestion logic.

### Key Features

- 🔍 Smart news aggregation with ML-based interesting score
- 📊 Podcast engagement analytics integration
- 📧 Daily email digest of top stories
- 📱 Responsive web interface
- 📈 Performance analytics dashboard

## Quick Start

### Prerequisites

- Python 3.8+
- Node.js 14+
- NewsAPI key (get one at https://newsapi.org)

### Backend Setup

```bash
cd backend
python -m venv venv

# For fish shell:
. venv/bin/activate.fish
# For bash/zsh:
# source venv/bin/activate

# Install dependencies
pip install --upgrade pip
pip install fastapi
pip install "uvicorn[standard]"
pip install sqlalchemy
pip install pydantic
pip install python-dotenv
pip install newsapi-python
pip install requests

# Configure environment
cp .env.example .env
# Edit .env and add your NewsAPI key

# Start the server
python -m uvicorn main:app --host 127.0.0.1 --port 8000 --reload
```

### Frontend Setup

```bash
cd frontend
npm install
npm start
```

The application will be available at:
- Frontend: http://localhost:3000
- Backend API: http://localhost:8000

## Project Structure

```
.
├── backend/           # FastAPI server
│   ├── main.py       # Main API implementation
│   ├── requirements.txt
│   └── .env.example  # Environment variables template
└── frontend/         # React application
    ├── src/         
    │   ├── App.js   # Main React component
    │   └── index.js # React entry point
    └── public/      
```

## Documentation

- [Development Roadmap](ROADMAP.md) - Project phases and technical details
- [Contributing Guidelines](CONTRIBUTING.md) - Development rules and best practices
- [License](LICENSE) - MIT License

## Key Development Principles

1. **Cost Efficiency**: Optimize for minimal infrastructure costs
2. **Data-Driven**: Use metrics to guide development
3. **User-Centric**: Focus on business leader needs
4. **Quality First**: Maintain high code standards
5. **Continuous Learning**: Leverage feedback loops

## Development Status
Current Version: v0.1.1
- ✅ Basic news aggregation
- ✅ FastAPI backend
- ✅ React frontend
- ✅ Initial interesting score implementation
- ✅ Story database implementation
  - PostgreSQL models and migrations
  - Story service layer
  - Comprehensive test coverage
- ✅ Email integration
- 🔄 Podcast analytics (in progress)

## Testing

The project maintains high test coverage with:

### Backend Tests
- Unit tests for models and services
- Integration tests for API endpoints
- Database interaction tests

Run the tests:
```bash
cd backend
pytest  # Run all tests
pytest --cov=.  # Run with coverage report
```

### Test Categories
- `tests/test_models.py`: Database model tests
- `tests/test_story_service.py`: Service layer tests
- `tests/test_api.py`: API endpoint tests
- 📅 Podcast analytics (planned)

See [ROADMAP.md](ROADMAP.md) for detailed development plans and upcoming features.

## Getting Started with Development

1. Review [CONTRIBUTING.md](CONTRIBUTING.md) for development guidelines
2. Check existing issues for tasks
3. Fork the repository
4. Create a feature branch
5. Submit a pull request

## Monitoring and Metrics

Key metrics we track:
- Story relevance accuracy
- Email engagement rates
- API performance
- Resource utilization
- Podcast segment performance

## Support and Questions

- Create an issue for bugs or feature requests
- Use appropriate issue templates
- Provide relevant context and logs

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.