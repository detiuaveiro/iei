#!/usr/bin/env python3
import json
import sys

try:
    d = json.load(sys.stdin)
    t = "".join(
        c.get("text", "")
        for s in d.get("steps", [])
        if s.get("type") == "model_output"
        for c in s.get("content", [])
        if c.get("type") == "text"
    )
    if not t and "outputs" in d:
        t = "".join(
            o.get("text", "")
            for o in d["outputs"]
            if o.get("type") == "text"
        )
    if t:
        print(f"\n{t.strip()}\n")
    else:
        print(f"\n{d}\n")
except Exception as e:
    print("Erro ao processar JSON:", e)
