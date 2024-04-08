from modeltranslation.translator import register, TranslationOptions
from .models import InstallationStep


@register(InstallationStep)
class InstallationStepTranslationOptions(TranslationOptions):
    fields = ('title', 'description',)
