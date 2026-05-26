#!/usr/bin/env python3
"""One-shot import of 36 signals from the Compas Lumiknows dashboard.

Source: https://compas-dashboard-org.netlify.app/  (rawTSData JS array)
All Russian content has been translated to English inline below.

Mapping rules (per Signal Library design spec §3 + import discussion):
- id            ← kebab-case slug of title
- name          ← title
- year          ← 2026 (current)
- domain        ← second part of `futures` (after "Organisation, "), via DOMAIN_MAP
- human_task    ← pre-translated "How can I…?" formulation
- existential_essence ← pre-translated existential_core
- compas_segment ← first integer in `compas` (e.g., "4, 3" → 4)
- macrotrend    ← first item in `macro`, remapped via MACRO_REMAP
- diffusion_stage ← derived from `horizon` + `influence` (see diffusion_for)
- url           ← link
- shift_from/shift_to ← pre-translated
- time_horizon  ← "1-3"→"1–4", "3-7"→"5–9", "7+"→"10–14"
- disruptiveness ← influence ≥9 Significant, ≥7 Major, else Moderate
- source_channel ← "AI Lumiknows"
- tags          ← hashtags, "Неотраслевой" remapped to "Lifestyle"

Run: python tools/import_compas.py
"""
import re
from datetime import date
from pathlib import Path

VAULT_ROOT = Path(__file__).resolve().parent.parent
ACTIVE_DIR = VAULT_ROOT / "signals" / "active"
TODAY = date.today().isoformat()

DOMAIN_MAP = {
    "Work": "Workplace",
    "Energy": "Energy",
    "Society": "Society",
    "Wellbeing": "Wellbeing",
    "Finance & Banking": "Finance",
    "Medicine & Healthcare": "Health",
    "Communication": "Communication",
    "Mobility": "Mobility",
    "Knowledge": "Knowledge",
    "Education": "Education",
    "Retail": "Retail",
    "AI": "AI",
}

HORIZON_MAP = {
    "1-3": "1–4",
    "3-7": "5–9",
    "7+": "10–14",
}

# User decision: do NOT add new macrotrends to taxonomy.
# Remap source-only macros to closest existing taxonomy macros.
MACRO_REMAP = {
    "Sustainables": "Sustainable Development",
    "Digital Sensorics": "Ambient Intelligence",
}


def slugify(text: str) -> str:
    return re.sub(r"[^a-z0-9]+", "-", text.lower()).strip("-")


def parse_first_compas(s) -> int:
    return int(str(s).split(",")[0].strip())


def parse_first_macro(s: str) -> str:
    first = s.split(",")[0].strip()
    return MACRO_REMAP.get(first, first)


def parse_futures_domain(s: str) -> str:
    """Take the second part of 'Organisation, X' and map to our taxonomy."""
    parts = [p.strip() for p in s.split(",")]
    candidate = parts[-1] if len(parts) > 1 else parts[0]
    if candidate not in DOMAIN_MAP:
        raise ValueError(f"Unknown domain candidate: {candidate!r} (from {s!r})")
    return DOMAIN_MAP[candidate]


def parse_tags(hashtags: str) -> list[str]:
    raw = [t.strip().lstrip("#") for t in hashtags.split(",")]
    return [
        ("Lifestyle" if t == "Неотраслевой" else t)
        for t in raw if t
    ]


def diffusion_for(horizon: str, influence: int) -> str:
    if horizon == "7+":
        return "Emerging"
    if horizon == "3-7":
        return "Innovator"
    if horizon == "1-3":
        return "Early Adopter" if influence >= 8 else "Innovator"
    return "Innovator"


def disruptiveness_for(influence: int) -> str:
    if influence >= 9:
        return "Significant"
    if influence >= 7:
        return "Major"
    return "Moderate"


def yq(v: str) -> str:
    """Escape a string for embedding in a double-quoted YAML scalar."""
    return v.replace("\\", "\\\\").replace('"', '\\"')


