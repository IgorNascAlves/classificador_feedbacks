def format_email_content(total_feedbacks, positive_percentage, negative_percentage, sorted_features):
    feature_list = "\n".join([f"{feature[0]}: {feature[1]} pedidos" for feature in sorted_features])
    email_content = f"""
    Olá,

    Aqui está o resumo dos feedbacks da semana:

    Total de feedbacks: {total_feedbacks}
    % de feedbacks positivos: {positive_percentage}%
    % de feedbacks negativos: {negative_percentage}%

    Principais funcionalidades pedidas:
    {feature_list}

    Obrigado,
    Equipe AluMind
    """
    return email_content


