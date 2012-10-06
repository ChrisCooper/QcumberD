//Enable Dropdown boxes
$('.dropdown-header').click(function () {
    $(this).parent().next().toggleClass('hide');
    return false;
});