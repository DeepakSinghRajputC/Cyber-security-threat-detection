# Contributing to AI-Based Cybersecurity Threat Detection

Thank you for your interest in contributing! This guide will help you get started.

## Table of Contents
- [Code of Conduct](#code-of-conduct)
- [Getting Started](#getting-started)
- [Development Setup](#development-setup)
- [How to Contribute](#how-to-contribute)
- [Coding Standards](#coding-standards)
- [Testing](#testing)
- [Pull Request Process](#pull-request-process)

## Code of Conduct

Be respectful, inclusive, and professional in all interactions.

## Getting Started

1. Fork the repository
2. Clone your fork: `git clone https://github.com/YOUR_USERNAME/Cyber-security-threat-detection.git`
3. Create a branch: `git checkout -b feature/your-feature-name`

## Development Setup

### Backend
```bash
cd backend
python -m venv venv
source venv/bin/activate
pip install -r requirements.txt
```

### Frontend
```bash
cd frontend
npm install
```

## How to Contribute

### Reporting Bugs
- Use GitHub Issues
- Include detailed steps to reproduce
- Specify your environment (OS, Python version, etc.)
- Provide error messages and logs

### Suggesting Enhancements
- Use GitHub Issues with "enhancement" label
- Describe the feature clearly
- Explain the use case
- Provide examples if possible

### Code Contributions
1. Check existing issues or create a new one
2. Discuss your approach before starting
3. Write clean, documented code
4. Add tests for new features
5. Update documentation

## Coding Standards

### Python (Backend)
- Follow PEP 8 style guide
- Use type hints where appropriate
- Add docstrings to functions and classes
- Keep functions small and focused

```python
def process_data(data: pd.DataFrame) -> np.ndarray:
    """
    Process network traffic data.
    
    Args:
        data: Raw traffic DataFrame
        
    Returns:
        Processed feature array
    """
    # Implementation
    pass
```

### JavaScript/React (Frontend)
- Use functional components with hooks
- Follow ESLint configuration
- Use meaningful variable names
- Keep components small and reusable

```jsx
function MetricCard({ title, value, icon: Icon }) {
  return (
    <div className="metric-card">
      <Icon />
      <h3>{title}</h3>
      <p>{value}</p>
    </div>
  );
}
```

## Testing

### Backend Tests
```bash
cd backend
python test_system.py
```

### Frontend Tests
```bash
cd frontend
npm test
```

### Manual Testing
- Test all API endpoints
- Verify UI functionality
- Check Docker builds
- Test with different user roles

## Pull Request Process

1. **Update Documentation**
   - Update README if needed
   - Update API_DOCUMENTATION.md for API changes
   - Add comments to complex code

2. **Run Tests**
   - Ensure all tests pass
   - Add new tests for new features

3. **Create Pull Request**
   - Use descriptive title
   - Reference related issues
   - Describe changes clearly
   - Include screenshots for UI changes

4. **Code Review**
   - Address review comments
   - Make requested changes
   - Keep discussions constructive

5. **Merge**
   - Squash commits if needed
   - Update CHANGELOG.md

## Project Structure

```
├── backend/
│   ├── app/              # Application modules
│   ├── models/           # Trained models (gitignored)
│   ├── data/            # Data files (gitignored)
│   ├── main.py          # FastAPI entry point
│   └── requirements.txt  # Dependencies
├── frontend/
│   ├── src/
│   │   ├── components/  # React components
│   │   ├── pages/       # Page components
│   │   └── utils/       # Utilities
│   └── package.json     # Dependencies
├── demo_data/           # Sample data
└── docker-compose.yml   # Docker configuration
```

## Areas for Contribution

### High Priority
- [ ] Add unit tests
- [ ] Improve error handling
- [ ] Add database persistence
- [ ] Implement WebSocket support
- [ ] Add more ML models

### Medium Priority
- [ ] Improve UI/UX
- [ ] Add data visualization options
- [ ] Implement export functionality
- [ ] Add API rate limiting
- [ ] Create admin dashboard

### Low Priority
- [ ] Add dark/light theme toggle
- [ ] Implement notification system
- [ ] Add multi-language support
- [ ] Create mobile-responsive views

## Questions?

- Open a GitHub Issue
- Check existing documentation
- Review closed issues for similar questions

## License

By contributing, you agree that your contributions will be licensed under the MIT License.

---

Thank you for contributing! 🎉
