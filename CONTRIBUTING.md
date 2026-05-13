# 🤝 Contributing to Medical Billing & Automatic Servo Dispenser

First off — **thank you for taking the time to contribute!** 🎉  
Every contribution, big or small, makes this project better for everyone.

This document provides all the guidelines you need to contribute effectively.

---

## 📚 Table of Contents

- [📋 Code of Conduct](#-code-of-conduct)
- [🚀 How to Get Started](#-how-to-get-started)
- [🐛 Reporting Bugs](#-reporting-bugs)
- [✨ Requesting Features](#-requesting-features)
- [🔧 Setting Up the Development Environment](#-setting-up-the-development-environment)
- [📦 Making Changes](#-making-changes)
- [✅ Pull Request Guidelines](#-pull-request-guidelines)
- [📝 Commit Message Convention](#-commit-message-convention)
- [💡 Ideas for Contribution](#-ideas-for-contribution)
- [🎨 Style Guidelines](#-style-guidelines)

---

## 📋 Code of Conduct

By participating in this project, you agree to uphold the following:

- 🤗 **Be welcoming** — Beginners and experts are equally valued here
- 💬 **Be respectful** — Constructive criticism only; no personal attacks
- 🧠 **Be collaborative** — Help others understand your changes
- 🕊️ **Be patient** — Maintainers review PRs in their spare time

---

## 🚀 How to Get Started

Not sure where to begin? Here are some great entry points:

| Label | What it means |
|---|---|
| `good first issue` | Small, well-scoped tasks — perfect for first-timers |
| `help wanted` | Maintainers are actively seeking help on this |
| `bug` | Something isn't working correctly |
| `enhancement` | A new feature or improvement request |
| `documentation` | Improving docs, comments, or the README |

Browse [open issues](https://github.com/suyashsahu00/Medical_Dispenser_Project/issues) to find something that interests you.

---

## 🐛 Reporting Bugs

Found something broken? Please [open a bug report](https://github.com/suyashsahu00/Medical_Dispenser_Project/issues/new) and include:

### Bug Report Template

```
**Describe the bug**
A clear description of what the bug is.

**To Reproduce**
Steps to reproduce the behavior:
1. Go to '...'
2. Click on '...'
3. See error

**Expected behavior**
What you expected to happen.

**Screenshots / Logs**
If applicable, paste console output or attach screenshots.

**Environment:**
- OS: [e.g. Windows 11]
- Python Version: [e.g. 3.11]
- Arduino IDE Version: [e.g. 2.3.0]
- Arduino Board: [e.g. UNO]
- COM Port: [e.g. COM4]
- pyserial Version: [run `pip show pyserial`]
```

---

## ✨ Requesting Features

Have a great idea? [Open a feature request](https://github.com/suyashsahu00/Medical_Dispenser_Project/issues/new) and describe:

- **What problem does this solve?**
- **What is your proposed solution?**
- **Are there any alternatives you've considered?**

---

## 🔧 Setting Up the Development Environment

### Step 1 — Fork & Clone

```bash
# Fork the repository on GitHub, then:
git clone https://github.com/YOUR_USERNAME/Medical_Dispenser_Project.git
cd Medical_Dispenser_Project
```

### Step 2 — Create a Virtual Environment

```bash
cd PythonApp
python -m venv venv

# Activate (Windows)
venv\Scripts\activate

# Activate (macOS/Linux)
source venv/bin/activate
```

### Step 3 — Install Dependencies

```bash
pip install -r requirements.txt
```

### Step 4 — Verify Everything Works

```bash
# Run the app (Arduino not required — it will start in Demo Mode)
python app_billing_two_boxes.py
```

You should see the billing GUI open without errors.

---

## 📦 Making Changes

### Step 1 — Sync with Upstream

Always start from the latest `main` branch:

```bash
git remote add upstream https://github.com/suyashsahu00/Medical_Dispenser_Project.git
git fetch upstream
git checkout main
git merge upstream/main
```

### Step 2 — Create a Feature Branch

Never work directly on `main`. Create a descriptive branch:

```bash
# For a new feature
git checkout -b feature/your-feature-name

# For a bug fix
git checkout -b fix/description-of-bug

# For documentation
git checkout -b docs/what-you-are-improving
```

### Step 3 — Make Your Changes

- Keep changes **focused** — one feature or fix per PR
- Test your changes thoroughly before committing
- Update `medicines.csv` documentation if you change the schema
- If you add new dependencies, update `requirements.txt`:
  ```bash
  pip freeze > requirements.txt
  ```

### Step 4 — Commit Your Changes

```bash
git add .
git commit -m "✨ Add: your feature description"
git push origin feature/your-feature-name
```

---

## ✅ Pull Request Guidelines

When opening a PR, please:

1. **Fill out the PR template completely**
2. **Link the related issue** using `Closes #123` in the description
3. **Keep PRs small and focused** — large PRs are harder to review
4. **Add screenshots** if your change affects the UI
5. **Ensure no new warnings** appear in the console
6. **Test with and without Arduino** connected (Demo Mode must still work)

### PR Checklist

```
[ ] My code follows the style guidelines of this project
[ ] I have tested the app in Demo Mode (no Arduino)
[ ] I have tested with Arduino connected (if hardware-related)
[ ] I have updated medicines.csv documentation if schema changed
[ ] I have updated requirements.txt if I added new dependencies
[ ] My changes don't break the PDF bill generation
[ ] I have added comments for any non-obvious logic
```

---

## 📝 Commit Message Convention

Use the following emoji prefixes for consistent, readable commit history:

| Emoji | Prefix | When to Use |
|:---:|---|---|
| ✨ | `Add:` | New feature or file |
| 🐛 | `Fix:` | Bug fix |
| ♻️ | `Refactor:` | Code refactoring (no behavior change) |
| 📝 | `Docs:` | Documentation only changes |
| ⚡ | `Perf:` | Performance improvements |
| 🎨 | `Style:` | UI/UX or formatting changes |
| 🔧 | `Config:` | Configuration changes |
| 🧪 | `Test:` | Adding or updating tests |
| 🗑️ | `Remove:` | Deleting unused code or files |
| ⬆️ | `Upgrade:` | Dependency upgrades |

### Good Commit Examples

```bash
git commit -m "✨ Add: patient name field to PDF invoice"
git commit -m "🐛 Fix: serial port not closing on app exit"
git commit -m "📝 Docs: add wiring diagram to README"
git commit -m "⚡ Perf: cache medicines.csv on startup to reduce disk reads"
```

---

## 💡 Ideas for Contribution

Looking for inspiration? Here are open improvement areas:

### 🔰 Beginner-Friendly
- [ ] Add tooltips to UI buttons explaining what each does
- [ ] Validate expiry dates in `medicines.csv` and warn about expired stock
- [ ] Add a "Clear Cart" button to the billing interface
- [ ] Improve error messages with more helpful guidance

### 🔶 Intermediate
- [ ] Migrate medicine database from CSV to SQLite
- [ ] Add low-stock alerts when quantity falls below a threshold
- [ ] Implement an "Undo" feature for cart operations
- [ ] Add daily sales summary report generation

### 🔴 Advanced
- [ ] Build a web interface using Flask or FastAPI
- [ ] Add pharmacist login/authentication
- [ ] Implement barcode scanning for medicine lookup
- [ ] Add thermal/receipt printer support
- [ ] Support multiple language interfaces (Hindi, etc.)
- [ ] Add a dashboard with analytics and charts

---

## 🎨 Style Guidelines

### Python

- Follow [PEP 8](https://pep8.org/) conventions
- Use **4 spaces** for indentation (no tabs)
- Keep line length ≤ **100 characters**
- Add docstrings to all functions:
  ```python
  def get_box_number(med_type: str) -> int:
      """
      Maps a medicine type string to its dispenser box number (1–4).
      
      Args:
          med_type: The 'type' field from medicines.csv (e.g., 'box1', 'painkiller')
      
      Returns:
          Integer box number between 1 and 4.
      """
  ```
- Use **type hints** wherever possible
- Prefer **f-strings** over `.format()` or `%` formatting

### Arduino (C++)

- Use **2-space indentation**
- Add a comment above every function explaining its purpose
- Avoid `delay()` for durations longer than 1 second — use `millis()` instead
- Keep `loop()` non-blocking where possible

### CSV Data

- Always include all columns when adding new rows
- Use consistent casing for the `type` field: `box1`, `box2`, `box3`, `box4`
- Date format for `expiry_date`: `MM/YYYY`
- Date format for `date_of_sale`: `YYYY-MM-DD`

---

## ❓ Questions?

If you have any questions not answered here, feel free to:

- [Open a Discussion](https://github.com/suyashsahu00/Medical_Dispenser_Project/discussions)
- [Open an Issue](https://github.com/suyashsahu00/Medical_Dispenser_Project/issues) with the `question` label

---

<div align="center">

**Thank you for contributing! 🚀**  
*Every line of code, every bug report, every suggestion — it all matters.*

</div>
