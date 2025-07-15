"""
AI-powered YAML translation module with comprehensive telemetry
"""

import sys
import yaml
import time
from pathlib import Path
from openai import OpenAI
from more_itertools import chunked
from datetime import datetime

try:
    from utils.telemetry import BatchTelemetry, save_translation_history, format_time
    from config.settings import get_setting
except ImportError:
    # Fallback implementations if modules are not available
    def get_setting(category, key=None):
        defaults = {
            'api': {'model': 'gpt-4o-mini', 'batch_size': 50, 'timeout': 30, 'max_retries': 3},
            'files': {'auto_backup': True, 'output_suffix': 'translated_', 'preserve_formatting': True},
            'ui': {'show_progress': True, 'detailed_logging': True}
        }
        if key is None:
            return defaults.get(category, {})
        return defaults.get(category, {}).get(key)
    
    def save_translation_history(entry):
        pass  # No-op fallback
    
    def format_time(seconds):
        if seconds < 1:
            return f"{int(seconds * 1000)}ms"
        elif seconds < 60:
            return f"{seconds:.1f}s"
        else:
            return f"{int(seconds // 60)}m {int(seconds % 60)}s"
    
    class BatchTelemetry:
        def __init__(self, total_batches):
            self.total_batches = total_batches
            self.batches = [{'started': None, 'finished': None, 'api_start': None, 'api_end': None, 'file_start': None, 'file_end': None, 'status': 'pending'} for _ in range(total_batches)]
        
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
            pass  # Simplified for fallback
        
        def print_final_summary(self, total_start_time, total_items, translated_items):
            total_time = time.time() - total_start_time
            print(f"\n✅ Translation completed in {format_time(total_time)}")
            print(f"📊 Translated {translated_items}/{total_items} items")

def flatten_yaml(d, prefix=""):
    """Flatten nested YAML structure."""
    items = {}
    for k, v in d.items():
        new_key = f"{prefix}.{k}" if prefix else k
        if isinstance(v, dict):
            items.update(flatten_yaml(v, new_key))
        else:
            items[new_key] = v
    return items

def unflatten_yaml(d):
    """Unflatten YAML structure."""
    result = {}
    for k, v in d.items():
        keys = k.split(".")
        ref = result
        for part in keys[:-1]:
            ref = ref.setdefault(part, {})
        ref[keys[-1]] = v
    return result

def save_progress(output_dict, out_file):
    """Save progress after each batch."""
    rebuilt = unflatten_yaml(output_dict)
    with open(out_file, "w", encoding="utf-8") as f:
        yaml.dump(rebuilt, f, allow_unicode=True, default_flow_style=False, sort_keys=False)

