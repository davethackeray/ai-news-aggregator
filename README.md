# AI News Aggregator

A web application that aggregates AI-related news using NewsAPI, built with FastAPI and React.

## Features

- Fetches and displays latest AI and machine learning news
- Calculates interesting scores for news articles
- Clean and responsive UI using Chakra UI
- Real-time updates using FastAPI backend

## Prerequisites

- Python 3.8+
- Node.js 14+
- NewsAPI key (get one at https://newsapi.org)

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

## Setup

### Backend

1. Create and activate virtual environment:
```bash
cd backend
python -m venv venv
# For fish shell:
. venv/bin/activate.fish
# For bash/zsh:
# source venv/bin/activate
```

2. Install dependencies:
```bash
pip install --upgrade pip
pip install fastapi
pip install "uvicorn[standard]"
pip install sqlalchemy
pip install pydantic
pip install python-dotenv
pip install newsapi-python
pip install requests
```

3. Set up environment variables:
```bash
cp .env.example .env
# Edit .env and add your NewsAPI key
```

4. Start the backend server:
```bash
python -m uvicorn main:app --host 127.0.0.1 --port 8000 --reload
```

### Frontend

1. Install dependencies:
```bash
cd frontend
npm install
```

2. Start the development server:
```bash
npm start
```

The application will be available at:
- Frontend: http://localhost:3000
- Backend API: http://localhost:8000

## Environment Variables

Backend (.env):
```
NEWS_API_KEY=your_newsapi_key_here
```

## Contributing

1. Fork the repository
2. Create your feature branch (`git checkout -b feature/amazing-feature`)
3. Commit your changes (`git commit -m 'Add some amazing feature'`)
4. Push to the branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request

## License

This project is licensed under the MIT License - see the LICENSE file for details.