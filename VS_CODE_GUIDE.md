# 🎨 VS Code Quick Reference Guide

## 📂 Open Project in VS Code

**Already Open!** Your project is now open in VS Code at `/home/ubuntu/Downloads/demo`

---

## 🗂️ File Explorer Organization

### Left Sidebar (File Explorer)
```
demo/
├── 📄 Core Files (Main Implementation)
│   ├── fastapi_service.py       ← START HERE: FastAPI + LangGraph
│   ├── agents.py                ← 4-agent system
│   ├── streamlit_app.py         ← Beautiful UI
│   └── database.py              ← Data persistence
│
├── 🧪 Tests (Quality Assurance)
│   ├── tests/
│   │   ├── unit/test_agents.py  ← 17 unit tests
│   │   └── integration/
│   │       └── test_workflow.py ← Integration tests
│   └── pytest.ini               ← Test config
│
├── 🚀 Deployment
│   ├── Dockerfile               ← Production build
│   ├── docker-compose.yml       ← Orchestration
│   └── requirements.txt          ← Dependencies
│
├── 📚 Documentation
│   ├── README.md                ← Start here
│   ├── ARCHITECTURE.md          ← Technical design
│   └── PROJECT_STRUCTURE.md     ← This guide
│
├── 🎬 Video Guides (NEW)
│   ├── VIDEO_GUIDE.md
│   ├── VIDEO_RECORDING_SCRIPT.md
│   ├── RECORDING_START_GUIDE.md
│   └── VIDEO_RECORDING_SUMMARY.txt
│
└── 📊 Evaluation Reports
    ├── Evaluation_Report_Anupam_Dosi.md
    └── Evaluation_Scorecard_Anupam_Dosi.txt
```

---

## ⌨️ VS Code Keyboard Shortcuts

### Navigation
| Shortcut | Action |
|----------|--------|
| `Ctrl+P` | Open file by name |
| `Ctrl+Shift+E` | Focus on file explorer |
| `Ctrl+B` | Toggle sidebar |
| `Ctrl+\` | Split editor |
| `Ctrl+Tab` | Switch between open files |

### Editing
| Shortcut | Action |
|----------|--------|
| `Ctrl+/` | Toggle comment |
| `Ctrl+Shift+L` | Select all occurrences |
| `Ctrl+H` | Find and replace |
| `Ctrl+F` | Find |
| `Alt+Up/Down` | Move line up/down |

### Debugging
| Shortcut | Action |
|----------|--------|
| `F5` | Start debugging |
| `F10` | Step over |
| `F11` | Step into |
| `Shift+F11` | Step out |
| `Ctrl+Shift+D` | Debug panel |

---

## 🏃 Running from VS Code

### Method 1: Using Debug (F5)
1. Press **F5** or go to **Run** → **Start Debugging**
2. Select configuration (FastAPI, Streamlit, or Tests)
3. View output in Debug Console

### Method 2: Using Terminal
1. Press **Ctrl+`** to open integrated terminal
2. Run commands:
   ```bash
   python fastapi_service.py
   streamlit run streamlit_app.py --server.port=8501
   pytest tests/ -v --cov
   ```

### Method 3: Using Tasks
1. Press **Ctrl+Shift+B** to run build task
2. Select from available tasks

---

## 📌 Must-Read Files (In Order)

### 1. **README.md** (2 min read)
   - Project overview
   - Quick start
   - Features summary

### 2. **ARCHITECTURE.md** (5 min read)
   - System design
   - Component overview
   - Data flow

### 3. **fastapi_service.py** (10 min read)
   - Main application
   - LangGraph orchestration
   - Claude API integration
   - Routes and endpoints

### 4. **agents.py** (10 min read)
   - 4 specialized agents
   - Risk calculation
   - Decision logic

### 5. **streamlit_app.py** (5 min read)
   - UI implementation
   - 3 tabs (Single, Batch, Analytics)
   - Visualizations

### 6. **tests/unit/test_agents.py** (5 min read)
   - Test examples
   - 17 comprehensive tests
   - Sample data fixtures

---

## 🔍 Code Navigation Tips

