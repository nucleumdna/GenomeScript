# GenomeScript

A domain-specific language for genomic data analysis with a web-based IDE.

## Features

- Custom lexer and parser for genomic analysis commands
- Web-based editor with syntax highlighting
- Real-time tokenization and error detection
- Support for common genomic file formats (FASTA, VCF, BAM)

## Documentation 📚

- [Getting Started](docs/getting-started.md)
- [API Documentation](docs/api/index.md)
- [Tutorials](docs/tutorials/index.md)
- [Security Guide](docs/security/index.md)
- [Contributing Guidelines](CONTRIBUTING.md)

## Project Structure

```
.
├── docs/               # Documentation
│   ├── api/           # API reference
│   ├── tutorials/     # Tutorials
│   └── security/      # Security guide
├── frontend/          # React frontend
│   ├── src/
│   │   ├── components/
│   │   └── api/
│   └── public/
├── src/              # Python backend
│   └── compiler/
│       └── lexer.py
├── tests/            # Test files
└── scripts/          # Development scripts
```

## Quick Start

1. Clone the repository:
```bash
git clone https://github.com/yourusername/genomescript.git
cd genomescript
```

2. Set up the Python environment:
```bash
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
```

3. Set up the frontend:
```bash
cd frontend
npm install
```

4. Start the development servers:
```bash
./scripts/start-dev.sh
```

## Development

- Backend runs on http://localhost:8000
- Frontend runs on http://localhost:3000
- API documentation at http://localhost:8000/docs

## Testing

Run the test suite:
```bash
python -m pytest tests/
```

## Contributing

Please read our [Contributing Guidelines](CONTRIBUTING.md) before submitting pull requests.

## License

MIT License - see [LICENSE](LICENSE) file for details
