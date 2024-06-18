from django.forms.widgets import ClearableFileInput

class MultipleFileInput(ClearableFileInput):
    allow_multiple_selected = True

    def value_from_datadict(self, data, files, name):
        if isinstance(files.get(name), list):
            return files.getlist(name)
        return files.get(name)

    def format_value(self, value):
        if value is None or isinstance(value, str):
            return value
        if isinstance(value, list):
            return [super().format_value(v) for v in value]
        return super().format_value(value)
