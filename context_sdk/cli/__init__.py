from __future__ import annotations

import argparse
import json
import logging
import os
import sys


def main() -> None:
    parser = argparse.ArgumentParser(prog="context-sdk", description="Versioned context engine CLI.")
    parser.add_argument("--token", default=os.environ.get("GITHUB_TOKEN"), help="GitHub token")
    parser.add_argument("--ref", default="HEAD", help="Git ref: branch, tag, or commit SHA")
    parser.add_argument("--disk-cache", default=None, help="Disk cache directory")
    parser.add_argument("--verbose", "-v", action="store_true", help="Debug logging")

    sub = parser.add_subparsers(dest="command", required=True)

    fetch_p = sub.add_parser("fetch", help="Fetch and display a context file")
    fetch_p.add_argument("repo")
    fetch_p.add_argument("path")
    fetch_p.add_argument("--keys", nargs="*")
    fetch_p.add_argument("--max-items", type=int, default=None)
    fetch_p.add_argument("--depth", type=int, default=None)
    fetch_p.add_argument("--metadata", action="store_true")
    fetch_p.add_argument("--raw", action="store_true")

    list_p = sub.add_parser("list", help="List files in a repo directory")
    list_p.add_argument("repo")
    list_p.add_argument("directory", nargs="?", default="")

    pin_p = sub.add_parser("pin", help="Resolve ref to a commit SHA")
    pin_p.add_argument("repo")

    merge_p = sub.add_parser("merge", help="Merge multiple context files")
    merge_p.add_argument("repo")
    merge_p.add_argument("paths", nargs="+")
    merge_p.add_argument("--keys", nargs="*")

    cache_p = sub.add_parser("cache", help="Show cache statistics")
    cache_p.add_argument("repo")

    args = parser.parse_args()

    if args.verbose:
        logging.basicConfig(level=logging.DEBUG, format="%(levelname)s %(name)s: %(message)s")
    else:
        logging.basicConfig(level=logging.WARNING, format="%(levelname)s: %(message)s")

    from context_sdk.core.engine import ContextEngine

    engine = ContextEngine(repo=args.repo, token=args.token, ref=args.ref, disk_cache=args.disk_cache)

    try:
        if args.command == "fetch":
            envelope = engine.load_context(args.path, ref=args.ref)
            if args.raw:
                print(json.dumps(envelope.to_dict(), indent=2, ensure_ascii=False))
            else:
                keys = args.keys if args.keys else None
                result = engine.get_context_slice(envelope, keys=keys, max_items=args.max_items, depth=args.depth, include_metadata=args.metadata)
                print(json.dumps(result, indent=2, ensure_ascii=False))
                print(f"\n# {envelope.summary()}", file=sys.stderr)

        elif args.command == "list":
            for f in engine.list_context_files(args.directory, ref=args.ref):
                print(f)

        elif args.command == "pin":
            print(engine.pin_to_latest(args.ref))

        elif args.command == "merge":
            envelope = engine.merge_contexts(args.paths, ref=args.ref)
            keys = args.keys if args.keys else None
            print(json.dumps(engine.get_context_slice(envelope, keys=keys, include_metadata=True), indent=2, ensure_ascii=False))

        elif args.command == "cache":
            print(json.dumps(engine.cache_stats(), indent=2))

    except FileNotFoundError as exc:
        print(f"Error: {exc}", file=sys.stderr)
        sys.exit(1)
    except KeyboardInterrupt:
        sys.exit(0)
    except Exception as exc:
        print(f"Error: {exc}", file=sys.stderr)
        if args.verbose:
            raise
        sys.exit(1)


if __name__ == "__main__":
    main()