class Translator:
    def __init__(self):
        self.client = None
        self.settings = {
            'model': get_setting('api', 'model'),
            'batch_size': get_setting('api', 'batch_size'),
            'timeout': get_setting('api', 'timeout'),
            'max_retries': get_setting('api', 'max_retries')
        }
    
    def initialize_client(self, api_key):
        """Initialize OpenAI client."""
        try:
            self.client = OpenAI(api_key=api_key)
            # Test the API key with a simple request
            self.client.models.list()
            return True
        except Exception as e:
            print(f"❌ Failed to initialize OpenAI client: {e}")
            return False
    
    def run(self, file_path, language, api_key):
        """Main translation workflow."""
        if not self.initialize_client(api_key):
            return None
        
        return self.translate_yaml_file(file_path, language)
    
    def translate_yaml_file(self, file_path, lang):
        """Translate YAML file with enhanced progress tracking."""
        total_start = time.time()
        print(f"🔄 Loading file: {file_path}")
        
        # Create backup if enabled
        if get_setting('files', 'auto_backup'):
            self.create_backup(file_path)
        
        try:
            with open(file_path, "r", encoding="utf-8") as f:
                original = yaml.safe_load(f)
        except Exception as e:
            print(f"❌ Error loading YAML file: {e}")
            return None

        flat = flatten_yaml(original)
        keys = list(flat.keys())
        values = list(flat.values())

        # Prepare output dictionary
        output = {}
        translatable_items = []
        
        # Process all elements
        for key, val in zip(keys, values):
            if isinstance(val, str) and val.lower() not in ("true", "false") and val.strip():
                translatable_items.append((key, val))
                if get_setting('ui', 'detailed_logging'):
                    print(f"🔍 Queued: {key} = '{val[:50]}{'...' if len(val) > 50 else ''}'")
            else:
                output[key] = val

        total_translatable = len(translatable_items)
        print(f"📊 Total translatable texts: {total_translatable}")
        
        if total_translatable == 0:
            print("✅ No translatable text found!")
            return None

        # Generate output filename
        output_suffix = get_setting('files', 'output_suffix')
        output_file = f"{output_suffix}{Path(file_path).name}"
        translated_count = 0
        
        # Initialize telemetry
        chunks = list(chunked(translatable_items, self.settings['batch_size']))
        total_batches = len(chunks)
        telemetry = BatchTelemetry(total_batches)

        print(f"\n🚀 Starting translation into {total_batches} batches...")

        # Process batches
        for batch_num, chunk in enumerate(chunks, 1):
            batch_idx = batch_num - 1
            telemetry.start_batch(batch_idx)
            
            batch_size = len(chunk)
            print(f"\n📡 Batch {batch_num}/{total_batches} ({batch_size} items)")
            
            if self.process_batch(chunk, lang, output, telemetry, batch_idx):
                translated_count += len(chunk)
                
                # Save progress
                telemetry.start_file_ops(batch_idx)
                save_progress(output, output_file)
                telemetry.end_file_ops(batch_idx)
                telemetry.finish_batch(batch_idx)
                
                print(f"💾 Progress saved: {translated_count}/{total_translatable} items")
                
                # Show telemetry if enabled
                if get_setting('ui', 'show_progress'):
                    telemetry.print_status()
            else:
                print(f"❌ Batch {batch_num} failed, skipping...")
        
        # Final summary
        total_time = time.time() - total_start
        telemetry.print_final_summary(total_start, total_translatable, translated_count)
        
        # Save to history
        try:
            save_translation_history({
                'timestamp': datetime.now().isoformat(),
                'file': file_path,
                'language': lang,
                'items_translated': translated_count,
                'total_items': total_translatable,
                'duration': format_time(total_time),
                'status': 'completed' if translated_count > 0 else 'failed'
            })
        except:
            pass  # Ignore history save errors
        
        print(f"\n✅ Translation completed! Output: {output_file}")
        return output_file
    
    def process_batch(self, chunk, lang, output, telemetry, batch_idx):
        """Process a single batch of translations."""
        try:
            # Prepare texts
            texts_to_translate = [item[1] for item in chunk]
            prompt = "\n".join([f"{i+1}. {text}" for i, text in enumerate(texts_to_translate)])
            
            print(f"🤖 Sending to AI...")
            telemetry.start_api(batch_idx)
            
            # Make API call with retry logic
            for attempt in range(self.settings['max_retries']):
                try:
                    resp = self.client.chat.completions.create(
                        model=self.settings['model'],
                        messages=[
                            {"role": "system", "content": f"Translate these texts to {lang}. Keep ALL placeholders like {{value}}, {{player}}, &7, &a, %placeholders% EXACTLY as they are. Return only the translated text in numbered format."},
                            {"role": "user", "content": prompt}
                        ],
                        timeout=self.settings['timeout']
                    )
                    break
                except Exception as e:
                    if attempt < self.settings['max_retries'] - 1:
                        print(f"⚠️  API call failed (attempt {attempt + 1}), retrying...")
                        time.sleep(2 ** attempt)  # Exponential backoff
                    else:
                        raise e
            
            telemetry.end_api(batch_idx)
            response_text = resp.choices[0].message.content.strip()
            
            # Parse response
            lines = response_text.splitlines()
            translated_batch = []
            for line in lines:
                if ". " in line and line[0].isdigit():
                    translated_batch.append(line.split(". ", 1)[1])
                elif line.strip() and not line.startswith(("1.", "2.", "3.", "4.", "5.")):
                    translated_batch.append(line.strip())
            
            # Apply translations
            for i, (key, original) in enumerate(chunk):
                if i < len(translated_batch):
                    output[key] = translated_batch[i]
                else:
                    print(f"⚠️  Missing translation for: {key}")
                    output[key] = original
            
            api_time = telemetry.get_api_time(batch_idx)
            print(f"✅ Batch completed ({format_time(api_time or 0)})")
            return True
            
        except Exception as e:
            print(f"❌ Batch processing failed: {e}")
            return False
    
    def create_backup(self, file_path):
        """Create backup of original file."""
        try:
            backup_path = f"{file_path}.backup"
            with open(file_path, 'r', encoding='utf-8') as src:
                with open(backup_path, 'w', encoding='utf-8') as dst:
                    dst.write(src.read())
            print(f"💾 Backup created: {backup_path}")
        except Exception as e:
            print(f"⚠️  Backup creation failed: {e}")