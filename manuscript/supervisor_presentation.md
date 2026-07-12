# 📊 Slide Deck: Systematic Literature Review on GNSS-Denied Localization
**Target Audience:** Research Supervisor & Thesis Committee  
**Version:** 1.0 (Journal-Ready)  
**Format:** Markdown-to-PPT Slide Layout  

---

## Slide 1: Title Slide
### **Ten Years of GNSS-Denied Localization: A Systematic Literature Review (2015–2026)**
* **Presenter:** [Your Name / Placeholder]
* **Supervisor:** [Supervisor Name / Placeholder]
* **Date:** July 12, 2026
* **Focus:** Taxonomic classification, sensor-fusion co-occurrence, and empirical accuracy analysis.

> **Speaker Notes:**
> * Begin by introducing the scope of the presentation. Over the past decade, autonomous navigation in GNSS-denied environments has transitioned from a niche robotics challenge to a core requirement for commercial and military UAVs/UGVs.
> * Mention that this slide deck summarizes the methodology and findings of an SLR processing 995 peer-reviewed publications.

---

## Slide 2: Research Motivation & Scope
### **Why GNSS-Denied Localization?**
* **The GNSS Deficit:** Multi-path reflections in urban canyons, signal blockage indoors/underground, and vulnerability to jamming/spoofing.
* **The Solution:** Self-contained, ego-motion sensors (proprioceptive and exteroceptive) that estimate state without external infrastructure.
* **The Literature Challenge:** Rapid expansion of papers from 2015 to 2026, creating a need for a systematic, quantitative taxonomy of sensor–algorithm combinations.

> **Speaker Notes:**
> * Explain the physical limitations of GNSS. 
> * Point out that while many sensor and algorithm combinations exist, there has been no comprehensive study mapping their usage frequency and empirical accuracy distributions. This SLR addresses that exact gap.

---

## Slide 3: Systematic Review Methodology (PRISMA)
### **Paper Identification and Selection Flow**
* **Database Source:** IEEE Xplore
* **Initial Search Results:** 1,000 papers (2015–2026)
* **Screening Criteria:** Concatenated lower-case text corpus (`Title + Abstract + Keywords`) checked for 22 key localization/navigation terms.
* **Exclusion Tally:** 5 papers excluded (focused purely on grid power state estimation or communication protocols without localization).
* **Final Eligible Corpus:** **995 papers** (399 Journal articles, 596 Conference papers).
* **Quantitative Accuracy Synthesis:** 44 papers extracted with explicit numerical trajectory errors (ATE/RMSE).

> **Speaker Notes:**
> * Briefly outline the search query. Highlight that by creating a unified text corpus and programmatically filtering, we kept the review 100% reproducible and PRISMA-compliant.
> * Note the 5 excluded papers to demonstrate the rigour of our inclusion/exclusion filter.

---

## Slide 4: Publication Trends Over Time
### **The Rise of GNSS-Denied Navigation (2015–2026)**
* **Annual Growth:** Steady upward trajectory, growing from **24 papers in 2015** to **225 papers in 2025**.
* **Venues:** Strong concentration in top-tier IEEE journals:
  1. *IEEE Transactions on Instrumentation and Measurement* (56 papers)
  2. *IEEE Robotics and Automation Letters* (43 papers)
  3. *IEEE Sensors Journal* (41 papers)
  4. *IEEE Access* (41 papers)
* **Citation Metric:** Cumulative 11,574 citations across the corpus, with a mean citation count of 11.6 per paper.

> **Speaker Notes:**
> * Point out that the volume of publications has nearly decupled over the decade, peaking in 2025. This underscores the maturity and high interest in the field.
> * Point out that the venue ranking shows that the community values highly rigorous, peer-reviewed engineering transactions.

---

