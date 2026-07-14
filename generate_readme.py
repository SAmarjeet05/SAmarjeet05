import argparse
import datetime
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

    resolved_mode = args.mode
    if args.time is not None:
        resolved_mode = _resolve_mode_from_time(builder, args.time)
        print(f"Resolved mode from --time {args.time.strftime('%H:%M')}: {resolved_mode.capitalize()}")
    
    if args.build_cache:
        builder.build_all_caches()
    else:
        builder.build(force_mode=resolved_mode, use_cache=args.use_cache)

if __name__ == "__main__":
    main()
