# LinLED Coffee Machine

The LinLED Coffee Machine Demonstrator, based on PyQt bindings PySide6, demonstrates LinLED's IR hand movement detection technology integrated within a coffee machine for intuitive user interactions.

### Prerequesites

- Python >= 3.10

### Instalation

#### Windows

```bash
python -m venv venv
.\venv\Scripts\activate
pip install -r requirements.txt
```

### Build

```bash
pyinstaller --onefile linled_coffee.py.py
```

### Try on local

```bash
python linled_coffee.py.py
```
