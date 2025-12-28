import json
import os
from datetime import datetime
from typing import Dict, Any

class DebateLogger:
    def __init__(self, log_file: str = None):
        if log_file:
            self.log_file = log_file
        else:
            # Default to timestamped jsonl file if none provided
            timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
            self.log_file = f"debate_log_{timestamp}.jsonl"
            
    def log_step(self, step_name: str, content: Any):
        """Log a step in JSONL format"""
        entry = {
            "timestamp": datetime.now().isoformat(),
            "event_type": step_name,
            "payload": content
        }
        
        with open(self.log_file, 'a') as f:
            f.write(json.dumps(entry) + "\n")