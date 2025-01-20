Instructions for New Developers:

1. Initial Setup (Day 1)
   First, review these documents in order:
   - README.md for project overview and basic setup
   - CONTRIBUTING.md for development standards
   - ROADMAP.md for current status and next tasks
2. Environment Setup (Day 1)
    Backend:
    ```bash
    # Navigate to backend directory
    cd backend
    
    # Create and activate virtual environment
    python3 -m venv venv
    source venv/bin/activate  # For bash/zsh
    # OR
    . venv/bin/activate.fish  # For fish shell
    # OR
    .\venv\Scripts\activate  # For Windows
    
    # Install dependencies
    python3 -m pip install --upgrade pip
    python3 -m pip install -r requirements.txt
    cp .env.example .env
    # Get NewsAPI key from newsapi.org and add to .env
    
    # Set up the database
    createdb ainews  # Create main database
    createdb ainews_test  # Create test database
    alembic upgrade head  # Run migrations
    
    # Run the server
    python -m uvicorn main:app --host 127.0.0.1 --port 8000 --reload
    ```

    Frontend:
    ```bash
    cd frontend
    npm install
    npm start
    ```

    Testing:
    ```bash
    cd backend
    # Install test dependencies
    pip install pytest pytest-cov

    # Run tests
    pytest  # Run all tests
    pytest tests/test_models.py  # Run specific test file
    pytest -v  # Verbose output
    pytest --cov=.  # Run tests with coverage report
    ```

    Development Workflow:
    1. Create feature branch
    2. Write tests for new functionality
    3. Implement features
    4. Ensure tests pass
    5. Run migrations if needed
    6. Submit PR with tests and documentation
   ```

3. Project Status (Day 1-2)
    Currently Completed:
    - Basic news aggregation
    - Frontend display
    - Enhanced scoring system
    - Database implementation with tests
    - Daily digest system (markdown-based)
    
    In Progress:
    - Story scoring refinement
    - Analytics dashboard
    
    Daily Digest System:
    ```bash
    # Generate today's digest manually
    cd backend
    python scripts/generate_digest.py
    
    # Digests are saved to backend/digests/
    # Format: digest-YYYY-MM-DD.md

    Note: Also review upcoming podcast analytics features in the ROADMAP to ensure
    environment includes any dependencies or API credentials for analyzing listener data.
    ```

    Note: For local development, we generate markdown files instead of sending emails.
    This provides an easy way to verify content and formatting while keeping the
    system simple and avoiding email service dependencies.

4. Your First Tasks (Day 2+)
   a. Check ROADMAP.md's "Next Up (Prioritized)" section
   b. Pick an unclaimed task from "Immediate Tasks"
   c. Create a feature branch following CONTRIBUTING.md guidelines
   d. Submit PRs following the checklist in CONTRIBUTING.md

5. Development Rules
   - Keep files under 300 lines
   - Follow code style in CONTRIBUTING.md
   - Write tests for new features
   - Update documentation as you go
   - Consider cost implications of changes

6. Daily Workflow
   - Pull latest changes
   - Check ROADMAP.md for task status
   - Update your task progress
   - Regular commits with descriptive messages
   - Daily code reviews

7. Key Constraints
   - Local-first development to minimize costs
   - Consider cloud migration triggers in ROADMAP.md
   - Maintain high test coverage
   - Focus on performance optimization

8. Getting Help
   - Check existing documentation first
   - Review similar implementations in codebase
   - Create detailed issues for blockers
   - Request reviews early for complex changes

Remember: Our mission is to help business leaders make informed decisions about AI integration while keeping the system cost-effective and maintainable.