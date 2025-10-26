# IQAutoJobs - Complete Testing Guide

## 🎯 Testing the Full User Journey

Follow these steps to test the complete user experience from browsing to applying for a job.

### Prerequisites
- Both workflows are running:
  - **Frontend:** http://localhost:5000
  - **Backend API:** http://localhost:8000
- Database populated with sample data (5 users, 2 companies, 3 jobs)

---

## Test Scenario 1: New User Applying to a Job

### Step 1: Browse Jobs (Unauthenticated)
1. Open your browser and navigate to: `http://localhost:5000`
2. Click the **"Browse Jobs"** button on the homepage
3. **Expected Result:** You should see 3 job listings:
   - Senior Software Engineer @ TechCorp Inc ($150k-$200k)
   - Product Manager @ TechCorp Inc ($130k-$170k)
   - Full Stack Developer @ StartupXYZ ($120k-$160k)

### Step 2: View Job Details
1. Click **"View Details"** on any job card
2. **Expected Result:** Job details page loads showing:
   - Full job description
   - Company information (TechCorp Inc or StartupXYZ)
   - Salary range
   - Location
   - **"Apply Now"** button prominently displayed

### Step 3: Attempt to Apply (Triggers Registration)
1. Click the **"Apply Now"** button
2. **Expected Result:** You are automatically redirected to the registration page
3. **Check URL:** Should be `/auth/register?returnTo=/jobs/[job-id]&action=apply`
4. **Expected Message:** A blue alert box appears saying:
   > "Please create an account to apply for this job. You'll be redirected back after registration."

### Step 4: Complete Registration
Fill out the registration form:
- **First Name:** Test
- **Last Name:** User  
- **Email:** testuser@example.com
- **I am a:** Candidate looking for jobs
- **Password:** password123 (min 8 characters)
- **Confirm Password:** password123

1. Click **"Create Account"**
2. **Expected Result:** 
   - Account created successfully
   - Secure httpOnly cookies set (access_token, refresh_token)
   - **Automatically redirected back to the job details page**

### Step 5: Apply to the Job
1. You should now be back on the job details page
2. Click **"Apply Now"** again
3. **Expected Result:** The Apply Dialog opens (not a redirect this time!)

### Step 6: Submit Application
In the Apply Dialog:
1. Click **"Upload Resume/CV"** or drag-and-drop a file
2. Upload a PDF, DOC, or DOCX file (max 10MB)
3. **Optional:** Enter a cover letter in the text area
4. Click **"Submit Application"**
5. **Expected Result:**
   - File uploads successfully to Cloudflare R2
   - Application submitted
   - Success message appears
   - Dialog closes automatically

---

## Test Scenario 2: Existing User Login

### Step 1: Login with Demo Credentials
1. Navigate to: `http://localhost:5000/auth/login`
2. Use one of these demo accounts:
   - **Candidate:** candidate@demo.com / password
   - **Employer:** employer@demo.com / password
   - **Admin:** admin@demo.com / password
3. Click **"Sign In"**
4. **Expected Result:**
   - Logged in successfully
   - Redirected to dashboard
   - httpOnly cookies set

### Step 2: Browse and Apply as Authenticated User
1. Navigate to `/jobs`
2. Click on any job
3. Click **"Apply Now"**
4. **Expected Result:** Apply dialog opens immediately (no redirect!)
5. Upload CV and submit

---

## Test Scenario 3: Session Management

### Step 1: Check Protected Routes
1. Without logging in, try to access: `http://localhost:5000/dashboard`
2. **Expected Result:** Redirected to login page

### Step 2: Logout
1. Login first if not already logged in
2. Find and click the **Logout** button (in navigation/header)
3. **Expected Result:**
   - Cookies cleared
   - Redirected to home page
   - Cannot access dashboard without logging in again

### Step 3: Session Expiry
1. Login to the application
2. Wait 15 minutes (access token expires)
3. Try to apply to a job
4. **Expected Result:** 
   - Session expired error
   - Redirected to login page
   - After login, redirected back to the job

---

## Test Scenario 4: Navigation & Pages

### Pages to Test:
| Page | URL | Expected Content |
|------|-----|------------------|
| **Home** | `/` | Landing page with hero, stats, CTA buttons |
| **Jobs** | `/jobs` | List of 3 jobs with search/filters |
| **Job Details** | `/jobs/[id]` | Full job info + Apply button |
| **Companies** | `/companies` | List of 2 companies |
| **Users** | `/users` | List of 5 registered users |
| **Login** | `/auth/login` | Login form with demo credentials |
| **Register** | `/auth/register` | Registration form |
| **Dashboard** | `/dashboard` | Protected - requires authentication |

---

## Test Scenario 5: API Endpoints

### Test with cURL or Postman:

