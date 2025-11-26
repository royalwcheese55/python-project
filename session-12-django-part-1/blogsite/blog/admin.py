from django.contrib import admin
from blog.models import Post, Comment,Category

# Register your models here.
# admin.site.register(Post)
admin.site.register(Comment)
# admin.site.register(Category)

admin.site.site_header = "My Blog"
admin.site.site_title = 'My Blog Portal'

@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ('name', 'post_count', 'created_at')
    
    def post_count(self, obj):
        return obj.posts.count()
    post_count.short_description = 'Number of posts'
    
@admin.register(Post)
class PostAdmin(admin.ModelAdmin):
    list_display = ('title', 'author', 'published', 'get_categories')
    
    # fieldsets = (
    #     ('Content', {
    #         'fields': ('title', 'content', 'author')
    #     }),
    # )
    
    search_fields = ('title', 'author__username', 'content')

    def get_categories(self, obj):
        return ", ".join([c.name for c in obj.categories.all()])
    get_categories.short_description = 'Categories'