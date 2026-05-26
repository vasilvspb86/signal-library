# Aging signals — retirement candidates

Quarterly retirement candidates. Active signals where `year` is >3 years old OR `verified_at` is >6 months old.

```dataview
TABLE
  file.link AS Signal,
  year AS Year,
  verified_at AS "Last verified",
  diffusion_stage AS Diffusion
FROM "signals/active"
WHERE status = "active"
  AND (
    year < (date(today).year - 3)
    OR verified_at < (date(today) - dur(6 months))
  )
SORT verified_at ASC
```