### Go to Definition
```
Place cursor on function/class name
Right-click → "Go to Definition"
Or: Ctrl+Click on name
```

### Find All References
```
Right-click on symbol
Select "Find All References"
Shows all places where symbol is used
```

### Search in Files
```
Ctrl+Shift+F - Opens search across entire project
Useful for finding specific patterns or errors
```

### Peek Definition
```
Ctrl+Shift+F10 - Peek at definition without navigating
Perfect for quick understanding
```

---

## 🎨 Syntax Highlighting & Extensions

### Recommended Extensions (Install from Extensions sidebar)

1. **Python** (Microsoft)
   - Best Python support
   - IntelliSense
   - Debugging

2. **Pylance**
   - Advanced type checking
   - Better IntelliSense

3. **Black Formatter**
   - Auto-format Python code
   - Consistent style

4. **Pytest**
   - Run tests directly
   - View test results

5. **Thunder Client**
   - Test API endpoints
   - Like Postman but in VS Code

6. **Docker**
   - Docker file support
   - Container management

### Install Instructions
1. Click Extensions icon (Ctrl+Shift+X)
2. Search for extension name
3. Click "Install"
4. Reload window

---

## 🧪 Running Tests

### Via Terminal
```bash
# Run all tests
pytest tests/ -v --cov=. --cov-report=term-missing

# Run specific file
pytest tests/unit/test_agents.py -v

# Run specific test
pytest tests/unit/test_agents.py::TestApplicantProfileAgent::test_employed_profile -v
```

### Via Debug Configuration
1. Press **F5**
2. Select "Tests" configuration
3. View results in Debug Console

### Via Pytest Explorer (If installed)
1. Click Test icon in sidebar
2. View all tests in tree format
3. Right-click → Run test

---

## 🐛 Debugging Python Code

### Setting Breakpoints
1. Click left of line number to set breakpoint (red dot appears)
2. Press **F5** to start debugging
3. Execution pauses at breakpoint
4. Use Debug Console to inspect variables

### Debug Controls
- **F5** - Continue
- **F10** - Step over
- **F11** - Step into
- **Shift+F11** - Step out
- **Ctrl+Shift+D** - View variables panel

### Variables Panel
Shows:
- Local variables
- Global variables
- Watched expressions
- Call stack

---

## 💡 Code Snippets & IntelliSense

### Auto-completion
- Start typing and press **Ctrl+Space**
- Shows available completions
- Press **Enter** to insert

### Function Signature
- Hover over function name
- Shows parameters and return type
- Extremely helpful!

### Parameter Hints
- Type function name and open parenthesis
- See all available parameters
- Press **Escape** to close hints

---

## 📋 Project Statistics

### Files Count
```
Total Python files: 10+
Test files: 2
Documentation files: 15+
Configuration files: 5
```

### Lines of Code
```
fastapi_service.py: ~300 lines
agents.py: ~250 lines
streamlit_app.py: ~400 lines
tests: ~400 lines (combined)
```

### Test Coverage
```
97% coverage on core code
All critical paths tested
98% coverage on agents.py
```

---

## 🔗 Important File Relationships

```
Entry Points:
├── fastapi_service.py (API server)
│   ├── imports agents.py
│   ├── imports database.py
│   └── uses LangGraph
│
├── streamlit_app.py (UI)
│   ├── calls FastAPI endpoints
│   ├── imports database.py
│   └── displays results
│
└── tests/
    ├── imports agents.py
    ├── imports fastapi_service.py
    └── imports conftest.py (fixtures)

Dependencies:
├── agents.py (core business logic)
│   ├── Applicant Profile Agent
│   ├── Financial Risk Agent
│   ├── Loan Decision Agent
│   └── Compliance Agent
│
├── database.py (persistence)
│   └── SQLite integration
│
└── requirements.txt
    ├── FastAPI
    ├── Streamlit
    ├── LangGraph
    ├── Anthropic (Claude)
    └── Pytest
```

---

## ⚙️ VS Code Settings

