$(function () {
    $('[data-toggle="popover"]').popover('show')
})

$(function () {
    $('[data-toggle="popover"]').on(
        'hide.bs.popover', function(e){
            e.preventDefault();
            e.stopPropagation();
        }
    ).popover();
})