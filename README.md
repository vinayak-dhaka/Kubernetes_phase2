



##  **Phase 2: Remediation for Predicted Kubernetes Issues**

###  **Video Demo**


https://github.com/user-attachments/assets/526b5219-694e-4972-aa5a-4bcf6e8ca3f9
###  **Web interface **
https://68000d22b820d52237f84c7d--polite-dieffenbachia-accee2.netlify.app/



###  **Objective**
Following the predictions from **Phase 1**, **Phase 2** focuses on creating a **remediation system** capable of automatically responding to predicted Kubernetes issues. The goal is to **minimize downtime** and **mitigate failures** by triggering timely, intelligent remediation actions.

---

### **Our Solution**
We developed a **functional agent** that listens to predictions from our ML model and responds with appropriate **remediation actions**, either by executing them or recommending them for execution. The system is **modular**, **scalable**, and designed to operate in " **real-time environments**.and **we have deployed the model on website plus a demonstration video to run on your local machine**

---

###  **Key Remediation Actions Implemented**

-  **Pod Restart or Relocation** when failure is predicted  
- **Scaling Pods Automatically** during resource exhaustion alerts  
-  **Optimizing CPU/Memory Resources** to handle potential bottlenecks  

Each action is linked to the **prediction category** detected (**pod failure**, **resource bottleneck**, or **network issue**).

---

### **Agent Behavior**

- The agent **consumes predictions** from the ML model (**Phase 1**)  
- Based on the **prediction class**, it maps to a corresponding **remediation script**  
- The script is either **executed automatically** or **logged as a recommended action**  
- The entire process simulates **self-healing behavior** in Kubernetes

---

###  **Integration Summary**
The project achieves **full-cycle resilience** by combining **predictive intelligence** with **automated remediation**. The system is **extendable** to more failure types and can be **plugged into real Kubernetes environments** with minimal changes.

---

##  Setup & Running the Project

Follow these steps to set up the environment and run the remediation agent:



###  Prerequisites
- Ensure a working **Kubernetes cluster** is running and accessible.

### Commands to Get Started

```bash
# 1. Set up Python environment
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# 2. Install dependencies
pip install -r requirements.txt

# 3. Sync using uv (if using uv package manager)
uv sync

# 4. Run the agent
uv run graph_k8s.py