### Recommended Settings (already configured)
```json
{
  "python.linting.enabled": true,
  "python.linting.pylintEnabled": true,
  "python.linting.flake8Enabled": true,
  "python.formatting.provider": "black",
  "[python]": {
    "editor.defaultFormatter": "ms-python.black-formatter",
    "editor.formatOnSave": true,
    "editor.rulers": [88]
  }
}
```

---

## 🚀 Common Workflows

### Workflow 1: Understanding the System
1. Open **README.md**
2. Read **ARCHITECTURE.md**
3. Open **agents.py** and explore agents
4. Open **fastapi_service.py** and see how agents are orchestrated
5. Check **tests/** to see usage examples

### Workflow 2: Making Code Changes
1. Make changes in editor
2. Save file (Ctrl+S)
3. Run tests (Ctrl+Shift+P → pytest)
4. View results in integrated terminal
5. Debug if needed (F5)

### Workflow 3: Recording Video
1. Open **VIDEO_RECORDING_SCRIPT.md**
2. Read through script
3. Open terminal (Ctrl+`)
4. Verify services: `curl http://localhost:8000/health`
5. Open browser to http://localhost:8501
6. Start OBS recording

### Workflow 4: Debugging an Issue
1. Find file with issue
2. Set breakpoint (click line number)
3. Press F5 to start debugging
4. Step through code (F10/F11)
5. Inspect variables in Variables panel
6. Understand the problem
7. Fix and test

---

## 📱 Split Screen Editing

### View Multiple Files
```
Ctrl+\ - Split editor vertically
Ctrl+- - Split horizontally
Ctrl+Backspace - Close split
```

### Example: Compare Implementation & Tests
1. Open agents.py in left pane
2. Press Ctrl+\
3. Open test_agents.py in right pane
4. Compare implementation with tests

---

## 🎯 Quick Actions

### Format Code
```
Ctrl+Shift+P → "Format Document"
Formats entire file with Black
```

### Rename Symbol
```
F2 on a symbol
Renames all occurrences
Great for refactoring
```

### Go to Line
```
Ctrl+G
Type line number
Navigate directly to line
```

### Open Recent Files
```
Ctrl+R
Shows list of recently opened files
Quick switch between files
```

---

## 🔧 Troubleshooting

### Python Extension Not Working
1. Press **Ctrl+Shift+P**
2. Type "Python: Select Interpreter"
3. Choose `/home/ubuntu/Downloads/demo/venv/bin/python`
4. Reload window

### Tests Not Running
1. Check pytest is installed: `pip list | grep pytest`
2. Make sure in correct directory
3. Check pytest.ini exists
4. Run `pytest --version`

### IntelliSense Not Working
1. Try reloading window (Ctrl+K, Ctrl+R)
2. Check Python extension is enabled
3. Try restarting VS Code

### Debugging Not Starting
1. Check breakpoint is set (red dot)
2. Make sure file is saved
3. Check Debug Console for errors
4. Try F5 again

---

## 📚 Learning Resources

### In This Project
- Code examples in tests/
- Comments explaining complex logic
- Clear variable names
- Well-structured functions

### Online Resources
- https://code.visualstudio.com/docs/editor/debugging
- https://www.python.org/dev/peps/pep-0008/ (Python style)
- https://fastapi.tiangolo.com/ (FastAPI docs)
- https://streamlit.io/ (Streamlit docs)

---

## ✅ Getting Started Checklist

- [ ] Project is open in VS Code
- [ ] Read README.md
- [ ] Read ARCHITECTURE.md
- [ ] Explore fastapi_service.py
- [ ] Look at agents.py
- [ ] Check tests/ folder
- [ ] Run tests (Ctrl+Shift+P → pytest)
- [ ] Start FastAPI (Terminal)
- [ ] Start Streamlit (Terminal)
- [ ] Visit http://localhost:8501
- [ ] Understanding the system complete!

---

## 🎉 You're All Set!

You now have:
✅ Project open in VS Code
✅ File structure visible
✅ All shortcuts available
✅ Debug configurations ready
✅ Documentation at hand

Start exploring! Any questions, use Ctrl+Shift+P and search for help.

---

**Happy coding! 🚀**
