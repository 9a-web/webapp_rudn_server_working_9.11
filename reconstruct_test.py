import importlib.util
import sys
import inspect
from pydantic import BaseModel
import typing
from datetime import datetime
from typing import Optional, List, Any

def load_pyc(path, module_name):
    spec = importlib.util.spec_from_file_location(module_name, path)
    module = importlib.util.module_from_spec(spec)
    sys.modules[module_name] = module
    spec.loader.exec_module(module)
    return module

try:
    models = load_pyc("models_backup.pyc", "backend.models")
    print("Successfully loaded models module")
    
    with open("reconstructed_models.txt", "w") as f:
        # Get all members
        for name, obj in inspect.getmembers(models):
            if inspect.isclass(obj):
                f.write(f"\nclass {name}")
                if issubclass(obj, BaseModel):
                     f.write("(BaseModel):\n")
                     for field_name, field in obj.model_fields.items():
                         # Pydantic v2 uses model_fields, v1 uses __fields__
                         f.write(f"    {field_name}: {field.annotation}\n")
                else:
                    f.write(":\n    pass\n")

except Exception as e:
    print(f"Error: {e}")
    # Try pydantic v1 fallback
    try:
        import traceback
        traceback.print_exc()
    except:
        pass
