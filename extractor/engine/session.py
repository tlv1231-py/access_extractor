import os
from contextlib import contextmanager

import pythoncom
import win32com.client


class AccessSessionError(Exception):
    pass


@contextmanager
def AccessSession(db_path: str):
    db_path = os.path.abspath(db_path)
    if not os.path.exists(db_path):
        raise FileNotFoundError(f"Database not found: {db_path}")

    app = None
    try:
        pythoncom.CoInitialize()
        app = win32com.client.Dispatch("Access.Application")
        app.Visible = False
        app.OpenCurrentDatabase(db_path)
        yield app
    except pythoncom.com_error as e:
        raise AccessSessionError(f"COM error interacting with Access: {e}") from e
    finally:
        if app is not None:
            try:
                app.CloseCurrentDatabase()
            except Exception:
                pass
            try:
                app.Quit()
            except Exception:
                pass
        pythoncom.CoUninitialize()
