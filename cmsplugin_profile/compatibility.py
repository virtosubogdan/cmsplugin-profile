import django

# Widget for toggle buttons
try:
    from cms_blogger.widgets import ToggleWidget
except:
    class ToggleWidget(django.forms.widgets.CheckboxInput):
        pass
