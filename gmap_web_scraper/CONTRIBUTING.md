# Contributing to Google Maps Web Scraper

Thank you for your interest in contributing! This document provides guidelines for contributing to this project.

## 🤝 How to Contribute

### Reporting Bugs
1. Check existing issues to avoid duplicates
2. Use the bug report template
3. Include detailed steps to reproduce
4. Provide system information (OS, Python version, etc.)

### Suggesting Features
1. Check if the feature already exists or is planned
2. Use the feature request template
3. Explain the use case and benefits

### Code Contributions

#### Getting Started
1. Fork the repository
2. Clone your fork: `git clone https://github.com/yourusername/gmap-web-scraper.git`
3. Create a virtual environment: `python -m venv gscraper_env`
4. Install dependencies: `pip install -r requirements.txt`
5. Create a feature branch: `git checkout -b feature/your-feature-name`

#### Development Guidelines

**Code Style**
- Follow PEP 8 guidelines
- Use meaningful variable and function names
- Add docstrings for functions and classes

**Testing**
- Write tests for new functionality
- Ensure all tests pass: `python manage.py test`

**Documentation**
- Update README.md if needed
- Add inline comments for complex logic

#### Submitting Changes
1. Commit your changes: `git commit -m "Add: description of changes"`
2. Push to your fork: `git push origin feature/your-feature-name`
3. Create a Pull Request with:
   - Clear title and description
   - Reference related issues

## 🔍 Code Review Process

1. **Automated Checks**: All PRs run through CI/CD
2. **Manual Review**: Maintainers review code quality
3. **Testing**: Reviewers test functionality
4. **Approval**: At least one maintainer approval required

## 📝 Commit Message Guidelines

Use conventional commits format:
- `feat:` New feature
- `fix:` Bug fix
- `docs:` Documentation changes
- `style:` Code style changes
- `refactor:` Code refactoring

Example: `feat: add export to JSON functionality`

## ❓ Questions?

- Open a discussion on GitHub
- Check existing documentation
- Contact maintainers directly

Thank you for contributing! 🎉
