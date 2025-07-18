# AgriWaste2Fuel – Smart Farm Waste Tracker & Bio-Fertilizer Planner

**Annam.Ai Hackathon-Based Internship Project – Group 3A**  
**Date:** 6th September 2025

---

## Project Overview

**AgriWaste2Fuel** is an AI-powered platform that helps farmers detect, classify, and manage agricultural waste in an eco-friendly way. It guides them on whether to compost or convert the waste into biogas and estimates the environmental benefits like GHG emission savings and carbon credit potential.

> ⚠️**Note:** This is currently an idea-stage project under active brainstorming and planning. The implementation will follow in the coming weeks.

---

##  Problem Statement

> **Domain:** Agriculture & Environment  
> **Challenge:** Efficient farm waste management with environmental benefit tracking.

We aim to build a **smart waste converter** that:
- Detects & classifies farm waste.
- Recommends biogas or compost processing.
- Estimates GHG emissions saved.
- Converts those savings into potential carbon credits.

---

## Team Members – Group 3A

| Name             | Email                             | Phone       | Institution & Year                            |
|------------------|------------------------------------|-------------|-----------------------------------------------|
| Yashodip More    | yashodipmore2004@gmail.com         | 7820811636  | R.C. Patel Institute of Technology, 4th Year  |
| Komal Kumavat    | komalkumavat025@gmail.com          | 9860690939  | R.C. Patel Institute of Technology, 4th Year  |
| S.M. Sakthivel   | m.sakthivelofficial@gmail.com      | 7418194398  | Achariya college of engineering technology, 4th Year           |
| Barun Saha       | barun.vsaha@gmail.com              | 8708322197  | VIT Chennai, Mechatronics – 4th Year          |
| Bibaswan Das     | bibaswand04@gmail.com              | 7044895853  | VIT Chennai, CSE – 4th Year                   |

> **GitHub Links:** To be added after repository setup.

---

## Mentor

**Name:** Dr. Niranjan Deshpande 
**Contribution:** Provided weekly guidance, helped in refocusing on core objectives and practical implementation.

---

## Week 1 Summary – Internship Kickoff

### Activities Completed
- Brainstormed real-world farmer problems in Maharashtra.
- Finalized the idea: biogas + compost + GHG + credit.
- Designed architecture for decision engine.
- Created decision-tree model for biogas vs compost.
- Identified data sources (ICAR, MNRE, TERI).
- Explored initial models for yield prediction.
- Visualized project flow and interfaces.

### Challenges Faced
- Lack of open datasets for biogas/compost yield.
- Balancing core vs extra features.
- Aligning the team focus during ideation.

### Mentor Guidance
- Encouraged us to center the project around **real-world utility**.
- Suggested using **regression models** for estimating output.
- Recommended **farmer-first design** over complex ML.

---

## System Modules

### 1. **Farm Waste Detection & Classification**
- Image-based detection (YOLOv8)
- Manual keyword input (NLP/regex)
- Waste quantity estimation

### 2. **Biogas or Compost Recommendation**
- Decision tree logic based on type & quantity
- Output: suggested method, steps, tools, expected result

### 3. **GHG Savings Prediction**
- Use weight and standard emission factors
- Calculate savings using:  
  `GHG Saved = weight × (EF_burning − EF_conversion)`

### 4. **Carbon Credit Estimation**
- 1 ton CO₂e saved = 1 credit
- Multiply by market rate
- Optional: generate digital certificate

---

## Tech Stack (Proposed)

| Component        | Tools/Frameworks                            |
|------------------|---------------------------------------------|
| Frontend         | ReactJS or Flutter                          |
| Backend          | Python (FastAPI), OpenCV, Pillow            |
| Waste Matching   | Regex/NLTK                                  |
| AI/ML            | YOLOv8 (PyTorch), TorchServe or Flask       |
| Database         | PostgreSQL / SQLite / Firebase              |
| Hosting          | Vercel / Heroku (dev), AWS EC2 (prod)       |
| Certificate Gen. | PDFKit / ReportLab                          |

---

## Expected Output

- Waste category & quantity
- Recommended waste treatment method
- GHG saved in tons of CO₂e
- Carbon credits earned
- Farmer-friendly dashboard

---

## Next Steps

1. Complete team GitHub repository setup.
2. Implement Module 1 (YOLOv8 + manual input system).
3. Develop initial UI prototype (React or Flutter).
4. Integrate GHG calculator and credit estimation.
5. Finalize dataset sources and regression models.

---

## Contribution Guidelines

- All team members will commit weekly updates.
- Use feature branches and pull requests for collaboration.
- Document all scripts and models.

---

##  Acknowledgements

Thanks to the **Annam.Ai team** and our **mentors** for providing this opportunity and guidance to innovate on real-world agricultural challenges.

---
