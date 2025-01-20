Instructions for New Developers:

1. Initial Setup (Day 1)
   First, review these documents in order:
   - README.md for project overview and basic setup
   - CONTRIBUTING.md for development standards
   - ROADMAP.md for current status and next tasks

2. Environment Setup (Day 1)
   Backend:
   ```bash
   cd backend
   python -m venv venv
   . venv/bin/activate.fish  # For fish shell
   pip install --upgrade pip
   pip install -r requirements.txt
   cp .env.example .env
   # Get NewsAPI key from newsapi.org and add to .env
   python -m uvicorn main:app --host 127.0.0.1 --port 8000 --reload
   ```

   Frontend:
   ```bash
   cd frontend
   npm install
   npm start
   ```

3. Project Status (Day 1-2)
   Currently Completed:
   - Basic news aggregation
   - Frontend display
   - Initial scoring system
   
   In Progress:
   - Database implementation
   - Email integration
   - Story scoring refinement

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