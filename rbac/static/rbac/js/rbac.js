// (function (jq) {
//     jq('.sub-menu .title').click(function () {
//         $(this).next().toggleClass('hide');
//     })
// })(jQuery);
$(function () {
    $('.sub-menu .title').click(function () {
        $(this).next().toggleClass('hide');
    })
});