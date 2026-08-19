---
title: "EP Blog"
description: "A blog for PageMotor. Post content type, chronological index with excerpts and pagination, categories, tags, bylines, and previous/next navigation."
---

EP Blog adds blogging to PageMotor. The core platform ships Page, HTML, Home and 404 content types; EP Blog adds a Post type with its own admin manager, a reverse-chronological index, categories and tags, author bylines, and post-to-post navigation.

Published by [ElmsPark Studio](https://elmspark.com).

## Overview

- **Post content type** with its own Select Post / Create New Post / Edit Post screens.
- **Post details panel** in the editor: category, tags, excerpt, featured image URL.
- **Chronological index** with excerpts, category badges, bylines and pagination.
- **Categories** defined once in settings, picked per post from a dropdown.
- **Tags** as free comma-separated text, filterable on the index.
- **Bylines** with the author's display name, toggleable.
- **Previous/next navigation** and a byline shortcode for single posts.
- **BlogPosting structured data** on every post, automatically.
- **RSS feed of posts** at `/feed/rss/post` via EP RSS 1.1.6 or later.
- **Comments** on posts via EP Comments; **scheduled publishing** via EP Scheduled Content.

## Requirements

- **PageMotor 0.8.3 or later**
- **EP Suite base class** (bundled)
- **EP RSS 1.1.6+** (optional, for the post feed)

## Installation

1. Download `ep-blog.zip` from the [EP Suite downloads page](https://updates.elmspark.com/download.php?plugin=ep-blog).
2. Upload via **Plugins → Manage Plugins**. Activate.

## Getting started

1. Open **Plugins → Blog** and define your categories, one per line. Plain names work (`News`); use `slug|Name` when you want to control the slug.
2. Create a page for the blog, for example `/journal/`, and put `[ep-blog]` in its body. Enter that page's URL as the **Blog index URL** in settings.
3. Create posts under **Content → Post**. Set each post's Parent to the blog page so post URLs nest under it (`/journal/my-post/`).
4. Optionally add `[ep-blog-meta]` at the top of each post's body and `[ep-blog-post-nav]` at the bottom.

Posts render through your theme automatically — EP Blog clones the theme's Page template into a Post template the first time it runs, so there is no Theme Editor work to do.

## Shortcodes

| Shortcode | Renders |
|---|---|
| `[ep-blog]` | The index: newest first, excerpts, pagination |
| `[ep-blog category="news"]` | Index pinned to one category |
| `[ep-blog-recent limit="5"]` | Compact recent-posts list |
| `[ep-blog-categories]` | Category list with counts |
| `[ep-blog-meta]` | Byline for the current post: date, author, category, tags |
| `[ep-blog-post-nav]` | Older/newer links on the current post |

Index arguments: `category`, `tag`, `limit` (posts per page), `pagination="off"`, `heading="h3"`.

EP Blog is also available as a Box plugin — place it in a Block via the Theme Editor to render the index without shortcodes.

## Settings

- **Categories.** One per line, `Name` or `slug|Name`.
- **Blog index URL.** The page carrying `[ep-blog]`. Category and tag links on single posts point here.
- **Posts per page.** 5 to 20.
- **Excerpt length.** Short (160), medium (240) or long (320) characters. A hand-written excerpt on the post always wins over the generated one.
- **Date format.** Four formats, day-first or month-first.
- **Author byline.** Show or hide the author on posts and in the index.

## Feeds, comments, scheduling

- With **EP RSS 1.1.6+** active, your post feed is at `/feed/rss/post` (Atom: `/feed/atom/post`).
- **EP Comments** works on posts exactly as on pages, including the per-page toggle.
- **EP Scheduled Content** publishes post drafts automatically at a future date and time.

## API

`list-posts` (public): returns live posts newest first with URL, date, author, category, tags and excerpt. Optional `category`, `tag` and `limit` arguments.
