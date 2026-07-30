from __future__ import annotations

from rest_framework import serializers


class TranslatableModelSerializer(serializers.ModelSerializer):
    """
    Mixin for DRF Serializers to dynamically resolve localized fields
    based on ?lang= query param or Accept-Language HTTP header with Fallback logic:
    Target Language (ru/uz/en) -> ru -> uz -> en -> Any available translation.
    """
    translatable_fields: tuple[str, ...] = ()

    def get_fields(self):
        fields = super().get_fields()
        return fields

    def get_default_complete_fields(self):
        return super().get_fields()

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field_name in self.translatable_fields:
            if field_name not in self.fields:
                self.fields[field_name] = serializers.CharField(read_only=True, required=False)

    def get_requested_language(self) -> str:
        request = self.context.get("request")
        if request:
            lang = request.query_params.get("lang")
            if lang in ["ru", "uz", "en"]:
                return lang
            
            accept_lang = request.headers.get("Accept-Language", "").lower()
            if "uz" in accept_lang:
                return "uz"
            elif "en" in accept_lang:
                return "en"
            elif "ru" in accept_lang:
                return "ru"

        return "ru"

    def to_representation(self, instance):
        ret = super().to_representation(instance)
        lang = self.get_requested_language()

        for field_name in self.translatable_fields:
            localized_val = getattr(instance, f"{field_name}_{lang}", None)
            
            # Fallback chain: ru -> uz -> en -> first non-empty
            if not localized_val:
                for fallback_lang in ["ru", "uz", "en"]:
                    val = getattr(instance, f"{field_name}_{fallback_lang}", None)
                    if val:
                        localized_val = val
                        break
            
            if not localized_val:
                localized_val = getattr(instance, field_name, "")

            ret[field_name] = localized_val

        return ret
