from jinja2 import StrictUndefined, Environment, BaseLoader, TemplateNotFound
import os
import inflect
import shutil


inflection = inflect.engine()

def mixed_case(string):
    return ''.join([s.capitalize() for s in string.split('_')])

class MetaDataLoader(BaseLoader):
    def __init__(self, input_root):
        self.input_root = input_root

    def get_source(self, environment, template):
        path = os.path.join(self.input_root, template)
        if not os.path.exists(path):
            raise TemplateNotFound(path)
        mtime = os.path.getmtime(path)
        with open(path) as f:
            source = f.read()
        return source, template, lambda: mtime == os.path.getmtime(path)


class TemplateProcessor:
    def __init__(self, architecture, semantics, output_root):
        self.architecture = architecture
        self.input_root = os.path.join('architectures', architecture)
        self.semantics = semantics
        self.output_root = output_root
        self.environment = Environment(autoescape=False, loader=MetaDataLoader(self.input_root), undefined=StrictUndefined)
        self.environment.filters["singular"] = inflection.singular_noun
        self.environment.filters["mixed_case"] = mixed_case

    def __process_template(self, template, target, data):
        data['warning'] = "Automatically generated from {} - DO NOT EDIT".format(template)
        data['output'] = self.output_root
        data['architecture'] = self.architecture
        print(template, '->', target)
        j2_template = self.environment.get_template(template)
        result = j2_template.render(data)
        fh = open(target, "w")
        fh.write(result)
        fh.close()

    def process_templates(self):
        for directory, _, files in os.walk(self.input_root):
            for file in files:
                relative_dir = directory[len(self.input_root) + 1:]
                output_dir = os.path.join(self.output_root, relative_dir)
                template = os.path.join(relative_dir, file)
                os.makedirs(output_dir, exist_ok=True)
                if file.endswith('.j2'):
                    base_name = file[0:-3]
                    if '%E' in base_name:
                        for entity in self.semantics.get_entities():
                            final_output = os.path.join(output_dir, base_name.replace('%E', entity.get_name()))
                            self.__process_template(template, final_output, {'entity': entity})
                    else:
                        final_output = os.path.join(output_dir, base_name)
                        self.__process_template(template, final_output, {'schema': self.semantics})
                elif file.endswith('.j2h'):
                    pass  # macros
                else:
                    final_output = os.path.join(output_dir, file)
                    shutil.copy(os.path.join(self.input_root, template), final_output)
                    print(template, '->', final_output)
