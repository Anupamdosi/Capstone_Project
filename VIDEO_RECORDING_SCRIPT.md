# 🎥 Complete Video Recording Script
## Agentic AI Intelligent Loan Approval System

**Total Duration**: 8-10 minutes  
**Recording Tool**: OBS Studio (Recommended)  
**Quality**: 1080p, 30fps

---

## ✅ PRE-RECORDING CHECKLIST

Before you start, ensure:
- [ ] FastAPI running on http://localhost:8000
- [ ] Streamlit running on http://localhost:8501
- [ ] OBS Studio installed and configured
- [ ] Microphone tested and working
- [ ] Browser zoomed to 125% for readability
- [ ] All unnecessary applications closed
- [ ] Network stable

**Command to verify services:**
```bash
curl http://localhost:8000/health
# Should show: {"status":"healthy"}
```

---

## 🎬 RECORDING SCRIPT (Detailed Steps)

### SECTION 1: INTRO & TITLE (0:00 - 0:30)
**Duration**: 30 seconds

**Actions**:
1. Show title slide (if you have one) or desktop
2. Speak in clear, professional tone

**Script**:
```
"Welcome to the Agentic AI Intelligent Loan Approval System demonstration.

This is a production-ready application that uses artificial intelligence 
and multi-agent systems to automatically analyze and approve loan applications.

In this video, I'll walk you through all the key features and show you 
how the system works end-to-end."
```

**Pause**: 2 seconds at end

---

### SECTION 2: SYSTEM OVERVIEW (0:30 - 1:30)
**Duration**: 1 minute

**Actions**:
1. Open browser
2. Navigate to: http://localhost:8501
3. Wait for Streamlit to load
4. Point to each tab slowly
5. Show metrics at top

**Script**:
```
"Here's the Streamlit interface. The system has 3 main sections:

First - Single Application Tab: Submit one loan application and get 
an instant AI decision within milliseconds.

Second - Batch Processing Tab: Upload multiple applications at once 
for rapid bulk processing.

Third - Analytics Tab: View comprehensive statistics, charts, trends, 
and your complete application history.

Let me show you how each one works."
```

**Visual Cues**:
- Point cursor to "Single Application" tab
- Point cursor to "Batch Processing" tab  
- Point cursor to "Analytics" tab
- Pause 1 second between each

---

### SECTION 3: SINGLE APPLICATION DEMO (1:30 - 3:30)
**Duration**: 2 minutes

**Actions**:
1. Click on "Single Application" tab
2. Scroll down to see form
3. Fill in form with these EXACT values:

| Field | Value |
|-------|-------|
| Age | 35 |
| Income | 750000 |
| Employment Type | Employed |
| Credit Score | 720 |
| Loan Amount | 2500000 |
| Tenure | 180 (months) |
| Existing Liabilities | 500000 |
| Location | India |

**Step-by-step**:
```
Step 1: Click "Single Application" tab
Step 2: Scroll down to form
Step 3: Fill Age field → type "35"
Step 4: Fill Income field → type "750000"
Step 5: Select Employment Type → click "Employed"
Step 6: Fill Credit Score → type "720"
Step 7: Fill Loan Amount → type "2500000"
Step 8: Fill Tenure Months → type "180"
Step 9: Fill Existing Liabilities → type "500000"
Step 10: Location dropdown → select "India"
Step 11: Click "Analyze Application" button
Step 12: Wait for result (< 1 second)
```

**Script**:
```
"Now let me show you how to submit a single loan application.

I'll fill in the form with sample applicant data:

[FILL FORM WHILE SPEAKING]

The applicant is 35 years old, employed, with a good credit score of 720.
They're requesting a loan amount of 25 lakh rupees with a 15-year tenure.

Now I'll click the 'Analyze Application' button...

[CLICK BUTTON]

Watch how fast the system works - the decision appears almost instantly!

[SHOW RESULT]

The system has made its decision: [STATE THE DECISION]

It shows:
- The decision (Approved/Rejected/Requires Manual Review)
- A risk score indicating the level of risk
- A confidence level for the decision
- A detailed explanation of why this decision was made

This ensures complete transparency. The applicant or loan officer can see 
exactly why the decision was made, not just the yes/no answer.

The explanation is powered by Claude AI, providing professional, 
natural language reasoning that's easy to understand."
```

**Timing**:
- 0:15 - Start filling form
- 0:45 - Click Analyze button
- 1:00 - Result appears
- 1:50 - Finish reading explanation

---

### SECTION 4: BATCH PROCESSING DEMO (3:30 - 5:00)
**Duration**: 1.5 minutes

**Actions**:
1. Click on "Batch Processing" tab
2. Show the upload area
3. Click to select file
4. Select `sample_data.json` from `/home/ubuntu/Downloads/demo/`
5. Click "Process Batch" button
6. Wait for results
7. Show summary statistics
8. Expand one or two results