def render_signal(s: dict) -> str:
    slug = slugify(s["title"])
    compas = parse_first_compas(s["compas"])
    macro = parse_first_macro(s["macro"])
    domain = parse_futures_domain(s["futures"])
    diffusion = diffusion_for(s["horizon"], s["influence"])
    horizon = HORIZON_MAP[s["horizon"]]
    disruptiveness = disruptiveness_for(s["influence"])
    tags = parse_tags(s["hashtags"])
    # Render tags as YAML flow list with double-quoted entries
    tags_yaml = "[" + ", ".join(f'"{t}"' for t in tags) + "]"

    return f"""---
id: {slug}
name: {s["title"]}
year: 2026
domain: {domain}
human_task: "{yq(s["human_task_en"])}"
existential_essence: "{yq(s["existential_essence_en"])}"
compas_segment: {compas}
macrotrend: {macro}
diffusion_stage: {diffusion}
status: active
captured_at: {TODAY}
verified_at: {TODAY}
schema_version: 1

url: {s["link"]}
time_horizon: "{horizon}"
disruptiveness: {disruptiveness}
source_channel: "AI Lumiknows"
shift_from: "{yq(s["shift_from_en"])}"
shift_to: "{yq(s["shift_to_en"])}"
tags: {tags_yaml}
---

# {s["title"]}

> {s["subtitle_en"]}

## Anti-hype marker
{s["why_ts_en"]}

## FROM → TO
- **From:** {s["shift_from_en"]}
- **To:** {s["shift_to_en"]}
"""


