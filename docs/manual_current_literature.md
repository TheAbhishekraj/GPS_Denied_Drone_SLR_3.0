# Literature Guide: High-Impact Papers in GNSS-Denied Localization

This guide summarizes key publications from our literature review database (2015–2026) that have shaped state-estimation and localization paradigms in GNSS-denied environments.

---

## 1. Landmark Surveys & Reviews

### "A Survey of Enabling Technologies for Network Localization, Tracking, and Navigation"
- **Authors:** F. Author et al.
- **Year:** 2018
- **Citations:** 412
- **Venue:** *IEEE Communications Surveys & Tutorials*
- **Key Focus:** Comprehensive survey detailing radio frequency (RF), ultra-wideband (UWB), WiFi, and cellular-based positioning techniques. Establishes the foundations of device-free localization and anchor-based tracking.

### "A Survey on Odometry for Autonomous Navigation Systems"
- **Authors:** F. Author et al.
- **Year:** 2019
- **Citations:** 187
- **Venue:** *IEEE Access*
- **Key Focus:** Focuses on the mathematical frameworks behind wheel, visual, and LiDAR odometry, comparing their error growth rates and suitability across different robotic platforms.

---

## 2. Visual-Inertial Odometry & SLAM (VIO/VI-SLAM)

### "A Benchmark Comparison of Monocular Visual-Inertial Odometry Algorithms for Flying Robots"
- **Authors:** F. Author et al.
- **Year:** 2018
- **Citations:** 313
- **Venue:** *IEEE International Conference on Robotics and Automation (ICRA)*
- **Key Focus:** Compares key open-source monocular VIO pipelines (MSCKF, OKVIS, ROVIO, VINS-Mono) on flying robots. Provides empirical evidence that tightly-coupled visual-inertial optimization bounds trajectory drift to under 1% of travel distance, making VIO the go-to approach for micro aerial vehicle (MAV) navigation.

### "Deep Auxiliary Learning for Visual Localization and Odometry"
- **Authors:** F. Author et al.
- **Year:** 2018
- **Citations:** 205
- **Venue:** *IEEE International Conference on Robotics and Automation (ICRA)*
- **Key Focus:** One of the earliest highly-cited papers demonstrating deep learning for visual odometry, introducing auxiliary loss functions (depth, optical flow) to train neural networks that perform robust relative pose estimation under dynamic lighting.

---

## 3. LiDAR-Inertial-Visual Fusion

### "FAST-LIVO2: Fast, Direct LiDAR–Inertial–Visual Odometry"
- **Authors:** F. Author et al.
- **Year:** 2025
- **Citations:** 151
- **Venue:** *IEEE Transactions on Robotics*
- **Key Focus:** Proposes a tightly-coupled direct LiDAR-inertial-visual odometry framework. By fusing raw sparse LiDAR points and pixel intensity patches without extracting hand-crafted features, it achieves centimetre-level localization accuracy and high frame rates on computationally constrained drone platforms.

### "R³LIVE++: A Robust, Real-Time, Radiance Reconstruction Package With a Tightly-Coupled LiDAR-Visual-Inertial Odometry"
- **Authors:** F. Author et al.
- **Year:** 2024
- **Citations:** 47
- **Venue:** *IEEE Transactions on Pattern Analysis and Machine Intelligence (TPAMI)*
- **Key Focus:** Merges LiDAR-inertial-visual state estimation with real-time radiance map reconstruction, allowing autonomous drones to navigate complex GNSS-denied environments while generating dense, photo-realistic 3D maps.

---

## 4. Ultra-Wideband (UWB) & Local Beacons

### "Design of an UWB indoor-positioning system for UAV navigation in GNSS-denied environments"
- **Authors:** F. Author et al.
- **Year:** 2015
- **Citations:** 156
- **Venue:** *International Conference on Indoor Positioning and Indoor Navigation (IPIN)*
- **Key Focus:** A pioneering paper on using UWB time-of-flight (ToF) range measurements for closed-loop flight control of quadrotors indoors. Establishes the decimetre-level accuracy limits of active beacon configurations.
