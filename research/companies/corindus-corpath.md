# Corindus Vascular Robotics – CorPath System

## Summary
CorPath is a robotic-assisted catheter system for **interventional cardiology procedures** (PCI — percutaneous coronary intervention), not cardiac surgery. It is a fundamentally different technology from surgical robots like da Vinci, competing in the endovascular/minimally invasive interventional space rather than open or minimally invasive surgical bypass. Corindus was acquired by Siemens Healthineers in 2019 for $1.1B; as of 2023, Siemens has **discontinued the cardiology (PCI) line of the business** and now develops CorPath exclusively for neurovascular procedures. This is an important status change from the platform's original PCI-focused positioning.

## What CorPath Is
- **Technology**: Robotic system for remote control of guide catheters, guidewires, and interventional devices during cardiac catheterization
- **Indication (as originally cleared)**: Percutaneous coronary intervention (PCI), coronary angioplasty, stent placement, peripheral vascular intervention (PVI), and neurovascular intervention
- **Delivery**: Catheter-based (no incisions beyond femoral/radial access); operator controls from a radiation-shielded cockpit/control console rather than standing tableside
- **Key benefits marketed**: Eliminates hand tremor, reduces operator radiation exposure by roughly 90%+, enables sub-millimeter, 1mm-incremented catheter/guidewire advancement for more precise stent and balloon placement

## Key Distinction: PCI vs. CABG Surgery
- **CorPath (interventional)**: Minimally invasive catheter-based technique; treats lesions without opening the chest; done under conscious sedation
- **da Vinci-assisted surgical CABG**: Cardiac surgery performed through small incisions; grafts bypass occluded vessels; done under general anesthesia
- **Not competitors**: These address different patient populations and clinical pathways. A hospital may offer both; many patients are triaged to one or the other based on anatomy and comorbidities, not by direct substitution.

## Technology in Detail

### Mechanical architecture
The system has three main components: a **robotic drive (bedside unit)** mounted on an articulating arm attached to the procedure table rail, a **single-use, disposable cassette** that loads onto the drive, and an **operator control console/cockpit** (typically in a separate radiation-shielded area of the cath lab). The drive's motors actuate the cassette, which translates joystick/console inputs into linear and rotational movement of a standard 0.014" guidewire and a proprietary guide catheter, plus linear advancement of balloon and stent catheters. A Y-connector holder in the cassette grips the guide catheter hub; a drive gear enables robotic rotation of the guide catheter itself. An "Extended Reach Arm," engineered against a range of patient body sizes, gives the bedside unit the reach and articulation needed to access the patient from the table rail. (Source: Corindus "How It Works" documentation, patent filings, FARM product-development case study.)

### Precision claims
CorPath's headline differentiator is **sub-millimeter measurement with 1mm incremental advancement** of guidewires, balloons, and stents from the console — marketed as reducing measurement error, minimizing the need for extra stents, and lowering the incidence of "longitudinal geographic miss" (stent malposition relative to the lesion). The GRX generation added **Active Guide Management**, giving the operator robotic control of the guide catheter itself (not just the guidewire/device), also in 1mm increments.

### Radiation exposure reduction — the data
This is the platform's most consistently cited clinical benefit, because interventional cardiologists accumulate career-long radiation exposure standing tableside:
- **PRECISE registration trial** (CorPath 200): operators working from the shielded cockpit saw a **median 92.5% reduction** in radiation exposure compared to published tableside benchmarks.
- **RAPID-II study** (robotic peripheral intervention with drug-coated balloons): mean operator radiation dose reduced by **96.9% ± 5.0%** versus the tableside monitor position.
- Across PRECISE, PRECISION, CORA-PCI and related studies, the consistent finding is **~90–97% reduction in operator radiation exposure**, with **no increase in patient radiation dose or procedure/fluoroscopy time**.

