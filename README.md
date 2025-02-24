# Daily Pennsylvanian Headline Scraper  

## **Project Overview**  
This project scrapes the **main headline** from The Daily Pennsylvanian homepage and extracts the **author(s)** by following the headline link. The scraped data is stored in `data/daily_pennsylvanian_headlines.json` to track headline changes over time.

---

## **🔄 Recent Modifications**  
### **1️⃣ Added Author Extraction by Following the Headline Link**  
#### **What Changed?**  
- Instead of just **extracting the headline**, the scraper now **follows the article link** to fetch the **author(s)**.  
- Extracts **multiple authors** if available.  

#### **Why This Change?**  
- The **homepage only shows the headline**, not the author(s).  
- **Tracking authorship** helps analyze writing patterns and contributions over time.  

#### **How It Works?**  
1. **Finds the main headline** from `<a class="frontpage-link large-link">` on the homepage.  
2. **Extracts the full article URL** from the `<a>` tag.  
3. **Sends a request to the article page** to fetch the HTML content.  
4. **Finds the authors** inside `<span class="byline">`, extracting text from `<a class="author-name">`.  

#### **Example Output:**
```json
{
  "headline": "Penn to reduce graduate admissions, rescind acceptances amid federal research funding cuts",
  "authors": ["Isha Chitirala", "Finn Ryan"]
}
