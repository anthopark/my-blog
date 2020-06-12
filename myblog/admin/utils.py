from myblog.models import BlogEntry, Tag
from flask_table import Table, Col, DateCol, LinkCol


class BlogEntryTable(Table):
    entry_id = Col('ID')
    title = Col('Title')
    date_posted = DateCol('Date Posted')
    is_published = Col('published')
    publish = LinkCol('Publish', 'blogs.publish_entry', url_kwargs=dict(id='entry_id'))
    unpublish = LinkCol('Unpublish', 'blogs.unpublish_entry', url_kwargs=dict(id='entry_id'))
    delete = LinkCol('Delete', 'blogs.delete_entry', url_kwargs=dict(id='entry_id'))


class EntryItem:
    def __init__(self, entry):
        self.entry = entry
        self.entry_id = entry.id
        self.title = entry.title
        self.date_posted = entry.date_posted
        self.is_published = entry.is_published

class TagTable(Table):
    tag_id = Col('ID')
    name = Col('Name')
    entry_num = Col('Num of Blogs')
    delete = LinkCol('Delete', 'blogs.delete_tag', url_kwargs=dict(id='tag_id'))



class TagItem:
    def __init__(self, tag):
        self.tag_id = tag.id
        self.name = tag.name
        self.entry_num = len(tag.entries)


def build_blog_entry_table():

    entries = BlogEntry.query.order_by(BlogEntry.id).all()
    items = [EntryItem(e) for e in entries]

    return BlogEntryTable(items)


def build_tag_table():
    
    tags = Tag.query.order_by(Tag.id).all()
    items = [TagItem(t) for t in tags ]

    return TagTable(items)
