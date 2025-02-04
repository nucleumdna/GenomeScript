# Contributing to GenomeScript 🧬

We love your input! We want to make contributing to GenomeScript as easy and transparent as possible.

## Development Process
1. Fork the repo
2. Create a branch
3. Make your changes
4. Submit a PR

## Pull Request Process
1. Update documentation
2. Run tests
3. Update CHANGELOG
4. Submit PR with description

## Code Style
- Python: Follow PEP 8
- TypeScript: Use prettier
- Run linters before committing

## Testing
```bash
# Run Python tests
python -m pytest tests/

# Run frontend tests
cd frontend
npm test
```

## License
By contributing, you agree that your contributions will be licensed under the MIT License.

## Code of Conduct 📜

By participating in this project, you agree to abide by our [Code of Conduct](CODE_OF_CONDUCT.md). Please read it before contributing.

## How Can I Contribute? 🤝

### 1. Reporting Bugs 🐛

Before creating bug reports, please check the issue tracker as you might find out that you don't need to create one. When you create a bug report, please include as many details as possible:

- Use a clear and descriptive title
- Describe the exact steps to reproduce the problem
- Provide specific examples to demonstrate the steps
- Describe the behavior you observed and what behavior you expected
- Include any relevant genomic data files (if possible)

### 2. Suggesting Enhancements 💡

Enhancement suggestions are tracked as GitHub issues. When creating an enhancement suggestion, please include:

- A clear and descriptive title
- A detailed description of the proposed functionality
- Any possible implementation details
- Why this enhancement would be useful to GenomeScript users

### 3. Code Contributions 💻

#### Development Environment Setup

1. Fork and clone the repository:
```bash
git clone https://github.com/your-username/genomescript.git
cd genomescript
```

2. Create a virtual environment:
```bash
python -m venv venv
source venv/bin/activate  # or `venv\Scripts\activate` on Windows
```

3. Install dependencies:
```bash
pip install -r requirements.txt
pip install -r requirements-dev.txt
```

4. Install pre-commit hooks:
```bash
pre-commit install
```

#### Code Style Guidelines 📝

We use several tools to maintain code quality:

- **Black** for code formatting
- **isort** for import sorting
- **mypy** for type checking
- **pylint** for code analysis

Run the full suite:
```bash
# Format code
black .
isort .

# Check types
mypy src tests

# Run linter
pylint src tests
```

#### Testing Guidelines 🧪

- Write tests for all new features
- Maintain or improve code coverage
- Use pytest fixtures appropriately
- Include both unit and integration tests

Run tests:
```bash
# Run all tests
pytest

# Run with coverage
pytest --cov=src tests/

# Run specific test file
pytest tests/test_lexer.py
```

### Pull Request Process 🔄

1. Create a new branch:
```bash
git checkout -b feature/your-feature-name
```

2. Make your changes:
   - Write clear commit messages
   - Keep commits focused and atomic
   - Reference issues in commit messages

3. Update documentation:
   - Add/update docstrings
   - Update README if needed
   - Add to CHANGELOG.md

4. Run tests and checks:
```bash
# Run all checks
make check

# Run tests
make test
```

5. Push and create PR:
```bash
git push origin feature/your-feature-name
```

#### PR Review Checklist ✅

- [ ] Tests pass
- [ ] Code follows style guidelines
- [ ] Documentation updated
- [ ] Changelog updated
- [ ] PR description is clear
- [ ] Commits are clean and focused

## Project Structure 📁

```
genomescript/
├── src/
│   ├── compiler/      # Lexer, parser, AST
│   ├── vm/           # Virtual machine
│   ├── genomics/     # Genomic analysis
│   ├── ai/           # AI models
│   └── blockchain/   # Blockchain integration
├── tests/
├── docs/
└── examples/
```

## Getting Help 🆘

- Join our [Discord server](https://discord.gg/genomescript)
- Check the [documentation](https://docs.genomescript.org)
- Ask on [Stack Overflow](https://stackoverflow.com/questions/tagged/genomescript)

## Recognition 🏆

Contributors are recognized in several ways:
- Listed in CONTRIBUTORS.md
- Mentioned in release notes
- Featured on our website

## License 📄

By contributing to GenomeScript, you agree that your contributions will be licensed under its MIT License. 