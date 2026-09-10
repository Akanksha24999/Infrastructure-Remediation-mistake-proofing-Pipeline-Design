# Staging Infrastructure, Poka-Yoke Build Gate & DCYN Data Pipeline

A production-grade cloud staging solution implementing Infrastructure-as-Code (IaC), automated CI/CD security build gates, and deterministic binary data validation.

---

## 📌 WHAT WAS BUILT (Project Features & Components)

### 1. GCP Infrastructure-as-Code (`terraform/`)
* **GCS `D0 Raw Landing` Bucket (`gs://habot-staging-d0-raw-landing-*`):**
  * Serves as the raw, un-orchestrated landing zone for incoming student onboarding JSON files.
  * Configured with **Uniform Bucket-Level Access** (disables public ACL vulnerabilities), **Object Versioning**, AES-256 Encryption, and **Coldline Lifecycle Rules** (auto-archives files after 30 days, purges after 90 days).
* **BigQuery `D1 Staged/Enforced` Analytics Dataset (`d1_staged_enforced_staging.student_onboarding_staged`):**
  * Serves as the schema-enforced columnar data warehouse for structured analytics.
  * Configured with **Explicit Schema Enforcement** (`student_id`, `age`, `evaluation_score`, `dcyn_*`), **Daily Partitioning** (`ingestion_timestamp`), and **Dataset Access Control Bindings**.

### 2. Poka-Yoke Automated CI/CD Build Gate (`.github/workflows/ci_security_gate.yml`)
* **Fail-Closed Rule:** Operates on an automated security policy where any secret leak or syntax error immediately halts execution (`exit 1`).
* **Secret Scanner:** Uses regex matching to scan code for hardcoded GCP keys, AWS credentials, RSA private keys, and API tokens.
* **Code Format Enforcer:** Enforces Python `flake8` linting and `terraform fmt` validation.

### 3. Backend API & DCYN Binary Logic Library (`backend/`)
* **Django REST Framework API (`POST /api/v1/student-onboarding/ingest/`):**
  * Ingests student onboarding submissions and enforces strict field validation limits ($3 \le \text{Age} \le 18$ and $0.0 \le \text{Assessment Score} \le 100.0$).
* **DCYN (Discretized Binary Yes/No) Logic Library:** Converts qualitative assessment criteria into deterministic binary integer flags ($1 = \text{Yes}, 0 = \text{No}$):
  * `dcyn_has_parent_consent`: `1` if consent is True, else `0`.
  * `dcyn_requires_lsa_support`: `1` if evaluation score $< 70.0$, else `0`.
  * `dcyn_is_eligible_for_program`: `1` if age is valid AND consent is True, else `0`.

---

## 🛠️ HOW TO RUN AND DEPLOY THIS PROJECT

### Step 1: Run & Test the Django Backend API Locally

1. Open a terminal and navigate to the `backend/` directory:
   ```bash
   cd backend
   ```

2. Set up virtual environment and install dependencies:
   ```bash
   python3 -m venv venv
   source venv/bin/activate
   pip install django djangorestframework flake8
   ```

3. Run database migrations:
   ```bash
   python manage.py makemigrations
   python manage.py migrate
   ```

4. Start the Django API development server:
   ```bash
   python manage.py runserver 8001
   ```

5. Open a **second terminal window** and send a test POST payload using `curl`:
   ```bash
   curl -X POST http://127.0.0.1:8001/api/v1/student-onboarding/ingest/ \
     -H "Content-Type: application/json" \
     -d '{
       "student_name": "Alexander Smith",
       "age": 9,
       "evaluation_score": 64.5,
       "parent_consent_given": true,
       "guardian_email": "parent@example.com"
     }'
   ```

#### Expected Response Output:
```json
{
  "status": "success",
  "message": "Student onboarding payload validated and DCYN binary flags generated.",
  "data": {
    "id": "b13a7c64-...",
    "student_name": "Alexander Smith",
    "age": 9,
    "evaluation_score": 64.5,
    "parent_consent_given": true,
    "guardian_email": "parent@example.com",
    "dcyn_has_parent_consent": 1,
    "dcyn_requires_lsa_support": 1,
    "dcyn_is_eligible_for_program": 1,
    "created_at": "2026-09-10T22:00:00Z"
  }
}
```

---

### Step 2: Deploy Infrastructure to Google Cloud Platform (GCP)

1. Navigate to the `terraform/` directory:
   ```bash
   cd terraform
   ```

2. Copy the variable overrides file and set your GCP Project ID:
   ```bash
   cp terraform.tfvars.example terraform.tfvars
   # Edit terraform.tfvars: gcp_project_id = "your-actual-gcp-project-id"
   ```

3. Authenticate Google Cloud CLI:
   ```bash
   gcloud auth login
   gcloud auth application-default login
   ```

4. Initialize and apply Terraform:
   ```bash
   terraform init
   terraform plan
   terraform apply -auto-approve
   ```

---

### Step 3: Push Code to GitHub & Trigger CI/CD Build Gate

1. Navigate to the repository root:
   ```bash
   cd ..
   ```

2. Initialize Git, stage files, and commit:
   ```bash
   git add .
   git commit -m "feat: complete staging infrastructure, build gate, and DCYN backend"
   git branch -M main
   ```

3. Link your remote GitHub repository and push:
   ```bash
   git remote add origin https://github.com/YOUR_GITHUB_USERNAME/YOUR_REPO_NAME.git
   git push -u origin main
   ```

4. Go to your GitHub Repository $\rightarrow$ click the **Actions** tab to view your Poka-Yoke Build Gate (`ci_security_gate.yml`) execute automatically.

---

### Step 4: Build the 15-Slide Presentation Deck

1. Review the outline guide at [docs/SLIDE_PRESENTATION_OUTLINE.md](docs/SLIDE_PRESENTATION_OUTLINE.md).
2. Open Google Slides or PowerPoint and build a 15-slide presentation following the outline.
3. Ensure your name, contact information, and GitHub repository URL are included on Slide 1 & 15.

---

### Step 5: Submit the Project Form

Submit your repository URL and Google Slides presentation link on the submission Google Form before **13-September-2026**.

---

## 📁 Repository Directory Structure

```
.
├── .github/workflows/              # TASK 2: Poka-Yoke CI/CD Build Gate
│   └── ci_security_gate.yml        # Fail-closed secret scanner & linter gate
│
├── backend/                        # TASK 3: Django DRF API & DCYN Serializer
│   ├── config/                     # Django core configuration (settings, urls, wsgi, asgi)
│   ├── student_onboarding/         # App logic (models, serializers, views, tests, migrations)
│   └── manage.py
│
├── terraform/                      # TASK 1: GCP Infrastructure as Code
│   ├── main.tf                     # Provider & project binding
│   ├── gcs.tf                      # D0 Raw Landing storage bucket
│   ├── bigquery.tf                 # D1 Staged/Enforced analytics dataset & table
│   ├── variables.tf                # Input variable declarations
│   ├── outputs.tf                  # Exported resource outputs
│   └── terraform.tfvars.example    # Variable overrides example
│
├── docs/                           # Technical & Interview Documentation
│   ├── ARCHITECTURE_EXPLANATION.md # Architecture & component connection rationale
│   ├── AWS_VS_GCP_GUIDE.md         # AWS to GCP Concept Mapping
│   ├── GCP_DEPLOYMENT_GUIDE.md     # Step-by-step CLI deployment commands
│   └── SLIDE_PRESENTATION_OUTLINE.md # 15-slide presentation deck breakdown
│
├── .gitignore                      # Git build cache & credential exclusions
└── README.md                       # High-level project documentation
```
