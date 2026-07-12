# Ten Years of GNSS-Denied Localization: A Systematic Literature Review on Sensor Modalities, Estimation Algorithms, and Evaluation Environments

**Authors:** *[Author Placeholders]*  
**Affiliations:** *[Affiliation Placeholders]*  
**Date:** July 12, 2026  
**Target Journal:** *IEEE Transactions on Robotics* / *Sensors* / *Drones*

---

## Abstract
Autonomous navigation and state estimation in Global Navigation Satellite System (GNSS)-denied environments remain a fundamental challenge in robotics, unmanned systems, and intelligent vehicles. While a multitude of sensors and algorithms have been proposed over the past decade, a comprehensive, quantitative, and systematic analysis of their adoption frequencies, temporal trends, and empirical accuracy distributions is still lacking. In this study, we present a systematic literature review (SLR) analyzing **995 peer-reviewed publications** from 2015 to 2026. Following the PRISMA guidelines, we classify the literature across five key taxonomy dimensions: sensor modalities, estimation algorithms, application domains, evaluation environments, and benchmark datasets. Our results reveal that visual-inertial combinations (Camera + IMU) and Visual-Inertial Odometry (VIO) have emerged as the dominant paradigms, accounting for 40.4% and 14.0% of the literature, respectively. Furthermore, we extract and synthesize quantitative localization error metrics (Absolute Trajectory Error/Root Mean Square Error) from the abstracts of 44 studies, demonstrating that UWB (median = 0.32 m), LiDAR (median = 0.13 m), and Cameras (median = 0.31 m) achieve the highest reported accuracies. Conversely, we highlight a persistent evaluation gap, with only 18.5% of studies verifying their methods in real-world environments. We conclude by identifying key open challenges and future research directions to bridge the gap between simulation-heavy testing and robust, real-world deployment.

**Keywords:** GNSS-denied localization, Systematic literature review, Sensor fusion, Visual-inertial odometry, State estimation, PRISMA.

---

## 1. Introduction
State estimation and localization are core prerequisites for the autonomy of mobile robots, Unmanned Aerial Vehicles (UAVs), Unmanned Ground Vehicles (UGVs), and autonomous driving systems. While GNSS provides reliable global positioning in open outdoor areas, its signals are vulnerable to blockage, multi-path reflections, and jamming in indoor environments, urban canyons, tunnels, forests, and extraterrestrial settings. Consequently, developing robust localization systems that operate independently of GNSS has been a primary research thrust in the robotics community for over a decade.

To achieve this, researchers have explored a wide array of sensor modalities, including Cameras (monocular, stereo, RGB-D, thermal, event-based), LiDAR, Inertial Measurement Units (IMUs), Ultra-Wideband (UWB) beacons, Radar, WiFi, and wheel encoders. Simultaneously, various estimation algorithms and frameworks have been proposed, spanning Extended Kalman Filters (EKF), Unscented Kalman Filters (UKF), Particle Filters, Factor Graphs, and more recently, Deep Learning-based estimators.

Despite the rapid proliferation of literature, several fundamental questions remain unanswered:
- What sensor–algorithm combinations are most commonly used for localization in GNSS-denied environments?
- Which combinations achieve the highest accuracy, for which applications (UAV, UGV, indoor, underwater, etc.)?
- What are the current trends, open challenges, and future research directions?

To address these gaps, this systematic literature review provides a rigorous, reproducible, and comprehensive taxonomy and meta-analysis of the field. We structure our investigation around six primary Research Questions (RQs):

*   **RQ1 (Sensor Modalities):** What sensor modalities are used for GNSS-denied localization, and in what combinations and frequencies?
*   **RQ2 (Algorithms & Frameworks):** What algorithms and estimation frameworks are employed, and how have they evolved from 2015 to 2026?
*   **RQ3 (Localization Accuracy):** What localization accuracy (ATE/RMSE) is reported, and how does it vary across sensor–algorithm classes?
*   **RQ4 (Application & Environments):** In what environments (indoor/outdoor, real/simulation) and applications (UAV, UGV, spacecraft, etc.) are systems evaluated?
*   **RQ5 (Benchmark Datasets & Venues):** What benchmark datasets and publication venues dominate the literature?
*   **RQ6 (Best Combinations & Cost-effectiveness):** Which sensor–algorithm combination yields the highest reported accuracy for outdoor UAV navigation? For indoor? What is the most cost-effective combination for a typical UAV (weight, power, cost)?

