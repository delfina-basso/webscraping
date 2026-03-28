import feedparser
import pandas as pd
import re
import os
from urllib.error import URLError
import xml.sax


#RSS feeds saved in a dictionary with site name as key and URL as value.
feed_URLs = { "Clarin": "https://www.clarin.com/rss/mundo/",
             "El Economista": "https://eleconomista.com.ar/economia/feed/",
             "Wall Street Journal": "https://feeds.content.dowjones.io/public/rss/RSSWorldNews"
            }

#Dictionary of common countries' names and demonyms to ease search
countries_aliases = {
    "Estados Unidos": ["us", "u.s.", "usa", "estados unidos", "united states", "americans", "american", "estadounidenses"],
    "Reino Unido": ["uk", "united kingdom", "inglaterra", "british", "britain", "england", "english", "britanico", "inglés"],
    "China": ["china", "chinese", "chino", "chinas", "chinos"],
    "Rusia": ["russia", "russian", "rusia", "ruso", "rusos", "rusas"],
    "Alemania": ["germany", "german", "alemania", "alemán"],
    "Argentina": ["argentina", "argentino", "bonaerense", "marplatense", "cordobés"],
    "Francia": ["francia", "france", "francés", "french"],
    "India": ["india", "indio", "indian"],
    "Brasil": ["brazil", "brasil", "brasileño", "brazilian"],
    "México": ["mexico", "mexican", "mexicano"],
    "Corea del Sur": ["south korea", "korean", "corea del sur", "surcoreano"],
    "Arabia Saudita": ["saudi", "saudí", "arabia saudita", "saudi arabia"],
    "Ucrania": ["ukraine", "ucrania", "ukraninian", "ukraninians", "ucraniano", "ucraniana", "ucranianos", "ucranianas"]
}

def clean_html_tags(html_txt) -> str:
    """
    Cleans every HTML tag from a text.
    """
    if not html_txt:
        return ""
    txt = html_txt
    txt = re.sub(r'<!\[CDATA\[|\]\]>', '', txt)
    txt = re.sub(r'<img[^>]*>', '', txt)
    txt = re.sub(r'<.*?>', '', txt)
    
    return txt

def get_country_name(entry)->str:
    """
    Extracts the name of a country from an entry, looking through its title or description
    to find a match with a preset dictionary. Returns "Country not specified" if it can't find one.
    """
    txt_title = entry.get("title", "")
    txt_description = entry.get("description", "")
    
    txt = f"{clean_html_tags(txt_title).lower()} {clean_html_tags(txt_description).lower()}"
    
    for country, aliases in countries_aliases.items():
        for alias in aliases:
            pattern = r'\b' + re.escape(alias) + r"(?:['’]s)?\b"
            if re.search(pattern, txt):
                return country
    
    return "Country not specified"

def process_rss_feeds(source_name:str, url:str, save_path:str):
    """
    Processes RSS feeds to extract every article's title, publication 
    date, summary and country associate to the article. This data is then 
    saved in a CSV file.
    """
    all_articles = []
        
    try:
        feed = feedparser.parse(url)  
        if feed.bozo:
            print(f"Error en el parseo: {feed.bozo_exception}")
            return False
        
        for entry in feed.entries:
            title = entry.get("title", "Untitled")
            pub_date = entry.get("pubDate") or entry.get("published") or "Publication date not found"
            summary = clean_html_tags(entry.get("description", "Description not found"))
            country_name = get_country_name(entry)
            
            article_data = {
                "source": source_name,
                "title": title,
                "publication_date": pub_date,
                "summary": summary,
                "country": country_name
            }
            all_articles.append(article_data)
    
    except xml.sax.SAXParseException as e:
        print(f"Error inesperado durante el parsing: {e}")
        return False
    except URLError as e:
        print(f"Error en el enlace: {e}")
        return False
    except Exception as e:
        print(f"Error inesperado: {e}")
        return False
        
    if not all_articles:
        return False
    
    data_frame = pd.DataFrame(all_articles)
    file_exists = os.path.exists(save_path)
    data_frame.to_csv(save_path, index=False, encoding="utf-8", mode="a" if file_exists else "w", header=not file_exists)
    
    return True