"""Database Seed Script for Plaxeron Placement Portal

Populates the SQLite database with rich mock data including Students, Companies,
Placement Drives, Applications, Interview Schedules, Notifications, and Support Tickets.

Usage:
    python seed_data.py
"""

import os
import sys
from datetime import datetime, date, time, timedelta
from werkzeug.security import generate_password_hash

PROJECT_DIR = os.path.abspath(os.path.dirname(__file__))
sys.path.append(PROJECT_DIR)

from app import app
from models import (
    db, Admin, Student, Company, PlacementDrive, Application, InterviewSchedule,
    CompanyNotification, StudentNotification, StudentDriveView, DriveActivityLog,
    SupportTicket, BroadcastMessage, CompanyBroadcast, DeletedStudentLog, DeletedCompanyLog
)

def seed_database():
    with app.app_context():
        print("Resetting and building database tables...")
        db.drop_all()
        db.create_all()

        # ----------------------------------------------------
        # 1. ADMIN ACCOUNT
        # ----------------------------------------------------
        print("Creating Superuser Admin account...")
        admin = Admin(
            email="admin@plaxeron.com",
            password=generate_password_hash("admin123")
        )
        db.session.add(admin)
        db.session.commit()

        # ----------------------------------------------------
        # 2. RECRUITER COMPANIES
        # ----------------------------------------------------
        print("Creating Companies...")
        companies_data = [
            ("Google LLC", "COMP-GOOG-01", "Technology & AI", "10,000+ employees", "Bengaluru, Karnataka", "https://google.com", "Global leader in search, cloud, AI, and developer platform technologies.", "Sarah Jenkins", "Director of University Hiring", "recruiting@google.com", "+91 9876543210", "Approved", True, True),
            ("Microsoft Corporation", "COMP-MSFT-02", "Enterprise Software & Cloud", "10,000+ employees", "Hyderabad, Telangana", "https://microsoft.com", "Empowering every person and organization through Azure cloud and developer software.", "Rahul Sharma", "Lead Talent Acquisition", "careers@microsoft.com", "+91 9876543211", "Approved", True, True),
            ("Amazon Web Services", "COMP-AMZN-03", "Cloud Infrastructure", "10,000+ employees", "Bengaluru, Karnataka", "https://aws.amazon.com", "Pioneering cloud computing infrastructure, scalable serverless platforms, and AI systems.", "Amanda Vance", "Campus Lead - APAC", "jobs@amazon.com", "+91 9876543212", "Approved", True, True),
            ("Adobe Systems", "COMP-ADBE-04", "Digital Media & Web Graphics", "5,000-10,000 employees", "Noida, Uttar Pradesh", "https://adobe.com", "Transforming creative digital content and document cloud experiences globally.", "Rajesh Kumar", "Senior HR Business Partner", "campus@adobe.com", "+91 9876543213", "Approved", True, True),
            ("NVIDIA Graphics", "COMP-NVDA-05", "Artificial Intelligence & Semiconductors", "10,000+ employees", "Pune, Maharashtra", "https://nvidia.com", "Accelerated computing pioneer creating GPUs, AI platforms, and autonomous systems.", "Elena Rostova", "Global Technical Recruiter", "university@nvidia.com", "+91 9876543214", "Approved", True, True),
            ("Goldman Sachs", "COMP-GS-06", "FinTech & Quantitative Finance", "10,000+ employees", "Bengaluru, Karnataka", "https://goldmansachs.com", "Leading global financial institution building ultra-low latency trading systems.", "Aditya Malhotra", "Engineering Campus Recruiter", "careers@gs.com", "+91 9876543215", "Approved", True, True),
            ("Razorpay Technologies", "COMP-RZP-07", "FinTech & Digital Payments", "1,000-5,000 employees", "Bengaluru, Karnataka", "https://razorpay.com", "India's leading payment gateway and neobanking platform for modern businesses.", "Neha Gupta", "Talent Acquisition Specialist", "careers@razorpay.com", "+91 9876543216", "Approved", True, True),
            ("Tata Consultancy Services", "COMP-TCS-08", "IT Services & Consulting", "10,000+ employees", "Mumbai, Maharashtra", "https://tcs.com", "Global IT services, consulting, and business solutions transformation enterprise.", "Vikram Patel", "Regional Campus HR", "campus.recruitment@tcs.com", "+91 9876543217", "Approved", True, True),

            # Pending Approvals (for Admin action review screenshot)
            ("QuantumScape AI", "COMP-QSAI-09", "Quantum Computing & ML", "100-500 employees", "Gurugram, Haryana", "https://quantumscape-ai.io", "Next-gen quantum machine learning algorithms and simulation engines.", "Siddharth Roy", "Founder & CTO", "hr@quantumscape-ai.io", "+91 9876543218", "Pending", False, True),
            ("ByteWave Networks", "COMP-BWN-10", "Cybersecurity & Edge Computing", "50-200 employees", "Chandigarh", "https://bytewave.net", "Zero-trust network security architecture and edge computing gateways.", "Kavita Reddy", "People Operations Manager", "hiring@bytewave.net", "+91 9876543219", "Pending", False, True),
        ]

        companies = []
        for name, cid, ind, size, loc, web, desc, hr, hr_desg, email, mob, status, is_appr, is_act in companies_data:
            c = Company(
                company_name=name,
                company_id=cid,
                industry=ind,
                company_size=size,
                location=loc,
                website=web,
                description=desc,
                hr_contact=hr,
                hr_designation=hr_desg,
                email=email,
                mobile=mob,
                password=generate_password_hash("company123"),
                approval_status=status,
                is_approved=is_appr,
                is_active=is_act
            )
            db.session.add(c)
            companies.append(c)
        db.session.commit()

        # ----------------------------------------------------
        # 3. PLACEMENT DRIVES
        # ----------------------------------------------------
        print("Creating Placement Drives...")
        drives_data = [
            (companies[0].id, "DRV-GOOG-2026-01", "Software Development Engineer II", "Architect scalable distributed microservices, storage engines, and high-throughput backend systems for Google Cloud.", "Min 8.5 CGPA in CSE/IT/ECE. Mastery in Data Structures & Algorithms.", "Python, C++, System Design, Kubernetes, Distributed Systems", 2800000, "Bengaluru", "Full Time", "Hybrid", "Entry Level", 12, "Online Assessment -> Tech Round 1 -> Tech Round 2 -> HR Review", "B.Tech,M.Tech", "4th Year,2nd Year", 25, "Approved"),
            (companies[0].id, "DRV-GOOG-2026-02", "AI / Machine Learning Engineer", "Build large language model pipelines, neural search rankers, and computer vision acceleration libraries.", "Min 9.0 CGPA. Machine Learning coursework required.", "Python, PyTorch, TensorFlow, C++, CUDA, Deep Learning", 3200000, "Bengaluru / Hyderabad", "Full Time", "On-site", "Entry Level", 6, "AI Coding Challenge -> 3x Technical Deep Dives", "M.Tech,B.Tech", "2nd Year,4th Year", 20, "Approved"),
            (companies[1].id, "DRV-MSFT-2026-01", "Cloud Systems & DevOps Engineer", "Architect Azure cloud infrastructure, automated CI/CD pipelines, and high-availability cluster controllers.", "Min 7.8 CGPA. Strong Linux background.", "Azure, Go, Python, Terraform, Docker, Linux Systems", 2200000, "Hyderabad", "Full Time", "Hybrid", "Entry Level", 15, "Coding Test -> System Architecture -> 2x Technical Interviews", "B.Tech,B.E.,M.Tech", "4th Year", 18, "Approved"),
            (companies[2].id, "DRV-AMZN-2026-01", "Full Stack Software Engineer", "Develop customer-facing ecommerce modules, cloud serverless APIs, and AWS developer toolchains.", "Min 7.5 CGPA across all CS branches.", "Java, React, AWS Lambda, TypeScript, Node.js, GraphQL", 2400000, "Bengaluru", "Full Time", "Hybrid", "Entry Level", 20, "Online Test -> 3x Technical Interviews -> Bar Raiser", "B.Tech,M.Tech,BCA,MCA", "4th Year,2nd Year,3rd Year", 15, "Approved"),
            (companies[3].id, "DRV-ADBE-2026-01", "Frontend & Web Graphics Engineer", "Engine WebGL canvas tools, real-time creative collaboration features, and UI engines for Adobe Creative Cloud.", "Min 8.0 CGPA. Strong JavaScript / Web performance background.", "JavaScript (ES6+), React, WebGL, WebAssembly, CSS3/Sass", 2000000, "Noida", "Full Time", "Hybrid", "Entry Level", 8, "Portfolio Review -> Live Coding -> Technical Interview", "B.Tech,BCA", "4th Year,3rd Year", 12, "Approved"),
            (companies[4].id, "DRV-NVDA-2026-01", "Embedded Systems & CUDA Engineer", "Optimize GPU kernel performance, deep learning runtime engines, and autonomous vehicle compute units.", "Min 8.8 CGPA in CSE/ECE/EE.", "C++, CUDA, OS Internals, Computer Architecture, Embedded C", 3000000, "Pune", "Full Time", "On-site", "Entry Level", 5, "Hardware/C++ Written Exam -> 3x Technical Rounds", "B.Tech,M.Tech", "4th Year,2nd Year", 22, "Approved"),
            (companies[5].id, "DRV-GS-2026-01", "Quantitative Software Analyst", "Design low-latency financial trading platforms, risk calculation engines, and algorithmic execution models.", "Min 8.5 CGPA in Math/CSE/ECE. Exceptional analytical aptitude.", "C++, Java, Python, Quantitative Modeling, Algorithms, SQL", 3500000, "Bengaluru", "Full Time", "On-site", "Entry Level", 10, "Math & CS Assessment -> 3x Quant/Tech Rounds", "B.Tech,M.Tech", "4th Year,2nd Year", 10, "Approved"),
            (companies[6].id, "DRV-RZP-2026-01", "Backend Software Engineer", "Build payment processing gateways, ledger databases, and automated fraud detection webhooks.", "Min 7.5 CGPA.", "Go, Node.js, PostgreSQL, Redis, Microservices, Kafka", 1800000, "Bengaluru", "Full Time", "Hybrid", "Entry Level", 12, "Machine Coding -> System Design -> Culture Fit Round", "B.Tech,BCA,MCA", "4th Year,3rd Year", 14, "Approved"),
            (companies[7].id, "DRV-TCS-2026-01", "Digital Systems Cadre Engineer", "Enterprise cloud migration, cybersecurity engineering, and full-stack software development.", "Min 6.5 CGPA across all disciplines.", "Java, Python, C#, SQL, DevOps Fundamentals, Web Tech", 900000, "Pan India", "Full Time", "On-site", "Entry Level", 50, "TCS NQT National Test -> Interview Round", "B.Tech,B.E.,M.Tech,BCA,MCA", "4th Year,3rd Year", 30, "Approved"),
            (companies[8].id, "DRV-QSAI-2026-01", "Quantum Algorithm Developer", "Develop novel quantum error correction codes and variational quantum eigensolvers.", "Min 9.0 CGPA.", "Python, Qiskit, C++, Applied Physics, Linear Algebra", 2600000, "Gurugram", "Full Time", "Hybrid", "Entry Level", 4, "Research Review -> Technical Interview", "M.Tech,B.Tech", "2nd Year,4th Year", 28, "Pending"),
        ]

        drives = []
        for cid, did, title, desc, elig, skills, sal, loc, jtype, wmode, exp, vac, sel, deg, yrs, days_left, st in drives_data:
            d = PlacementDrive(
                company_id=cid,
                drive_id=did,
                job_title=title,
                job_description=desc,
                eligibility_criteria=elig,
                required_skills=skills,
                salary=sal,
                location=loc,
                job_type=jtype,
                work_mode=wmode,
                experience_level=exp,
                vacancies=vac,
                selection_process=sel,
                target_degrees=deg,
                target_years=yrs,
                application_deadline=date.today() + timedelta(days=days_left),
                application_deadline_time=time(23, 59),
                publish_date=date.today() - timedelta(days=5),
                publish_time=time(9, 0),
                status=st
            )
            db.session.add(d)
            drives.append(d)
        db.session.commit()

        # ----------------------------------------------------
        # 4. STUDENTS
        # ----------------------------------------------------
        print("Creating Students...")
        students_data = [
            ("John Doe", "STU-2026-001", "student@plaxeron.com", "Indian Institute of Technology", "B.Tech", "Computer Science & Engineering", "4th Year", 9.4, 96.5, 95.8, "2026", "Python, C++, Flask, React, PostgreSQL, System Design", "https://linkedin.com/in/johndoe-plaxeron", "https://github.com/johndoe-dev", "Software engineer focusing on high-concurrency microservices and database engines.", "+91 9123456789"),
            ("Priya Sharma", "STU-2026-002", "priya.sharma@example.com", "Delhi Technological University", "B.Tech", "Information Technology", "4th Year", 8.9, 93.0, 94.2, "2026", "Java, Spring Boot, Microservices, Kubernetes, Redis", "https://linkedin.com/in/priyasharma", "https://github.com/priyasharma-code", "Cloud platform enthusiast and backend engineer.", "+91 9123456790"),
            ("Alex Chen", "STU-2026-003", "alex.chen@example.com", "National Institute of Technology", "M.Tech", "Data Science & Artificial Intelligence", "2nd Year", 9.7, 98.0, 97.5, "2026", "Python, PyTorch, CUDA, Deep Learning, Computer Vision", "https://linkedin.com/in/alexchen-ai", "https://github.com/alexchen-ai", "AI researcher published in computer vision conference proceedings.", "+91 9123456791"),
            ("Rahul Verma", "STU-2026-004", "rahul.verma@example.com", "Birla Institute of Technology", "BCA", "Computer Applications", "3rd Year", 8.5, 89.0, 90.4, "2026", "JavaScript, HTML5/CSS3, React, Node.js, MongoDB", "https://linkedin.com/in/rahulverma-web", "https://github.com/rahulverma-web", "Frontend craftsperson passionate about fast, pixel-perfect user experiences.", "+91 9123456792"),
            ("Ananya Patel", "STU-2026-005", "ananya.patel@example.com", "Vellore Institute of Technology", "B.Tech", "Electronics & Communication", "4th Year", 9.1, 95.0, 93.8, "2026", "C++, Embedded Systems, Linux Internals, Verilog, RTOS", "https://linkedin.com/in/ananyapatel-ec", "https://github.com/ananyapatel-hw", "Hardware-software co-design engineer specializing in embedded Linux.", "+91 9123456793"),
            ("Rohan Mehta", "STU-2026-006", "rohan.mehta@example.com", "IIIT Hyderabad", "B.Tech", "Computer Science & Engineering", "4th Year", 9.6, 97.2, 96.9, "2026", "C++, Competitive Programming, Algorithms, Go, Distributed Storage", "https://linkedin.com/in/rohanmehta-cs", "https://github.com/rohanmehta-algo", "Candidate Master on Codeforces. Loves building operating systems.", "+91 9123456794"),
            ("Sneha Reddy", "STU-2026-007", "sneha.reddy@example.com", "BITS Pilani", "M.Tech", "Software Systems", "2nd Year", 8.7, 91.5, 92.0, "2026", "Java, AWS, GraphQL, Docker, Terraform, CI/CD Pipelines", "https://linkedin.com/in/snehareddy-cloud", "https://github.com/snehareddy-cloud", "Cloud infrastructure & DevOps practitioner.", "+91 9123456795"),
            ("Karan Malhotra", "STU-2026-008", "karan.malhotra@example.com", "PSG College of Technology", "MCA", "Computer Applications", "3rd Year", 8.2, 87.0, 88.5, "2026", "Python, Django, PostgreSQL, Docker, Bootstrap, REST APIs", "https://linkedin.com/in/karanmalhotra", "https://github.com/karanmalhotra-dev", "Full-stack web application developer.", "+91 9123456796"),
        ]

        students = []
        for name, sid, email, coll, deg, br, yr, cgpa, p10, p12, g_yr, sk, li, gh, bio, cont in students_data:
            s = Student(
                name=name,
                student_id=sid,
                email=email,
                password=generate_password_hash("student123"),
                dob="2002-06-15",
                college=coll,
                degree=deg,
                branch=br,
                year_of_study=yr,
                cgpa=cgpa,
                tenth_percent=p10,
                twelfth_percent=p12,
                graduation_year=g_yr,
                skills=sk,
                linkedin=li,
                github=gh,
                bio=bio,
                contact=cont,
                is_active=True
            )
            db.session.add(s)
            students.append(s)
        db.session.commit()

        # ----------------------------------------------------
        # 5. APPLICATIONS
        # ----------------------------------------------------
        print("Creating Applications...")
        apps_data = [
            (students[0].id, drives[0].id, "APP-2026-GOOG-01", "Interview", "Cleared Online Assessment (100/100). Technical Interview scheduled."),
            (students[0].id, drives[1].id, "APP-2026-GOOG-02", "Shortlisted", "Shortlisted based on ML publications and strong CGPA."),
            (students[0].id, drives[2].id, "APP-2026-MSFT-01", "Shortlisted", "Resume screened and approved by Cloud Engineering team."),
            (students[1].id, drives[3].id, "APP-2026-AMZN-01", "Placed", "Selected for Full Stack SDE role at ₹24 LPA! Offer letter issued."),
            (students[1].id, drives[4].id, "APP-2026-ADBE-01", "Shortlisted", "Portfolio shortlisted for Adobe Creative Cloud team."),
            (students[2].id, drives[1].id, "APP-2026-GOOG-03", "Interview", "Invited for AI/ML technical deep dive with Senior Research Scientist."),
            (students[2].id, drives[5].id, "APP-2026-NVDA-01", "Shortlisted", "CUDA programming assessment passed with top score."),
            (students[3].id, drives[4].id, "APP-2026-ADBE-02", "Applied", "Application submitted. Under HR initial review."),
            (students[3].id, drives[7].id, "APP-2026-RZP-01", "Shortlisted", "Selected for machine coding round."),
            (students[4].id, drives[5].id, "APP-2026-NVDA-02", "Interview", "Embedded Systems technical round scheduled."),
            (students[5].id, drives[0].id, "APP-2026-GOOG-04", "Interview", "Cleared Round 1 & Round 2 technical interviews!"),
            (students[5].id, drives[6].id, "APP-2026-GS-01", "Placed", "Selected for Quantitative Analyst role at ₹35 LPA!"),
            (students[6].id, drives[2].id, "APP-2026-MSFT-02", "Interview", "DevOps & Cloud architecture interview scheduled."),
            (students[7].id, drives[8].id, "APP-2026-TCS-01", "Applied", "NQT Assessment registration confirmed."),
        ]

        applications = []
        for sid, did, code, st, rem in apps_data:
            a = Application(
                student_id=sid,
                drive_id=did,
                application_code=code,
                application_date=datetime.now() - timedelta(days=3),
                status=st,
                remark=rem
            )
            db.session.add(a)
            applications.append(a)
        db.session.commit()

        # ----------------------------------------------------
        # 6. INTERVIEW SCHEDULES
        # ----------------------------------------------------
        print("Creating Interview Schedules...")
        schedules_data = [
            (companies[0].id, drives[0].id, applications[0].id, date.today() + timedelta(days=2), time(10, 0), "Online (Google Meet)", "System Design & Data Structures Evaluation.", "Scheduled"),
            (companies[0].id, drives[1].id, applications[5].id, date.today() + timedelta(days=4), time(14, 30), "Online (Google Meet)", "Neural Network Optimization & PyTorch Internals.", "Scheduled"),
            (companies[4].id, drives[5].id, applications[9].id, date.today() + timedelta(days=3), time(11, 0), "Online (Zoom)", "Embedded C & OS Memory Management Deep Dive.", "Scheduled"),
            (companies[0].id, drives[0].id, applications[10].id, date.today() + timedelta(days=1), time(16, 0), "Online (Google Meet)", "Final HR & Executive Leadership Interview.", "Scheduled"),
            (companies[1].id, drives[2].id, applications[12].id, date.today() + timedelta(days=5), time(11, 30), "Online (Microsoft Teams)", "Azure Kubernetes & Terraform Live Lab Test.", "Scheduled"),
        ]

        for cid, did, app_id, idate, itime, mode, notes, st in schedules_data:
            isch = InterviewSchedule(
                company_id=cid,
                drive_id=did,
                application_id=app_id,
                interview_date=idate,
                interview_time=itime,
                mode=mode,
                notes=notes,
                schedule_status=st
            )
            db.session.add(isch)
        db.session.commit()

        # ----------------------------------------------------
        # 7. NOTIFICATIONS, TICKETS & BROADCASTS
        # ----------------------------------------------------
        print("Creating Notifications, Support Tickets & System Broadcasts...")
        db.session.add(StudentNotification(
            student_id=students[0].id,
            notif_type="success",
            icon="bi-check-circle-fill",
            text="Congratulations! You have been shortlisted for Google SDE II Technical Interview.",
            notif_key="notif-stu-1-goog-shortlist",
            is_read=False
        ))

        db.session.add(CompanyNotification(
            company_id=companies[0].id,
            notif_type="info",
            icon="bi-person-badge",
            text="New application received from Rohan Mehta (CGPA 9.6, IIIT Hyderabad) for SDE II.",
            notif_key="notif-comp-1-new-app",
            is_read=False
        ))

        db.session.add(BroadcastMessage(
            target="all",
            subject="Campus Placement Drive Season 2026 Officially Launched!",
            message="Welcome all Students and Recruiting Partners! Placement drives for Google, Microsoft, Amazon, Adobe, and NVIDIA are now active.",
            sent_by=admin.id,
            recipient_count=15
        ))

        db.session.add(SupportTicket(
            student_id=students[0].id,
            subject="Resume re-upload request for Google drive",
            message="I updated my GitHub projects link on my resume. Kindly allow re-upload for Google SDE II application.",
            category="Resume / Profile",
            status="In Progress",
            admin_reply="Under review by placement team.",
            submitter_type="student"
        ))

        db.session.add(SupportTicket(
            company_id=companies[0].id,
            subject="Request for additional interview slot capacity",
            message="We would like to add 5 more interview slots for the AI/ML Drive next Tuesday.",
            category="Interview Scheduling",
            status="Resolved",
            admin_reply="Additional slots approved and enabled in company dashboard.",
            submitter_type="company"
        ))

        db.session.add(DriveActivityLog(
            company_id=companies[0].id,
            drive_id=drives[0].id,
            action="created",
            summary="Placement drive 'Software Development Engineer II' created and submitted for admin approval."
        ))

        db.session.commit()
        print("🎉 Database seeding completed successfully!")

if __name__ == "__main__":
    seed_database()