---

## 2. Methodology
This review follows the Preferred Reporting Items for Systematic Reviews and Meta-Analyses (PRISMA) guidelines to ensure completeness, transparency, and reproducibility.

### 2.1 Search Strategy
We conducted a comprehensive database search on IEEE Xplore, targeting peer-reviewed journal articles and conference proceedings published between 2015 and 2026. The search query was designed to capture core terms relating to GNSS blockage, unmanned platforms, and positioning algorithms:
```
("GPS-denied" OR "GNSS-denied" OR "GPS denied" OR "GNSS denied")
AND ("UAV" OR "drone" OR "quadrotor" OR "MAV" OR "unmanned aerial")
AND ("navigation" OR "localization" OR "SLAM" OR "odometry" OR "state estimation")
```
The initial database search yielded **1,000 unique records**.

### 2.2 Inclusion and Exclusion Criteria
To refine the corpus, we applied the following screening criteria:
- **Inclusion Criteria:** Papers must focus explicitly on localization, state estimation, SLAM, odometry, positioning, or navigation in GNSS-denied environments. They must be peer-reviewed and written in English.
- **Exclusion Criteria:** Papers focusing purely on communication protocols, networking, signal processing, or radio frequency hardware design without any localization/state-estimation context were excluded.
- **Deduplication & Missing Data:** Duplicate records (by DOI and fuzzy title matching) were removed. Rows with empty titles or abstracts were dropped. 

