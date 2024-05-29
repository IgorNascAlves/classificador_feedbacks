document.addEventListener('DOMContentLoaded', function () {
    var featureRows = document.querySelectorAll('.clickable-row');
    var clearFilterButton = document.getElementById('clear-filter');

    featureRows.forEach(function (row) {
        row.addEventListener('click', function () {
            var feature = this.getAttribute('data-feature');
            highlightSelectedFeature(this);
            filterFeedbacks(feature);
        });
    });

    clearFilterButton.addEventListener('click', function () {
        clearFilter();
    });

    function highlightSelectedFeature(selectedRow) {
        featureRows.forEach(function (row) {
            row.classList.remove('selected-feature');
        });
        selectedRow.classList.add('selected-feature');
    }

    function filterFeedbacks(feature) {
        var feedbackRows = document.querySelectorAll('.feedback-row');
        feedbackRows.forEach(function (row) {
            if (row.getAttribute('data-code') === feature ) {
                row.style.display = '';
            } else {
                row.style.display = 'none';
            }
        });
    }

    function clearFilter() {
        var feedbackRows = document.querySelectorAll('.feedback-row');
        feedbackRows.forEach(function (row) {
            row.style.display = '';
        });
        featureRows.forEach(function (row) {
            row.classList.remove('selected-feature');
        });
    }
});
