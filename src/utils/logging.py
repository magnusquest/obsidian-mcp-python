import os
import logging
import json
from datetime import datetime
from enum import Enum
from typing import Optional, Dict, Any

class ErrorCategoryType(Enum):
  VALIDATION = 'VALIDATION'
  AUTHENTICATION = 'AUTHENTICATION'
  AUTHORIZATION = 'AUTHORIZATION'
  BUSINESS_LOGIC = 'BUSINESS_LOGIC'
  DATA_ACCESS = 'DATA_ACCESS'
  EXTERNAL_SERVICE = 'EXTERNAL_SERVICE'
  SYSTEM = 'SYSTEM'
  UNKNOWN = 'UNKNOWN'

class LogLevel(Enum):
  ERROR = 0
  WARN = 1
  INFO = 2
  DEBUG = 3
  TRACE = 4

log_level_to_severity = {
  LogLevel.ERROR: 3,
  LogLevel.WARN: 2,
  LogLevel.INFO: 1,
  LogLevel.DEBUG: 0,
  LogLevel.TRACE: 0
}

DEFAULT_CONFIG = {
  "level": LogLevel.DEBUG if os.getenv("NODE_ENV") != "production" else LogLevel.INFO,
  "include_timestamps": True,
  "include_level": True,
  "mask_sensitive_data": True,
  "sensitive_fields": ["password", "token", "secret", "key", "auth", "credential"],
  "log_dir": "logs",
  "files": True,
  "file_names": {
    "combined": "combined.log",
    "error": "error.log",
    "warn": "warn.log",
    "info": "info.log",
    "debug": "debug.log"
  }
}

class Logger:
  def __init__(self, name: str, config: Optional[Dict[str, Any]] = None):
    self.name = name
    self.config = {**DEFAULT_CONFIG, **(config or {})}
    self.timers = {}
    self.logger = logging.getLogger(name)
    self.logger.setLevel(self.config["level"].value)
    self._initialize_logger()

  def _initialize_logger(self):
    log_dir = self.config["log_dir"]
    if self.config["files"] and log_dir:
      os.makedirs(log_dir, exist_ok=True)

    formatter = logging.Formatter(
      fmt='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
      datefmt='%Y-%m-%d %H:%M:%S'
    )

    if self.config["files"]:
      file_names = self.config["file_names"]
      for level, filename in file_names.items():
        file_handler = logging.FileHandler(os.path.join(log_dir, filename))
        file_handler.setLevel(getattr(logging, level.upper(), logging.DEBUG))
        file_handler.setFormatter(formatter)
        self.logger.addHandler(file_handler)

    console_handler = logging.StreamHandler()
    console_handler.setFormatter(formatter)
    self.logger.addHandler(console_handler)

  def _mask_sensitive_data(self, data: Dict[str, Any]) -> Dict[str, Any]:
    if not self.config["mask_sensitive_data"]:
      return data

    sensitive_fields = self.config["sensitive_fields"]
    masked_data = {}

    for key, value in data.items():
      if any(field in key.lower() for field in sensitive_fields):
        masked_data[key] = "********"
      elif isinstance(value, dict):
        masked_data[key] = self._mask_sensitive_data(value)
      else:
        masked_data[key] = value

    return masked_data

  def log(self, level: LogLevel, message: str, context: Optional[Dict[str, Any]] = None):
    if level.value > self.config["level"].value:
      return

    context = self._mask_sensitive_data(context or {})
    log_method = getattr(self.logger, level.name.lower(), self.logger.debug)
    log_method(f"{message} | Context: {json.dumps(context)}")

  def error(self, message: str, context: Optional[Dict[str, Any]] = None):
    self.log(LogLevel.ERROR, message, context)

  def warn(self, message: str, context: Optional[Dict[str, Any]] = None):
    self.log(LogLevel.WARN, message, context)

  def info(self, message: str, context: Optional[Dict[str, Any]] = None):
    self.log(LogLevel.INFO, message, context)

  def debug(self, message: str, context: Optional[Dict[str, Any]] = None):
    self.log(LogLevel.DEBUG, message, context)

  def trace(self, message: str, context: Optional[Dict[str, Any]] = None):
    self.log(LogLevel.TRACE, message, context)

  def start_timer(self, timer_id: str):
    self.timers[timer_id] = datetime.now()

  def end_timer(self, timer_id: str, message: str = "Operation completed", level: LogLevel = LogLevel.DEBUG):
    start_time = self.timers.pop(timer_id, None)
    if not start_time:
      self.warn(f"Timer '{timer_id}' does not exist")
      return 0

    elapsed_time = (datetime.now() - start_time).total_seconds() * 1000
    self.log(level, f"{message} in {elapsed_time:.2f}ms", {"timer_id": timer_id, "processing_time_ms": elapsed_time})
    return elapsed_time

  def set_level(self, level: LogLevel):
    self.config["level"] = level
    self.logger.setLevel(level.value)

def create_logger(name: str, config: Optional[Dict[str, Any]] = None) -> Logger:
  return Logger(name, config)

root_logger = create_logger("obsidian-mcp-server", {"files": True, "log_dir": "logs"})
