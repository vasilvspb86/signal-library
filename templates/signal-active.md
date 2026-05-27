---
# MUST fields (12). Fill all before pushing.
id: <% tp.file.title.toLowerCase().replace(/\s+/g, '-') %>
name: ""
year: <% new Date().getFullYear() %>
domain: ""                              # ∈ signals/_taxonomy.yml domains
human_task: ""                          # "How can I …?"
existential_essence: ""                 # The deeper-meaning layer (curator's interpretation)
compas_segment:                         # 1–8
macrotrend: ""
diffusion_stage: ""                     # Emerging | Innovator | Early Adopter | Early Majority | Mainstream
status: active
captured_at: <% tp.date.now("YYYY-MM-DD") %>
verified_at: <% tp.date.now("YYYY-MM-DD") %>
schema_version: 1

# MAY fields — fill if known
url: ""                                 # Omit if signal is observed pattern (not project/product)
location: ""
category: ""                            # Social | Economic | Technological | Political | Scientific | Ecological | Design Experience
players: []
disruptiveness: ""                      # Insignificant | Minor | Moderate | Major | Significant
time_horizon: ""                        # 1–4 | 5–9 | 10–14 | 15–19 | 20+
scope: ""                               # Global | Widespread | Sector | Niche | Limited
cross_industry: []
source_channel: ""
shift_from: ""                          # Structured FROM (alt to body section)
shift_to: ""                            # Structured TO
trend: ""                               # One-line trend name this signal belongs to
microtrend: ""                          # More specific micro-trend formulation
next: ""                                # Forward projection: what comes next if this signal scales

tags: []
---

# <% tp.file.title %>

> [One-line subtitle capturing the shift the signal represents.]

## Anti-hype marker
[What norm does this break? Why is this not just mainstream noise?]

## FROM → TO
- **From:** [old behavior / value logic]
- **To:** [new behavior / emerging norm]

## Bridge Map
- [[]]
- [[]]
- [[]]
