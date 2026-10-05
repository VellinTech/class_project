# Class Project

A collection of small, self-contained FastAPI projects created for learning and practicing API development.

Each subfolder is a **completely independent project**. Every project has its own virtual environment, `requirements.txt`, `models.py`, `services.py`, and `main.py`. Nothing is shared between projects, so each one can be installed, run, and tested separately.

## Folder Structure

```text
class_project/

├── Event_Registration/
│   ├── .venv/
│   ├── src/
│   │   ├── models.py
│   │   └── services.py
│   ├── main.py
│   └── requirements.txt
│
├── Student_Registration/
│   ├── .venv/
│   ├── src/
│   │   ├── models.py
│   │   └── services.py
│   ├── main.py
│   └── requirements.txt
│
├── Fee_Payment/
│   ├── .venv/
│   ├── src/
│   │   ├── models.py
│   │   └── services.py
│   ├── main.py
│   └── requirements.txt
│
├── Product/
│   ├── .venv/
│   ├── src/
│   │   ├── models.py
│   │   └── services.py
│   ├── main.py
│   └── requirements.txt
│
├── User/
│   ├── .venv/
│   ├── src/
│   │   ├── models.py
│   │   └── services.py
│   ├── main.py
│   └── requirements.txt
│
└── Vehicle/
    ├── .venv/
    ├── src/
    │   ├── models.py
    │   └── services.py
    ├── main.py
    └── requirements.txt
```

## Running Any Project

Every project follows the same setup process. Replace `<folder>` with the project you want to run.

### 1. Move into the project folder

```bash
cd class_project/<folder>
```

### 2. Create a virtual environment

Skip this step if `.venv/` already exists.

```bash
python -m venv .venv
```

### 3. Activate the virtual environment

| Shell          | Command                                                                                |
| -------------- | -------------------------------------------------------------------------------------- |
| Git Bash / WSL | `source .venv/Scripts/activate` on Windows or `source .venv/bin/activate` on Linux/Mac |
| PowerShell     | `.venv\Scripts\Activate.ps1`                                                           |
| Command Prompt | `.venv\Scripts\activate.bat`                                                           |

You should see `(.venv)` at the beginning of your terminal prompt after activation.

### 4. Install dependencies

```bash
pip install -r requirements.txt
```

### 5. Start the server

```bash
uvicorn main:app --reload
```

If `uvicorn` gives a `Permission denied` error in Git Bash on Windows, use:

```bash
python -m uvicorn main:app --reload
```

### 6. Open Swagge