### Evolution: CorPath 200 → CorPath GRX → neurovascular-only
- **CorPath 200** (FDA-cleared 2012): first-generation system; robotic control of guidewire and a single rapid-exchange (RX) device; PCI only.
- **CorPath GRX** (FDA 510(k) clearance October 2016; commercial shipments began late January 2017): second generation. Added **Active Guide Management** (robotic guide-catheter control) and a redesigned, more ergonomic cockpit. Cleared for peripheral vascular intervention (PVI) in February 2018.
- **"Rotate-on-Retract"** (FDA clearance March 2018): first automated robotic movement in Corindus's *technIQ* automation series — automatically rotates the guidewire as it's retracted, aimed at reducing manual workload and procedure steps.
- **Neurovascular Intervention (NVI) indication**: Corindus submitted for FDA premarket clearance in February 2019; the system earned **CE Mark approval for neurovascular use** and was cleared in Europe, Australia, and New Zealand, but the U.S. NVI submission's outcome coincided with Siemens's broader 2023 restructuring (see below). The CorPath GRX Neuro Study (NCT04236856), a prospective single-arm international multicenter trial across 117 patients at 10 sites in 6 countries (2020–2022), was the first trial of robotic-assisted neurovascular aneurysm embolization and reported the platform as safe and effective for that use.

### Telerobotics and remote PCI — a genuine technical milestone
Corindus achieved the **world's first-in-human telerobotic (remote) PCI**, performed December 4–5, 2018, in India. Dr. Tejas M. Patel remotely treated five patients at Apex Heart Institute in Ahmedabad, Gujarat, operating the CorPath GRX system's joysticks and video monitor from roughly **20 miles away**, connected via a hardwired internet line. This "ReMOTE" study's results were published in September 2019 in *EClinicalMedicine* (a Lancet journal). It demonstrated that catheter-level robotic PCI could, in principle, be performed with the operator physically remote from the patient — a notable proof of concept for extending interventional cardiology expertise to underserved or rural areas via low-latency wired connections, though it has not become a routine clinical care model.

## Use-Cases and Deployments

### Clinical trial evidence (expanded)
- **PRECISE** (registration trial, CorPath 200): established safety/feasibility and the ~92.5% radiation reduction figure that underpins the platform's core marketing claim.
- **PRECISION and PRECISION GRX** (final pooled results published May 2025, *JSCAI*): multicenter, prospective, single-arm registries spanning **more than 1,700 procedures** total — PRECISION enrolled 2013–2017 (CorPath 200), PRECISION GRX enrolled 2017–2020 (CorPath GRX). Clinical success was defined as <30% residual stenosis and final TIMI-3 flow post-PCI without in-hospital major adverse cardiac events (MACE). The pooled analysis is the largest published real-world dataset comparing first- and second-generation robotic PCI platforms.
- **CORA-PCI** (Complex Robotically-Assisted PCI, published *JACC: Cardiovascular Interventions*, 2017): tested the GRX system specifically on **complex (B2/C-type) coronary lesions** — 78.3% of the 157 treated lesions were B2/C. Results: **99.1% angiographic success** and **91% technical success** (i.e., completing the case with the robot without manual conversion), with the **primary endpoint achieved in 100% of patients** and no procedural complications. The two leading reasons for manual conversion were inadequate guide-catheter backup support and the inability to advance two devices simultaneously (e.g., for kissing-balloon bifurcation technique) — a real, documented limitation of the robotic workflow.
- **SAFE-T study**: examined CorPath GRX in chronic total occlusion (CTO) PCI, focused on confirming cath-lab staff radiation exposure is not worse than manual CTO PCI.
- **CorPath GRX STEMI Study** (NCT04459299): evaluated robotic PCI feasibility in ST-elevation MI (time-critical, emergent PCI), a more demanding use case than elective PCI.
- Recent (2025) real-world/single-center studies (e.g., "Robotic PCI in Real-World Practice," *JSCAI* 2025) continue to characterize learning curves, procedural complexity, and outcomes as adoption matured outside initial trial settings.

