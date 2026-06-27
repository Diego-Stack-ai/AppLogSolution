import os
import sys
import py_compile
import traceback

def main():
    print("=== 1. AUDIT FILE REALE ===")
    files = ["legacy_parser_adapter.py", "main.py", "test_simulation.py", "requirements.txt", "Dockerfile"]
    for f in files:
        if os.path.exists(f):
            print(f"FILE: {f}")
            print(f"PATH: {os.path.abspath(f)}")
            print(f"SIZE: {os.path.getsize(f)} bytes")
            print("STATO: PRESENTE\n")
        else:
            print(f"FILE: {f}\nSTATO: ASSENTE\n")

    print("=== 2. VALIDAZIONE SINTASSI PYTHON ===")
    for f in ["legacy_parser_adapter.py", "main.py", "test_simulation.py"]:
        try:
            py_compile.compile(f, doraise=True)
            print(f"{f}: PASS")
        except Exception as e:
            print(f"{f}: FAIL\n{traceback.format_exc()}")

    print("\n=== 3. VALIDAZIONE IMPORT REALI ===")
    libs = ["flask", "firebase_admin", "pdfplumber", "pypdf", "gunicorn", "psutil", "reportlab"]
    for lib in libs:
        try:
            mod = __import__(lib)
            version = getattr(mod, '__version__', 'N/A')
            print(f"LIBRERIA: {lib}\nIMPORT OK\nVERSIONE: {version}\n")
        except ImportError as e:
            print(f"LIBRERIA: {lib}\nFAIL\nERRORE: {e}\n")

if __name__ == "__main__":
    main()
