# Python Interview Questions & Coding Challenges - Session 12

## Concept Questions

- What is Django's MTV pattern? 

- What's the difference between blank=True and null=True?

- What's the difference between auto_now and auto_now_add?

- What are Django migrations and why are they important?

- What is the N+1 query problem? How to avoid it in Django

- What is the Meta class in Django models?

- What's the purpose of __str__() method in models?


## Coding Challenge:

### 1. Implement the Blog app on your own
Follow the quick reference guide to create the blog app on your local step by step

### 2. Django ORM practice
```
# Write these queries in shell and save the output:

# 1. Get all published posts
# 2. Get all posts by user 'john'
# 3. Get all posts in "Technology" category
# 4. Count total posts
# 5. Count total comments
# 6. Get posts with no categories
# 7. Get the 3 newest posts
# 8. Get all categories sorted alphabetically
```

### 3. Add a View Counter
- Step 1: Update Model to add a views integer field
- Step 2: Create & Run Migration
- Step 3: Increase the post views when the post_detail view is processed
- Step 4: Update Admin to show post views
- Step 5: Show in Template
```html
<!-- In post_detail.html, add: -->
<div class="meta">
    {{ post.views }} views
</div>
```


### 4. Add Custom Model Methods
- Add These Methods to Post Model
``` python
def get_excerpt(self):
    """Return first 100 characters of content"""

def published_recently(self):
    """Check if published in last 7 days"""

def has_multiple_categories(self):
    """Check if post has more than one category"""
```

- Use in Templates:
```html
<!-- In index.html: -->
<p>{{ post.get_excerpt }}</p>

{% if post.published_recently %}
    <span class="badge">🆕 New!</span>
{% endif %}
```

- use in Admin:
``` python
# Add to PostAdmin list_display:
def is_new(self, obj):
    return obj.published_recently()
is_new.boolean = True
is_new.short_description = 'Recent?'
```