### FDA clearance timeline
| Date | Clearance |
|---|---|
| 2012 | CorPath 200 — first FDA 510(k) clearance, PCI |
| Oct 2016 | CorPath GRX — 510(k) clearance (2nd generation) |
| Jan 2017 | CorPath GRX commercial shipments begin |
| Feb 2018 | CorPath GRX — 510(k) clearance for peripheral vascular intervention (PVI) |
| Mar 2018 | "Rotate-on-Retract" — first automated robotic movement clearance |
| Feb 2019 | Neurovascular intervention (NVI) 510(k) submitted to FDA |

### International approvals
CorPath GRX holds **CE Mark approval** and is cleared for neurovascular intervention in Europe, Australia, and New Zealand — ahead of equivalent U.S. clearance. At the time Siemens announced the CorPath GRX Neuro Study results, the company described GRX as poised to become "the world's first and only robotic platform indicated for PCI, PVI, and neurovascular intervention" — a goal that has since been narrowed by Siemens's 2023 strategic pivot (below).

### Installed base and notable deployments
Precise, current, company-disclosed installed-base figures were not found in public reporting (Siemens does not break out unit counts for this line). Documented deployments include multiple U.S. academic/tertiary centers that ran the PRECISE/PRECISION/CORA-PCI trials, plus international sites such as **Can Tho S.I.S General Hospital (Vietnam)**, which implemented CorPath in 2023, and **Apex Heart Institute (Ahmedabad, India)**, site of the 2018 first-in-human telerobotic PCI. Adoption was consistently described industry-wide as slower than initially projected — a fact Siemens itself later cited as the reason for exiting the cardiology segment.

## Investors, IPO, and Financial History

### Pre-acquisition: public company (NYSE American: CVRS)
Corindus Vascular Robotics was founded in 2002 (Waltham, MA) and went public via IPO in **May 2015**, raising **$42 million** by offering 11 million shares at $3.80/share. Before the IPO, the company had raised roughly **$26.6 million** through a September 2014 securities purchase agreement.

**Post-IPO shareholder base** included:
- HealthCor Partners Management (~38%)
- Koninklijke Philips (~18%)
- Robert Smith (~9%)
- 20/20 Capital (~6%)
- CEO David Handler (~3%)

