# PersonalFinanceManager 📈💰📊

Gestor de Finanzas Personales.

---

## 🚀 Características

- Registro de transacciones
- Visualización de transacciones
- Visualización de balance actual
- Edición de transacciones
- Eliminación de transacciones
- Visualización gráfica con `matplotlib` de gastos mensuales por categoría
- Carga y guardado automático de datos en archivo JSON
- Test básico con `pytest` para validar comportamiento del sistema

---

## 🔧 Instalación

1. Clonar este repositorio:
    ```bash
   git clone https://github.com/JulianaCarvajal/PersonalFinanceManager.git
   cd PersonalFinanceManager
   ```
2. Crear y activar un entorno virtual
    ```bash
   python -m venv .venv
   # PowerShell
   .\.venv\Scripts\Activate.ps1
   # Git Bash
   source .venv/Scripts/activate
   ```
3. Instalar dependencias:
    ```bash
   pip install -r requirements.txt
   ```

---

## ▶️ Uso

Ejecutar el archivo principal:
```
python main.py
```
Se mostrará el menú del gestor y se podrá navegar utilizando la línea de comandos.

---

## 📊 Visualización de gastos

El sistema permite mostrar los gastos de un mes determinado en un gráfico tipo **donut**, agrupados por categoría.


---

## 🧪 Testeo

Puedes ejecutar los tests con:
```
# PowerShell
$env:PYTHONPATH="."
pytest

# Git Bash / Linux / Mac
PYTHONPATH=. pytest
```

---

## 📂 Estructura del proyecto

```
PersonalFinanceManager/
│
├── main.py
├── manager.py
├── models.py
├── .gitignore
├── requirements.txt
├── README.md
├── transactions.json          # Ignorado por Git
├── tests/
│   └── test_finance_manager.py
```