**Script**:
```
"The Batch Processing feature is perfect for processing multiple 
applications at once.

[CLICK BATCH PROCESSING TAB]

I have a JSON file with 5 loan applications. Let me upload it...

[CLICK UPLOAD AREA]
[SELECT sample_data.json]
[CLICK PROCESS BATCH]

The system is now processing all 5 applications simultaneously.

[WAIT FOR RESULTS]

Excellent! The batch has been processed. Here's the summary:

[POINT TO METRICS]

- Total applications processed: [SHOW NUMBER]
- Approved: [SHOW NUMBER] applications (shown in green)
- Rejected: [SHOW NUMBER] applications (shown in red)
- Manual Review: [SHOW NUMBER] applications (shown in orange)

The system processed all 5 applications in just a few seconds, making 
intelligent decisions for each one.

You can expand each result to see the detailed analysis including:
- Applicant information
- Risk factors
- Final decision
- Complete reasoning

This is incredibly powerful for processing hundreds or thousands of 
applications efficiently."
```

**Timing**:
- 0:10 - Show upload area
- 0:25 - Upload file
- 0:40 - Results appear
- 1:20 - Expand results
- 1:30 - End section

---

### SECTION 5: ANALYTICS DASHBOARD (5:00 - 6:30)
**Duration**: 1.5 minutes

**Actions**:
1. Click on "Analytics" tab
2. Show metric boxes at top
3. Point to each chart
4. Scroll down to show application history
5. Expand one application

**Script**:
```
"The Analytics tab gives you a complete overview of all your loan data.

[CLICK ANALYTICS TAB]

At the top, you see key performance metrics:

[POINT TO EACH METRIC]

- Total Applications Processed: Shows the total count
- Approved Applications: Green boxes showing approvals
- Rejected Applications: Red boxes showing rejections
- Manual Review Applications: Orange boxes for those needing review
- Average Risk Score: The mean risk across all applications
- Approval Rate: The percentage approved

Below we have visualizations:

[POINT TO RISK SCORE CHART]

The Risk Score Distribution histogram shows how your applicants are 
distributed across the risk spectrum. This helps you understand your 
overall portfolio risk.

[POINT TO PIE CHART]

The Decision Breakdown pie chart shows the proportion of approvals, 
rejections, and manual reviews. The colors are intuitive:
- Green for positive outcomes (approvals)
- Red for negative outcomes (rejections)
- Orange for warning status (manual review)

[SCROLL DOWN]

And finally, here's the complete history of all applications. Each row 
is an application you can expand to see the full analysis.

[EXPAND ONE APPLICATION]

When you expand, you see all the details: applicant information, 
decision, risk score, and the complete AI-generated explanation."
```

**Timing**:
- 0:10 - Show metrics
- 0:40 - Show charts
- 1:10 - Show history
- 1:30 - End section

---

### SECTION 6: KEY FEATURES SUMMARY (6:30 - 7:30)
**Duration**: 1 minute

**Actions**:
1. Scroll back to top
2. Point to various UI elements
3. Speak about key features

**Script**:
```
"Let me highlight the key features that make this system special:

[POINT TO FEATURES AS YOU MENTION THEM]

✅ Real-time Decisions
   Loan decisions are made in under 500 milliseconds. This provides 
   instant feedback to applicants.

✅ Multi-Agent Architecture
   Behind the scenes, 4 specialized AI agents work together:
   - Applicant Profile Agent analyzes employment and background
   - Financial Risk Agent assesses debt and income ratios
   - Loan Decision Agent makes the final decision
   - Compliance Agent ensures regulatory requirements are met

✅ Explainable AI
   Every decision includes a detailed explanation in natural language. 
   This is critical for compliance and customer satisfaction.

✅ Beautiful Analytics
   Visual dashboards help you understand trends and patterns in your 
   loan portfolio.

✅ Persistent Data
   All applications are automatically saved in a SQLite database. 
   Nothing is ever lost.

✅ Batch Processing
   Process thousands of applications with a single upload.

✅ Export Capabilities
   Export data to JSON or CSV for further analysis.

✅ Production Ready
   The code follows best practices and is ready for enterprise deployment."
```

**Timing**:
- 0:10 per feature
- Total: 1:20 (leaving 10s buffer)

---

### SECTION 7: TECHNICAL ARCHITECTURE (7:30 - 8:30)
**Duration**: 1 minute [OPTIONAL - Can skip for non-technical audience]

**Actions**:
1. Open new tab
2. Navigate to: http://localhost:8000/docs
3. Show Swagger UI
4. Explain the API

**Script**:
```
"For developers and technical teams:

This system uses a sophisticated microservices architecture with:

[SHOW SWAGGER UI]

A REST API built with FastAPI. You can see all the endpoints documented 
here. There's an endpoint for single application analysis and one for 
batch processing.

Behind the API:
- A multi-agent system using LangGraph orchestration
- Claude AI for natural language explanations
- SQLite for data persistence
- FastAPI for high-performance processing
- Streamlit for the user interface

The entire system is containerized with Docker, making it easy to deploy 
to any environment - local development, cloud platforms, or on-premises 
servers.

The code is also production-ready with:
- Comprehensive unit and integration tests (98% code coverage)
- Proper error handling and logging
- Security best practices
- Scalable architecture that can handle high volumes"
```