([Corindus Vascular Robotics Form S-3 — SEC EDGAR](https://www.sec.gov/Archives/edgar/data/1528557/000138713117002118/cvrs-s3_041417.htm))

A **2017 follow-on financing round** brought in new strategic and institutional investors: **Boston Scientific Corporation**, BioStar Ventures, Consonance Capital, and Hudson Executive Capital. Over its life as an independent company, Corindus raised a cumulative **$202 million**, with investors also including 20/20 HealthCare Partners, BioStar Capital, CardioTek, and Concord Resources. Boston Scientific's participation is notable — it signaled interest from an established interventional-device player well before Siemens's acquisition.

### The Siemens Healthineers acquisition (2019)
- **Announced**: August 8, 2019.
- **Structure**: All-cash merger; Siemens Medical Solutions (a Siemens Healthineers AG subsidiary) acquired all outstanding Corindus common stock for **$4.28/share**, an aggregate deal value of **approximately $1.1 billion**.
- **Premium**: $4.28/share represented a substantial premium to Corindus's $2.42 closing price the day before announcement (roughly a 77% premium), and the stock had traded well below that level for much of its history as a small-cap medtech name — the deal was a major liquidity event for its investor base, including Boston Scientific and HealthCor.
- **Closing conditions**: Corindus board approval, stockholder approval, Hart-Scott-Rodino antitrust clearance, other customary conditions.
- **Closed**: effective October 29, 2019 (end of Q4 2019 as guided).

### Strategic rationale for Siemens Healthineers
Siemens Healthineers positioned the deal as extending its **Advanced Therapies** business — the division covering cardiovascular and neuro-interventional image-guided therapy systems (angiography suites, imaging-guided procedure rooms). The stated logic: Siemens already supplied the imaging backbone (fluoroscopy/angiography systems) in the cath lab; Corindus's robotics added a **precision-control layer on top of that imaging**, positioning Siemens to sell a more complete "image-guided, robotically-precise" procedure room rather than imaging hardware alone. The pitch to investors emphasized reduced procedure variability, improved standardization, and — longer-term — the ability to decouple physician expertise from physical location via telerobotics (the India remote-PCI work was cited as proof of concept for this vision).

### Post-acquisition integration and the 2023 reversal
- Corindus was **rebranded as Siemens Healthineers Endovascular Robotics**, run as a dedicated business unit within Advanced Therapies.
- Siemens continued R&D investment, funding further FDA clearances (PVI in 2018, automation features) and the international neurovascular launch.
- **However, in 2023 Siemens Healthineers announced it was discontinuing the CorPath cardiology (PCI) line of business.** CFO Jochen Schmitz stated the "use of Corindus robots for cardiology operations did not fulfill our expectations" — i.e., hospital adoption for PCI never reached the volume that justified the investment. The wind-down triggered **€329 million (~$362 million) in charges**, the largest component being a **€244 million impairment of intangible assets** tied to the cardiovascular application of the platform. This charge was large enough to be cited as a material driver of a reported **81% drop in Siemens Healthineers' quarterly profit** in the period it was recognized.
- **Going forward, Siemens has narrowed CorPath development exclusively to neurovascular intervention** (aneurysm embolization, stroke thrombectomy-adjacent procedures), where Schmitz described a path to market as still "several years" out. The PCI/PVI cardiology product line is no longer being actively sold or developed.

## Sales, Commercial Positioning, and Pricing
- **List price** (as reported around the CorPath GRX launch window, ACC/2017 reporting): roughly **$650,000** for the capital equipment, plus a **$650–750 single-use disposable cassette** per procedure — a recurring consumable revenue model layered on top of the capital sale, typical of surgical/interventional robotics.
- Siemens does not publicly break out CorPath/Endovascular Robotics revenue as a separate line in its financial disclosures; the clearest financial signal is the 2023 impairment charge, which functions as an implicit admission that commercial adoption underperformed the original underwriting case.
- **Adoption trajectory**: initial post-acquisition messaging (2020–2022) emphasized expanding indications (PVI, then pursuing neurovascular) as the growth vector; the 2023 pivot effectively abandoned the original growth thesis (broad PCI/PVI hospital adoption) in favor of a narrower neurovascular-only bet.

## Relevance to Hospital Robotic CABG Programs
**Not a direct competitor, and now an even more distant one.** A hospital with a robotic CABG program (da Vinci) would, at most, consider CorPath a **complementary** technology for interventional cardiology cases — not a replacement, and as of 2023 not even an actively-marketed cardiology product from Siemens.
- CABG programs treat complex multivessel disease and surgical candidates.
- PCI programs (historically CorPath-enabled) treat suitable lesions in interventional labs, but Siemens has stopped selling CorPath for that indication.
- Many centers offer both surgical and interventional pathways for different patient populations; the CorPath story is now primarily useful as a cautionary case study in medtech robotics adoption — strong trial data and a clear radiation-safety benefit did not translate into the commercial volume Siemens underwrote at acquisition.

---

## Sources
- [Siemens Healthineers acquisition announcement (2019)](https://www.siemens-healthineers.com/press/releases/pr-20190808032shs.html)
- [Siemens Healthineers completes Corindus acquisition](https://www.siemens-healthineers.com/press/releases/pr-closing-corindus.html)
- [CNBC: Siemens Healthineers buys Corindus for $1.1 billion](https://www.cnbc.com/2019/08/08/siemens-healthineers-buys-corindus-for-1point1-billion.html)
- [MedTech Dive: Siemens acquires Corindus for $1.1B](https://www.medtechdive.com/news/siemens-acquires-corindus-vascular-robotics-1-billion/560515/)
- [Corindus 8-K, SEC EDGAR (2019 merger)](https://www.sec.gov/Archives/edgar/data/1528557/000138713119005895/ex99-1.htm)
- [Robotics Business Review: Corindus IPO nets $42M](https://www.roboticsbusinessreview.com/health-medical/corindus_vascular_robotics_ipo_nets_42m/)
- [Renaissance Capital: CVRS IPO profile](https://www.renaissancecapital.com/Profile/CVRS/Corindus-Vascular/IPO)
- [Corindus rebrands to Siemens Healthineers Endovascular Robotics](https://www.therobotreport.com/corindus-rebrands-to-siemens-healthineers-endovascular-robotics/)
- [Siemens discontinues cardiology robotics — DOTmed](https://www.dotmed.com/news/story/60482)
- [MassDevice: Siemens Healthineers cutting back on surgical robotics program](https://www.massdevice.com/siemens-healthineers-cuts-corindus-surgical-robotics/)
- [MD+DI: Siemens calls it quits in cardiovascular surgical robotics](https://www.mddionline.com/robotics/siemens-calls-it-quits-in-robotic-heart-surgery)
- [FierceBiotech: Siemens Healthineers profits plummet 81% amid exit from cardiology robotics](https://www.fiercebiotech.com/medtech/siemens-healthineers-profits-plummet-81-amid-exit-cardiology-robotics-slowed-covid-test)
- [Corindus "How It Works" — CorPath GRX](https://www.corindus.com/corpath-grx/how-it-works)
- [ACC: "The Robot Will See You Now" — pricing and radiation-exposure context](https://www.acc.org/latest-in-cardiology/articles/2017/08/01/18/42/the-robot-will-see-you-now-robotics-in-the-cath-lab-have-staff-breathing-a-sigh-of-relief)
- [Business Wire: Corindus first-in-human telerobotic coronary intervention, India](https://www.businesswire.com/news/home/20181206005067/en/Corindus%E2%80%99-Technology-Successfully-Used-in-World%E2%80%99s-First-in-Human-Telerobotic-Coronary-Intervention)
- [DAIC: First-in-human telerobotic coronary intervention published in EClinicalMedicine](https://www.dicardiology.com/content/first-human-telerobotic-coronary-intervention-procedures-published-eclinicalmedicine)
- [CORA-PCI study — ScienceDirect/JACC: Cardiovascular Interventions](https://www.sciencedirect.com/science/article/pii/S1936879817307719)
- [PRECISION and PRECISION GRX final results — JSCAI (2025)](https://www.jscai.org/article/S2772-9303(25)01097-X/fulltext)
- [Robotic-Assisted PCI: recent advances (PMC review, 2026)](https://pmc.ncbi.nlm.nih.gov/articles/PMC13171391/)
- [Scoping review of the CorPath GRX system in neuroendovascular surgery — PMC](https://pmc.ncbi.nlm.nih.gov/articles/PMC11662343/)
- [CorPath GRX Neuro Study — ClinicalTrials.gov (NCT04236856)](https://clinicaltrials.gov/study/NCT04236856)
- [Corindus FDA submission for neurovascular intervention indication](https://www.biospace.com/corindus-announces-fda-submission-for-neurovascular-intervention-indication-for-corpath-grx-vascular-robotic-system)
- [Corindus receives FDA clearance for "Rotate on Retract" automated movement](https://www.mpo-mag.com/breaking-news/corindus-receives-fda-clearance-for-first-automated-robotic-movement-for-corpath-grx-platform/)
- [PCI vs CABG outcomes comparison](https://www.ncbi.nlm.nih.gov/pmc/articles/PMC6756629/)
- [Corindus Vascular Robotics Form S-3 (2017) — SEC EDGAR](https://www.sec.gov/Archives/edgar/data/1528557/000138713117002118/cvrs-s3_041417.htm)
