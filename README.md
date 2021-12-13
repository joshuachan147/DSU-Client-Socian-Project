DSU Client Socian Project
==============================
## ✨ Introducing SusTracker ™️ ✨

**SusTracker Scenario:**

1. Socian dispatches its drone to keep tabs on the suspect
2. It's given a description of the suspect: blue 🎩 / red 🧥 / black 👟
3. Drone moves into the area & uses **Object Detection** to find the subject
4. Drone remains locked onto the suspect with **Object Tracking**
5. Using **Object Detection/Tracking**, the drone notifies officers if the suspect pulls out a weapon

**We will implement these models:**

1. Clothing-Identified Suspect Detection
2. (Moving) person tracking
3. Held-Weapon Detection

**Our Proof of Concept / End Result**
A Python Program given video footage with a clothing description that can create a new video to...
→ Detect the suspect and draw a bounding box with algorithm 
→ Continue to track and box the suspect
→ Colors the bounding box red when the suspect pulls out a weapon
