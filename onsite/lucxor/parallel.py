"""
Parallel processing module for lucxor.

This module contains classes and functions for parallel processing.
"""

import os
import logging
from typing import List, Optional
from concurrent.futures import ThreadPoolExecutor, as_completed

logger = logging.getLogger(__name__)

# Default thread count
DEFAULT_NUM_THREADS = 4


class PSMProcessingWorker:
    """Worker thread class for PSM processing"""

    def __init__(self, model=None, flr_calculator=None, round_number=0):
        self.model = model
        self.flr_calculator = flr_calculator
        self.round_number = round_number

    def process_psm(self, psm) -> None:
        """Process a single PSM"""
        try:
            if self.round_number == 0:
                # Update PSM config with model
                psm.config["model"] = self.model
                psm.process(psm.config, round_number=0)
            elif self.round_number == 2:
                psm.process_round2(self.flr_calculator)
        except Exception as e:
            logger.error(f"PSM processing error: {str(e)}")

    def process_psm_batch(self, psms: List) -> None:
        """Process a batch of PSMs"""
        for psm in psms:
            self.process_psm(psm)


def parallel_psm_processing(
    psms: List,
    model=None,
    flr_calculator=None,
    round_number=0,
    num_threads: Optional[int] = None,
) -> None:
    """
    Process PSM list in parallel

    Args:
        psms: PSM list
        model: Model object
        flr_calculator: FLR calculator
        round_number: Round number
        num_threads: Number of threads
    """
    if num_threads is None:
        num_threads = os.cpu_count() or DEFAULT_NUM_THREADS

    worker = PSMProcessingWorker(model, flr_calculator, round_number)

    # Skip threading overhead for single thread
    if num_threads == 1:
        worker.process_psm_batch(psms)
        return

    # Split PSM list into chunks
    chunk_size = max(1, len(psms) // num_threads)
    psm_chunks = [psms[i : i + chunk_size] for i in range(0, len(psms), chunk_size)]

    with ThreadPoolExecutor(max_workers=num_threads) as executor:
        futures = []
        for chunk in psm_chunks:
            future = executor.submit(worker.process_psm_batch, chunk)
            futures.append(future)

        # Wait for all tasks to complete
        for future in as_completed(futures):
            try:
                future.result()
            except Exception as e:
                logger.error(f"PSM parallel processing error: {str(e)}")


def get_optimal_thread_count(
    num_items: int, max_threads: int = None
) -> int:
    """
    Calculate optimal thread count based on data size

    Args:
        num_items: Number of data items
        max_threads: Maximum number of threads

    Returns:
        Optimal thread count
    """
    if max_threads is None:
        max_threads = os.cpu_count() or DEFAULT_NUM_THREADS

    # Use fewer threads for small datasets
    if num_items < 10:
        return min(2, max_threads)
    elif num_items < 100:
        return min(4, max_threads)
    else:
        return max_threads