---

### SECTION 8: CLOSING (8:30 - 9:00)
**Duration**: 30 seconds

**Actions**:
1. Return to Streamlit tab
2. Show GitHub link if visible
3. Final thoughts

**Script**:
```
"The Agentic AI Intelligent Loan Approval System demonstrates how 
modern artificial intelligence can automate complex business processes 
while maintaining complete transparency and explainability.

This system can:
- Process hundreds of applications per minute
- Provide consistent, fair decisions
- Generate detailed explanations for every decision
- Integrate with existing financial systems
- Scale to enterprise requirements

The complete code is open-source and available on GitHub. The system 
has achieved an A grade (92/100) in comprehensive evaluation with all 
11 case study requirements met.

Thank you for watching this walkthrough. For more information, visit 
the GitHub repository or check out the comprehensive documentation 
included with the project.

For questions or to learn more, visit: 
https://github.com/Anupamdosi/Capstone_Project"
```

---

## 🎙️ AUDIO TIPS

1. **Speak Clearly**: Enunciate each word
2. **Pace**: Slow down - viewers need time to follow
3. **Pauses**: Add 1-2 second pauses between major points
4. **Volume**: Consistent level, not too loud or soft
5. **Tone**: Professional but friendly
6. **Avoid Filler**: Don't use "um", "uh", "like"

---

## 🖱️ MOUSE MOVEMENT TIPS

1. **Move Slowly**: Fast mouse movements are distracting
2. **Highlight**: When pointing, keep cursor still for 2+ seconds
3. **Click Deliberately**: Don't rapid-click
4. **Zoom**: Use 125% browser zoom for better visibility
5. **Cursor Highlighting**: Use OBS cursor highlighting feature

---

## ⏱️ TIMING BREAKDOWN

| Section | Time | Duration |
|---------|------|----------|
| Intro | 0:00 - 0:30 | 30 sec |
| Overview | 0:30 - 1:30 | 1 min |
| Single App | 1:30 - 3:30 | 2 min |
| Batch Processing | 3:30 - 5:00 | 1.5 min |
| Analytics | 5:00 - 6:30 | 1.5 min |
| Features | 6:30 - 7:30 | 1 min |
| Technical (Opt) | 7:30 - 8:30 | 1 min |
| Closing | 8:30 - 9:00 | 30 sec |
| **TOTAL** | | **~9 minutes** |

---

## 🎬 OBS STUDIO SETUP

### Before Recording:

1. **Add Video Source**:
   - Click "+" under Sources
   - Select "Display Capture" or "Window Capture"
   - Choose your monitor/browser window

2. **Add Audio Source**:
   - Click "+" under Sources
   - Select "Audio Input Capture"
   - Choose your microphone

3. **Check Settings**:
   - Resolution: 1920x1080 (1080p)
   - Frame rate: 30fps
   - Bitrate: 6000-8000 kbps

4. **Test Recording**:
   - Click "Start Recording"
   - Record 30 seconds
   - Click "Stop Recording"
   - Play back to verify audio/video quality

### During Recording:

1. Click "Start Recording"
2. Follow the script above
3. Take breaks between sections if needed (you can edit later)
4. Speak to camera/audience
5. When done, click "Stop Recording"

---

## 📤 POST-RECORDING STEPS

1. **Export**:
   - Wait for export to complete
   - File will be ready in your output folder

2. **Test**:
   - Play video in VLC or browser
   - Verify audio is clear
   - Check video quality

3. **Upload Options**:
   - YouTube (easiest)
   - GitHub Releases
   - Google Drive
   - LinkedIn (for professional network)

4. **Share Link**:
   - Generate shareable link
   - Send to team/audience

---

## 💾 SAMPLE DATA FILE

The sample_data.json file contains:
```json
[
  {"applicant_id": "APP-001", "age": 35, "income": 800000, ...},
  {"applicant_id": "APP-002", "age": 42, "income": 1200000, ...},
  {"applicant_id": "APP-003", "age": 28, "income": 500000, ...},
  {"applicant_id": "APP-004", "age": 55, "income": 1500000, ...},
  {"applicant_id": "APP-005", "age": 38, "income": 900000, ...}
]
```

All in Indian Rupees (₹)

---

## ✅ FINAL RECORDING CHECKLIST

- [ ] Services running (FastAPI + Streamlit)
- [ ] Browser zoomed to 125%
- [ ] OBS Studio configured
- [ ] Microphone tested
- [ ] Test recording done
- [ ] Ready to record main video
- [ ] Follow script above
- [ ] Recording complete
- [ ] Video exported
- [ ] Video tested
- [ ] Ready to upload

---

## 🎉 YOU'RE READY!

Follow this script and you'll create a professional, comprehensive video 
walkthrough of your entire Agentic AI Loan Approval System.

**Good luck with your recording! 🎬✨**

For questions, refer to the main VIDEO_GUIDE.md file.
