from __future__ import annotations

import ctypes
import json
import logging
from ctypes import wintypes

logger = logging.getLogger(__name__)

_TARGET_PREFIX = "access_extractor:"


def save_profile(name: str, repo: str, token: str) -> None:
    """Save a named repo/token pair to Windows Credential Manager."""
    target = f"{_TARGET_PREFIX}{name}"
    credential = json.dumps({"repo": repo, "token": token}).encode("utf-8")

    class CREDENTIAL(ctypes.Structure):
        _fields_ = [
            ("Flags", wintypes.DWORD),
            ("Type", wintypes.DWORD),
            ("TargetName", wintypes.LPWSTR),
            ("Comment", wintypes.LPWSTR),
            ("LastWritten", ctypes.c_uint64),
            ("CredentialBlobSize", wintypes.DWORD),
            ("CredentialBlob", ctypes.POINTER(ctypes.c_byte)),
            ("Persist", wintypes.DWORD),
            ("AttributeCount", wintypes.DWORD),
            ("Attributes", ctypes.c_void_p),
            ("TargetAlias", wintypes.LPWSTR),
            ("UserName", wintypes.LPWSTR),
        ]

    blob = (ctypes.c_byte * len(credential))(*credential)
    cred = CREDENTIAL()
    cred.Flags = 0
    cred.Type = 1  # CRED_TYPE_GENERIC
    cred.TargetName = target
    cred.Comment = f"Access Extractor profile: {name}"
    cred.CredentialBlobSize = len(credential)
    cred.CredentialBlob = blob
    cred.Persist = 2  # CRED_PERSIST_LOCAL_MACHINE
    cred.UserName = repo

    advapi32 = ctypes.windll.advapi32
    if not advapi32.CredWriteW(ctypes.byref(cred), 0):
        raise RuntimeError(f"Failed to save profile {name!r} to Credential Manager")
    logger.info("Saved profile: %s", name)


def load_profile(name: str) -> dict[str, str] | None:
    """Load a named profile from Windows Credential Manager."""
    target = f"{_TARGET_PREFIX}{name}"
    advapi32 = ctypes.windll.advapi32
    p_cred = ctypes.c_void_p()

    if not advapi32.CredReadW(target, 1, 0, ctypes.byref(p_cred)):
        return None

    try:
        class CREDENTIAL(ctypes.Structure):
            _fields_ = [
                ("Flags", wintypes.DWORD),
                ("Type", wintypes.DWORD),
                ("TargetName", wintypes.LPWSTR),
                ("Comment", wintypes.LPWSTR),
                ("LastWritten", ctypes.c_uint64),
                ("CredentialBlobSize", wintypes.DWORD),
                ("CredentialBlob", ctypes.POINTER(ctypes.c_byte)),
                ("Persist", wintypes.DWORD),
                ("AttributeCount", wintypes.DWORD),
                ("Attributes", ctypes.c_void_p),
                ("TargetAlias", wintypes.LPWSTR),
                ("UserName", wintypes.LPWSTR),
            ]

        cred = ctypes.cast(p_cred, ctypes.POINTER(CREDENTIAL)).contents
        blob = bytes(cred.CredentialBlob[i] for i in range(cred.CredentialBlobSize))
        return json.loads(blob.decode("utf-8"))
    finally:
        advapi32.CredFree(p_cred)


def delete_profile(name: str) -> None:
    """Delete a named profile from Windows Credential Manager."""
    target = f"{_TARGET_PREFIX}{name}"
    advapi32 = ctypes.windll.advapi32
    advapi32.CredDeleteW(target, 1, 0)
    logger.info("Deleted profile: %s", name)


def list_profiles() -> list[str]:
    """List all saved profile names."""
    advapi32 = ctypes.windll.advapi32
    p_creds = ctypes.c_void_p()
    count = wintypes.DWORD()
    prefix = _TARGET_PREFIX

    if not advapi32.CredEnumerateW(prefix + "*", 0, ctypes.byref(count), ctypes.byref(p_creds)):
        return []

    try:
        class CREDENTIAL(ctypes.Structure):
            _fields_ = [
                ("Flags", wintypes.DWORD),
                ("Type", wintypes.DWORD),
                ("TargetName", wintypes.LPWSTR),
                ("Comment", wintypes.LPWSTR),
                ("LastWritten", ctypes.c_uint64),
                ("CredentialBlobSize", wintypes.DWORD),
                ("CredentialBlob", ctypes.POINTER(ctypes.c_byte)),
                ("Persist", wintypes.DWORD),
                ("AttributeCount", wintypes.DWORD),
                ("Attributes", ctypes.c_void_p),
                ("TargetAlias", wintypes.LPWSTR),
                ("UserName", wintypes.LPWSTR),
            ]

        cred_array = ctypes.cast(p_creds, ctypes.POINTER(ctypes.POINTER(CREDENTIAL)))
        names = []
        for i in range(count.value):
            target = cred_array[i].contents.TargetName
            if target and target.startswith(_TARGET_PREFIX):
                names.append(target[len(_TARGET_PREFIX):])
        return names
    finally:
        advapi32.CredFree(p_creds)
