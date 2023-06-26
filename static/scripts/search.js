var token = localStorage.getItem('token');

$(document).ready(function () {
    $.ajaxSetup({cache: false});
    $('#search').keyup(function () {
        $('#result').html('');
        $('#state').val('');
        var searchField = $('#search').val();
        var expression = new RegExp(searchField, "i");

        $.get('http://158.160.51.82:30/api/v1/articles/', function (data) {
            $('#result').html('');

            $.each(data, function (index, article) {
                if (article.title.search(expression) !== -1) {
                    $('#result').append(`<li class="link-class"><a href="http://158.160.51.82:30/article_page/${article.id}/" class="search-item">${article.title}</a></li>`);
                }
            });
        });
    });

    $('#result').on('click', 'li', function () {
        var click_text = $(this).text().split('|');
        $('#search').val($.trim(click_text[0]));
        $("#result").html('');
    });
});