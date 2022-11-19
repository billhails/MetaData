import argparse
from utils.templating import TemplateProcessor
from utils.parse_schema import get_semantics

arg_parser = argparse.ArgumentParser()
arg_parser.add_argument("-s", "--schema", help="specify the xml schema")
arg_parser.add_argument("-o", "--output", help="output directory (will be created if needed)")
arg_parser.add_argument("-a", "--architecture", help="target architecture")

args = arg_parser.parse_args()

if not args.schema:
    raise Exception("--schema is required (--help for help)")

if not args.output:
    raise Exception("--output is required (--help for help)")

if not args.architecture:
    raise Exception("--architecture is required (--help for help)")

semantics = get_semantics(args.schema)

TemplateProcessor(args.architecture, semantics, args.output).process_templates()
