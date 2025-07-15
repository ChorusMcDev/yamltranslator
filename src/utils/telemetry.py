"""
Telemetry and performance tracking for YAML Translator Tool
"""

import time
import json
from pathlib import Path
from datetime import datetime
from functools import wraps

try:
    from config.settings import get_setting
except ImportError:
    # Fallback if settings module is not available
    def get_setting(category, key=None):
        defaults = {
            'ui': {'show_progress': True, 'detailed_logging': True},
            'history': {'auto_save': True, 'max_entries': 100}
        }
        if key is None:
            return defaults.get(category, {})
        return defaults.get(category, {}).get(key, True)

def track_performance(func):
    """Decorator to track function performance."""
    @wraps(func)
    def wrapper(*args, **kwargs):
        start_time = time.time()
        result = func(*args, **kwargs)
        end_time = time.time()
        execution_time = end_time - start_time
        
        if get_setting('ui', 'detailed_logging'):
            print(f"⏱️  {func.__name__}: {execution_time:.4f}s")
        
        return result
    return wrapper

def format_time(seconds):
    """Format time in human-readable format."""
    if seconds < 1:
        return f"{int(seconds * 1000)}ms"
    elif seconds < 60:
        return f"{seconds:.1f}s"
    elif seconds < 3600:
        return f"{int(seconds // 60)}m {int(seconds % 60)}s"
    else:
        hours = int(seconds // 3600)
        minutes = int((seconds % 3600) // 60)
        return f"{hours}h {minutes}m"

def format_timestamp(timestamp):
    """Format timestamp."""
    return datetime.fromtimestamp(timestamp).strftime("%H:%M:%S")

class BatchTelemetry:
    def __init__(self, total_batches):
        self.total_batches = total_batches
        self.batches = []
        for i in range(total_batches):
            self.batches.append({
                'started': None,
                'finished': None,
                'api_start': None,
                'api_end': None,
                'file_start': None,
                'file_end': None,
                'status': 'pending'
            })
    
    def start_batch(self, batch_idx):
        self.batches[batch_idx]['started'] = time.time()
        self.batches[batch_idx]['status'] = 'running'
    
    def start_api(self, batch_idx):
        self.batches[batch_idx]['api_start'] = time.time()
    
    def end_api(self, batch_idx):
        self.batches[batch_idx]['api_end'] = time.time()
    
    def start_file_ops(self, batch_idx):
        self.batches[batch_idx]['file_start'] = time.time()
    
    def end_file_ops(self, batch_idx):
        self.batches[batch_idx]['file_end'] = time.time()
    
    def finish_batch(self, batch_idx):
        self.batches[batch_idx]['finished'] = time.time()
        self.batches[batch_idx]['status'] = 'completed'
    
    def get_batch_time(self, batch_idx):
        batch = self.batches[batch_idx]
        if batch['started'] and batch['finished']:
            return batch['finished'] - batch['started']
        return None
    
    def get_api_time(self, batch_idx):
        batch = self.batches[batch_idx]
        if batch['api_start'] and batch['api_end']:
            return batch['api_end'] - batch['api_start']
        return None
    
    def get_file_time(self, batch_idx):
        batch = self.batches[batch_idx]
        if batch['file_start'] and batch['file_end']:
            return batch['file_end'] - batch['file_start']
        return None
    
    def print_status(self):
        if not get_setting('ui', 'show_progress'):
            return
            
        print("\n" + "="*80)
        print("📊 BATCH TELEMETRY")
        print("="*80)
        
        for i, batch in enumerate(self.batches, 1):
            if batch['status'] == 'completed':
                start_time = format_timestamp(batch['started'])
                end_time = format_timestamp(batch['finished'])
                elapsed = format_time(self.get_batch_time(i-1))
                api_time = format_time(self.get_api_time(i-1)) if self.get_api_time(i-1) else "N/A"
                file_time = format_time(self.get_file_time(i-1)) if self.get_file_time(i-1) else "N/A"
                
                print(f"{i:2d}. batch - ✅ Started: {start_time} - Finished: {end_time} - Total: {elapsed} (API: {api_time}, File: {file_time})")
            
            elif batch['status'] == 'running':
                start_time = format_timestamp(batch['started'])
                elapsed = format_time(time.time() - batch['started'])
                print(f"{i:2d}. batch - 🔄 Started: {start_time} - Running... - Elapsed: {elapsed}")
            
            else:  # pending
                print(f"{i:2d}. batch - ⏳ Waiting...")
    
    def print_final_summary(self, total_start_time, total_items, translated_items):
        total_time = time.time() - total_start_time
        total_api_time = sum(self.get_api_time(i) or 0 for i in range(len(self.batches)))
        total_file_time = sum(self.get_file_time(i) or 0 for i in range(len(self.batches)))
        processing_time = total_time - total_api_time - total_file_time
        
        print("\n" + "="*80)
        print("🎯 FINAL SUMMARY")
        print("="*80)
        print(f"📁 Total items processed: {translated_items}/{total_items}")
        print(f"⏱️  Total time elapsed: {format_time(total_time)}")
        print(f"🌐 API request time: {format_time(total_api_time)} ({total_api_time/total_time*100:.1f}%)")
        print(f"💾 File operations time: {format_time(total_file_time)} ({total_file_time/total_time*100:.1f}%)")
        print(f"⚙️  Processing time: {format_time(processing_time)} ({processing_time/total_time*100:.1f}%)")
        print(f"⚡ Translation speed: {translated_items/total_time:.1f} items/sec")
        print(f"📊 Completed batches: {sum(1 for b in self.batches if b['status'] == 'completed')}/{len(self.batches)}")

def get_history_file():
    """Get history file path."""
    try:
        from config.settings import _settings
        return _settings.config_dir / 'history.json'
    except ImportError:
        return Path.home() / '.yaml-translator' / 'history.json'

def save_translation_history(entry):
    """Save translation history entry."""
    if not get_setting('history', 'auto_save'):
        return
    
    history_file = get_history_file()
    history_file.parent.mkdir(exist_ok=True)
    
    # Load existing history
    history = []
    if history_file.exists():
        try:
            with open(history_file, 'r') as f:
                history = json.load(f)
        except Exception:
            pass
    
    # Add new entry
    entry['timestamp'] = datetime.now().isoformat()
    history.insert(0, entry)  # Add to beginning
    
    # Limit history size
    max_entries = get_setting('history', 'max_entries')
    if len(history) > max_entries:
        history = history[:max_entries]
    
    # Save history
    try:
        with open(history_file, 'w') as f:
            json.dump(history, f, indent=2)
    except Exception as e:
        print(f"⚠️  Could not save history: {e}")

def save_operation_history(entry):
    """Save operation history (formatting, reversing, etc.)."""
    save_translation_history(entry)

def get_translation_history():
    """Get translation history."""
    history_file = get_history_file()
    
    if not history_file.exists():
        return []
    
    try:
        with open(history_file, 'r') as f:
            return json.load(f)
    except Exception:
        return []

def clear_history():
    """Clear all history."""
    history_file = get_history_file()
    try:
        if history_file.exists():
            history_file.unlink()
        print("✅ History cleared.")
    except Exception as e:
        print(f"❌ Error clearing history: {e}")

# Legacy classes for backward compatibility
class Telemetry:
    def __init__(self):
        self.operations = []

    def log_operation(self, operation_name, status, duration):
        self.operations.append({
            'operation': operation_name,
            'status': status,
            'duration': duration
        })

    def print_summary(self):
        print("\nTelemetry Summary:")
        for op in self.operations:
            print(f"Operation: {op['operation']}, Status: {op['status']}, Duration: {op['duration']:.4f} seconds")