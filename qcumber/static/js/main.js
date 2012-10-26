//Enable Dropdown boxes
$('.dropdown-header').click(function () {
    $(this).parent().next().slideToggle('medium');
    return false;
});