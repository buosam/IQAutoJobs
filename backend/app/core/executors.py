"""
Global executor instances for CPU-bound tasks.
"""
from concurrent.futures import ProcessPoolExecutor
from typing import Optional

# This will be initialized during the application's lifespan startup.
executor: Optional[ProcessPoolExecutor] = None
