from django.db.models.signals import post_delete
from django.dispatch import receiver
from .models import CodeSnippet, OCRProcess

@receiver(post_delete, sender=CodeSnippet)
def delete_related_ocrprocess(sender, instance, **kwargs):
    try:
        ocr_process = OCRProcess.objects.get(snippet=instance)
        ocr_process.delete()
    except OCRProcess.DoesNotExist:
        pass
