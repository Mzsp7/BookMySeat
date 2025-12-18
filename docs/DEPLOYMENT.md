# Deployment Guide (Render)

This guide explains how to deploy your **BookMySeat** project to [Render](https://render.com).

## 1. Prepare for Deployment

I have already configured the following files for you:
- **`requirements.txt`**: Added production servers (`gunicorn`) and static handling (`whitenoise`).
- **`settings.py`**: Configured to use environment variables for security and WhiteNoise for CSS/JS.
- **`build.sh`**: Script to automate migrations and static collection.
- **`render.yaml`**: A blueprint file that sets up both the Web Service and Database automatically.

## 2. Pushing to GitHub

Ensure all recent changes are pushed to your repository:

```bash
git add .
git commit -m "Configure for Render deployment"
git push origin main
```

## 3. Deploying on Render

1.  **Create a Render account** at [render.com](https://render.com).
2.  **Connect your GitHub account** to Render.
3.  On your Render Dashboard, click **"New +"** and select **"Blueprint"**.
4.  Connect your `BookMySeat` repository.
5.  Render will read the `render.yaml` file and automatically:
    - Create a **PostgreSQL Database**.
    - Create a **Web Service**.
    - Configure the Build and Start commands.

## 4. Set Environment Variables

After the blueprint starts, you need to add your specific keys in the Render Dashboard (**Dashboard -> Your Web Service -> Env Vars**):

| Key | Value |
| :--- | :--- |
| `STRIPE_PUBLIC_KEY` | Your pk_test_... key |
| `STRIPE_SECRET_KEY` | Your sk_test_... key |
| `STRIPE_WEBHOOK_SECRET` | Your whsec_... key |
| `EMAIL_HOST_USER` | zaidpatil4@gmail.com |
| `EMAIL_HOST_PASSWORD` | your-16-digit-app-password |
| `DEBUG` | `False` |

## 5. Update Stripe Webhook

Once your app is live (e.g., `https://bookmyseat-xxxx.onrender.com`), you need to update your Stripe Webhook URL:

1.  Go to [Stripe Dashboard -> Webhooks](https://dashboard.stripe.com/test/webhooks).
2.  Add a new endpoint or update the existing one to:
    `https://your-app-name.onrender.com/movies/webhook/stripe/`

---

## 💡 Troubleshooting

- **Static Files not loading?**: I've added WhiteNoise, so this should work automatically.
- **Database errors?**: Render's blueprint automatically creates a PostgreSQL database and connects it via `DATABASE_URL`.
- **First-time setup**: The `build.sh` script automatically runs `python scripts/add_seats.py` so your theaters will be ready immediately!

**Your app is now ready for the world!** 🌍🚀
