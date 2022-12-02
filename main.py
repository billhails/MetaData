#
#  MetaData - API Generator.
#  Copyright (C) 2022  Bill Hails
#
#  This program is free software: you can redistribute it and/or modify
#  it under the terms of the GNU General Public License as published by
#  the Free Software Foundation, either version 3 of the License, or
#  (at your option) any later version.
#
#  This program is distributed in the hope that it will be useful,
#  but WITHOUT ANY WARRANTY; without even the implied warranty of
#  MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#  GNU General Public License for more details.
#
#  You should have received a copy of the GNU General Public License
#  along with this program.  If not, see <https://www.gnu.org/licenses/>.
#
import argparse
from utils.templating import TemplateProcessor
from utils.parse_schema import get_semantics
from utils.generate_dotenv import generate_dotenv

arg_parser = argparse.ArgumentParser(prog="metadata", description="build an API from an XML schema")
arg_parser.add_argument("-s", "--schema", help="specify the xml schema")
arg_parser.add_argument("-o", "--output", help="output directory (will be created if needed)")
arg_parser.add_argument("-a", "--architecture", help="target architecture")
arg_parser.add_argument(
    "--generate-dotenv",
    help="instead, generate a .env file in the supplied architecture source",
    dest='dotenv',
    action='store_true'
)

args = arg_parser.parse_args()

if args.dotenv:
    if not args.architecture:
        raise Exception("--architecture is required (--help for help)")

    generate_dotenv(args.architecture)

else:
    if not args.schema:
        raise Exception("--schema is required (--help for help)")

    if not args.output:
        raise Exception("--output is required (--help for help)")

    if not args.architecture:
        raise Exception("--architecture is required (--help for help)")

    semantics = get_semantics(args.schema)

    TemplateProcessor(args.architecture, semantics, args.output).process_templates()
