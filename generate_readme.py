import argparse
import sys
from chronoai.builder import READMEBuilder

def main():
    parser = argparse.ArgumentParser(description="ChronoAI README Generator CLI")
    parser.add_argument(
        "--mode", 
        type=str, 
        choices=["boot", "inference", "optimization", "research"], 
        help="Force specific mode generation (e.g. boot, research)"
    )
    parser.add_argument(
        "--build-cache", 
        action="store_true", 
        help="Compile and update cache and preview files for all modes"
    )
    parser.add_argument(
        "--use-cache", 
        action="store_true", 
        help="Use cached README copy if available instead of dynamic rendering"
    )
    parser.add_argument(
        "--version", 
        action="store_true", 
        help="Print version details and metadata"
    )
    
    args = parser.parse_args()
    
    if args.version:
        from chronoai import __version__
        print(f"ChronoAI CLI version: v{__version__}")
        sys.exit(0)
        
    builder = READMEBuilder()
    
    if args.build_cache:
        builder.build_all_caches()
    else:
        builder.build(force_mode=args.mode, use_cache=args.use_cache)

if __name__ == "__main__":
    main()
