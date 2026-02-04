import pandas as pd

def validate_required_columns(df: pd.DataFrame) -> pd.DataFrame:
  required = {'user_input', 'reference'}
  
  if not required.issubset(df.columns):
    raise ValueError('Required column missing: "user_input" and "reference" are needed.')
  
  return df 


def validate_column_types(df: pd.DataFrame) -> pd.DataFrame:
    required_types = {'user_input': 'object', 'reference': 'object'}
    
    for col, expected_type in required_types.items():
      if df[col].dtype != expected_type:
        raise ValueError(f"Column '{col}' must be type '{expected_type}', got '{df[col].dtype}'")
    
    return df


def validate_non_null_fields(df: pd.DataFrame) -> pd.DataFrame:
    required_cols = ['user_input', 'reference']
    
    null_mask = df[required_cols].isnull() | (df[required_cols] == '')
    if null_mask.values.any():
        problematic_cols = df[required_cols].columns[null_mask.any()].tolist()
        raise ValueError(
            f'Document contains empty/NaN/Null values in columns: {problematic_cols}'
        )
    return df


def validate_dataset_schema(df: pd.DataFrame) -> pd.DataFrame:
  errors = []
  
  try:
    value = validate_required_columns(df)
  except ValueError as e:
    errors.append(f"Column validation: {e}")
    raise ValueError('Required column missing: "user_input" and "reference" are needed.')
  
  # try:
  #   validate_column_types(df)
  # except ValueError as e:
  #   errors.append(f"Type validation: {e}")

  # try:
  #   validate_non_null_fields(df)
  # except ValueError as e:
  #   errors.append(f"Null check: {e}")

  if errors:
    raise ValueError("Validation failed:\n" + "\n".join(errors))
  
  return value
  