document.addEventListener('DOMContentLoaded', function () {
    // Seleciona todas as linhas clicáveis de características
    var featureRows = document.querySelectorAll('.clickable-row');
    // Seleciona o botão de limpar filtro
    var clearFilterButton = document.getElementById('clear-filter');

    // Adiciona um event listener para cada linha clicável de características
    featureRows.forEach(function (row) {
        row.addEventListener('click', function () {
            // Obtém a característica associada à linha clicada
            var feature = this.getAttribute('data-feature');
            // Destaca a característica selecionada
            highlightSelectedFeature(this);
            // Filtra os feedbacks com base na característica selecionada
            filterFeedbacks(feature);
        });
    });

    // Adiciona um event listener para o botão de limpar filtro
    clearFilterButton.addEventListener('click', function () {
        // Limpa o filtro
        clearFilter();
    });

    // Função para destacar a característica selecionada
    function highlightSelectedFeature(selectedRow) {
        // Remove a classe 'selected-feature' de todas as linhas de características
        featureRows.forEach(function (row) {
            row.classList.remove('selected-feature');
        });
        // Adiciona a classe 'selected-feature' à linha de característica selecionada
        selectedRow.classList.add('selected-feature');
    }

    // Função para filtrar os feedbacks com base na característica selecionada
    function filterFeedbacks(feature) {
        // Seleciona todas as linhas de feedback
        var feedbackRows = document.querySelectorAll('.feedback-row');
        // Itera sobre todas as linhas de feedback
        feedbackRows.forEach(function (row) {
            // Verifica se a característica associada à linha de feedback corresponde à característica selecionada
            if (row.getAttribute('data-code') === feature) {
                // Exibe a linha de feedback se corresponder à característica selecionada
                row.style.display = '';
            } else {
                // Oculta a linha de feedback se não corresponder à característica selecionada
                row.style.display = 'none';
            }
        });
    }

    // Função para limpar o filtro e restaurar todas as linhas de feedback e características
    function clearFilter() {
        // Seleciona todas as linhas de feedback
        var feedbackRows = document.querySelectorAll('.feedback-row');
        // Restaura todas as linhas de feedback para exibição
        feedbackRows.forEach(function (row) {
            row.style.display = '';
        });
        // Remove a classe 'selected-feature' de todas as linhas de características
        featureRows.forEach(function (row) {
            row.classList.remove('selected-feature');
        });
    }
});
