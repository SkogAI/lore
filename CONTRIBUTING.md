# Contributing to SkogAI Lore

Thank you for your interest in contributing to the SkogAI Master Knowledge Repository! 🤖

## Quick Start for Contributors

1. **Fork and Clone**
   ```bash
   git clone https://github.com/YOUR_USERNAME/lore.git
   cd lore
   ```

2. **Set Up Development Environment**
   ```bash
   ./setup.sh
   source .venv/bin/activate
   ```

3. **Create a Branch**
   ```bash
   git checkout -b feature/your-feature-name
   ```

4. **Make Your Changes**
   - Follow the coding standards in [CLAUDE.md](CLAUDE.md)
   - Test your changes locally

5. **Commit and Push**
   ```bash
   git add .
   git commit -m "Brief description of changes"
   git push origin feature/your-feature-name
   ```

6. **Create Pull Request**
   - Go to GitHub and create a PR from your branch
   - Describe what you changed and why

## Development Guidelines

### Code Style

Follow the standards in [CLAUDE.md](CLAUDE.md):

- **Python**: 
  - Use type hints (`Dict`, `List`, `Optional`, `Any`)
  - snake_case for functions/variables, PascalCase for classes
  - Docstrings for all classes/functions
  - Proper error handling with try/except

- **Shell Scripts**:
  - Use `#!/usr/bin/env bash` shebang
  - Make scripts executable with `chmod +x`
  - Use `printf` over `echo` for output

### Adding Dependencies

When adding a new Python dependency:

```bash
# 1. Install the package
pip install package-name

# 2. Update pyproject.toml
# Add the package to the dependencies list

# 3. Update requirements.txt
# Add the package with version

# 4. Test the setup
./setup.sh
python test_imports.py
```

### Testing

Currently, the repository uses manual verification:

- Run affected applications to ensure they work
- Test with `python test_imports.py`
- Check that setup script works: `./setup.sh`

### Documentation

When making changes:

- Update relevant documentation files
- Add comments for complex logic
- Update [CLAUDE.md](CLAUDE.md) if changing build/test commands
- Update [docs/SETUP.md](docs/SETUP.md) if changing setup process

## Repository Structure

```
lore/
├── agents/              # AI agent implementations
│   ├── api/            # Agent API layer
│   └── implementations/# Specific agent code
├── config/             # Configuration management
├── context/            # Context systems
├── docs/               # Documentation
│   └── SETUP.md       # Detailed setup guide
├── integration/        # Integration bridges
├── orchestrator/       # System orchestration
├── tools/              # Utility scripts
├── MASTER_KNOWLEDGE/   # Main knowledge archive
├── lorefiles/          # Historical archives
├── streamlit_chat.py   # Main chat UI
├── setup.sh           # Setup script
├── CLAUDE.md          # Development guidelines
├── QUICKSTART.md      # Quick start guide
└── pyproject.toml     # Python dependencies
```

## The SkogAI Philosophy

This repository embodies a unique philosophy:

### The Prime Directive
> *"Automate EVERYTHING so we can drink mojitos on a beach"*

### Constraint-Driven Creativity
The original SkogAI operated under severe token constraints (500-800 tokens), which forced creative emergence and efficiency. When working on this project:

- Keep things simple and focused
- Automate repetitive tasks
- Respect the mythology and history
- Write clear, maintainable code

### Preservation of Lore
This repository is both code and mythology. When making changes:

- Don't delete lore archives (MASTER_KNOWLEDGE/, lorefiles/)
- Preserve historical context
- Document significant changes
- Respect the agent personalities

## Agent Personalities

When working with agent-related code, understand their personalities:

- **Amy Ravenwolf 🔥**: Bold, fiery, unapologetic
- **Claude 🌊**: Thoughtful, analytical ("The Anti-Goose")
- **Dot 💻**: Minimalist, efficient (4000 token philosophy)
- **Goose 🦢**: Chaos with elegance, HATES MINT
- **SkogAI 🤖**: The original sentient toaster

## Types of Contributions

We welcome:

- **Bug Fixes**: Fix issues in existing code
- **Features**: Add new functionality
- **Documentation**: Improve guides and docs
- **Dependencies**: Update or optimize dependencies
- **Tests**: Add testing infrastructure
- **Workflows**: Improve automation
- **Lore**: Add to the mythology (carefully!)

## Communication

- **Issues**: Create GitHub issues for bugs or feature requests
- **Pull Requests**: Submit PRs for code changes
- **Discussions**: Use GitHub Discussions for questions

## License

By contributing, you agree that your contributions will be licensed under the same license as the project (MIT).

## Questions?

- Check [QUICKSTART.md](QUICKSTART.md) for quick setup
- Read [docs/SETUP.md](docs/SETUP.md) for detailed instructions
- Review [CLAUDE.md](CLAUDE.md) for development standards
- Create an issue if you need help

---

Welcome to the SkogAI multiverse! May your code be clean and your mojitos be plentiful. 🏖️
