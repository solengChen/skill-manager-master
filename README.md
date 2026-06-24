# Skill Manager - Installation Package

## 📦 Package Contents

```
skill-manager-master/
├── SKILL.md                    # Skill definition file (core)
├── scripts/                    # Python scripts directory
│   ├── scan_skills.py         # Skill scanning script
│   ├── update_skill_table.py  # Skill table update script
│   └── sync_skills.py         # Sync check script
├── 安装说明.md                 # Chinese installation guide
├── README.md                  # English installation guide
├── install.bat                # Windows quick install script
└── install.sh                # Linux/Mac install script (alternative)
```

## 🚀 Quick Install (Windows)

### Method 1: Using Install Script
```cmd
# Enter the package directory and double-click install.bat
# Or run in command line:
install.bat
```

### Method 2: Manual Installation
```cmd
# 1. Create global skills directory
mkdir %USERPROFILE%\.agents\skills\skill-manager

# 2. Copy all files to that directory
copy SKILL.md %USERPROFILE%\.agents\skills\skill-manager\
copy scripts\* %USERPROFILE%\.agents\skills\skill-manager\

# 3. Run update script to initialize skill table
python %USERPROFILE%\.agents\skills\skill-manager\update_skill_table.py
```

## 📋 Installation Requirements

### Required Environment
- **Python 3.6+**
- **PyYAML** (for parsing YAML frontmatter)

### Install PyYAML
```bash
pip install pyyaml
```

## ✅ Verify Installation

After installation, run the following command to verify:
```bash
python %USERPROFILE%\.agents\skills\skill-manager\sync_skills.py
```

Should output something like:
```json
{
  "installed_count": 5,
  "recorded_count": 5,
  "new_skills": [],
  "removed_skills": [],
  "changed_skills": [],
  "needs_sync": false
}
```

## 🎯 Usage

### Call Skill Manager
In Trae AI Agent, you can:
1. Call "Skill Manager" through Trae's skill system
2. Or use script commands directly

### Common Commands

```bash
# Scan all installed skills
python %USERPROFILE%\.agents\skills\skill-manager\scan_skills.py

# Update skill table (JSON + Markdown)
python %USERPROFILE%\.agents\skills\skill-manager\update_skill_table.py

# Check sync status
python %USERPROFILE%\.agents\skills\skill-manager\sync_skills.py
```

## 📖 Features

### 1. Automatic Skill Scanning
- Scan global skills directory: `~/.agents/skills/`
- Scan project-local skills directory: `./.trae/skills/`
- Parse SKILL.md frontmatter to get skill information

### 2. Skill Table Management
- JSON format: `skill_table.json` (for program reading)
- Markdown format: `技能管理表.md` (for human reading)
- Auto-categorization: AI, Dev Tools, Testing, Cloud Services, etc.

### 3. Sync Check
- Detect new skills
- Detect removed skills
- Detect skill description changes
- needs_sync flag to remind updates

### 4. Requirement-First Analysis
- Understand user requirements first
- Analyze task complexity and required skill types
- Evaluate if skills are really needed (avoid over-engineering)

## 🛠️ Customization

### Modify Classification Keywords
Edit keyword lists in `scripts/update_skill_table.py`:

```python
ai_keywords = ['ai', 'image', 'face', 'generate', ...]
dev_keywords = ['code', 'develop', 'design', ...]
# Add or modify keywords to fit your needs
```

### Modify Scan Directories
Edit `scripts/scan_skills.py` to add more scan paths:

```python
# In scan_skills() function, add
custom_skills_dir = Path('your/custom/path')
installed_skills.extend(scan_directory(custom_skills_dir))
```

## ❓ FAQ

### Q: Can't find skill after installation?
A: Make sure files are copied to correct location: `%USERPROFILE%\.agents\skills\skill-manager\`

### Q: Python scripts won't run?
A: Make sure Python and PyYAML are installed. Run `pip install pyyaml` to reinstall dependencies

### Q: How to uninstall?
A: Simply delete `%USERPROFILE%\.agents\skills\skill-manager\` directory

---

**Version**: 1.0.0  
**Created**: 2026-06-25  
**Author**: AI Assistant
