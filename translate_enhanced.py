"""
Enhanced YAML Translator with improved placeholder handling and telemetry
This is the updated version of your original translate.py with all improvements
"""

import sys
import yaml
import time
from pathlib import Path
from openai import OpenAI
from more_itertools import chunked
from datetime import datetime

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

def translate_yaml_file(file_path, lang, api_key, batch_size=50):
    """Enhanced translation with comprehensive telemetry and progress tracking."""
    total_start = time.time()
    print(f"🔄 Loading file: {file_path}")
    
    # Initialize OpenAI client
    client = OpenAI(api_key=api_key)
    
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
            print(f"🔍 Queued: {key} = '{val[:50]}{'...' if len(val) > 50 else ''}'")
        else:
            output[key] = val

    total_translatable = len(translatable_items)
    print(f"📊 Total translatable texts: {total_translatable}")
    
    if total_translatable == 0:
        print("✅ No translatable text found!")
        return None

    # Generate output filename
    output_file = f"translated_{Path(file_path).name}"
    translated_count = 0
    
    # Initialize telemetry
    chunks = list(chunked(translatable_items, batch_size))
    total_batches = len(chunks)
    telemetry = BatchTelemetry(total_batches)

    print(f"\n🚀 Starting translation into {total_batches} batches...")

    # Process batches
    for batch_num, chunk in enumerate(chunks, 1):
        batch_idx = batch_num - 1
        telemetry.start_batch(batch_idx)
        
        batch_size_actual = len(chunk)
        print(f"\n📡 Batch {batch_num}/{total_batches} ({batch_size_actual} items)")
        
        try:
            # Prepare texts
            texts_to_translate = [item[1] for item in chunk]
            prompt = "\n".join([f"{i+1}. {text}" for i, text in enumerate(texts_to_translate)])
            
            print(f"🤖 Sending to AI...")
            telemetry.start_api(batch_idx)
            
            # Make API call
            resp = client.chat.completions.create(
                model="gpt-4o-mini",
                messages=[
                    {"role": "system", "content": f"Translate these texts to {lang}. Keep ALL placeholders like {{value}}, {{player}}, &7, &a, %placeholders% EXACTLY as they are. Return only the translated text in numbered format."},
                    {"role": "user", "content": prompt}
                ],
                timeout=30
            )
            
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
                    translated_count += 1
                else:
                    print(f"⚠️  Missing translation for: {key}")
                    output[key] = original
            
            # Save progress
            telemetry.start_file_ops(batch_idx)
            save_progress(output, output_file)
            telemetry.end_file_ops(batch_idx)
            telemetry.finish_batch(batch_idx)
            
            api_time = telemetry.get_api_time(batch_idx)
            file_time = telemetry.get_file_time(batch_idx)
            print(f"✅ Batch completed (API: {format_time(api_time)}, File: {format_time(file_time)})")
            print(f"💾 Progress saved: {translated_count}/{total_translatable} items")
            
            # Show telemetry
            telemetry.print_status()
            
        except Exception as e:
            print(f"❌ Batch {batch_num} failed: {e}")
            telemetry.finish_batch(batch_idx)
    
    # Final summary
    telemetry.print_final_summary(total_start, total_translatable, translated_count)
    
    print(f"\n✅ Translation completed! Output: {output_file}")
    return output_file

if __name__ == "__main__":
    if len(sys.argv) != 4:
        print("❌ Usage: python translate_enhanced.py <file.yml> <language> <api_key>")
        print("Example: python translate_enhanced.py config.yml hungarian sk-...")
        sys.exit(1)
    
    file_path = sys.argv[1]
    language = sys.argv[2]
    api_key = sys.argv[3]
    
    translate_yaml_file(file_path, language, api_key)
