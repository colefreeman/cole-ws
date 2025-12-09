import pandas as pd

if 'transformer' not in globals():
    from mage_ai.data_preparation.decorators import transformer
if 'test' not in globals():
    from mage_ai.data_preparation.decorators import test


@transformer
def transform_french_sales_data(data, *args, **kwargs):
    """
    Transform French e-commerce sales data for business intelligence
    """
    df = data.copy()
    
    # Calculate revenue from unit price × quantity
    df['revenue'] = df['unit_price'] * df['quantity']
    
    # French tax calculations (HT = Hors Taxe, TTC = Toutes Taxes Comprises)
    df['montant_ht'] = df['revenue'] / (1 + df['tva_rate'])  # Price before tax
    df['montant_tva'] = df['revenue'] - df['montant_ht']     # TVA collected
    
    # Customer analytics
    df['is_repeat_customer'] = df.groupby('customer_id')['customer_id'].transform('count') > 1
    
    # Add time-based features
    df['timestamp'] = pd.to_datetime(df['timestamp'])
    df['hour'] = df['timestamp'].dt.hour
    df['day_name'] = df['timestamp'].dt.day_name()
    
    return df


@test
def test_revenue_calculation(output, *args):
    """
    Test that revenue is calculated correctly: unit_price × quantity
    """
    assert 'revenue' in output.columns, 'Revenue column missing'
    
    # Test first row calculation
    first_row = output.iloc[0]
    expected_revenue = first_row['unit_price'] * first_row['quantity']
    actual_revenue = first_row['revenue']
    
    assert abs(actual_revenue - expected_revenue) < 0.01, f'Revenue calculation incorrect: expected {expected_revenue}, got {actual_revenue}'