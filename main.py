import argparse
import os
import shutil
import xml.etree.ElementTree as eT
from jinja2 import Template, StrictUndefined
from Semantics.Association import Association
from Semantics.Description import Description
from Semantics.Entity import Entity
from Semantics.Field import Field
from Semantics.Reference import Reference
from Semantics.Schema import Schema
from Semantics.Union import Union

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

my_tree = eT.parse(args.schema)


def parse_schema(node):
    match node.tag:
        case 'schema':
            return Schema(node.attrib, [parse_schema(n) for n in node])
        case 'entity':
            return Entity(node.attrib, [parse_schema(n) for n in node])
        case 'description':
            return Description(node.text)
        case 'field':
            return Field(node.attrib)
        case 'reference':
            return Reference(node.attrib)
        case 'union':
            return Union(node.attrib, [parse_schema(n) for n in node])
        case 'association':
            return Association(node.attrib)
        case _:
            raise "Error unrecognised node type {}".format(node.tag)


schema = parse_schema(my_tree.getroot())
schema.validate()
schema.build()

architecture = "architectures/{arch}/".format(arch=args.architecture)


def process_template(src, target, data):
    data['warning'] = "Automatically generated from {} - DO NOT EDIT".format(src)
    data['output'] = args.output
    data['architecture'] = args.architecture
    print(src, '->', target)
    fh = open(src, "r")
    template = fh.read()
    fh.close()
    j2_template = Template(template, autoescape=False, undefined=StrictUndefined)
    result = j2_template.render(data)
    fh = open(target, "w")
    fh.write(result)
    fh.close()


for root, _, files in os.walk(architecture):
    for file in files:
        source_file = os.path.join(root, file)
        output_path = os.path.join(args.output, root[len(architecture):])
        os.makedirs(output_path, exist_ok=True)
        if file.endswith('.j2'):
            base_name = file[0:-3]
            if '%E' in base_name:
                for entity in schema.get_entities():
                    output_filename = base_name.replace('%E', entity.get_name())
                    final_output = os.path.join(output_path, output_filename)
                    process_template(source_file, final_output, {'entity': entity})
            else:
                final_output = os.path.join(output_path, base_name)
                process_template(source_file, final_output, {'schema': schema})
        else:
            final_output = os.path.join(output_path, file)
            shutil.copy(source_file, final_output)
            print(source_file, '->', final_output)
