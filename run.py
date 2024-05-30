from app.main import create_app  # Importa a função create_app do módulo app

# Cria uma instância do aplicativo utilizando a função create_app
app = create_app()

# Verifica se este arquivo é executado como o programa principal
if __name__ == "__main__":
    # Inicia o servidor Flask em modo de depuração se este arquivo for o programa principal
    app.run(debug=True)
