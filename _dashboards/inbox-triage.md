# Inbox triage — all drafts by capture date

Daily quick-triage view. Keep, delete, or move to `_archive/reading/`.

```dataview
TABLE
  file.link AS Draft,
  file.folder AS Folder,
  captured_at AS Captured,
  url AS URL,
  source_channel AS Source
FROM "signals/_inbox"
WHERE status = "draft"
SORT captured_at DESC
```
