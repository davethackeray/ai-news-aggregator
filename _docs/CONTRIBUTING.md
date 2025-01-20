# Contributing to AI News Aggregator

## Core Values
1. **User-Centric Development**: Every feature should directly benefit business leaders seeking AI insights
2. **Data-Driven Decisions**: Use metrics to guide development priorities
3. **Cost Efficiency**: Optimize for performance while minimizing infrastructure costs
4. **Code Quality**: Maintain high standards for maintainability and reliability
5. **Continuous Learning**: Leverage feedback loops to improve recommendations

## Development Guidelines

### 1. Code Organization

#### File Structure
- Keep files focused and compact (< 300 lines)
- Group related functionality
- Use meaningful file names
```
backend/
  ├── api/           # Route handlers
  ├── services/      # Business logic
  ├── models/        # Database models
  ├── utils/         # Helper functions
  └── tests/         # Test files

frontend/
  ├── components/    # Reusable UI components
  ├── hooks/         # Custom React hooks
  ├── services/      # API clients
  ├── utils/         # Helper functions
  └── tests/         # Test files
```

#### Naming Conventions
- Use clear, descriptive names
- Follow language-specific conventions:
  * Python: snake_case for functions/variables
  * JavaScript: camelCase for variables, PascalCase for components
- Prefix private methods with underscore

### 2. Code Quality Standards

#### General Principles
- Write self-documenting code
- Follow SOLID principles
- Keep functions small and focused
- Use meaningful variable names
- Add comments for complex logic only

#### Python Specific
```python
# Good
def calculate_interesting_score(story: Story) -> float:
    """Calculate story interest score based on multiple factors."""
    content_score = analyze_content_relevance(story.content)
    engagement_score = get_historical_engagement(story.source)
    return weighted_average([content_score, engagement_score])

# Bad
def calc_score(s):
    # Calculate score
    c = analyze(s.content)
    e = hist_eng(s.source)
    return (c + e) / 2
```

#### JavaScript/React Specific
```javascript
// Good
const NewsCard = ({ story, onShare }) => {
  const { title, description, score } = story;
  return (
    <Card>
      <CardTitle>{title}</CardTitle>
      <CardBody>{description}</CardBody>
      <InterestScore value={score} />
    </Card>
  );
};

// Bad
const Card = (props) => {
  return (
    <div>
      <h3>{props.story.title}</h3>
      <p>{props.story.description}</p>
      <span>{props.story.score}</span>
    </div>
  );
};
```

### 3. Performance Guidelines

#### Database
- Use appropriate indexes
- Write optimized queries
- Implement caching where beneficial
- Regular cleanup of old data

#### API
- Implement pagination
- Use appropriate caching headers
- Rate limit endpoints
- Validate input data

#### Frontend
- Implement code splitting
- Optimize bundle size
- Use proper React memo/useMemo
- Lazy load components

### 4. Testing Requirements

#### Backend
- Unit tests for utilities and services
- Integration tests for API endpoints
- >= 80% test coverage
- Test edge cases and error handling

#### Frontend
- Component unit tests
- Integration tests for key flows
- E2E tests for critical paths
- Accessibility testing

### 5. Git Workflow

#### Podcast Analytics Development
 - Coordinate with analytics team to validate new metrics
 - Ensure new tests cover podcast-related data ingestion and usage

#### Branch Naming
```
feature/add-email-integration
bugfix/fix-scoring-calculation
refactor/optimize-database-queries
```

#### Commit Messages
```
feat: implement daily email digest
fix: correct interesting score calculation
refactor: optimize database queries
test: add tests for scoring algorithm
```

#### Pull Request Process
1. Keep PRs focused and small
2. Include tests
3. Update documentation
4. Add migration scripts if needed
5. Request review from 2 team members

### 6. Documentation Standards

#### Code Documentation
- Document complex algorithms
- Explain business logic
- Document API endpoints
- Keep documentation close to code

#### API Documentation
```python
@app.get("/api/news")
async def get_news(
    limit: int = Query(10, description="Number of stories to return"),
    min_score: float = Query(0.7, description="Minimum interesting score")
) -> List[Story]:
    """
    Fetch news stories filtered by interesting score.
    
    Args:
        limit: Maximum number of stories to return
        min_score: Minimum interesting score threshold
        
    Returns:
        List of Story objects meeting the criteria
    """
```

### 7. Cost Optimization

#### Database
- Regular cleanup of old data
- Optimize queries and indexes
- Use appropriate instance sizes

#### API Usage
- Cache external API responses
- Implement rate limiting
- Monitor usage patterns

#### Infrastructure
- Start small and scale as needed
- Use serverless where appropriate
- Monitor resource utilization

### 8. Review Checklist

#### Before Submitting PR
- [ ] Code follows style guidelines
- [ ] Tests are written and passing
- [ ] Documentation is updated
- [ ] No unnecessary dependencies added
- [ ] Performance impact considered
- [ ] Security implications reviewed

#### Before Merging
- [ ] PR is up to date with main branch
- [ ] All review comments addressed
- [ ] CI/CD pipeline passing
- [ ] No conflicts
- [ ] Migration plan if needed

### 9. Security Guidelines

#### General
- No secrets in code
- Use environment variables
- Implement proper authentication
- Regular dependency updates
- Input validation

#### API Security
- Rate limiting
- Input sanitization
- proper CORS settings
- Authentication/Authorization

### 10. Monitoring and Maintenance

#### Metrics to Track
- API response times
- Error rates
- Resource utilization
- User engagement
- Story relevance accuracy

#### Regular Tasks
- Dependency updates
- Performance monitoring
- Security scanning
- Database maintenance
- Log analysis

## Getting Help

### Resources
- Project documentation in `/docs`
- API documentation at `/api/docs`
- ROADMAP.md for project direction
- README.md for setup instructions

### Questions
- Check existing issues first
- Use issue templates
- Be specific and provide context
- Include relevant logs/errors

Remember: The goal is to build a sustainable, maintainable system that provides value to business leaders while keeping costs minimal. When in doubt, optimize for clarity and simplicity over clever solutions.