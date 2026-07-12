# PRISMA 2020 Flow Diagram

This flow diagram illustrates the systematic selection and screening process of literature for the GNSS-Denied Localization Systematic Literature Review, in accordance with the PRISMA (Preferred Reporting Items for Systematic Reviews and Meta-Analyses) guidelines.

```mermaid
flowchart TD
    subgraph Identification
        A["Database Searching (IEEE Xplore)<br>(n = 1000)"] --> C["Records Screened<br>(n = 1000)"]
    end

    subgraph Screening
        C -->|Records Excluded by Screening Criteria<br>not related to localization/navigation<br>n = 5| D["Excluded Records<br>(n = 5)"]
        C --> E["Full-Text Articles Assessed for Eligibility<br>(n = 995)"]
    end

    subgraph Eligibility
        E -->|Excluded with reasons<br>n = 0| F["Excluded Articles<br>(n = 0)"]
        E --> G["Studies Included in Qualitative Synthesis<br>(n = 995)"]
    end

    subgraph Inclusion
        G --> H["Studies Included in Quantitative Synthesis<br>Accuracy/Error Extraction from Abstracts<br>(n = 44)"]
    end

    style A fill:#D4E6F1,stroke:#2980B9,stroke-width:2px,color:#1B4F72
    style C fill:#D4E6F1,stroke:#2980B9,stroke-width:2px,color:#1B4F72
    style D fill:#FADBD8,stroke:#E74C3C,stroke-width:2px,color:#78281F
    style E fill:#D4E6F1,stroke:#2980B9,stroke-width:2px,color:#1B4F72
    style F fill:#FADBD8,stroke:#E74C3C,stroke-width:2px,color:#78281F
    style G fill:#D5F5E3,stroke:#27AE60,stroke-width:2px,color:#145A32
    style H fill:#D5F5E3,stroke:#27AE60,stroke-width:2px,color:#145A32
```

## Detailed Counts at Each Phase

1. **Identification**:
   - Source: IEEE Xplore database export.
   - Search Query: `("GPS-denied" OR "GNSS-denied" OR "GPS denied" OR "GNSS denied") AND ("UAV" OR "drone" OR "quadrotor" OR "MAV" OR "unmanned aerial") AND ("navigation" OR "localization" OR "SLAM" OR "odometry" OR "state estimation")`
   - Total records exported: **1,000**

2. **Screening**:
   - Initial check: empty titles/abstracts check (0 dropped), publication year check 2015-2026 (0 dropped), duplicates check (0 dropped).
   - Text-corpus screening: keeping only papers matching key localization/navigation terms.
   - **5** papers were excluded because their titles, abstracts, and keywords did not contain explicit terms related to state estimation, localization, SLAM, odometry, or navigation (focusing instead purely on wireless communication protocols or hardware-level radio frequency modeling with no localization context).
   - Remaining papers: **995**

3. **Eligibility**:
   - **995** papers were eligible for classification and qualitative synthesis.
   - Classification categories:
     - Sensor modalities (Camera, IMU, Radar, LiDAR, etc.)
     - Algorithms/frameworks (VIO, VO, EKF, Deep Learning, etc.)
     - Application domains (UAV/Drone, UGV, Spacecraft, etc.)
     - Evaluation environments (Indoor, Outdoor, Simulation, Real-World)
     - Benchmark datasets (KITTI, EuRoC, TUM, etc.)

4. **Inclusion**:
   - **995** papers are included in the qualitative synthesis.
   - **44** papers contain quantitative accuracy/error metrics explicitly in their abstracts (e.g., ATE, RMSE, position error) and are included in the quantitative accuracy meta-analysis.