SIGNALS = [
    {
        "title": "Kickresume",
        "link": "https://www.kickresume.com/en/ai-career-bot/",
        "existential_essence_en": "Customize communication with various AI recruiters.",
        "human_task_en": "How can I customize communication with various AI recruiters?",
        "subtitle_en": "AI career bot.",
        "why_ts_en": "Automating the routine of job applications through an AI agent.",
        "shift_from_en": "Manual search and stress of self-presentation",
        "shift_to_en": "AI agent conducts the conversation for the candidate",
        "hashtags": "#AIProxy, #CareerAutonomy",
        "compas": "1", "macro": "Deep Customisation", "futures": "Organisation, Work",
        "horizon": "1-3", "influence": 7,
    },
    {
        "title": "Cornerstone",
        "link": "https://www.cornerstoneondemand.com/platform/hr-and-workforce-intelligence/",
        "existential_essence_en": "Fit into the emerging local skill-based labor market.",
        "human_task_en": "How can I fit into the emerging local skill-based labor market?",
        "subtitle_en": "Talent analytics.",
        "why_ts_en": "Shift from fixed org-chart to dynamic skill graph.",
        "shift_from_en": "Rigid job title and hierarchy",
        "shift_to_en": "Liquid and measurable skill portfolio",
        "hashtags": "#SkillBasedGraphs, #SkillPassport",
        "compas": "4", "macro": "Distributed Innovations", "futures": "Organisation, Work",
        "horizon": "1-3", "influence": 7,
    },
    {
        "title": "G42",
        "link": "https://www.g42.ai/resources/news/ai-agents-can-now-apply-jobs-g42",
        "existential_essence_en": "Reach a new level of agency to prepare for future work alongside AI agents.",
        "human_task_en": "How can I reach a new level of agency to prepare for future work alongside AI agents?",
        "subtitle_en": "AI agents for job search.",
        "why_ts_en": "Algorithms take over the function of social expansion.",
        "shift_from_en": "Human as linear executor",
        "shift_to_en": "Human as partner and operator of AI agents",
        "hashtags": "#AgenticDelegation, #AIHybrids",
        "compas": "7", "macro": "True Self & Identity", "futures": "Organisation, Work",
        "horizon": "3-7", "influence": 8,
    },
    {
        "title": "Oklo",
        "link": "https://oklo.com",
        "existential_essence_en": "Lifestyle signal. Gain energy independence from megacities to sustain one's own AI infrastructure.",
        "human_task_en": "How can I gain energy independence from megacities to sustain my own AI infrastructure?",
        "subtitle_en": "Green micro-energy.",
        "why_ts_en": "Creating sovereign energy grids outside megacities.",
        "shift_from_en": "Dependence on central power grids",
        "shift_to_en": "Autonomous green micro-capacities",
        "hashtags": "#Неотраслевой, #EnergySovereignty",
        "compas": "4, 3", "macro": "Sustainables, Independence", "futures": "Organisation, Energy",
        "horizon": "7+", "influence": 8,
    },
    {
        "title": "RestofWorld",
        "link": "https://restofworld.org/2026/china-ai-one-person-companies-incentives/",
        "existential_essence_en": "Realize entrepreneurial potential through local state-owned coworking spaces.",
        "human_task_en": "How can I realize my entrepreneurial potential through local state-owned coworking spaces?",
        "subtitle_en": "China's solo unicorns.",
        "why_ts_en": "Removing barriers to solo creation in a complex economy.",
        "shift_from_en": "Working in a corporation for scale",
        "shift_to_en": "Fully free solo creator with corporate-level power",
        "hashtags": "#SoloUnicorn, #RadicalAutonomy",
        "compas": "4, 5", "macro": "Distributed Innovations, Democratisation of Creativity", "futures": "Organisation, Work",
        "horizon": "3-7", "influence": 9,
    },
    {
        "title": "Reddit (China Dating)",
        "link": "https://www.reddit.com/r/AutoNewspaper/comments/1s7mhtx/world_china_city_work_new_dating_trend_promotes/",
        "existential_essence_en": "Lifestyle signal. Preserve family integrity in the face of an all-consuming corporate machine.",
        "human_task_en": "How can I preserve my family's integrity in the face of an all-consuming corporate machine?",
        "subtitle_en": "Thread on \"paired hiring\".",
        "why_ts_en": "The organization takes on responsibility for the employee's micro-community.",
        "shift_from_en": "Isolated professional (Work-Life Balance)",
        "shift_to_en": "Integration of family into the corporate environment (Synthesis)",
        "hashtags": "#Неотраслевой, #WorkLifeSymphony",
        "compas": "6", "macro": "Compatibilitas", "futures": "Organisation, Society",
        "horizon": "1-3", "influence": 8,
    },
    {
        "title": "Rent a Human",
        "link": "https://rentahuman.ai/",
        "existential_essence_en": "Lifestyle signal. Find use for one's physical body and senses when cognitive labor is devalued by AI.",
        "human_task_en": "How can I find use for my physical body and senses when cognitive labor is devalued by AI?",
        "subtitle_en": "Renting out the physical body.",
        "why_ts_en": "A provocative project reflecting the crisis of devalued cognitive labor.",
        "shift_from_en": "Valuing humans by cognitive labor",
        "shift_to_en": "Monetization of purely physical presence",
        "hashtags": "#Неотраслевой, #Physicalization",
        "compas": "1, 7", "macro": "Deep Customisation, Physicalisation", "futures": "Organisation, Work",
        "horizon": "3-7", "influence": 7,
    },
    {
        "title": "Creator Fund",
        "link": "https://creatorfund.co/about/",
        "existential_essence_en": "Earn the right to realize one's vision, bypassing legacy approval institutions and relying on a community of peers.",
        "human_task_en": "How can I earn the right to realize my vision, bypassing legacy approval institutions and relying on a community of peers?",
        "subtitle_en": "Support for young creators.",
        "why_ts_en": "Decentralization of investment and trust.",
        "shift_from_en": "Dependence on venture funds and approval",
        "shift_to_en": "Direct support from a decentralized community",
        "hashtags": "#SelfActualisation, #GenZAutonomy",
        "compas": "5, 6", "macro": "Democratisation of Creativity, Social Capital", "futures": "Organisation, Finance & Banking",
        "horizon": "1-3", "influence": 7,
    },
    {
        "title": "Neiry",
        "link": "https://neiry.ru/mt-ny-promo",
        "existential_essence_en": "Lifestyle signal. Take conscious control of one's mental health based on brain data.",
        "human_task_en": "How can I take conscious control of my mental health based on brain data?",
        "subtitle_en": "Neural interface.",
        "why_ts_en": "Shift in tools for self-regulation and burnout prevention.",
        "shift_from_en": "Intuitive stress management",
        "shift_to_en": "Reliance on objective brain biodata",
        "hashtags": "#Неотраслевой, #NeuroFeedback",
        "compas": "7", "macro": "Mental & Emotional Wellbeing", "futures": "Organisation, Wellbeing",
        "horizon": "1-3", "influence": 8,
    },
    {
        "title": "Dock.io",
        "link": "https://dock.io",
        "existential_essence_en": "Reclaim ownership and control of one's digital profile.",
        "human_task_en": "How can I reclaim ownership and control of my digital profile?",
        "subtitle_en": "Digital skills passport.",
        "why_ts_en": "Decentralized sovereignty over personal data.",
        "shift_from_en": "Data held hostage by HR platforms",
        "shift_to_en": "Sole ownership of digital identity",
        "hashtags": "#TrueIdentity, #SelfSovereign",
        "compas": "2, 3", "macro": "Data Edge, Sovereignty", "futures": "Organisation, Work",
        "horizon": "3-7", "influence": 8,
    },
    {
        "title": "Chief Outsiders",
        "link": "https://chiefoutsiders.com",
        "existential_essence_en": "Move beyond corporate loyalty by selling one's unique top-tier expertise in metered, fractional doses.",
        "human_task_en": "How can I move beyond corporate loyalty by selling my unique top-tier expertise in metered, fractional doses?",
        "subtitle_en": "Fractional top executives.",
        "why_ts_en": "End of the lifetime-employment era, even at C-level.",
        "shift_from_en": "Employee tied to a single corporation",
        "shift_to_en": "Mobile and fractional expertise",
        "hashtags": "#FractionalLife, #LiquidTalent",
        "compas": "4, 3", "macro": "Distributed Innovations, Independence", "futures": "Organisation, Work",
        "horizon": "1-3", "influence": 8,
    },
    {
        "title": "Dassault",
        "link": "https://www.3ds.com/about/company/leadership/laurence-barthes",
        "existential_essence_en": "Reduce anxiety by living through the consequences of organizational decisions in safe virtual simulation.",
        "human_task_en": "How can I reduce anxiety by living through the consequences of organizational decisions in safe virtual simulation?",
        "subtitle_en": "Virtual leader twins.",
        "why_ts_en": "Reducing cognitive load and the cost of errors through simulations.",
        "shift_from_en": "Stress of blind decision-making",
        "shift_to_en": "Safe hypothesis testing on a digital twin",
        "hashtags": "#DigitalTwins, #RiskAnxiety",
        "compas": "1, 7", "macro": "Emotional AI, Mental & Emotional Wellbeing", "futures": "Organisation, Work",
        "horizon": "3-7", "influence": 7,
    },
    {
        "title": "Moderna",
        "link": "https://www.modernatx.com/",
        "existential_essence_en": "Reach C-suite-level competency to manage a unified pool of carbon (human) and silicon (AI agent) intelligence.",
        "human_task_en": "How can I reach C-suite-level competency to manage a unified pool of carbon and silicon intelligence?",
        "subtitle_en": "Integrated AI management.",
        "why_ts_en": "Erasing boundaries between managing people and algorithms.",
        "shift_from_en": "Separate management of IT and HR",
        "shift_to_en": "Unified management pool for carbon and silicon intelligence",
        "hashtags": "#FocusOnMeaning, #TechLiberation",
        "compas": "4", "macro": "Distributed Innovations", "futures": "Organisation, Medicine & Healthcare",
        "horizon": "1-3", "influence": 9,
    },
    {
        "title": "Block.xyz",
        "link": "https://block.xyz/inside/from-hierarchy-to-intelligence",
        "existential_essence_en": "Find one's place in a self-organizing peer network instead of submitting to a vertical hierarchy.",
        "human_task_en": "How can I find my place in a self-organizing peer network instead of submitting to a vertical hierarchy?",
        "subtitle_en": "Intelligence instead of hierarchy.",
        "why_ts_en": "Dismantling rigid organizational structures in favor of flexible networks.",
        "shift_from_en": "Submission to vertical hierarchy",
        "shift_to_en": "Self-organizing network of entrepreneurial cells",
        "hashtags": "#PeerToPeer, #DistributedInnovations",
        "compas": "4", "macro": "Distributed Innovations", "futures": "Organisation, Work",
        "horizon": "3-7", "influence": 9,
    },
    {
        "title": "Haier (RenDanHeYi)",
        "link": "https://rendanheyi.com/",
        "existential_essence_en": "Realize entrepreneurial potential by leveraging the resources of a global ecosystem.",
        "human_task_en": "How can I realize my entrepreneurial potential by leveraging the resources of a global ecosystem?",
        "subtitle_en": "Entrepreneurial-cell model.",
        "why_ts_en": "Large-scale proof of viable ecosystems without middle managers.",
        "shift_from_en": "Executor inside a department",
        "shift_to_en": "CEO of one's own micro-enterprise",
        "hashtags": "#MicroEnterprises, #SafeAutonomy",
        "compas": "4", "macro": "Distributed Innovations", "futures": "Organisation, Work",
        "horizon": "3-7", "influence": 9,
    },
    {
        "title": "Gloat",
        "link": "https://gloat.com/",
        "existential_essence_en": "Unlock hidden talents by safely experimenting with roles inside the company.",
        "human_task_en": "How can I unlock my hidden talents by safely experimenting with roles inside the company?",
        "subtitle_en": "Talent marketplace.",
        "why_ts_en": "Enabling internal workforce mobility without bureaucracy.",
        "shift_from_en": "Career growth on a rigid ladder",
        "shift_to_en": "Liquid project-based identity within the company",
        "hashtags": "#SkillFluidity, #SelfDiscovery",
        "compas": "4", "macro": "Distributed Innovations", "futures": "Organisation, Work",
        "horizon": "1-3", "influence": 8,
    },
    {
        "title": "Buurtzorg",
        "link": "https://www.buurtzorg.com/",
        "existential_essence_en": "Restore meaning and empathy to one's profession by abandoning rigid KPIs.",
        "human_task_en": "How can I restore meaning and empathy to my profession by abandoning rigid KPIs?",
        "subtitle_en": "Self-managing teams.",
        "why_ts_en": "Proof of effective empathic self-management beating rigid metrics.",
        "shift_from_en": "Work driven by conveyor-belt KPIs",
        "shift_to_en": "Return of higher purpose and care for the Other",
        "hashtags": "#CareForOthers, #SelfManagement",
        "compas": "6", "macro": "Social Capital", "futures": "Organisation, Work",
        "horizon": "1-3", "influence": 9,
    },
    {
        "title": "Nike by Melrose",
        "link": "https://www.nike.com/retail/s/nike-by-melrose",
        "existential_essence_en": "Lifestyle signal. Feel part of one's tribe through physical brand localization.",
        "human_task_en": "How can I feel part of my tribe through physical brand localization?",
        "subtitle_en": "Hyperlocal retail.",
        "why_ts_en": "Lifestyle signal. Brands take on the role of a neighborhood's social glue.",
        "shift_from_en": "Global, faceless corporations",
        "shift_to_en": "Localized tribe and physical integration",
        "hashtags": "#Неотраслевой, #Planetocentricity",
        "compas": "6, 4", "macro": "Planetocentricity, Post Smart City", "futures": "Organisation, Retail",
        "horizon": "1-3", "influence": 6,
    },
    {
        "title": "Unilever",
        "link": "https://resources.gloat.com/resources/unilever-customer-success-story/",
        "existential_essence_en": "Freely apply one's best skills wherever they are needed most, bypassing bureaucracy.",
        "human_task_en": "How can I freely apply my best skills wherever they are needed most, bypassing bureaucracy?",
        "subtitle_en": "Mobility case study.",
        "why_ts_en": "Free flow of skills (Boundaryless Work).",
        "shift_from_en": "Rigid attachment to a single function",
        "shift_to_en": "Free application of talents outside bureaucracy",
        "hashtags": "#BoundarylessWork, #SkillFluidity",
        "compas": "4", "macro": "Distributed Innovations", "futures": "Organisation, Work",
        "horizon": "1-3", "influence": 7,
    },
    {
        "title": "WeChat Work",
        "link": "https://work.weixin.qq.com/",
        "existential_essence_en": "Unify family, friends, and work into a single seamless digital and social stream.",
        "human_task_en": "How can I unify family, friends, and work into a single seamless digital and social stream?",
        "subtitle_en": "Super-app.",
        "why_ts_en": "Erasing boundaries between personal, urban, and work spaces.",
        "shift_from_en": "Work/Life Balance separation",
        "shift_to_en": "Work-Life Symphony in a unified stream",
        "hashtags": "#LifeSymphony, #SuperApp",
        "compas": "4, 6", "macro": "Post Smart City, Social Capital", "futures": "Organisation, Communication",
        "horizon": "1-3", "influence": 9,
    },
    {
        "title": "Tesla (OTA Updates)",
        "link": "https://www.tesla.com/support/software-updates",
        "existential_essence_en": "Lifestyle signal. Receive predictive analytics and resolution of potential problems before they arise.",
        "human_task_en": "How can I receive predictive analytics and resolution of potential problems before they arise?",
        "subtitle_en": "Over-the-air product updates.",
        "why_ts_en": "Lifestyle signal. Things that don't age but improve over time.",
        "shift_from_en": "Breakdown followed by repair",
        "shift_to_en": "Ambient intelligence and background care",
        "hashtags": "#Неотраслевой, #AmbientCare",
        "compas": "2", "macro": "Ambient Intelligence", "futures": "Organisation, Mobility",
        "horizon": "1-3", "influence": 8,
    },
    {
        "title": "Eightfold-Novartis",
        "link": "https://eightfold.ai/customers/novartis/",
        "existential_essence_en": "Be evaluated on actual knowledge and abilities, not on social labels and resume lines.",
        "human_task_en": "How can I be evaluated on actual knowledge and abilities, not on social labels and resume lines?",
        "subtitle_en": "Hiring by skill graph.",
        "why_ts_en": "Assessing true potential hidden behind formal job titles.",
        "shift_from_en": "Evaluation by social labels (Resume)",
        "shift_to_en": "Evaluation of genuine cognitive abilities",
        "hashtags": "#SkillsOverTitles, #TrueIdentity",
        "compas": "7, 4", "macro": "True Self & Identity, Distributed Innovations", "futures": "Organisation, Work",
        "horizon": "3-7", "influence": 8,
    },
    {
        "title": "Automattic",
        "link": "https://automattic.com/work-with-us/",
        "existential_essence_en": "Gain absolute life freedom by fully controlling one's work schedule and location.",
        "human_task_en": "How can I gain absolute life freedom by fully controlling my work schedule and location?",
        "subtitle_en": "Asynchronous work.",
        "why_ts_en": "Abandoning synchronicity unlocks radical life autonomy.",
        "shift_from_en": "Synchronous office presence",
        "shift_to_en": "Asynchronous schedule and freedom of movement",
        "hashtags": "#AsyncLife, #TotalAutonomy",
        "compas": "3, 4", "macro": "Independence, Distributed Innovations", "futures": "Organisation, Work",
        "horizon": "1-3", "influence": 8,
    },
    {
        "title": "HBR (Read Sci-Fi)",
        "link": "https://hbr.org/2017/07/why-business-leaders-need-to-read-more-science-fiction",
        "existential_essence_en": "Overcome paralyzing fear of uncertainty through imagination training.",
        "human_task_en": "How can I overcome paralyzing fear of uncertainty through imagination training?",
        "subtitle_en": "Sci-Fi for leaders.",
        "why_ts_en": "Lifestyle signal. Return to intuitive and artistic cognition in business.",
        "shift_from_en": "Management by rigid past metrics",
        "shift_to_en": "Imagination training to adapt to chaos",
        "hashtags": "#Неотраслевой, #SciFiThinking",
        "compas": "7, 5", "macro": "Mental & Emotional Wellbeing, Democratisation of Creativity", "futures": "Organisation, Knowledge",
        "horizon": "1-3", "influence": 8,
    },
    {
        "title": "Braintrust",
        "link": "https://www.usebraintrust.com/",
        "existential_essence_en": "Become a full co-owner of the system where one creates value daily.",
        "human_task_en": "How can I become a full co-owner of the system where I create value daily?",
        "subtitle_en": "Talent network.",
        "why_ts_en": "Trustless-ecosystem model where talents own a share of the platform.",
        "shift_from_en": "Talent exploitation by a centralized platform",
        "shift_to_en": "Co-ownership of the network and sovereignty",
        "hashtags": "#UserOwned, #FairValue",
        "compas": "4, 3", "macro": "Distributed Innovations, Sovereignty", "futures": "Organisation, Work",
        "horizon": "3-7", "influence": 8,
    },
    {
        "title": "DeGruyter",
        "link": "https://www.degruyterbrill.com/document/doi/10.1515/jqas-2024-0010/html",
        "existential_essence_en": "Move from rigid roles to dynamic lineups by building adaptive ensembles based on compatibility alchemy.",
        "human_task_en": "How can I move from rigid roles to dynamic lineups by building adaptive ensembles based on compatibility alchemy?",
        "subtitle_en": "Quantum compatibility analysis.",
        "why_ts_en": "Lifestyle signal. Predictive algorithms decide who works best with whom.",
        "shift_from_en": "Team formation by intuition",
        "shift_to_en": "Removing decision stress through predictive analytics",
        "hashtags": "#Неотраслевой, #DataDeterminism",
        "compas": "4, 2", "macro": "Distributed Innovations, Ambient Intelligence", "futures": "Organisation, Work",
        "horizon": "3-7", "influence": 7,
    },
    {
        "title": "Architizer",
        "link": "https://architizer.com/projects/yagaba-kubori-intergenerational-library",
        "existential_essence_en": "Rebuild intergenerational connection by transferring tacit knowledge.",
        "human_task_en": "How can I rebuild intergenerational connection by transferring tacit knowledge?",
        "subtitle_en": "Intergenerational library.",
        "why_ts_en": "Lifestyle signal. Demand for empathy and experience transfer outside the digital environment.",
        "shift_from_en": "Digital isolation between generations",
        "shift_to_en": "Physical spaces for tacit-knowledge transfer",
        "hashtags": "#Неотраслевой, #TacitKnowledge",
        "compas": "6, 8", "macro": "Compatibilitas, Unity-Centricity", "futures": "Organisation, Education",
        "horizon": "3-7", "influence": 7,
    },
    {
        "title": "Meta Pods",
        "link": "https://www.businessinsider.com/metas-reality-labs-shifts-to-ai-native-pods-efficiency-2026-3",
        "existential_essence_en": "Abandon legacy job titles to become part of a flat design defined by degree of AI interaction.",
        "human_task_en": "How can I abandon legacy job titles to become part of a flat design defined by degree of AI interaction?",
        "subtitle_en": "AI-native pods.",
        "why_ts_en": "Human-algorithm synthesis as the new base unit of the company.",
        "shift_from_en": "Hierarchy of purely human roles",
        "shift_to_en": "Flat design of hybrid (Human+AI) cells",
        "hashtags": "#AIHybrids, #CoCreation",
        "compas": "4", "macro": "Distributed Innovations", "futures": "Organisation, Work",
        "horizon": "1-3", "influence": 9,
    },
    {
        "title": "Doordash",
        "link": "https://techcrunch.com/2026/03/19/doordash-launches-a-new-tasks-app-that-pays-couriers-to-submit-videos-to-train-ai",
        "existential_essence_en": "Monetize one's corporeality and physical movement through space.",
        "human_task_en": "How can I monetize my corporeality and physical movement through space?",
        "subtitle_en": "Couriers as data collectors.",
        "why_ts_en": "Couriers as physical sensors for training algorithms.",
        "shift_from_en": "Value of human as courier",
        "shift_to_en": "Ultra-monetization of basic physical movement",
        "hashtags": "#DataHarvesting, #GigSurvival",
        "compas": "1, 7", "macro": "Deep Customisation, Physicalisation", "futures": "Organisation, Work",
        "horizon": "1-3", "influence": 6,
    },
    {
        "title": "ScienceDaily",
        "link": "https://www.sciencedaily.com/releases/2025/10/251025084616.htm",
        "existential_essence_en": "Get a map of the body's sixth sense — interoception — to understand body-brain communication.",
        "human_task_en": "How can I get a map of my body's sixth sense — interoception — to understand body-brain communication?",
        "subtitle_en": "Brain synchronization research.",
        "why_ts_en": "Lifestyle signal. Deep understanding of physiology as the foundation of intelligence.",
        "shift_from_en": "Life in a digital cognitive bubble",
        "shift_to_en": "Return to embodiment and interoception",
        "hashtags": "#Неотраслевой, #CognitiveSync",
        "compas": "7", "macro": "Physicalisation", "futures": "Organisation, AI",
        "horizon": "7+", "influence": 9,
    },
    {
        "title": "FLOWSTATE",
        "link": "https://www.google.com/search?q=FLOWSTATE+Resonance+Analysis",
        "existential_essence_en": "Learn to enter deep focus on demand, escaping the noise.",
        "human_task_en": "How can I learn to enter deep focus on demand, escaping the noise?",
        "subtitle_en": "Resonance Analysis.",
        "why_ts_en": "Lifestyle signal. Attentional focus becomes a manageable and sellable resource.",
        "shift_from_en": "Toxic information noise",
        "shift_to_en": "Machine-assisted immersion into flow state",
        "hashtags": "#Неотраслевой, #FlowState",
        "compas": "1, 7", "macro": "Emotional AI, Mental & Emotional Wellbeing", "futures": "Organisation, Wellbeing",
        "horizon": "1-3", "influence": 7,
    },
    {
        "title": "EMOTIV",
        "link": "https://www.emotiv.com/enterprise/",
        "existential_essence_en": "Give access to one's brain in exchange for guaranteed protection from emotional burnout.",
        "human_task_en": "How can I give access to my brain in exchange for guaranteed protection from emotional burnout?",
        "subtitle_en": "Neuroinformatics for enterprise.",
        "why_ts_en": "Voluntary biometric surrender to save one's psyche.",
        "shift_from_en": "Hiding one's emotional state",
        "shift_to_en": "Erasing brain-privacy boundaries in exchange for AI care",
        "hashtags": "#NeuroTransparency, #BrainHealth",
        "compas": "1, 7", "macro": "Emotional AI, Digital Sensorics", "futures": "Organisation, Wellbeing",
        "horizon": "3-7", "influence": 8,
    },
    {
        "title": "HUMANYZE",
        "link": "https://humanyze.com/",
        "existential_essence_en": "Protect the content of communications by letting algorithms analyze metadata only.",
        "human_task_en": "How can I protect the content of communications by letting algorithms analyze metadata only?",
        "subtitle_en": "Systems-health analytics.",
        "why_ts_en": "Collecting big data about the company without violating personal meaning.",
        "shift_from_en": "Analyzing the content of messages",
        "shift_to_en": "Protecting meaning, analyzing only meta-patterns",
        "hashtags": "#SocialPhysics, #SelfDiscovery",
        "compas": "2", "macro": "New Privacy", "futures": "Organisation, Work",
        "horizon": "3-7", "influence": 7,
    },
    {
        "title": "HEIDI HEALTH",
        "link": "https://www.heidihealth.com/",
        "existential_essence_en": "Surround oneself with an invisible care environment that removes routine friction.",
        "human_task_en": "How can I surround myself with an invisible care environment that removes routine friction?",
        "subtitle_en": "Background AI.",
        "why_ts_en": "AI recedes into the background, anticipating needs before they reach consciousness.",
        "shift_from_en": "Active interaction with interfaces",
        "shift_to_en": "Background ultra-personalized care",
        "hashtags": "#AmbientIntel, #AmbientCare",
        "compas": "2, 1", "macro": "Ambient Intelligence, Deep Customisation", "futures": "Organisation, Work",
        "horizon": "3-7", "influence": 7,
    },
    {
        "title": "Royal Society",
        "link": "https://royalsocietypublishing.org/rstb/article/379/1911/20230144/109521/Minds-in-movement-embodied-cognition-in-the-age-of",
        "existential_essence_en": "Return to one's body by recognizing the inseparability of mind and physiology.",
        "human_task_en": "How can I return to my body by recognizing the inseparability of mind and physiology?",
        "subtitle_en": "Embodied intelligence.",
        "why_ts_en": "Lifestyle signal. Return of the value of physically experiencing things.",
        "shift_from_en": "Full virtualization of cognitive labor",
        "shift_to_en": "Symbiosis of physiology and intelligence",
        "hashtags": "#Неотраслевой, #EmbodiedCognition",
        "compas": "7, 1", "macro": "Physicalisation, Emotional AI", "futures": "Organisation, Knowledge",
        "horizon": "3-7", "influence": 9,
    },
    {
        "title": "Revolut AI",
        "link": "https://dev.to/ji_ai/revolut-trained-an-ai-on-40-billion-banking-events-the-results-are-wild-4d1e",
        "existential_essence_en": "Reduce anxiety by offloading responsibility for one's fate onto a general predictive algorithm.",
        "human_task_en": "How can I reduce anxiety by offloading responsibility for my fate onto a general predictive algorithm?",
        "subtitle_en": "Event prediction.",
        "why_ts_en": "Algorithms predict events, lifting the burden of uncertainty.",
        "shift_from_en": "Self-conducted risk analysis",
        "shift_to_en": "Immersion in an invisible environment of predictive analytics",
        "hashtags": "#AlgorithmicDestiny, #DataDeterminism",
        "compas": "2", "macro": "Ambient Intelligence", "futures": "Organisation, Finance & Banking",
        "horizon": "3-7", "influence": 9,
    },
]


def main() -> int:
    ACTIVE_DIR.mkdir(parents=True, exist_ok=True)
    slugs_seen: set[str] = set()
    written = 0
    for s in SIGNALS:
        slug = slugify(s["title"])
        if slug in slugs_seen:
            print(f"DUPLICATE SLUG: {slug} — skipping {s['title']!r}")
            continue
        slugs_seen.add(slug)
        path = ACTIVE_DIR / f"{slug}.md"
        try:
            content = render_signal(s)
        except Exception as e:
            print(f"FAIL  {s['title']!r}: {e}")
            return 1
        path.write_text(content, encoding="utf-8")
        written += 1
        print(f"wrote {slug}.md")
    print(f"\n{written} signals written to {ACTIVE_DIR}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
