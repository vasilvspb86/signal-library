# Needs Attention — Active signals with blank MUST fields

These signals are in `signals/active/` but have one or more MUST fields blank. Push will fail until they are filled.

```dataview
TABLE
  file.link AS Signal,
  filter(["id","name","year","domain","human_task","existential_essence","compas_segment","macrotrend","diffusion_stage","captured_at","verified_at"], (f) => !this[f] OR this[f] = "") AS "Missing"
FROM "signals/active"
WHERE status = "active"
  AND (
       !id OR id = ""
    OR !name OR name = ""
    OR !year
    OR !domain OR domain = ""
    OR !human_task OR human_task = ""
    OR !existential_essence OR existential_essence = ""
    OR !compas_segment
    OR !macrotrend OR macrotrend = ""
    OR !diffusion_stage OR diffusion_stage = ""
    OR !captured_at
    OR !verified_at
  )
SORT file.name ASC
```
