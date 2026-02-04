import re
import html
import unicodedata
import pandas as pd


def remove_extra_whitespace(text, preserve_newlines=False) -> str:
  if not preserve_newlines:
    text = text.replace('\r\n', ' ')
    text = text.replace('\n', ' ')
    text = text.replace('\r', ' ')
  else:
    text = re.sub(r'\n{3,}', '\n\n', text)

  text = re.sub(r'\s+', ' ', text.strip())
  text = text.strip()
  
  return text


def normalize_unicode(text: str, unicode_form="NFKC") -> str:
  text = unicodedata.normalize(unicode_form, text)
  return text


def remove_control_characters(text: str, preserve_newlines=False) -> str:
  result = []
  
  for char in text:
    category = unicodedata.category(char)
  
    if category in ('Cc', 'Cf'):
      if preserve_newlines and char in ('\n', '\r', '\t'):
        result.append(char)
    else:
      result.append(char)
      
  return ''.join(result)


def clean_html(text: str) -> str:
  if '<' not in text:
    return text
  
  text = html.unescape(text)
  text = re.sub(r'<[^>]+>', '', text)
  text = re.sub(r' +', ' ', text)
  return text.strip()  


def _normalize_text(text: str) -> str:
  text = clean_html(text)
  text = normalize_unicode(text, unicode_form="NFKC")
  text = remove_control_characters(text, preserve_newlines=False)
  text = remove_extra_whitespace(text, preserve_newlines=False)
  return text.strip()


def clean_column(serie: pd.Series) -> pd.Series:
  original = serie.copy()
  cleaned = original.apply(lambda text:_normalize_text(text))
  return cleaned


def preprocess_dataframe(df: pd.DataFrame) -> pd.DataFrame:
  required_columns = ['user_input', 'reference']
  
  for col in required_columns:
    if col not in df.columns:
      raise ValueError(f"Column '{col}' not found in Dataframe")
    
  processed_df = df.copy()
  
  for col in required_columns:
    original = processed_df[col].copy()
    processed_df[col] = clean_column(df[col])
    
  return processed_df