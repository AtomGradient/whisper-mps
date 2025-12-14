# Development Setup (macOS)

This project uses **PDM** for dependency management and virtual environments. The instructions below assume **macOS** and use **Homebrew**, which is the simplest and most reliable setup.

---

## Prerequisites

Make sure you have the following installed:

* **macOS** (Apple Silicon recommended for MPS)
* **Python 3.10+**
* **Homebrew**

Check versions:

```bash
python3 --version
brew --version
```

If Homebrew is not installed, see [https://brew.sh](https://brew.sh)

---

## 1. Install PDM via Homebrew

Install PDM globally:

```bash
brew install pdm
```

Verify installation:

```bash
pdm --version
```

---

## 2. Clone the Repository

```bash
git clone https://github.com/<your-org>/whisper-mps.git
cd whisper-mps
```

---

## 3. Configure PDM Virtual Environment

Configure PDM to create the virtual environment inside the project directory:

```bash
pdm config venv.in_project true
```

This will create a `.venv/` folder at the project root.

---

## 4. Install Dependencies

Install all project dependencies and the package itself (editable mode):

```bash
pdm install
```

This will:

* Create a virtual environment
* Install all dependencies from `pyproject.toml`
* Install `whisper-mps` in editable (development) mode

---

## 5. Activate the Virtual Environment (Optional)

You can activate the environment manually:

```bash
source .venv/bin/activate
```

Or run commands without activating it using `pdm run`.

---

## 6. Run the CLI

The CLI entry point is defined in `pyproject.toml`:

```toml
[project.scripts]
whisper-mps = "whisper_mps.cli:main"
```

Run the CLI:

```bash
pdm run whisper-mps --help
```

Or, if the virtual environment is activated:

```bash
whisper-mps --help
```

---

## 7. Development Workflow

* Edit source files under `whisper_mps/`
* Changes take effect immediately (editable install)
* No reinstall needed

Run Python directly:

```bash
pdm run python -m whisper_mps.cli
```

---

## 8. Useful Commands

```bash
pdm info           # Show project & environment info
pdm list           # List installed dependencies
pdm update         # Update dependencies
pdm run pytest     # Run tests (if configured)
```

---

## 9. Troubleshooting

### `pdm: command not found`

Ensure Homebrew is on your PATH:

```bash
echo $PATH
which pdm
```

If needed, restart your shell:

```bash
exec zsh
```

---

## Notes

* This project targets **Apple Metal (MPS)** via PyTorch
* Apple Silicon Macs (M Series) are strongly recommended
* Python versions below 3.10 are not supported

---

Happy hacking 🚀
