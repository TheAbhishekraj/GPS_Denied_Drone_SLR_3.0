# Data Dictionary: GNSS-Denied Drone SLR 3.0 Datasets

This document provides metadata schemas and column definitions for the three processed datasets located in the `data/processed/` directory.

---

## 📄 1. `database_final.csv`
Contains the cleaned, screened metadata of **995 peer-reviewed publications** from the search engine export.

| Column Name | Data Type | Description | Example |
| :--- | :--- | :--- | :--- |
| `title` | String | Cleaned title of the publication, normalized of whitespace. | *Drift-Free Visual SLAM for Mobile Robot Localization* |
| `authors` | String | Semicolon-separated list of authors. | *M. Wang; C. Zhai; Y. Yang* |
| `affiliations` | String | Institutional affiliations of the authors. | *College of Information Engineering, Southwest University* |
| `publication` | String | Name of the journal or conference venue. | *IEEE Robotics and Automation Letters* |
| `year` | Integer | Year of publication (filtered to range 2015–2026). | *2022* |
| `abstract` | String | Cleaned abstract of the paper, stripped of HTML tags. | *In global navigation satellite system (GNSS) denied areas...* |
| `doi` | String | Digital Object Identifier of the publication. | *10.1109/LRA.2022.3203438* |
| `citation_count` | Integer | Article citation count tracked at the time of export. | *17* |
| `reference_count`| Integer | Total references cited inside the paper. | *35* |
| `issn` | String | International Standard Serial Number. | *2576-6813* |
| `funding` | String | Funding and grant details associated with the study. | *National Natural Science Foundation of China* |
| `text_corpus` | String | Lowercase concatenation of `title`, `abstract`, and keywords used for NLP. | *drift-free visual slam...* |

---

## 🏷️ 2. `classified_papers.csv`
Contains the taxonomy labels assigned to each of the **995 papers** via regex keyword parsing.

*Inherits all columns from `database_final.csv` and appends the following:*

| Column Name | Data Type | Description | Values / Multi-Label Categories |
| :--- | :--- | :--- | :--- |
| `sensors` | String | Semicolon-separated sensor modalities detected. | *Camera; IMU; LiDAR; UWB; GNSS/GPS* |
| `algorithms` | String | Semicolon-separated estimation algorithms detected. | *EKF; Visual-Inertial Odometry; Deep Learning* |
| `applications` | String | Semicolon-separated target platform/use case. | *UAV/Drone; Multi-Robot/Swarm; Inspection* |
| `environments` | String | Semicolon-separated testing environments. | *Indoor; Real-World; Simulation* |
| `datasets` | String | Semicolon-separated standardized datasets referenced. | *KITTI; EuRoC; Custom/Own* |

---

## 📊 3. `accuracy_data.csv`
Contains quantitative localization errors extracted from **44 paper abstracts**.

| Column Name | Data Type | Description | Example |
| :--- | :--- | :--- | :--- |
| `doi` | String | Digital Object Identifier of the source paper. | *10.1109/ACCESS.2022.3203438* |
| `title` | String | Title of the source paper. | *Drift-Free Visual SLAM for Mobile Robot Localization* |
| `year` | Integer | Year of publication. | *2022* |
| `sensors` | String | Sensor taxonomy labels mapped to the paper. | *Camera; IMU* |
| `algorithms` | String | Algorithm taxonomy labels mapped to the paper. | *Visual-Inertial Odometry* |
| `applications` | String | Application taxonomy labels mapped to the paper. | *UAV/Drone* |
| `environments` | String | Environment taxonomy labels mapped to the paper. | *Indoor* |
| `accuracy_m` | Float | **Normalised translation error (ATE/RMSE) in metres.** | *0.15* (corresponding to 15cm) |
| `accuracy_pct` | Float | Percentage-based tracking drift/error (where applicable). | *0.48* (corresponding to 0.48%) |
| `accuracy_unit_original` | String | Original unit of error reported by authors in abstract. | *cm* |
| `accuracy_text_match` | String | Literal raw string segment captured by regex match. | *accuracy of 15 cm* |
