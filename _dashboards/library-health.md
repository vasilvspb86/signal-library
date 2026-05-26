# Library health — distribution metrics

## Active signals total

```dataview
TABLE WITHOUT ID
  "Active signals" AS Metric,
  length(rows) AS Count
FROM "signals/active"
WHERE status = "active"
GROUP BY "all"
```

## Added this week

```dataview
LIST captured_at
FROM "signals/active"
WHERE status = "active"
  AND captured_at >= (date(today) - dur(7 days))
SORT captured_at DESC
```

## Inbox depth (alarm if >50)

```dataview
TABLE WITHOUT ID
  file.folder AS Inbox,
  length(rows) AS Drafts
FROM "signals/_inbox"
WHERE status = "draft"
GROUP BY file.folder
```

## Stale signals (>6 months since verified)

```dataview
LIST verified_at
FROM "signals/active"
WHERE status = "active"
  AND verified_at < (date(today) - dur(6 months))
SORT verified_at ASC
```

## Domain distribution

```dataview
TABLE WITHOUT ID
  domain AS Domain,
  length(rows) AS Count
FROM "signals/active"
WHERE status = "active"
GROUP BY domain
SORT length(rows) DESC
```

## Compas segment spread (1–8)

```dataview
TABLE WITHOUT ID
  compas_segment AS Segment,
  length(rows) AS Count
FROM "signals/active"
WHERE status = "active"
GROUP BY compas_segment
SORT compas_segment ASC
```
