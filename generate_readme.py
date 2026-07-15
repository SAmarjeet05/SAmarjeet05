import argparse
import datetime
import os
import sys

from chronoai.builder import READMEBuilder
from chronoai.resolvers.atmosphere_resolver import AtmosphereResolver


def _parse_time_override(value: str) -> datetime.time:
    try:
        return datetime.datetime.strptime(value, "%H:%M").time()
    except ValueError as exc:
        raise argparse.ArgumentTypeError("--time must be in HH:MM (24-hour) format") from exc


def _resolve_mode_from_time(builder: READMEBuilder, time_override: datetime.time) -> str:
    local_now = AtmosphereResolver.local_now(builder.config.timezone_name)
    mocked = local_now.replace(
        hour=time_override.hour,
        minute=time_override.minute,
        second=0,
        microsecond=0,
    )
    return AtmosphereResolver.resolve_mode(mocked)

def main():
    try:
        import sys
        sys.stdout.reconfigure(encoding='utf-8')
    except (AttributeError, ImportError):
        pass

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
        "--build-contribution",
        action="store_true",
        help="Compile and generate contribution snake SVGs for all atmospheres"
    )
    parser.add_argument(
        "--use-cache", 
        action="store_true", 
        help="Use cached README copy if available (now default, use --no-cache to disable)"
    )
    parser.add_argument(
        "--no-cache",
        action="store_true",
        help="Force fresh generation and ignore cached README"
    )
    parser.add_argument(
        "--debug",
        action="store_true",
        help="Print debug information during run"
    )
    parser.add_argument(
        "--version", 
        action="store_true", 
        help="Print version details and metadata"
    )
    parser.add_argument(
        "--time",
        type=_parse_time_override,
        help="Temporarily resolve atmosphere mode from local HH:MM time for testing",
    )
    
    args = parser.parse_args()
    
    if args.version:
        from chronoai import __version__
        print(f"ChronoAI CLI version: v{__version__}")
        sys.exit(0)
        
    builder = READMEBuilder()

    # Determine use_cache value (defaults to True unless --no-cache is specified)
    use_cache = True
    if args.no_cache:
        use_cache = False

    resolved_mode = args.mode
    if args.time is not None:
        resolved_mode = _resolve_mode_from_time(builder, args.time)
        print(f"Resolved mode from --time {args.time.strftime('%H:%M')}: {resolved_mode.capitalize()}")
    else:
        resolved_mode = resolved_mode or builder.get_current_mode()
    
    if args.build_cache:
        builder.build_all_caches()
        print("Compiling ChronoMotion Engine SVGs for all operational modes...")
        from chronoai.motion.renderer import ChronoMotionRenderer
        token = os.environ.get("GITHUB_TOKEN") or os.environ.get("GH_TOKEN")
        ChronoMotionRenderer.render_all_atmospheres(username=builder.config.username, token=token)
    elif args.build_contribution:
        print("Compiling ChronoMotion Engine SVGs for all operational modes...")
        from chronoai.motion.renderer import ChronoMotionRenderer
        token = os.environ.get("GITHUB_TOKEN") or os.environ.get("GH_TOKEN")
        ChronoMotionRenderer.render_all_atmospheres(username=builder.config.username, token=token)
    else:
        cache_used = builder.build(force_mode=resolved_mode, use_cache=use_cache)
        if args.debug:
            if args.time is not None:
                current_ist = args.time.strftime("%H:%M")
            else:
                local_now = AtmosphereResolver.local_now(builder.config.timezone_name)
                current_ist = local_now.strftime("%H:%M")
            
            cache_status = "HIT" if cache_used else "MISS"
            gen_mode = "Cached" if cache_used else "Dynamic"
            output_name = os.path.basename(builder.config.root_readme_path)
            
            print("═══════════════════════════════════════")
            print("ChronoAI Debug")
            print("═══════════════════════════════════════")
            print(f"Current Time (IST) : {current_ist}")
            print(f"Atmosphere         : {resolved_mode.capitalize()}")
            print(f"Theme File         : {resolved_mode}.json")
            print("GitHub Theme       : Auto")
            print(f"Cache              : {cache_status}")
            print(f"Generation Mode    : {gen_mode}")
            print(f"Output             : {output_name}")
            print("═══════════════════════════════════════")

if __name__ == "__main__":
    main()
