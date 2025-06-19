if 'data_exporter' not in globals():
    from mage_ai.data_preparation.decorators import data_exporter

@data_exporter
def export_answer_only(data, *args, **kwargs):
    """
    Simple exporter that just returns the answer text
    """
    
    # Extract the answer from your upstream data
    if isinstance(data, dict):
        answer = data.get('answer', 'No answer available')
    else:
        # If data is a DataFrame, get the first row's answer
        answer = data['answer'].iloc[0] if hasattr(data, 'iloc') and 'answer' in data.columns else str(data)
    
    print(answer)
    
    return answer

