"""Test package initialization and runtime compatibility patches."""

import os
import collections
import collections.abc

os.environ.setdefault("DATABASE_URI", "sqlite:///test.db")

# nose 1.3.7 references collections.Callable, removed in Python 3.11.
if not hasattr(collections, "Callable"):
    collections.Callable = collections.abc.Callable
