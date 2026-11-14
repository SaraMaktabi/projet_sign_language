Check your Python version:

```powershell
python --version
```



## Create and activate a virtual environment

Create it at the root of the repo:

```powershell
python -m venv .venv
```

Activate it:

- **Windows (PowerShell):** `.venv\Scripts\Activate.ps1`
- **Windows (CMD):** `.venv\Scripts\activate.bat`
- **Mac/Linux:** `source .venv/bin/activate`

You should see `(.venv)` at the start of your prompt.
If PowerShell blocks the activation, run once:

```powershell
Set-ExecutionPolicy -Scope CurrentUser RemoteSigned
```

## Install the dependencies

```powershell
cd Projet
python -m pip install --upgrade pip
python -m pip install -r requirements.txt
```

Installing TensorFlow can take a few minutes.

##  Verify the installation

```powershell
python -c "import tensorflow as tf, pandas, numpy, sklearn, cv2; print('TF', tf.__version__); print('OK')"
```

You should see `OK`. TensorFlow warnings (oneDNN, CPU) are normal.