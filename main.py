import logging
import os
import time
from typing import List

from complexity import calculate_eog_complexity_windowed, create_summary_file

logging.basicConfig(
    level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s"
)
logger = logging.getLogger("eog_complexity_windowed")


if __name__ == "__main__":
    participant = 2
    try:
        base_dir = os.path.dirname(os.path.abspath(__file__))
    except NameError:
        base_dir = os.getcwd()

    data_dir: str = os.path.join(base_dir, "data")
    results_base_dir: str = os.path.join(base_dir, "results")

    input_file: str = os.path.join(data_dir, f"{participant}_processed_data.parquet")
    output_dir: str = os.path.join(
        results_base_dir, f"{participant}_eog_complexity_windowed"
    )

    sampling_frequency: int = 200
    window_duration: float = 2.0
    window_overlap: float = 0.5  # Reintroduced overlap

    start_run_time: float = time.time()
    logger.info(f"Starting windowed EOG complexity calculation for: {participant}")
    logger.info(f"Input file: {input_file}")
    logger.info(f"Output directory: {output_dir}")
    logger.info(f"Sampling Frequency: {sampling_frequency} Hz")
    logger.info(f"Window Duration: {window_duration} s")
    logger.info(f"Window Overlap: {window_overlap*100:.0f}%")

    os.makedirs(output_dir, exist_ok=True)

    all_param_files: List[str]
    all_raw_files: List[str]
    checked_param_file_count: int
    total_expected_params: int

    all_param_files, all_raw_files, checked_param_file_count, total_expected_params = (
        calculate_eog_complexity_windowed(
            participant,
            output_dir,
            sf=sampling_frequency,
            window_duration_s=window_duration,
            window_overlap=window_overlap,
        )
    )

    logger.info("Creating summary file...")
    create_summary_file(
        all_param_files,
        all_raw_files,
        checked_param_file_count,
        total_expected_params,
        output_dir,
    )

    end_run_time: float = time.time()
    logger.info("Processing complete.")
    logger.info(f"Total time: {end_run_time - start_run_time:.2f} seconds")
    logger.info(
        f"Expected parameter files: {total_expected_params}. Parameter files saved (reported): {len(all_param_files)}. "
        f"Parameter files passing check: {checked_param_file_count}. Raw window files saved: {len(all_raw_files)}."
    )
    logger.info(f"Individual parameter results saved in {output_dir}")
    logger.info(f"Raw windowed signal data saved in {output_dir}")
    logger.info(f"Summary files saved in {output_dir}")
