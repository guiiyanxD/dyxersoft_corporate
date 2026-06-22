from django import forms

from . import selectors


class ContactoForm(forms.Form):
    nombre = forms.CharField(max_length=150)
    email = forms.EmailField()
    empresa = forms.CharField(max_length=150, required=False)
    servicio_interes = forms.ChoiceField(required=False)
    mensaje = forms.CharField(widget=forms.Textarea)

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields["servicio_interes"].choices = self._choices_servicio_interes()

    @staticmethod
    def _choices_servicio_interes():
        """Construye las choices dinámicamente desde los Servicios y Proyectos activos.

        Así el <select> del formulario y los botones "Solicitar demo"
        (?servicio=<slug_demo>) siempre quedan sincronizados con los datos
        reales del Admin, sin duplicar la lista de servicios en código.
        """
        choices = [("", "Seleccioná una opción (opcional)")]
        choices += [(s.slug, s.nombre) for s in selectors.servicios_activos()]
        choices += [(p.slug_demo, f"Demo — {p.nombre}") for p in selectors.proyectos_activos()]
        choices.append(("otro", "Otro / no especificado"))
        return choices
