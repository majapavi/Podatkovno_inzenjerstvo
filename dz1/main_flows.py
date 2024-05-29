import os
from typing import List, Tuple, Iterable

from prefect.flows import flow
from prefect.deployments.deployments import Deployment

from prefect_implementation.detection.impl.FileDetector import FileDetector
from prefect_implementation.quality_check.impl.QualityCheck import QualityCheck
from processing.flow import processing_flow_logic

file_source = "data"
detection_api = FileDetector(files_sources=[file_source])
quality_check_api = QualityCheck()

@flow(log_prints=True)
def detect_files() -> Iterable[str]:
    detected = detection_api.detect_files()
    return detected

def quality_check_files(paths: Iterable[str]) -> Tuple[List[str], List[str]]:
    valid_files, unvalid_files = quality_check_api.check_quality(paths)
    return (valid_files, unvalid_files)

def processing_deployment(paths: Iterable[str], result_output_path: str):
    for path in paths:
        processing_flow_logic(file_path=path, result_output_path=result_output_path)

@flow(log_prints=True)
def main_flow(result_output_path:str):
    detected_files = detect_files()
    valid_files, unvalid_files = quality_check_files(detected_files)
    processing_deployment(valid_files, result_output_path)

if __name__ == '__main__':
    main_flow(result_output_path="data\\output")    

    # Za pokretanje koristenjem prefect agenata
    main_flow_instance = Deployment.build_from_flow(name="main_flow",
                                                    flow=main_flow,
                                                    path=os.path.abspath(os.path.curdir),
                                                    work_queue_name="dz1",
                                                    work_pool_name="test-pool")
    main_flow_instance.apply() # type: ignore