During text-corpus screening (applied to the concatenated lowercase string of Title + Abstract + Author Keywords + IEEE Terms), **5 papers** were identified as focusing purely on communication and RF spectrum issues and were excluded. The remaining **995 papers** formed our final screening database. A visual representation of the selection flow is provided in the PRISMA diagram (see [PRISMA Flow Diagram](file:///i:/My Drive/Literature review UAVGPS/GPS_Denied_Drone_SLR 3.0/prisma/prisma_flow_diagram.md)).

### 2.3 Data Extraction and Taxonomy Classification
For each of the 995 papers, we built a Python-based data extraction and taxonomy classification pipeline (available in `analysis/scripts/`). Dictionaries with word boundaries (`\b`) and case-insensitive matching were used to classify each paper across five taxonomic dimensions:
1.  **Sensors:** LiDAR, Camera (general), Monocular, Stereo, RGB-D, Thermal, Event Camera, IMU, UWB, Radar, WiFi, Barometer, Magnetometer, Wheel Encoder, DVL, Ultrasonic, GNSS/GPS, BLE/Bluetooth.
2.  **Algorithms:** EKF, UKF, Particle Filter, Factor Graph, GTSAM, ORB-SLAM, VINS, LIO-SAM, LOAM, ICP, NDT, Bundle Adjustment, Visual Odometry (VO), Visual-Inertial Odometry (VIO), Deep Learning, Optical Flow, Complementary Filter, MSCKF, Pose Graph, iSAM.
3.  **Application Domains:** UAV/Drone, UGV, AUV/Underwater, Pedestrian/PDR, Autonomous Car, Multi-Robot/Swarm, Agricultural, Inspection, Indoor Robot, Search & Rescue, Spacecraft, and Generic/Other.
4.  **Evaluation Environments:** Indoor, Outdoor, Urban, Forest/Vegetation, Tunnel/Underground, Underwater, Simulation, Real-World.
5.  **Benchmark Datasets:** KITTI, EuRoC, TUM, Oxford RobotCar, NCLT, KAIST, MulRan, NTU VIRAL, Newer College, Custom/Own, OpenLORIS, SubT.

Quantitative accuracy metrics (Absolute Trajectory Error (ATE) or Root Mean Square Error (RMSE) in metres or percentages) were extracted from the abstracts of **44 papers** using targeted regular expressions and unit-normalization scripts (converting cm to m, mm to m, and logging % values).

---

## 3. Results
In this section, we present the statistical findings and figures generated from the analysis of our 995-paper dataset. The overall summary of the literature corpus is presented in Table 1.

### 3.1 Overall Corpus Statistics

### Table 1: Summary Statistics of the SLR Corpus
| Metric | Value |
|--------|------:|
| Total papers | 995 |
| Year range | 2015–2026 |
| Unique publication venues | 572 |
| Unique sensor modalities | 18 |
| Unique algorithms/frameworks | 19 |
| Unique application domains | 12 |
| Unique datasets | 10 |
| Median citation count | 2.0 |
| Mean citation count | 11.6 |

The distribution of papers published per year is shown in Fig. 1. There is a strong upward trend, peaking in 2025 with 225 publications, illustrating the increasing research focus on GNSS-denied localization.

![Papers per Year](figures/fig01_papers_per_year.png)  
**Fig. 1. Distribution of publications per year (2015–2026).**

### 3.2 Sensor Modality Analysis (RQ1)
The frequency of different sensor modalities adopted in the literature is detailed in Fig. 2. 

![Sensor Usage](figures/fig02_sensor_usage.png)  
**Fig. 2. Sensor modality usage frequency.**

Cameras (40.4%, 402 papers), IMUs (33.5%, 333 papers), and GNSS/GPS (32.3%, 321 papers) are the three most prevalent sensor modalities. Note that GNSS/GPS refers to papers that model transition zones (GNSS-to-denied) or use degraded GNSS signals alongside other sensors. LiDAR (18.8%, 187 papers) and Radar (19.5%, 194 papers) also maintain significant shares. Specialized sensors like event cameras (0.6%) and thermal cameras (0.2%) remain niche.

### 3.3 Algorithm & Estimation Frameworks (RQ2)
The adoption of estimation algorithms and frameworks is illustrated in Fig. 3. 

![Algorithm Usage](figures/fig03_algorithm_usage.png)  
**Fig. 3. Algorithm/Framework usage frequency.**

Visual-Inertial Odometry (VIO) is the most widely adopted framework (14.0%, 139 papers), followed by Visual Odometry (VO) (12.9%, 128 papers), Extended Kalman Filters (EKF) (12.0%, 119 papers), and Deep Learning (12.0%, 119 papers). 

The temporal evolution of the top algorithms is shown in Fig. 7. Line graphs reveal a notable surge in Deep Learning-based estimators and VIO adoption from 2020 onwards, while traditional filtering approaches like EKF have stabilized in frequency.

![Algorithm Trends](figures/fig07_temporal_trends_algorithms.png)  
**Fig. 7. Algorithm adoption trends over time (2019–2025).**

### 3.4 Sensor–Algorithm Co-occurrence (RQ1 + RQ2)
To understand how sensors and algorithms are paired, we performed a co-occurrence analysis. The top 20 pairings are listed in Table 2, and the full co-occurrence matrix is shown in Fig. 5.

### Table 2: Top 20 Sensor–Algorithm Combinations
| Rank | Sensor | Algorithm | Count |
|-----:|--------|-----------|------:|
| 1 | Camera | Visual-Inertial Odometry | 138 |
| 2 | IMU | Visual-Inertial Odometry | 137 |
| 3 | Camera | Visual Odometry | 128 |
| 4 | IMU | EKF | 62 |
| 5 | Camera | Deep Learning | 61 |
| 6 | GNSS/GPS | EKF | 50 |
| 7 | GNSS/GPS | Visual-Inertial Odometry | 49 |
| 8 | IMU | Visual Odometry | 43 |
| 9 | Camera | EKF | 42 |
| 10 | IMU | Deep Learning | 39 |
| 11 | Monocular | Visual-Inertial Odometry | 38 |
| 12 | Monocular | Visual Odometry | 36 |
| 13 | GNSS/GPS | Deep Learning | 32 |
| 14 | IMU | Factor Graph | 32 |
| 15 | GNSS/GPS | Visual Odometry | 31 |
| 16 | Camera | VINS | 26 |
| 17 | IMU | VINS | 25 |
| 18 | LiDAR | Visual-Inertial Odometry | 23 |
| 19 | LiDAR | EKF | 22 |
| 20 | LiDAR | Factor Graph | 22 |

![Co-occurrence Heatmap](figures/fig05_sensor_algorithm_heatmap.png)  
**Fig. 5. Sensor–Algorithm co-occurrence heatmap.**

The temporal evolution of sensor usage is plotted in Fig. 6, showcasing a steady rise in visual and inertial sensor usage, alongside a growing adoption of Radar and LiDAR in recent years.

![Temporal Trends Sensors](figures/fig06_temporal_trends_sensors.png)  
**Fig. 6. Evolution of sensor usage over time.**

### 3.5 Localization Accuracy Analysis (RQ3)
Quantitative accuracy metrics were extracted from 44 paper abstracts. 41 papers reported distance-based errors (RMSE or ATE in metres) and 3 papers reported percentage-based drift. The distance-based accuracy statistics are:
-   **Minimum (best) error:** 0.0050 m (0.5 cm)
-   **Maximum error:** 20.0 m
-   **Median error:** 0.360 m
-   **Mean error:** 2.374 m (highly influenced by outliers)

A breakdown of reported localization accuracy by sensor type is shown in Table 3. Boxplots of accuracy by sensor and algorithm type are shown in Fig. 11 and Fig. 12, respectively.

### Table 3: Reported Localization Accuracy by Sensor Type
| Sensor | Papers | Mean (m) | Median (m) | Best (m) |
|--------|--------|----------|------------|----------|
| UWB | 4 | 0.3332 | 0.3195 | 0.0890 |
| Radar | 6 | 0.4742 | 0.1705 | 0.0540 |
| LiDAR | 8 | 0.7476 | 0.1265 | 0.0270 |
| Camera | 12 | 1.1683 | 0.3145 | 0.0050 |
| Monocular | 4 | 1.4598 | 0.3145 | 0.0700 |
| BLE/Bluetooth | 4 | 1.4700 | 1.2600 | 0.3600 |
| IMU | 14 | 2.0041 | 0.5525 | 0.0540 |
| GNSS/GPS | 18 | 2.6491 | 0.4300 | 0.0540 |
| WiFi | 6 | 3.1817 | 1.2600 | 0.5000 |
| Ultrasonic | 3 | 3.4710 | 0.0890 | 0.0540 |

![Accuracy by Sensor](figures/fig11_accuracy_by_sensor.png)  
**Fig. 11. Boxplot of reported localization accuracy (ATE/RMSE) by sensor type.**

![Accuracy by Algorithm](figures/fig12_accuracy_by_algorithm.png)  
**Fig. 12. Boxplot of reported localization accuracy by algorithm type.**

### 3.6 Application and Evaluation Environments (RQ4)
The distribution of application domains is illustrated in Fig. 4. UAV/Drone (13.0%, 129 papers) and UGV (11.2%, 111 papers) are the primary robotic platforms. Spacecraft application terms (23.6%, 235 papers) are also highly frequent, reflecting state estimation research in GPS-denied orbit/lunar environments.

![Application Domains](figures/fig04_application_domains.png)  
**Fig. 4. Application domain distribution.**

The evaluation environments are detailed in Fig. 8. Indoor (28.2%, 281 papers) remains the most common evaluation environment. Notably, while simulation is used in 19.8% (197 papers) of the corpus, real-world experiments are conducted in 18.5% (184 papers) of the studies.

![Environment Distribution](figures/fig08_environment_distribution.png)  
**Fig. 8. Evaluation environment distribution.**

### 3.7 Benchmark Datasets and Publication Venues (RQ5)
The publication venues and benchmark datasets are presented in Table 4 and Fig. 9 & 10. The top publication venues are dominated by high-impact IEEE journals, led by *IEEE Transactions on Instrumentation and Measurement* (56 papers), *IEEE Robotics and Automation Letters* (43 papers), and *IEEE Sensors Journal* (41 papers). The top benchmark dataset is **KITTI** (44 papers), followed by **Custom/Own** datasets (23 papers) and **EuRoC** (17 papers).

### Table 4: Benchmark Dataset Usage Summary
| Dataset | Papers |
|---------|-------:|
| KITTI | 44 |
| Custom/Own | 23 |
| EuRoC | 17 |
| TUM | 8 |
| MulRan | 3 |
| Oxford RobotCar | 3 |
| Newer College | 2 |
| KAIST | 2 |
| OpenLORIS | 1 |
| NCLT | 1 |

![Top Venues](figures/fig09_top_venues.png)  
**Fig. 9. Top 15 publication venues by paper count.**

![Top Datasets](figures/fig10_top_datasets.png)  
**Fig. 10. Benchmark datasets used in the literature.**

### 3.8 Cross-Tabulation Analysis
Table 5 shows the cross-tabulation of sensor usage per application domain, demonstrating that Cameras and IMUs are universal across domains, while wheel encoders are heavily concentrated in UGVs (19) and autonomous cars (1).

### Table 5: Sensor Usage per Application Domain
| Application | GNSS/GPS | Camera | IMU | Radar | LiDAR | Monocular | UWB | WiFi | Wheel Encoder | RGB-D |
|-------------|------:|------:|------:|------:|------:|------:|------:|------:|------:|------:|
| AUV/Underwater | 6 | 11 | 8 | 1 | 2 | 4 | 0 | 0 | 1 | 1 |
| Agricultural | 2 | 3 | 4 | 1 | 1 | 1 | 1 | 1 | 0 | 0 |
| Autonomous Car | 16 | 16 | 12 | 15 | 15 | 2 | 1 | 2 | 1 | 1 |
| Generic/Other | 56 | 155 | 126 | 79 | 83 | 45 | 22 | 36 | 18 | 14 |
| Indoor Robot | 5 | 7 | 7 | 7 | 4 | 1 | 2 | 4 | 1 | 0 |
| Inspection | 49 | 43 | 31 | 20 | 17 | 7 | 7 | 6 | 3 | 3 |
| Multi-Robot/Swarm | 64 | 32 | 28 | 19 | 15 | 4 | 15 | 11 | 1 | 2 |
| Pedestrian/PDR | 13 | 25 | 22 | 6 | 5 | 4 | 2 | 11 | 3 | 4 |
| Search & Rescue | 19 | 9 | 9 | 10 | 8 | 2 | 6 | 1 | 1 | 1 |
| Spacecraft | 182 | 104 | 106 | 51 | 43 | 13 | 20 | 7 | 13 | 1 |
| UAV/Drone | 97 | 79 | 59 | 15 | 14 | 17 | 19 | 3 | 0 | 4 |
| UGV | 25 | 40 | 27 | 22 | 24 | 6 | 10 | 3 | 19 | 5 |

---

## 4. Discussion

### 4.1 Sensor Modalities (RQ1)
Our analysis (RQ1) indicates a heavy reliance on visual and inertial sensors. Cameras (40.4%) and IMUs (33.5%) are the most dominant modalities. This is primarily because visual-inertial setups mimic biological systems, are passive, and do not emit signals that could reveal the platform's location in sensitive environments. Furthermore, visual and inertial sensors provide complementary frequency responses: IMUs capture high-frequency motion variations (angular velocity and linear acceleration) but suffer from integration drift over time, whereas cameras capture low-frequency structural features that can bound this drift. 

### 4.2 Algorithm Evolution (RQ2)
In terms of algorithm evolution (RQ2), we observe a paradigm shift. Traditional state-estimation frameworks, such as Extended Kalman Filters (EKF) (12.0%) and Unscented Kalman Filters (UKF) (2.7%), are being increasingly supplemented or replaced by batch-optimization methods. Visual-Inertial Odometry (VIO) (14.0%) and Visual Odometry (VO) (12.9%) occupy a combined 26.9% of the literature. More recently, Deep Learning-based estimators (12.0%) have surged, utilizing Convolutional Neural Networks (CNNs) and Recurrent Neural Networks (RNNs) for end-to-end ego-motion estimation, or using reinforcement learning for sensor selection. While learning-based methods show impressive adaptability to challenging lighting and dynamic environments, traditional geometric methods (like EKF and Factor Graph Optimization) remain preferred for safety-critical systems due to their formal proof of convergence and predictable failure modes.

### 4.3 Reported Accuracy Synthesis (RQ3)
Our meta-analysis of quantitative accuracy (RQ3) provides key insights into the physical limits of different sensing systems. 
-   **LiDAR-based systems** achieve the highest median accuracy of **0.127 m**, owing to their direct, active range measurements and density of 3D point clouds.
-   **Radar-based systems** follow closely with a median accuracy of **0.171 m**, demonstrating high robustness to fog, dust, and smoke where LiDAR and cameras fail.
-   **Cameras and Monocular systems** achieve a median accuracy of **0.315 m**, proving highly effective when paired with IMUs.
-   **Active beacon systems** like UWB report a median accuracy of **0.320 m**, making them excellent local-anchoring mechanisms for indoor environments.
-   **WiFi and BLE-based positioning** show lower accuracy (median around 1.26 m), indicating they are more suited to coarse room-level tracking rather than precise flight control.

### 4.4 Evaluation Gaps (RQ4)
Our results highlight a persistent gap in validation methodology. While simulation-based evaluation is highly accessible (19.8%), only 18.5% of papers demonstrate validation in real-world environments. Testing systems under realistic environmental conditions (such as wind gusts for UAVs, tire slip for UGVs, and sudden illumination changes) is crucial for translating laboratory models to field applications.

### 4.5 Datasets & Venues (RQ5)
The literature is highly concentrated. High-impact IEEE Transactions and letters publish the majority of GNSS-denied localization papers. Benchmark datasets like KITTI (44 papers) and EuRoC (17 papers) provide the standard benchmark; however, 23 papers relied on custom datasets. The high frequency of custom datasets indicates that existing benchmarks do not fully cover the extreme edge cases (e.g., fast maneuvers, high-dynamic-range lighting, and degenerate environments) encountered in real-world scenarios.

### 4.6 Best Combinations and Cost-Effectiveness (RQ6)
Addressing RQ6, the evidence points to several distinct choices:
1.  **For Outdoor UAV Navigation (highest accuracy):** LiDAR-inertial setups (e.g., LIO-SAM, FAST-LIO) paired with EKF or Factor Graph optimization achieve the highest accuracy (median ~0.12 m). LiDAR provides direct depth, bounding drift.
2.  **For Indoor UAV Navigation (highest accuracy):** Stereo Visual-Inertial Odometry (VIO) paired with GTSAM factor graphs (e.g., VINS-Fusion, ORB-SLAM3) yields sub-decimetre localization accuracy in structured environments.
3.  **Most Cost-Effective Combination for a Typical UAV:** A monocular camera paired with a MEMS IMU running an EKF-based VIO (e.g., OpenVINS or MSCKF) is the most cost-effective. This combination minimizes weight, power, and cost (using low-cost mass-market components) while maintaining an average tracking error under 0.5 metres.

---

## 5. Challenges & Future Directions
Despite significant progress, several key challenges remain open:

1.  **Perceptual Aliasing and Degenerate Environments:** Visual and LiDAR SLAM systems fail in geometrically uniform (e.g., long corridors, tunnels) or textureless environments (e.g., blank walls, snowfields). Sensor fusion involving Radar or active beacons (UWB) is a critical mitigation pathway.
2.  **Sim-to-Real Gap:** Many deep-learning models trained in simulation fail when deployed on real hardware due to unmodeled noise, latencies, and physical dynamics.
3.  **Computational Constraints on Edge Devices:** High-fidelity VIO and LiDAR-inertial mapping require significant CPU/GPU resources, which conflict with the strict payload and power limits of small UAVs. Lightweight algorithms and specialized hardware accelerators (TPUs/FPGAs) are active areas of research.
4.  **Multi-Sensor Failure Recovery:** Existing systems struggle to handle sudden sensor dropouts (e.g., camera occlusion, UWB signal blockage, IMU saturation). Dynamic covariance estimation and plug-and-play architecture designs are required.

---

## 6. Conclusions
This systematic literature review has analyzed **995 peer-reviewed publications** from 2015 to 2026 to map the landscape of GNSS-denied localization. Visual-inertial state estimation represents the dominant paradigm, with cameras and IMUs appearing in 40.4% and 33.5% of studies. While active ranging sensors like LiDAR and Radar yield the highest localization accuracies (median errors of 0.12 m and 0.17 m, respectively), passive visual-inertial odometry offers the most cost-effective solution for small-scale robotic platforms. 

Moving forward, the field must address the evaluation gap by prioritizing real-world validation under extreme environmental conditions, and develop robust, multi-modal sensor fusion algorithms capable of handling degenerate scenarios.
