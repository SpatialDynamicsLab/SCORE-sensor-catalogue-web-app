from django import forms
from .models import InstallationStep

class InstallationStepForm(forms.ModelForm):
    class Meta:
        model = InstallationStep
        fields = ['sensor', 'step_number', 'title', 'description', 'step_type', 'image', 'input_type', 'input_label', 'redirect_url', 'input_processing_url']
        widgets = {
            'description': forms.Textarea(attrs={'cols': 40, 'rows': 5}),
            'step_type': forms.Select(choices=InstallationStep.STEP_TYPE_CHOICES),
        }
    def clean_step_number(self):
        step_number = self.cleaned_data.get('step_number')
        sensor = self.cleaned_data.get('sensor')

        # Check if the step_number is already assigned for the selected sensor
        if InstallationStep.objects.filter(sensor=sensor, step_number=step_number).exists():
            raise forms.ValidationError(f"Step number {step_number} is already assigned to this sensor.")
        return step_number