## Slide 5: Sensor Modality Taxonomy (RQ1)
### **Which Sensors Dominate GNSS-Denied Navigation?**
* **Visual Sensors (40.4%, 402 papers):** Cameras are the most dominant modality, with monocular (9.1%), RGB-D (3.2%), and stereo (2.3%) leading.
* **Inertial Sensors (33.5%, 333 papers):** IMUs provide high-frequency proprioceptive updates to bound short-term angular and linear velocities.
* **Active Ranging:** Radar (19.5%, 194 papers) and LiDAR (18.8%, 187 papers) occupy a major share of active exteroceptive sensing.
* **Niche Modalities:** WiFi (7.2%), UWB (6.8%), BLE (2.7%), and Event-based cameras (0.6%).

> **Speaker Notes:**
> * Highlight the dominance of cameras and IMUs. This is due to their low weight, low cost, and passive nature, making them highly suitable for small micro aerial vehicles (MAVs).
> * Mention that active sensors like LiDAR and Radar are gaining traction as weight and power consumption decrease.

---

## Slide 6: Estimation Algorithms & Evolution (RQ2)
### **The Shift from Filtering to Batch Optimization & Deep Learning**
* **VIO Dominance:** Visual-Inertial Odometry (VIO) is the most widely adopted estimation framework (14.0%, 139 papers).
* **Visual Odometry (VO):** Represents 12.9% (128 papers) of the literature.
* **Traditional Filtering:** Extended Kalman Filters (EKF) represent 12.0% (119 papers), serving as the baseline fusion engine.
* **Deep Learning (12.0%, 119 papers):** Massive post-2020 growth. Used for end-to-end ego-motion estimation and reinforcement learning-based sensor selection.

> **Speaker Notes:**
> * Talk about the shift in paradigms. Earlier work (2015–2018) relied heavily on EKF.
> * Modern state-of-the-art frameworks use batch optimization (Factor Graphs/GTSAM) and VIO because they handle non-linearities and sensor latencies much more gracefully.
> * Note the rise of Deep Learning, but mention that hybrid systems (deep learning for feature extraction, EKF for state estimation) are preferred for safety-critical flights.

---

## Slide 7: Sensor–Algorithm Co-occurrence Heatmap
### **Mapping the Most Frequent Integration Paradigms**
* **Top Co-occurring Pairs:**
  1. `Camera + Visual-Inertial Odometry` (138 papers)
  2. `IMU + Visual-Inertial Odometry` (137 papers)
  3. `Camera + Visual Odometry` (128 papers)
  4. `IMU + EKF` (62 papers)
  5. `Camera + Deep Learning` (61 papers)
* **Heatmap Insights:** Traditional filtering (EKF) is primarily paired with IMUs and GNSS transition logic, whereas modern visual sensors are tightly coupled with optimization-based VIO and learning frameworks.

> **Speaker Notes:**
> * Use this slide to show how the sensors and algorithms are actually paired in the literature.
> * The Camera+VIO and IMU+VIO pairings are nearly identical in count, indicating the universal adoption of tightly-coupled visual-inertial setups.

---

## Slide 8: Quantitative Accuracy Benchmarking (RQ3)
### **Empirical Trajectory Error Distributions**
* ** LiDaR (Median = `0.127 m`):** Direct range measurements yield the lowest localization drift (highest accuracy).
* **Radar (Median = `0.171 m`):** Excellent performance in degrade environments (dust, fog, smoke).
* **Cameras (Median = `0.315 m`):** Outstanding visual tracking, especially Monocular VIO.
* **UWB (Median = `0.320 m`):** Active local anchors provide high room-level precision.
* **WiFi/BLE (Median = `1.260 m`):** Fingerprinting and RSSI methods are limited to coarse tracking.

> **Speaker Notes:**
> * This is the meta-analysis section. Point out that LiDAR achieves the lowest error (median 12.7 cm) but comes at the cost of high payload weight and power consumption.
> * UWB is excellent for structured indoor environments but requires pre-deployed anchor beacons.

---

