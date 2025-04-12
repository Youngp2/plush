from django.contrib import admin
from . models import Item, ItemImage

# Register your models here.
class itemImageInline(admin.TabularInline):
    model = ItemImage
    extra = 1
    fields = ('image', 'is_main', 'image_preview')
    readonly_fields = ('image_preview',)
    
    def image_preview(self, obj):
        if obj.image:
            return f'<img src = "{obj.image.url}" style = "width:10px;" />'
        return " "
    image_preview.allow_tags = True
    image_preview.short_description = 'Preview'
    
class ItemAdmin(admin.ModelAdmin):
    inlines = [itemImageInline]
    
admin.site.register(Item, ItemAdmin)

