# AI Summarization Setup Guide

The Invoice Extractor includes AI-powered insights that analyze your spending patterns and provide actionable recommendations.

## 🤖 How It Works

The system provides **two modes** of operation:

### 1. Rule-Based Mode (Default)
- **No API key required**
- Works immediately out of the box
- Uses intelligent algorithms to analyze patterns
- Provides insights on:
  - Spending overview
  - Category breakdown
  - Top vendors
  - Currency distribution
  - Actionable recommendations

### 2. AI-Powered Mode (Optional)
- Uses OpenAI GPT-3.5 for advanced insights
- Provides more nuanced analysis
- Natural language summaries
- Contextual recommendations
- Requires OpenAI API key

## 🚀 Quick Start (Rule-Based)

**No setup needed!** Just run the application:

```bash
cd backend
python app.py
```

The system will automatically use rule-based summarization.

## ✨ Enable AI-Powered Mode

### Step 1: Get OpenAI API Key

1. Go to [OpenAI Platform](https://platform.openai.com/)
2. Sign up or log in
3. Navigate to API Keys section
4. Create a new API key
5. Copy the key (starts with `sk-...`)

### Step 2: Set Environment Variable

**On macOS/Linux:**
```bash
export OPENAI_API_KEY='your-api-key-here'
```

**On Windows (Command Prompt):**
```cmd
set OPENAI_API_KEY=your-api-key-here
```

**On Windows (PowerShell):**
```powershell
$env:OPENAI_API_KEY='your-api-key-here'
```

### Step 3: Install OpenAI Package

```bash
cd backend
pip install openai
```

### Step 4: Restart Backend

```bash
python app.py
```

You'll now see "Powered by GPT" badge in the AI insights section!

## 🔒 Using .env File (Recommended)

For persistent configuration:

### Step 1: Create .env file

```bash
cd backend
touch .env
```

### Step 2: Add your API key

```env
OPENAI_API_KEY=sk-your-actual-api-key-here
```

### Step 3: Install python-dotenv

```bash
pip install python-dotenv
```

### Step 4: Update app.py

Add at the top of `backend/app.py`:

```python
from dotenv import load_dotenv
load_dotenv()
```

### Step 5: Restart backend

```bash
python app.py
```

## 📊 What You Get

### Rule-Based Insights
```
📊 SPENDING OVERVIEW
You processed 15 invoices with a total spend of 25,450.00. 
Your average invoice amount is 1,696.67. All transactions 
are in INR.

💡 KEY INSIGHTS
Your highest spending category is Food, accounting for 45.2% 
of total expenses. You have transactions with 8 different 
vendors, with Swiggy being your top vendor.

🎯 RECOMMENDATIONS
Consider setting a budget for Food expenses as they dominate 
your spending. Track currency exchange rates to optimize 
international payments.
```

### AI-Powered Insights (with OpenAI)
```
📊 SPENDING OVERVIEW
Your spending pattern shows a strong preference for food 
delivery services, which might indicate a busy lifestyle. 
The concentration of expenses in a few vendors suggests 
loyalty but also potential for cost optimization.

💡 KEY INSIGHTS
Food delivery dominates at 45%, significantly higher than 
typical household spending. Swiggy and Zomato account for 
most transactions, suggesting convenience over cost. Weekend 
spending spikes indicate social dining patterns.

🎯 RECOMMENDATIONS
1. Consider meal prep on weekends to reduce delivery costs
2. Use vendor loyalty programs - you're already a frequent customer
3. Set a monthly food budget alert at ₹10,000
4. Compare prices between Swiggy and Zomato for same restaurants
```

## 💰 Cost Considerations

### Rule-Based Mode
- **Cost:** FREE
- **Speed:** Instant
- **Quality:** Good for basic insights

### AI-Powered Mode
- **Cost:** ~$0.002 per summary (very cheap!)
- **Speed:** 2-3 seconds
- **Quality:** Advanced, contextual insights

**Example:** Processing 100 invoice batches = ~$0.20

## 🔧 Troubleshooting

### "AI summary not showing"
- Check that backend is running
- Verify invoices were processed successfully
- Look for errors in backend console

### "Still using rule-based mode"
- Verify OPENAI_API_KEY is set: `echo $OPENAI_API_KEY`
- Check API key is valid (starts with `sk-`)
- Ensure `openai` package is installed: `pip list | grep openai`
- Restart backend after setting environment variable

### "OpenAI API error"
- Check API key is correct
- Verify you have credits in OpenAI account
- Check internet connection
- System will fallback to rule-based mode automatically

### "Rate limit exceeded"
- OpenAI has rate limits on free tier
- Wait a few minutes and try again
- Consider upgrading OpenAI plan
- Rule-based mode will be used as fallback

## 🎯 Features Comparison

| Feature | Rule-Based | AI-Powered |
|---------|-----------|------------|
| Setup Required | None | API Key |
| Cost | Free | ~$0.002/summary |
| Speed | Instant | 2-3 seconds |
| Insights Quality | Good | Excellent |
| Contextual Analysis | Basic | Advanced |
| Natural Language | Limited | Full |
| Recommendations | Generic | Personalized |
| Offline Support | Yes | No |

## 🌟 Best Practices

### For Rule-Based Mode
- Process invoices regularly for trend analysis
- Review category breakdowns monthly
- Act on high-percentage category warnings

### For AI-Powered Mode
- Process batches of 10+ invoices for better insights
- Include diverse time periods for trend analysis
- Review AI recommendations critically
- Use insights for budget planning

## 🔐 Security Notes

1. **Never commit API keys** to version control
2. Use `.env` file (add to `.gitignore`)
3. Rotate API keys periodically
4. Monitor OpenAI usage dashboard
5. Set spending limits in OpenAI account

## 📱 Mobile Access

AI summaries work on all devices:
- 📱 Mobile phones
- 📱 Tablets
- 💻 Desktop

The UI is fully responsive and optimized for reading insights on any screen size.

## 🆘 Need Help?

### Rule-Based Mode Issues
- Check backend logs for errors
- Verify invoices are being processed
- Ensure statistics are calculated

### AI-Powered Mode Issues
- Test API key: `curl https://api.openai.com/v1/models -H "Authorization: Bearer $OPENAI_API_KEY"`
- Check OpenAI status: https://status.openai.com/
- Review OpenAI usage: https://platform.openai.com/usage

## 🚀 Advanced: Custom AI Models

Want to use a different AI model? Edit `backend/services/ai_summarizer.py`:

```python
# Change model
response = self.client.chat.completions.create(
    model="gpt-4",  # or "gpt-3.5-turbo-16k"
    ...
)
```

Available models:
- `gpt-3.5-turbo` (default, cheapest)
- `gpt-3.5-turbo-16k` (longer context)
- `gpt-4` (best quality, more expensive)
- `gpt-4-turbo` (fast + quality)

## 📚 Learn More

- [OpenAI API Documentation](https://platform.openai.com/docs)
- [OpenAI Pricing](https://openai.com/pricing)
- [Best Practices for Prompts](https://platform.openai.com/docs/guides/prompt-engineering)

---

**Recommendation:** Start with rule-based mode. If you want more detailed insights, add OpenAI API key later!