## Slide 9: UAV-Specific Analysis: The Payload & Power Trade-off
### **robotic UAV Constraint Mapping**
UAVs present unique constraints that limit sensor selection:
* **Weight (Payload Limit):** Micro-drones cannot carry heavy 3D mechanical LiDARs (~500g–1kg) or large automotive Radar units.
* **Power consumption:** Computationally heavy algorithms (like dense volumetric SLAM or large deep neural networks) drain battery life rapidly.
* **Environmental Dynamics:** Outdoor UAVs face wind gusts (requiring high-frequency IMU tracking) and rapid lighting changes (causing camera failures).

> **Speaker Notes:**
> * Discuss the unique challenges of UAVs compared to ground vehicles. UGVs can carry heavy batteries and sensors, but UAVs are extremely sensitive to weight and power.
> * This leads us to our proposed "Best Method" recommendation on the next slide.

---

## Slide 10: Proposed "Best Methods" for UAV Navigation
### **Optimal Sensor–Algorithm Combinations for UAVs**

#### **Method A: Tightly-Coupled Visual-Inertial Odometry (VIO) [Best General / Cost-Effective]**
* **Sensors:** Monocular/Stereo Camera + MEMS IMU + Barometer.
* **Algorithm:** MSCKF (Multi-State Constraint Kalman Filter) or Factor Graph (GTSAM/VINS-Mono).
* **Why it's best:** Minimal payload weight (<50g), low power consumption, and bounds tracking drift to **under 0.5 metres** (median error 0.31m).

#### **Method B: Solid-State LiDAR-Inertial Odometry (LIO) [Best High-Accuracy]**
* **Sensors:** Lightweight Solid-State LiDAR (e.g. Livox) + MEMS IMU.
* **Algorithm:** FAST-LIO2 / LIO-SAM (Tightly-coupled Kalman filtering or factor graphs).
* **Why it's best:** Solid-state LiDARs are light (~200g) and draw low power while achieving **sub-decimetre accuracy (median error 0.12m)**.

> **Speaker Notes:**
> * Present these two proposed methods to your supervisor. 
> * Highlight that for standard lightweight drones, Method A (VIO) represents the most cost-effective and common solution. For high-precision mapping/inspection drones, Method B (LIO) is the state-of-the-art solution due to solid-state LiDAR advancements.

---

## Slide 11: Scope of Future Work & Open Challenges
### **Key Areas of Research Focus**
1. **Sim-to-Real Transfer:** Bridging the gap where deep learning estimators fail when transitioned from simulated environments to real-world flight dynamics.
2. **Degenerate Environments:** Resolving drift in textureless areas (e.g., blank corridors, open agricultural fields) by incorporating active beacons (UWB) or Radar.
3. **Neuromorphic & Thermal Sensing:** Fusing event-based and thermal cameras to maintain navigation during high-speed maneuvers or complete darkness.
4. **Collaborative / Swarm Relative Localization:** Inter-UAV ranging (UWB/Vision) to coordinate swarms without global GPS coordinates.

> **Speaker Notes:**
> * Emphasize that these four challenges represent the leading edge of GNSS-denied localization research.
> * Suggest that your research could focus on one of these areas (e.g., addressing degenerate corridors via hybrid VIO-UWB fusion).

---

## Slide 12: Conclusions
### **Summary of Contributions**
* **Methodology:** Conducted a rigorous, PRISMA-compliant systematic review of **995 papers**.
* **Taxonomy:** Mapped the evolution of 18 sensors and 20 algorithms, finding a strong shift towards tightly-coupled VIO.
* **Accuracy:** Quantified the trajectory errors across sensing modalities, benchmarking LiDAR (0.12m) and Cameras (0.31m) as optimal options.
* **Proposed Recommendation:** Proposed a clear dual-track design path for UAVs: **Visual-Inertial Odometry** for lightweight cost-efficiency, and **Solid-State LiDAR-Inertial Fusion** for high-precision deployment.

> **Speaker Notes:**
> * Wrap up by reiterating the value of this SLR in establishing the mathematical and empirical baselines for your future research.
> * Open the floor for questions and feedback from your supervisor.
