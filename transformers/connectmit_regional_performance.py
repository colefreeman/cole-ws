import pandas as pd

if 'transformer' not in globals():
    from mage_ai.data_preparation.decorators import transformer
if 'test' not in globals():
    from mage_ai.data_preparation.decorators import test


@transformer
def analyze_regional_performance(data, *args, **kwargs):
    """
    Analyze French regional sales performance for executive dashboard
    
    Transforms raw transaction data into regional business intelligence
    that French executives can immediately act upon
    """
    df = data.copy()
    
    print("🇫🇷 DEMO: French Regional Performance Analysis")
    print("=" * 60)
    print(f"📊 Analyzing {len(df)} transactions across French regions...")
    
    # Regional performance analysis
    regional_stats = df.groupby('region').agg({
        'revenue_euros': ['sum', 'mean', 'count'],
        'customer_type': lambda x: (x == 'Entreprise').sum()
    }).round(2)
    
    # Flatten column names
    regional_stats.columns = ['total_revenue', 'avg_basket', 'transactions', 'b2b_customers']
    
    # Add performance metrics
    regional_stats['revenue_rank'] = regional_stats['total_revenue'].rank(ascending=False)
    regional_stats['market_share_pct'] = (regional_stats['total_revenue'] / regional_stats['total_revenue'].sum() * 100).round(1)
    regional_stats['b2b_rate_pct'] = (regional_stats['b2b_customers'] / regional_stats['transactions'] * 100).round(1)
    
    # Sort by performance
    regional_stats = regional_stats.sort_values('total_revenue', ascending=False)
    
    # Display executive summary
    print("\n🏆 Regional Performance Ranking:")
    print("-" * 60)
    
    for region, row in regional_stats.head(10).iterrows():
        print(f"{int(row['revenue_rank'])}. {region}")
        print(f"   💰 Revenue: €{row['total_revenue']:,.2f} ({row['market_share_pct']}% of total)")
        print(f"   🛒 Avg Basket: €{row['avg_basket']:.2f}")
        print(f"   📊 Transactions: {int(row['transactions'])}")
        print(f"   🏢 B2B Rate: {row['b2b_rate_pct']}%")
        print()
    
    # Key insights for executives
    top_region = regional_stats.index[0]
    total_revenue = regional_stats['total_revenue'].sum()
    top_3_share = regional_stats.head(3)['market_share_pct'].sum()
    
    print("📈 Key Business Insights:")
    print(f"   🥇 Top Region: {top_region} (€{regional_stats.loc[top_region, 'total_revenue']:,.2f})")
    print(f"   💼 Total Market: €{total_revenue:,.2f}")
    print(f"   🎯 Top 3 Regions: {top_3_share:.1f}% of total revenue")
    print(f"   🏪 Highest B2B Rate: {regional_stats['b2b_rate_pct'].max():.1f}%")
    
    print("\n✅ Regional analysis complete - ready for executive dashboard!")
    
    # Reset index to include region as a column
    result = regional_stats.reset_index()
    
    return result


@test
def test_regional_analysis(output, *args) -> None:
    """
    Test that regional analysis was completed successfully
    """
    assert output is not None, 'Regional analysis output is undefined'
    assert len(output) > 0, 'No regional data generated'
    assert 'region' in output.columns, 'Missing region column'
    assert 'total_revenue' in output.columns, 'Missing total_revenue column'
    assert 'revenue_rank' in output.columns, 'Missing revenue_rank column'
    
    # Verify rankings are correct
    assert output.iloc[0]['revenue_rank'] == 1.0, 'Top region should have rank 1'
    assert output['total_revenue'].iloc[0] >= output['total_revenue'].iloc[1], 'Revenue should be sorted descending'
    
    print("✅ Regional analysis tests passed!")