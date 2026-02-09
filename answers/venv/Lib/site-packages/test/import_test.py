from dbtlabs.proto.public.v1.fields import *
from dbtlabs.proto.public.v1.events import *
from dbtlabs.proto.public.v1.records import *
import importlib
import pkgutil

def test_import():
    assert True

def test_import_public():
    assert True

def test_all_proto_modules_importable():
    """Test that ensures all modules under dbtlabs.proto can be imported without errors."""
    # List of base packages to check
    base_packages = [
        "dbtlabs.proto.public.v1.fields",
        "dbtlabs.proto.public.v1.events",
        "dbtlabs.proto.public.v1.records",
    ]

    # Try importing each base package
    for pkg_name in base_packages:
        try:
            # Import the package
            pkg = importlib.import_module(pkg_name)
            assert pkg is not None, f"Failed to import {pkg_name}"

            # Check if it's a package and walk through its submodules
            if hasattr(pkg, "__path__"):
                # Get all submodules
                for _, submodule_name, is_pkg in pkgutil.iter_modules(pkg.__path__, pkg.__name__ + "."):
                    try:
                        submodule = importlib.import_module(submodule_name)
                        assert submodule is not None, f"Failed to import {submodule_name}"
                    except ImportError as e:
                        assert False, f"Could not import submodule {submodule_name}: {str(e)}"
        except ImportError as e:
            assert False, f"Could not import {pkg_name}: {str(e)}. Is there a dependency from a public to a private proto?"