```bash
# List all jobs
curl http://localhost:8000/api/jobs/

# Get specific job
curl http://localhost:8000/api/jobs/[job-id]

# List companies
curl http://localhost:8000/api/public/companies/

# List users
curl http://localhost:8000/api/public/users/

# Register new user
curl -X POST http://localhost:8000/api/auth/register \
  -H "Content-Type: application/json" \
  -d '{
    "email": "newuser@test.com",
    "password": "password123",
    "first_name": "New",
    "last_name": "User",
    "role": "CANDIDATE"
  }'

# Login
curl -X POST http://localhost:8000/api/auth/login \
  -H "Content-Type: application/json" \
  -d '{
    "email": "candidate@demo.com",
    "password": "password"
  }'
```

---

## Test Scenario 6: File Upload Validation

### Test Invalid Files:
1. Try to upload a .txt file
   - **Expected:** Error: "Please upload a PDF or Word document"

2. Try to upload a file > 10MB
   - **Expected:** Error: "File size must be less than 10MB"

3. Upload valid file types:
   - ✅ PDF (.pdf)
   - ✅ Word Document (.doc)
   - ✅ Word Document (.docx)

---

## Common Issues & Solutions

### Issue: Jobs not loading (showing "0 jobs found")
**Solution:** Wait 2-3 seconds for the API call to complete. The frontend fetches data on mount.

### Issue: Register page shows 404
**Solution:** 
1. Restart the Frontend workflow
2. Clear browser cache
3. Try accessing `/auth/register` directly

### Issue: Apply dialog doesn't open
**Solution:** 
1. Check browser console for errors
2. Verify you're on the job details page (not the jobs list)
3. Ensure the job has an "Apply Now" button

### Issue: Session expires too quickly
**Note:** Access tokens expire after 15 minutes. This is intentional for security. Refresh tokens last 7 days.

---

## Security Features to Verify

1. ✅ **httpOnly Cookies** - Tokens not accessible via JavaScript
   - Check: Open browser DevTools > Application > Cookies
   - Should see `access_token` and `refresh_token` with HttpOnly flag

2. ✅ **Password Hashing** - Passwords stored as Argon2 hashes
   - Verify: Check database - no plain text passwords

3. ✅ **Authentication Checks** - Apply dialog verifies auth via API
   - Verify: Not checking localStorage, using `/api/auth/me` endpoint

4. ✅ **File Upload Validation** - Type and size checks
   - Test with various file types and sizes

5. ✅ **XSS Protection** - httpOnly cookies prevent token theft
   - Cannot access tokens via `document.cookie` in console

---

## Database Sample Data

### Users (5):
1. admin@demo.com / password (ADMIN)
2. employer@demo.com / password (EMPLOYER)
3. startup@demo.com / password (EMPLOYER)
4. candidate@demo.com / password (CANDIDATE)
5. jane@demo.com / password (CANDIDATE)

### Companies (2):
1. **TechCorp Inc** - Technology, 100-500 employees, San Francisco, CA
2. **StartupXYZ** - Fintech, 10-50 employees, New York, NY

### Jobs (3):
1. **Senior Software Engineer** @ TechCorp Inc
   - Full-time, Engineering, Senior
   - $150,000 - $200,000, San Francisco, CA

2. **Product Manager** @ TechCorp Inc
   - Full-time, Product, Mid-Level
   - $130,000 - $170,000, San Francisco, CA

3. **Full Stack Developer** @ StartupXYZ
   - Full-time, Engineering, Mid-Level
   - $120,000 - $160,000, New York, NY

---

## Success Criteria

✅ All these should work without errors:

- [ ] Can browse jobs without logging in
- [ ] Can view job details
- [ ] Unauthenticated users redirected to register when applying
- [ ] Registration completes and returns to job page
- [ ] Apply dialog opens after authentication
- [ ] CV upload works (PDF/DOC/DOCX)
- [ ] Application submission successful
- [ ] Login works with demo credentials
- [ ] Dashboard protected (requires auth)
- [ ] Logout clears session
- [ ] All pages render correctly
- [ ] No console errors (except expected WebSocket warnings)

---

## Performance Expectations

- **Jobs list:** Loads in < 2 seconds
- **Job details:** Loads in < 2 seconds
- **File upload:** Depends on file size and network
- **Page navigation:** Instant (client-side routing)

---

## Next Steps After Testing

If all tests pass, the application is ready for:
1. **Deployment to Railway/Replit**
2. **Production database migration**
3. **Adding optional features:**
   - User profile management
   - Google OAuth integration
   - Application status tracking
   - Employer job posting interface
   - Advanced search filters
   - Email notifications

---

## Need Help?

- Check backend logs: See "Backend API" workflow in Replit
- Check frontend logs: See "Frontend" workflow in Replit
- Database issues: Use Replit database tab
- API testing: Use `/docs` endpoint (Swagger UI) at `http://localhost:8000/docs`

**Happy Testing! 🎉**
