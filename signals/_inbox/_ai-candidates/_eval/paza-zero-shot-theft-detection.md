---
status: draft
captured_at: '2026-06-18'
captured_via: signal-compass-web-research
schema_version: 1
id: paza-zero-shot-theft-detection
name: Paza — Zero-Shot Retail Theft Detection
year: 2026
url: https://pith.science/paper/2604.14846
source_channel: Exa neural search
domain: Retail
human_task: Protect personal movement in commercial space from behavioral profiling systems that no longer require expensive custom training to deploy.
existential_essence: Protect personal movement in commercial space from behavioral profiling systems that no longer require expensive custom training to deploy.
compas_segment: 2
macrotrend: New Privacy
diffusion_stage: Innovator
time_horizon: April–May 2026 (preprint + review)
disruptiveness: Major
tags: []
shift_from: AI-based theft detection required weeks of custom model training on proprietary datasets, costing $200–500/month per store and limiting deployment to large chains.
shift_to: A zero-shot framework orchestrating off-the-shelf vision-language models can monitor 10–20 stores on a single GPU for $50–100/month, with built-in face obfuscation — making behavioral surveillance economically accessible to any retailer.
---

# Paza — Zero-Shot Retail Theft Detection

> Protect personal movement in commercial space from behavioral profiling systems that no longer require expensive custom training to deploy.

## Anti-hype marker
The system achieves 89.5% precision without any training data by using dwell-time plus behavioral pre-filters — meaning the privacy-preserving face-obfuscation feature ships alongside a system that infers intent from body language alone.

## FROM -> TO
- **From:** AI-based theft detection required weeks of custom model training on proprietary datasets, costing $200–500/month per store and limiting deployment to large chains.
- **To:** A zero-shot framework orchestrating off-the-shelf vision-language models can monitor 10–20 stores on a single GPU for $50–100/month, with built-in face obfuscation — making behavioral surveillance economically accessible to any retailer.

## Curator notes
- Distilled from web result captured on 2026-06-18 via signal-compass-web-research.
- Originating brief job_id: eval-success-08-antitrend-retail-facial-rec-1781774548
- Distillation provenance is verbatim -- see ## Original source below.

## Original source
> We present Paza, a zero-shot retail theft detection framework that achieves practical concealment detection without training any model. Our approach orchestrates multiple existing models in a layered pipeline - cheap object detection and pose estimation running continuously, with an expensive vision-language model (VLM) invoked only when behavioral pre-filters trigger.
