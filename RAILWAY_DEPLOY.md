# Railway.app Deployment Guide

## Quick Fix for Current Error

The deployment error was caused by hardcoded local file paths. This has been fixed.

## Deployment Steps

1. **Update your GitHub repository:**
   ```bash
   git add .
   git commit -m "Fix hardcoded paths for Railway deployment"
   git push
   ```

2. **In Railway Dashboard:**
   - Go to your service settings
   - Click "Redeploy" or wait for automatic deployment
   - The service should now start correctly

## Environment Variables (Optional)

Add these in Railway's environment variables section if you want to use OpenAI:

```env
OPENAI_API_KEY=your-api-key-here
SERVER_PORT=8080
SERVER_HOST=0.0.0.0
```

## Verify Deployment

After deployment, your service will be available at:
- `https://your-app-name.up.railway.app/`

The following endpoints will be available:
- `/` - Main web interface
- `/api/generate` - Message generation API
- `/api/timing` - Timing recommendations API
- `/api/compare` - Message comparison API

## Troubleshooting

1. **If CSV file is missing:**
   - The app will still run but with limited functionality
   - Upload `202507_.csv` to your repository

2. **Port binding issues:**
   - Railway automatically sets the PORT environment variable
   - The app is configured to use port 8080 by default

3. **OpenAI API errors:**
   - The app will run in simulation mode without an API key
   - Add `OPENAI_API_KEY` to environment variables for full functionality

## Notes

- The app works without external dependencies (pandas, flask, etc.)
- It will automatically fall back to simulation mode if OpenAI is not configured
- All paths are now relative, making it deployment-ready