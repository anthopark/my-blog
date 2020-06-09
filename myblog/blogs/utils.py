from myblog import db
from myblog.models import BlogEntry, User, Tag, entry_tag
from flask_login import current_user


def create_blog_entry(post_form) -> BlogEntry:
    entry = BlogEntry(title=post_form.title.data,
                      content=post_form.content.data,
                      author=current_user)

    db.session.add(entry)
    db.session.commit()

    return entry


def update_blog_entry(entry, post_form):

    entry.title = post_form.title.data
    entry.content = post_form.content.data
    db.session.commit()

    # updating tags
    existing_tags = set([t.name for t in entry.tags])
    updated_tags = split_tags(post_form.tags.data)

    new_tags = updated_tags - existing_tags
    removing_tags = existing_tags - updated_tags

    handle_tags(entry, new_tags)
    _delete_tags(entry, removing_tags)


def handle_tags(entry, tags: {str}):

    # for tag-entry association table
    tag_entry_ids = []

    for tag in tags:
        result = Tag.query.filter_by(name=tag.title()).first()
        if not result:
            new_tag = create_tag(tag)
            tag_entry_ids.append((new_tag.id, entry.id))
        else:
            tag_entry_ids.append((result.id, entry.id))
    
    _populate_assoc_table(tag_entry_ids)


def split_tags(tags_from_form: str) -> {str}:
    return set([t.strip().title() for t in tags_from_form.split(',') if t != ''])


def create_tag(tag: str) -> Tag:
    new_tag = Tag(name=tag.title())
    db.session.add(new_tag)
    db.session.commit()

    return new_tag


def _populate_assoc_table(ids: [(int, int)]) -> None:
    db.session.execute(entry_tag.insert().values(ids))
    db.session.commit()


def _delete_tags(entry, tags: {str}):
    for tag in tags:
        result = Tag.query.filter_by(name=tag.title()).first()
        if result:
            entry.tags.remove(result)
    
    db.session.commit()

def get_tags_from_blog_entry(entry) -> [str]:
    return [tag.name for tag in entry.tags]


def update_entry_tag(existing_tags: [str], updated_tags: [str], entry: BlogEntry):
    existing_tags = set(existing_tags)

    tag_entry_ids = []

    for upd_tag in updated_tags:
        if upd_tag not in existing_tags:
            result = Tag.query.filter_by(name=upd_tag.title()).first()
            if not result:
                # make a new tag
                new_tag = Tag(name=upd_tag.title())
                db.session.add(new_tag)
                tag_entry_ids.append((new_tag.id, entry.id))
            else:
                tag_entry_ids.append((result.id, entry.id))
        else:
            existing_tags.remove(upd_tag)

    db.session.execute(entry_tag.insert().values(tag_entry_ids))
    db.session.commit()

    # remaining tag to be deleted
    for rem_tag in existing_tags:
        result = Tag.query.filter_by(name=rem_tag.title()).first()
        if result:
            entry.tags.remove(result)

    db.session.commit()


def get_tag_frequency_list() -> [(str, int)]:
    result = []

    for t in Tag.query.all():
        result.append(
            (t.name.lower(), len(t.entries))
        )
    
    return sorted(result, key=(lambda x: x[0]))