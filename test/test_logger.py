# test/test_logger.py

from database.sqlite_logger import Logger

def test_logging_flow():
    logger = Logger()
    session_id = "sess_test_001"
    
    logger.start_session(session_id, "OP1001", "dig_trench")
    hazard_id = logger.log_hazard(session_id, "overheating", "Temp=90")
    logger.log_action(hazard_id, "Stop and Cool Down", is_correct=1)
    logger.end_session(session_id, 10.0)
    
    # No assert for now — just verify that no exceptions are thrown
    assert True
