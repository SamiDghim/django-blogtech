# Development Scripts

This directory contains shell scripts for common development tasks in the StudyBuddy project.

## Available Scripts

### 🔧 `./bin/dev` - Main Development Helper
A comprehensive script that provides access to all development operations.

**Usage:**
```bash
./bin/dev [command]
```

**Available Commands:**

#### Code Quality
- `format` - Format code with Black and isort
- `lint` - Run linting checks (flake8, black, isort)  
- `pylint` - Run advanced static analysis
- `check` - Run all checks (lint + pylint)
- `fix` - Format code then run lint checks

#### Django Operations
- `shell` - Open Django shell_plus (enhanced shell)
- `urls` - Show all Django URLs
- `migrate` - Run Django migrations
- `makemigrations` - Create new migrations
- `collectstatic` - Collect static files
- `test` - Run Django tests
- `seed` - Seed database with sample data

#### Build Operations
- `rebuild-css` - Rebuild Tailwind CSS
- `build` - Build CSS and JS assets

#### Help
- `help` - Show help message

### 🔍 `./bin/lint` - Linting Script
Runs comprehensive linting checks on your code.

**Usage:**
```bash
./bin/lint [target]    # target defaults to "base/ studybud/"
./bin/lint base/views.py    # lint specific file
```

**What it checks:**
- flake8 (PEP 8 compliance)
- Black formatting
- isort import organization

### 🎨 `./bin/format` - Code Formatting Script  
Automatically formats your code using Black and isort.

**Usage:**
```bash
./bin/format [target]    # target defaults to "base/ studybud/"
./bin/format base/views.py    # format specific file
```

### 🔍 `./bin/pylint` - Advanced Analysis Script
Runs Pylint with Django plugins for advanced static analysis.

**Usage:**
```bash
./bin/pylint [target]    # target defaults to "base/ studybud/"
```

## Quick Examples

```bash
# Format all code and run checks
./bin/dev fix

# Run comprehensive analysis
./bin/dev check

# Open enhanced Django shell
./bin/dev shell

# Show all Django URLs
./bin/dev urls

# Seed database with test data
./bin/dev seed

# Build frontend assets
./bin/dev build
```

## Integration with Package.json

The `package.json` now focuses only on frontend build operations:
- CSS building with Tailwind
- JavaScript bundling with esbuild
- Development watching

All Django-related linting and development operations have been moved to these shell scripts for better organization and clarity.

## Benefits

1. **Clear Separation**: Frontend (npm) vs Backend (shell scripts)
2. **Better UX**: Colored output and helpful messages
3. **Error Handling**: Proper exit codes and error messages
4. **Flexibility**: Easy to customize and extend
5. **Discoverability**: `./bin/dev help` shows all available commands
